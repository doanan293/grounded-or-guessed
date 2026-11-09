"""Blind, independent re-review of a sample of SemFault-250 labels.

    python scripts/blind_review.py packet    # sample, assign, write docs/analysis/gt-review/duyet-doc-lap/<member>.{md,csv}
    python scripts/blind_review.py score     # after the members fill their CSVs → data/blind_review.csv + summary
Design (fixed before anyone answers):
- 60 programs, seed 20261110: 30 from the labels a member already reviewed with the LLM suggestion visible (15 relocated
  by the oracle, 15 the LLM judged wrong) and 30 from labels no human has seen (20 the LLM judged right, 10 two-line).
- Each program goes to 2 members who have NOT seen it before; every member gets 20 programs.
- Reviewers see the code, links to program and tests, and candidate lines lettered in random order: the union of the
  original label, the oracle's line, the LLM's line and the reviewed label, padded with neighbouring code lines to at
  least four. Nothing says which line came from where; no LLM text is shown.
The answer key (letter → line) is regenerated from the seed, so it is not shipped in the reviewers' files.
"""
import csv
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[1]
REV = ROOT / "docs" / "analysis" / "gt-review"
OUT = REV / "duyet-doc-lap"
SEED = 20261110
MEMBERS = {"Tạ Công Nam": "ta-cong-nam", "Nguyễn Hoàng Hải": "nguyen-hoang-hai", "Đỗ Xuân Tráng": "do-xuan-trang",
           "Hoàng Trung Kiên": "hoang-trung-kien", "Mai Văn Tùng": "mai-van-tung", "Nguyễn Đức Tùng": "nguyen-duc-tung"}
GH = "https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark"


def candidates(src: list[str], relevant: set[int], minimum: int = 4) -> list[int]:
    """Relevant lines plus the nearest non-blank, non-comment lines around them until there are `minimum` lines."""
    out = set(l for l in relevant if 0 < l <= len(src))
    code = lambda l: 0 < l <= len(src) and src[l - 1].strip() and not src[l - 1].strip().startswith("#")
    dist = 1
    while len(out) < minimum and dist < len(src):
        for base in sorted(relevant):
            for l in (base - dist, base + dist):
                if len(out) < minimum and code(l):
                    out.add(l)
        dist += 1
    return sorted(out)


def assign(cases: list[dict], members: list[str], per_case: int, rng: random.Random, tries: int = 2000) -> dict:
    """Each case to `per_case` distinct members, never its `seen_by`, every member the same load."""
    target = len(cases) * per_case // len(members)
    for _ in range(tries):
        load, out, ok = Counter({m: 0 for m in members}), {}, True
        order = sorted(cases, key=lambda c: (c["seen_by"] is None, rng.random()))
        for c in order:
            pool = [m for m in members if m != c["seen_by"] and load[m] < target]
            if len(pool) < per_case:
                ok = False
                break
            rng.shuffle(pool)
            pick = sorted(pool, key=lambda m: load[m])[:per_case]
            for m in pick:
                load[m] += 1
            out[c["program"]] = pick
        if ok and set(load.values()) == {target}:
            return out
    raise RuntimeError("no balanced assignment found")


# An answer whose note cites the earlier, non-blind review files (which show the LLM suggestion and the earlier
# answers) is not blind; it is kept in the data but excluded from the blind statistics. Rule fixed after reading the
# notes, before computing any agreement figure.
NOT_BLIND = re.compile(r"thanh-vien|thanh vien|lần trước|LLM|Fable|gợi ý", re.I)


def answer_lines(ans: str, letters: dict[str, int]) -> set[int] | None:
    parts = [p.strip().upper() for p in re.split(r"[+,;]", ans or "") if p.strip()]
    if not parts or "?" in parts:
        return None
    return {int(p) if p.isdigit() else letters[p] for p in parts}


def _context(src: list[str], marks: dict[int, str], pad: int = 8) -> str:
    lo, hi = max(1, min(marks) - pad), min(len(src), max(marks) + 4)
    return "\n".join(f"{marks.get(i, ' ')} {i:3d}: {src[i - 1]}" for i in range(lo, hi + 1))


def build() -> list[dict]:
    """The sample with everything needed to make and score the packets (deterministic from SEED)."""
    rng = random.Random(SEED)
    rev = {r["program"]: r for r in json.loads((ROOT / "data" / "semfault_reviewed_gt.json").read_text())}
    oracle = {r["program"]: r for r in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())}
    llm = {}
    for f in sorted(REV.glob("llm_verdicts*.json")):
        for v in json.loads(f.read_text()):
            llm[v["program"]] = v
    seen = {}
    for name, slug in MEMBERS.items():
        for r in csv.DictReader(open(REV / "duyet-lan-1-co-goi-y" / f"{slug}.csv", encoding="utf-8-sig")):
            seen[r["program"]] = name
    relocated = sorted(p for p, o in oracle.items() if o["status"] == "corrected" and p in seen)
    flagged = sorted(p for p in seen if p not in relocated)
    kept = sorted(p for p, r in rev.items() if r["source"] == "llm_label")
    two = sorted(p for p, r in rev.items() if r["source"] == "llm_either")
    sample = (rng.sample(relocated, 15) + rng.sample(flagged, 15) + rng.sample(kept, 20) + rng.sample(two, 10))
    cases = []
    for p in sample:
        src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text().splitlines()
        relevant = set(rev[p]["original"]) | set(rev[p]["lines"])
        if oracle[p]["status"] == "corrected":
            relevant |= set(oracle[p]["lines"])
        if llm.get(p, {}).get("fault_line"):
            relevant.add(int(llm[p]["fault_line"]))
        cand = candidates(src, relevant)
        rng.shuffle(cand)
        letters = {chr(ord("A") + i): ln for i, ln in enumerate(cand)}
        group = ("relocated" if p in relocated else "flagged" if p in flagged else "kept" if p in kept else "two_line")
        cases.append({"program": p, "group": group, "seen_by": seen.get(p), "letters": letters,
                      "original": rev[p]["original"], "reviewed": rev[p]["lines"],
                      "llm": int(llm[p]["fault_line"]) if llm.get(p, {}).get("fault_line") else None, "src": src})
    who = assign(cases, list(MEMBERS), 2, rng)
    for c in cases:
        c["reviewers"] = who[c["program"]]
    return cases


def packet() -> None:
    cases = build()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, slug in MEMBERS.items():
        mine = [c for c in cases if name in c["reviewers"]]
        random.Random(f"{SEED}-{slug}").shuffle(mine)
        md = [f"# Duyệt mù dòng lỗi — {name} ({len(mine)} ca)", "",
              "**Làm độc lập:** không bàn với ai, không dùng ChatGPT/Claude/Copilot hay công cụ AI nào, không xem lại tệp duyệt",
              "lần trước. Kết quả chỉ có giá trị khi mỗi người tự quyết định.", "",
              "Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.", "",
              "- Các dòng ứng viên được đánh chữ `A`, `B`, `C`… ở lề trái, theo thứ tự ngẫu nhiên.",
              "- Đọc docstring, tên hàm và **kiểm thử** (link ở mỗi ca) để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.",
              "  Có thể chạy kiểm thử trên máy nếu muốn.",
              "- Ghi vào cột `answer` của tệp CSV cùng tên: một chữ (`B`), nhiều chữ nếu lỗi thật sự trải trên nhiều dòng",
              "  (`B+D`), một số dòng khác nếu không ứng viên nào đúng (`71`), hoặc `?` nếu không chắc. Cột `note` tùy ý.",
              "- Mỗi ca khoảng 3 phút.", ""]
        rows = []
        for k, c in enumerate(mine, 1):
            marks = {ln: L for L, ln in c["letters"].items()}
            first = min(marks)
            md += [f"## {k}. `{c['program']}`", "",
                   f"[Chương trình]({GH}/programs/{c['program']}.py#L{first}) · [Kiểm thử]({GH}/testcases/test_{c['program']}.py)",
                   "", "Ứng viên: " + ", ".join(f"`{L}` = dòng {ln}" for L, ln in sorted(c["letters"].items())), "",
                   "```python", _context(c["src"], marks), "```", ""]
            rows.append({"id": k, "program": c["program"], "candidates": " ".join(sorted(c["letters"])), "answer": "", "note": ""})
        (OUT / f"{slug}.md").write_text("\n".join(md) + "\n")
        with open(OUT / f"{slug}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, ["id", "program", "candidates", "answer", "note"])
            w.writeheader()
            w.writerows(rows)
        print(name, len(mine))


def score() -> None:
    """Per program: both answers, whether they agree, and whether they match the original / reviewed / LLM lines."""
    cases = {c["program"]: c for c in build()}
    answers, blind = {}, {}
    for name, slug in MEMBERS.items():
        for r in csv.DictReader(open(OUT / f"{slug}.csv", encoding="utf-8-sig")):
            answers.setdefault(r["program"], {})[name] = answer_lines(r["answer"], cases[r["program"]]["letters"])
            blind.setdefault(r["program"], {})[name] = not NOT_BLIND.search(r["note"] or "")
    rows = []
    hit = lambda a, target: None if a is None or not target else bool(a & set(target))
    for p, c in cases.items():
        a1, a2 = (answers.get(p, {}).get(m) for m in c["reviewers"])
        b1, b2 = (blind.get(p, {}).get(m, True) for m in c["reviewers"])
        both = a1 is not None and a2 is not None
        rows.append({"program": p, "group": c["group"], "answered": int(a1 is not None) + int(a2 is not None),
                     "r1_blind": int(b1), "r2_blind": int(b2),
                     "agree": "" if not both else int(bool(a1 & a2)),
                     **{f"r{i}_{t}": "" if hit(a, tgt) is None else int(hit(a, tgt))
                        for i, a in ((1, a1), (2, a2)) for t, tgt in
                        (("reviewed", c["reviewed"]), ("original", c["original"]), ("llm", [c["llm"]] if c["llm"] else []))}})
    with open(ROOT / "data" / "blind_review.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    summary = []
    for only_blind in (False, True):
        for g in ("all", "relocated", "flagged", "kept", "two_line"):
            rs = [r for r in rows if g == "all" or r["group"] == g]
            ok = lambda r, i: r[f"r{i}_reviewed"] != "" and (not only_blind or r[f"r{i}_blind"])
            ag = [r["agree"] for r in rs if r["agree"] != "" and (not only_blind or (r["r1_blind"] and r["r2_blind"]))]
            row = {"answers": "blind" if only_blind else "all", "group": g, "programs": len(rs), "pairs": len(ag),
                   "pairs_agree": sum(ag)}
            for t in ("reviewed", "original", "llm"):
                xs = [r[f"r{i}_{t}"] for r in rs for i in (1, 2) if r[f"r{i}_{t}"] != "" and (not only_blind or r[f"r{i}_blind"])]
                row[f"n_{t}"], row[f"match_{t}"] = len(xs), sum(xs)
            summary.append(row)
            print(row)
    with open(ROOT / "data" / "blind_review_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0]))
        w.writeheader()
        w.writerows(summary)


if __name__ == "__main__":
    packet() if sys.argv[1] == "packet" else score()

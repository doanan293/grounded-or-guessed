"""Build the ground-truth review packets.

    python scripts/gt_review_packet.py
Writes docs/analysis/gt-review/cases.md + review.csv for the labels the minimal-fix oracle relocated ("corrected"),
and cases_rest.md + review_rest.csv for the other 204 programs (confirmed, unverified, unverifiable). Verdict columns
are filled by the LLM pre-review, then by the human reviewer, whose verdict is final; the rest packet is reviewed by
a human only where the LLM disagrees with the label or is not confident.
Verdicts: new (the relocated line is the fault), original (the original label is right; the fix compensates),
either (guard/guarded-statement or multi-line fault: both lines are defensible), neither.
"""
import csv
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "analysis" / "gt-review"
MEMBERS = ["Doãn Văn An", "Tạ Công Nam", "Nguyễn Hoàng Hải", "Đỗ Xuân Tráng", "Hoàng Trung Kiên", "Mai Văn Tùng",
           "Nguyễn Đức Tùng"]
FIELDS = ["case", "program", "original", "new", "kind", "fix", "assigned_to", "llm_verdict", "llm_confidence",
          "llm_fault_line", "llm_reason", "human_verdict", "human_note"]


def llm(name: str) -> dict:
    """LLM pre-review verdicts (llm_verdicts*.json) by program, merged into the CSVs."""
    out = {}
    for f in sorted(OUT.glob(name)):
        for v in json.loads(f.read_text()):
            out[v["program"]] = {"llm_verdict": v["verdict"], "llm_confidence": v["confidence"],
                                 "llm_fault_line": v.get("fault_line", ""), "llm_reason": v["reason"]}
    return out


def context(src: list[str], lines: set[int], pad: int = 6) -> str:
    lo, hi = max(1, min(lines) - pad), min(len(src), max(lines) + pad)
    return "\n".join(f"{'>>' if i in lines else '  '} {i:3d}: {src[i - 1]}" for i in range(lo, hi + 1))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    recs = [r for r in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text()) if r["status"] == "corrected"]
    recs.sort(key=lambda r: r["program"])
    old = {}
    if (OUT / "review.csv").exists():  # keep verdicts already entered
        old = {r["program"]: r for r in csv.DictReader(open(OUT / "review.csv"))}
    pre = llm("llm_verdicts.json")
    rows, md = [], ["# Review of relocated ground-truth labels", "",
                    "For each program: `>>` marks the original label and the relocated label. The fix is the minimal edit",
                    "that makes every test pass at the relocated line. Verdict in `review.csv`: `new`, `original`, `either`,",
                    "`neither`. The human verdict is final.", ""]
    for k, r in enumerate(recs, 1):
        src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{r['program']}.py").read_text().splitlines()
        row = {"case": k, "program": r["program"], "original": ";".join(map(str, r["original"])),
               "new": ";".join(map(str, r["lines"])), "kind": r["kind"], "fix": r["code"],
               "assigned_to": MEMBERS[(k - 1) % len(MEMBERS)]}
        for f in ("llm_verdict", "llm_confidence", "llm_fault_line", "llm_reason", "human_verdict", "human_note"):
            row[f] = old.get(r["program"], {}).get(f, "")
        row.update(pre.get(r["program"], {}))
        rows.append(row)
        md += [f"## {k}. `{r['program']}` — reviewer: {row['assigned_to']}", "",
               f"Original label: line {row['original']}; relocated: line {row['new']} ({r['kind']}, {r['edit_size']} token(s)).",
               "", "```", context(src, set(r["original"]) | set(r["lines"])), "```", "",
               f"Fix at line {row['new']}: `{r['code']}`", ""]
    with open(OUT / "review.csv", "w", newline="") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rows)
    (OUT / "cases.md").write_text("\n".join(md) + "\n")
    print(f"{len(rows)} cases → {OUT}")
    rest_packet()


REST_FIELDS = ["case", "program", "status", "label", "fix", "llm_verdict", "llm_confidence", "llm_fault_line", "llm_reason",
               "human_verdict", "human_note"]


def rest_packet() -> None:
    """Every program whose label the oracle did not relocate; `label` is the line(s) the original benchmark names."""
    orig = {g["file"][:-3]: g["faulty_lines"] for g in
            json.loads((SEMLOC_ROOT / "benchmark" / "ground_truth.json").read_text())["programs"]}
    recs = sorted((r for r in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
                   if r["status"] != "corrected"), key=lambda r: r["program"])
    old = {}
    if (OUT / "review_rest.csv").exists():
        old = {r["program"]: r for r in csv.DictReader(open(OUT / "review_rest.csv"))}
    pre = llm("llm_verdicts_rest_*.json")
    rows, md = [], ["# Review of the remaining ground-truth labels", "",
                    "`>>` marks the original label. Status: `confirmed` = a minimal edit at this line makes every test",
                    "pass; `unverified` = the line is reached but no minimal edit was found; `unverifiable` = the oracle",
                    "could not run. Verdict: `label` (the label is the fault), `other` (the fault is at llm_fault_line),",
                    "`either` (guard/guarded statement or multi-line fault: the label is defensible).", ""]
    for k, r in enumerate(recs, 1):
        src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{r['program']}.py").read_text().splitlines()
        label = orig[r["program"]]
        row = {"case": k, "program": r["program"], "status": r["status"], "label": ";".join(map(str, label)),
               "fix": r.get("code", "")}
        for f in ("llm_verdict", "llm_confidence", "llm_fault_line", "llm_reason", "human_verdict", "human_note"):
            row[f] = old.get(r["program"], {}).get(f, "")
        row.update(pre.get(r["program"], {}))
        rows.append(row)
        md += [f"## {k}. `{r['program']}` — {r['status']}, label line {row['label']}", "",
               "```", context(src, set(label)), "```", ""]
        if row["fix"]:
            md += [f"Minimal fix at the label: `{row['fix']}`", ""]
    with open(OUT / "review_rest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, REST_FIELDS)
        w.writeheader()
        w.writerows(rows)
    (OUT / "cases_rest.md").write_text("\n".join(md) + "\n")
    print(f"{len(rows)} cases → {OUT / 'cases_rest.md'}")
    members_packet()


REVIEWERS = MEMBERS[1:]  # the lead author prepared the packet and does not review
GH = "https://github.com/doanan293/grounded-or-guessed/blob/main/third_party/semloc/benchmark"
SLUG = {"Tạ Công Nam": "ta-cong-nam", "Nguyễn Hoàng Hải": "nguyen-hoang-hai", "Đỗ Xuân Tráng": "do-xuan-trang",
        "Hoàng Trung Kiên": "hoang-trung-kien", "Mai Văn Tùng": "mai-van-tung", "Nguyễn Đức Tùng": "nguyen-duc-tung"}
MEMBER_FIELDS = ["id", "program", "G", "S", "F", "answer", "note"]


def members_packet() -> None:
    """Human review: the 46 relocated labels and every remaining label the LLM put on another line.

    Candidate lines per case: G = original benchmark label, S = line our oracle relocated it to (relocated cases),
    F = line the LLM pre-review proposes (when it differs). The reviewer answers with the letter(s) of the line(s)
    that hold the injected fault, or a line number; their CSV answers are final."""
    orig = {g["file"][:-3]: g["faulty_lines"] for g in
            json.loads((SEMLOC_ROOT / "benchmark" / "ground_truth.json").read_text())["programs"]}
    cases = []
    for r in csv.DictReader(open(OUT / "review.csv")):
        f = r["llm_fault_line"] if r["llm_verdict"] == "neither" else ""
        cases.append({"program": r["program"], "S": r["new"], "F": f, "fix": r["fix"], "kind": "relocated",
                      "llm": f"{r['llm_verdict']} ({r['llm_confidence']}): {r['llm_reason']}"})
    for r in csv.DictReader(open(OUT / "review_rest.csv")):
        if r["llm_verdict"] == "other":
            cases.append({"program": r["program"], "S": "", "F": r["llm_fault_line"], "fix": r["fix"], "kind": r["status"],
                          "llm": f"other ({r['llm_confidence']}): {r['llm_reason']}"})
    cases.sort(key=lambda c: c["program"])
    dest = OUT / "thanh-vien"
    dest.mkdir(exist_ok=True)
    for m, who in enumerate(REVIEWERS):
        mine = [c for i, c in enumerate(cases) if i % len(REVIEWERS) == m]
        old = {}
        if (dest / f"{SLUG[who]}.csv").exists():  # keep answers already entered
            old = {r["program"]: r for r in csv.DictReader(open(dest / f"{SLUG[who]}.csv"))}
        md = [f"# Duyệt nhãn dòng lỗi — {who} ({len(mine)} ca)", "",
              "Mỗi chương trình có **đúng một lỗi được cố ý tiêm vào**. Nhiệm vụ: chỉ ra dòng chứa lỗi đó.",
              "", "- `G` = nhãn gốc của bộ dữ liệu; `S` = dòng mà bộ kiểm chứng tự động của nhóm dời nhãn tới;",
              "  `F` = dòng mà LLM (Fable) đề xuất khi rà trước. Các dòng ứng viên được đánh dấu `>>` trong đoạn mã.",
              "- Đọc docstring, tên hàm và kiểm thử để biết hàm *muốn* làm gì; dòng lỗi là dòng làm khác ý đó.",
              "  Mở toàn bộ chương trình và kiểm thử bằng hai link ở mỗi ca nếu đoạn mã chưa đủ.",
              "- Ghi câu trả lời vào cột `answer` của tệp CSV cùng tên: `G`, `S`, `F`, hoặc nhiều chữ nếu lỗi thật",
              "  trải trên nhiều dòng (ví dụ `G+F`), hoặc một số dòng khác (ví dụ `71`). Cột `note`: ghi chú ngắn nếu muốn.",
              "- Nhận định của LLM chỉ để tham khảo, **không** phải đáp án; nếu thấy LLM sai, cứ chọn theo ý mình.",
              "- Mỗi ca thường mất 2–4 phút. Không chắc thì ghi `?` vào `answer` và lý do vào `note`.", ""]
        rows = []
        for k, c in enumerate(mine, 1):
            src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{c['program']}.py").read_text().splitlines()
            G = ";".join(map(str, orig[c["program"]]))
            cand = {int(x) for v in (G, c["S"], c["F"]) for x in str(v).split(";") if x}
            rows.append({"id": k, "program": c["program"], "G": G, "S": c["S"], "F": c["F"],
                         "answer": old.get(c["program"], {}).get("answer", ""),
                         "note": old.get(c["program"], {}).get("note", "")})
            first = min(cand)
            md += [f"## {k}. `{c['program']}`", "",
                   f"[Chương trình]({GH}/programs/{c['program']}.py#L{first}) · [Kiểm thử]({GH}/testcases/test_{c['program']}.py)",
                   "", f"- G (nhãn gốc): dòng {G}" + (f"\n- S (nhóm dời tới): dòng {c['S']}, bản sửa: `{c['fix']}`" if c["S"] else "")
                   + (f"\n- F (LLM đề xuất): dòng {c['F']}" if c["F"] else ""), "",
                   "```python", context(src, cand), "```", "", f"> LLM: {c['llm']}", ""]
        (dest / f"{SLUG[who]}.md").write_text("\n".join(md) + "\n")
        with open(dest / f"{SLUG[who]}.csv", "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, MEMBER_FIELDS)
            w.writeheader()
            w.writerows(rows)
        print(who, len(mine))


if __name__ == "__main__":
    main()

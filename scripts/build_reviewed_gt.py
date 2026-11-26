"""Build SemFault-250-reviewed → data/semfault_reviewed_gt.json.

    python scripts/build_reviewed_gt.py
Every program gets a label, by precedence:
  override   — lead-author correction backed by running the tests (OVERRIDES, with the reason);
  human      — a team member's answer in docs/analysis/gt-review/duyet-lan-1-co-goi-y/*.csv (the 46 relocated labels and
               every label the LLM pre-review put on another line; reviewers saw the LLM suggestion);
  llm_either — the LLM judged the original label defensible but the fault also on another line: both lines count;
  llm_label  — the LLM judged the original label right: kept.
Fails if any final label is empty, out of range, or only blank/comment lines.
"""
import csv
import json
import re
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[1]
REV = ROOT / "docs" / "analysis" / "gt-review"
OVERRIDES = {
    "storage_quota_split": ([66, 70], "fee must leave the pool once: fixing line 66 alone still fails a test, "
                                      "fixing 66 and 70 passes every test"),
    "fee_splitter": ([59, 61], "same two-line fee fault: the gross split (59) and the per-participant fee (61)"),
    "memory_moving_mean": ([65], "the original label 66 is blank; the LLM pre-review kept it but quoted the statement "
                                 "on line 65 (`avg = total / window`, should divide by len(tail))"),
    "shift_risk": ([65], "omission fault (missing normalisation): the reviewer chose the insertion point, a blank line "
                         "no method can rank; as in the sibling omission programs, the return statement is labelled"),
    "storage_mix": ([64], "omission fault (missing normalisation): the reviewer chose the insertion point, a blank line "
                          "no method can rank; as in the sibling omission programs, the return statement is labelled"),
}


def answer_lines(ans: str, row: dict) -> list[int]:
    """'G' / 'S' / 'F', combinations joined by '+', or explicit line numbers → sorted line list."""
    out = set()
    parts = [x.strip().upper() for x in ans.split("+") if x.strip()]
    if not parts:
        raise ValueError(f"empty answer for {row}")
    for x in parts:
        if x.isdigit():
            out.add(int(x))
        elif x in ("G", "S", "F") and row.get(x, "").strip():
            out |= {int(v) for v in re.split(r"[;,]", row[x]) if v.strip()}
        else:
            raise ValueError(f"unusable answer {ans!r} for {row.get('program')}")
    return sorted(out)


def reviewed(orig: dict, human: dict, llm: dict, overrides: dict) -> dict:
    out = {}
    for p, lines in orig.items():
        if p in overrides:
            out[p] = {"lines": sorted(overrides[p][0]), "source": "override", "note": overrides[p][1]}
        elif p in human:
            out[p] = {"lines": human[p], "source": "human"}
        elif llm.get(p, {}).get("verdict") == "either":
            out[p] = {"lines": sorted(set(lines) | {int(llm[p]["fault_line"])}), "source": "llm_either"}
        else:
            out[p] = {"lines": list(lines), "source": "llm_label"}
    return out


def main() -> None:
    orig = {g["file"][:-3]: g["faulty_lines"] for g in
            json.loads((SEMLOC_ROOT / "benchmark" / "ground_truth.json").read_text())["programs"]}
    human, reviewer = {}, {}
    for f in sorted((REV / "duyet-lan-1-co-goi-y").glob("*.csv")):
        for r in csv.DictReader(open(f, encoding="utf-8-sig")):
            human[r["program"]] = answer_lines(r["answer"], r)
            reviewer[r["program"]] = f.stem
    llm = {}
    for f in sorted(REV.glob("llm_verdicts_rest_*.json")):
        for v in json.loads(f.read_text()):
            llm[v["program"]] = v
    gt = reviewed(orig, human, llm, OVERRIDES)
    for p, v in gt.items():
        src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text().splitlines()
        assert v["lines"] and all(0 < ln <= len(src) for ln in v["lines"]), p
        assert any(src[ln - 1].strip() and not src[ln - 1].strip().startswith("#") for ln in v["lines"]), (p, v)
        if p in reviewer:
            v["reviewer"] = reviewer[p]
        v["original"] = orig[p]
    out = [{"program": p, **v} for p, v in sorted(gt.items())]
    (ROOT / "data" / "semfault_reviewed_gt.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter(v["source"] for v in gt.values()), "changed:", sum(v["lines"] != orig[p] for p, v in gt.items()))


if __name__ == "__main__":
    main()

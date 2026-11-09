"""How do the benchmark's original labels relate to the reviewed labels? → data/label_audit.csv

    python scripts/label_audit.py
Per program, one kind: same | extended (original kept, a second line added: two-line fault) | blank (original on a
blank line) | non_code (original on a log call, def header or comment) | off_by_one | farther. Rows: every program,
and the test split. No LLM calls.
"""
import csv
import json
from collections import Counter
from pathlib import Path

from flx._semloc import SEMLOC_ROOT

ROOT = Path(__file__).resolve().parents[1]
KINDS = ["same", "extended", "blank", "non_code", "off_by_one", "farther"]


def kind(original: list[int], reviewed: list[int], src: list[str]) -> str:
    if sorted(original) == sorted(reviewed):
        return "same"
    if set(original) <= set(reviewed):
        return "extended"
    text = [src[ln - 1].strip() if 0 < ln <= len(src) else "" for ln in original]
    if all(not t for t in text):
        return "blank"
    if all(not t or t.startswith(("#", "def ", "_log.", "log.", "logger.", "logging.")) for t in text):
        return "non_code"
    gap = min(abs(o - r) for o in original for r in reviewed)
    return "off_by_one" if gap <= 1 else "farther"


def main() -> None:
    rev = {r["program"]: r for r in json.loads((ROOT / "data" / "semfault_reviewed_gt.json").read_text())}
    test = set(json.loads((ROOT / "data" / "split.json").read_text())["test"])
    kinds = {}
    for p, r in rev.items():
        src = (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text().splitlines()
        kinds[p] = kind(r["original"], r["lines"], src)
    rows = []
    for subset, progs in (("all", list(kinds)), ("test", [p for p in kinds if p in test])):
        c = Counter(kinds[p] for p in progs)
        rows.append({"subset": subset, "n": len(progs), **{k: c.get(k, 0) for k in KINDS},
                     "moved": sum(c.get(k, 0) for k in ("blank", "non_code", "off_by_one", "farther")),
                     "two_line": sum(len(rev[p]["lines"]) > 1 for p in progs)})
    with open(ROOT / "data" / "label_audit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()

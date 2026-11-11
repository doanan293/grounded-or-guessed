"""Build data/semfault_renamed/: line-preserving renamed SemFault-250 (RQ3b). Programs whose per-test outcomes
change are excluded and listed in data/semfault_renamed/excluded.json.

    python scripts/make_renamed.py --workers 8
"""
import argparse
import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.rename import keep_names, rename_program, test_outcomes

ROOT = Path(__file__).resolve().parents[1]
BENCH = SEMLOC_ROOT / "benchmark"
OUT = ROOT / "data" / "semfault_renamed"


def _one(entry):
    f = entry["file"]
    prog, test = BENCH / "programs" / f, BENCH / "testcases" / f"test_{f}"
    src = prog.read_text()
    try:
        new = rename_program(src, keep_names(test.read_text()))
    except Exception as e:
        return f, None, f"rename failed: {type(e).__name__}: {e}"
    if new.count("\n") != src.count("\n"):
        return f, None, "line count changed"
    before, after = test_outcomes(src, prog, test), test_outcomes(new, prog, test)
    if not before or before != after:
        return f, None, f"outcomes changed: {sorted(k for k in before if before.get(k) != after.get(k))[:5]}"
    return f, new, ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    gt = json.loads((BENCH / "ground_truth.json").read_text())
    (OUT / "programs").mkdir(parents=True, exist_ok=True)
    (OUT / "testcases").mkdir(parents=True, exist_ok=True)
    kept, excluded = [], {}
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for (f, new, why), entry in zip(pool.map(_one, gt["programs"]), gt["programs"]):
            if new is None:
                excluded[f[:-3]] = why
                continue
            (OUT / "programs" / f).write_text(new)
            shutil.copy(BENCH / "testcases" / f"test_{f}", OUT / "testcases" / f"test_{f}")
            kept.append(entry)
    (OUT / "ground_truth.json").write_text(json.dumps({**gt, "programs": kept}, indent=2))
    (OUT / "excluded.json").write_text(json.dumps(excluded, indent=2))
    print(f"renamed {len(kept)} programs; excluded {len(excluded)}")


if __name__ == "__main__":
    main()

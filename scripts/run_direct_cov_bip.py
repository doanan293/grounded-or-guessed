"""Baseline 2b (LLM + coverage) on the BugsInPy targets; one run id per repeat.

    python scripts/run_direct_cov_bip.py --model gemini-3.8-flash-high --run-id direct_cov_bip_gemini_r1
Writes runs/<run_id>.json = {bug: [ranked lines]}; resumable; exits 1 if any bug failed.
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from flx.coverage import load
from flx.direct_cov import run_bip

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    os.environ["FLX_RUN_ID"] = args.run_id
    targets = json.loads((ROOT / "data" / "bugsinpy_targets.json").read_text())
    out = ROOT / "runs" / f"{args.run_id}.json"
    done = json.loads(out.read_text()) if out.exists() else {}
    todo = [b for b in sorted(targets) if b not in done]

    def one(b):
        try:
            return b, run_bip(targets[b], load(ROOT / "data" / "coverage" / "bugsinpy" / f"{b}.json"), args.model)
        except Exception as e:  # recorded as a failure; rerun the same run id to resume
            print(f"{b}: {type(e).__name__}: {e}", file=sys.stderr)
            return b, None

    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for b, lines in pool.map(one, todo):
            if lines is None:
                failed += 1
                continue
            done[b] = lines
            out.write_text(json.dumps(done, indent=1))
    print(f"{args.run_id}: {len(done)}/{len(targets)} bugs, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

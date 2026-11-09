"""Stage 2 of propose-and-verify (flx.pav) on a program list, for one repeat of stage 1.

    python scripts/run_pav.py --programs dev --stage1 data/rankings/direct_tests_dev_gemini_r1.json \\
        --model gemini-3.8-flash-high --run-id pav_dev_gemini_r1 --k 3 --attempts 2
Writes runs/<run_id>.json = {program: {"stage1": [...], "checks": {line: [[passed, size], ...]}}}; resumable;
exits 1 if any program failed. Rankings for chosen knobs are made by scripts/pav_eval.py (no LLM calls).
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.pav import run

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--programs", default="dev", help="dev | test | path to a JSON list")
    ap.add_argument("--stage1", type=Path, required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--attempts", type=int, default=2)
    ap.add_argument("--bench", type=Path, default=SEMLOC_ROOT / "benchmark")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    os.environ["FLX_RUN_ID"] = args.run_id
    progs = (json.loads((ROOT / "data" / "split.json").read_text())[args.programs] if args.programs in ("dev", "test")
             else json.loads(Path(args.programs).read_text()))
    stage1 = json.loads(args.stage1.read_text())
    out = ROOT / "runs" / f"{args.run_id}.json"
    done = json.loads(out.read_text()) if out.exists() else {}
    todo = [p for p in progs if p not in done]

    def one(p):
        try:
            return p, run(p, args.bench, stage1[p], args.model, k=args.k, attempts=args.attempts)
        except Exception as e:
            print(f"{p}: {type(e).__name__}: {e}", file=sys.stderr)
            return p, None

    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for p, res in pool.map(one, todo):
            if res is None:
                failed += 1
                continue
            done[p] = res
            out.write_text(json.dumps(done, indent=1))
    print(f"{args.run_id}: {len(done)}/{len(progs)} programs, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

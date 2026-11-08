"""Run baseline 2b (LLM + coverage evidence) on a program list; one run id per repeat.

    python scripts/run_direct_cov.py --programs test --model gemini-3.8-flash-high --run-id direct_cov_test_gemini_r1
Writes runs/<run_id>.json = {program: [ranked lines]}; resumable; exits 1 if any program failed.
"""
import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.direct_cov import run

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--programs", default="test", help="dev | test | path to a JSON list")
    ap.add_argument("--model", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--bench", type=Path, default=SEMLOC_ROOT / "benchmark")
    ap.add_argument("--cov", type=Path, default=ROOT / "data" / "coverage" / "semfault")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    os.environ["FLX_RUN_ID"] = args.run_id
    progs = (json.loads((ROOT / "data" / "split.json").read_text())[args.programs] if args.programs in ("dev", "test")
             else json.loads(Path(args.programs).read_text()))
    out = ROOT / "runs" / f"{args.run_id}.json"
    done = json.loads(out.read_text()) if out.exists() else {}
    todo = [p for p in progs if p not in done]

    def one(p):
        try:
            return p, run(p, args.bench, load(args.cov / f"{p}.json"), args.model)
        except Exception as e:  # recorded as a failure; the run is then unhealthy
            print(f"{p}: {type(e).__name__}: {e}", file=sys.stderr)
            return p, None

    failed = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for p, lines in pool.map(one, todo):
            if lines is None:
                failed += 1
                continue
            done[p] = lines
            out.write_text(json.dumps(done, indent=1))
    print(f"{args.run_id}: {len(done)}/{len(progs)} programs, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()

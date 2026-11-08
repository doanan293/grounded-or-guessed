"""Collect per-test coverage matrices for every SemFault-250 program (or another benchmark dir).

    python scripts/coverage_all.py --benchmark third_party/semloc/benchmark --out data/coverage/semfault --workers 8
"""
import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from flx.coverage import collect, save


def _one(args):
    name, src, test, out = args
    save(collect(name, src, test), out / f"{name}.json")
    return name


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    gt = json.loads((args.benchmark / "ground_truth.json").read_text())["programs"]
    jobs = [(e["file"].removesuffix(".py"), args.benchmark / "programs" / e["file"],
             args.benchmark / "testcases" / f"test_{e['file']}", args.out) for e in gt]
    jobs = [j for j in jobs if not (args.out / f"{j[0]}.json").exists()]  # resumable
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        done = list(pool.map(_one, jobs))
    print(f"collected {len(done)} new matrices into {args.out}")


if __name__ == "__main__":
    main()

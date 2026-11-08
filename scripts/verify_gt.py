"""Build SemFault-250-verified (spec §3.1): verify / correct each program's ground truth by execution.

    FLX_RUN_ID=verify_gt python scripts/verify_gt.py --model gpt-6-luna --out data/semfault_verified_gt.json [--only a,b]
Resumable: programs already in --out are skipped.
"""
import argparse
import csv
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.verify_gt import llm_propose, verify

ROOT = Path(__file__).resolve().parents[1]
BENCH = SEMLOC_ROOT / "benchmark"


def _one(args):
    entry, executable, model = args
    name = entry["file"].removesuffix(".py")
    return verify(name, BENCH / "programs" / entry["file"], BENCH / "testcases" / f"test_{entry['file']}",
                  entry["function"], entry["faulty_lines"], llm_propose(model), executable=executable)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "semfault_verified_gt.json")
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    os.environ.setdefault("FLX_RUN_ID", "verify_gt")
    labels = {r["program"]: r["category"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv"))}
    done = {r["program"]: r for r in json.loads(args.out.read_text())} if args.out.exists() else {}
    entries = json.loads((BENCH / "ground_truth.json").read_text())["programs"]
    only = set(filter(None, args.only.split(",")))
    jobs = [(e, labels[e["file"][:-3]] != "not_executed", args.model) for e in entries
            if e["file"][:-3] not in done and (not only or e["file"][:-3] in only)]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for r in pool.map(_one, jobs):
            done[r["program"]] = r
            args.out.write_text(json.dumps(sorted(done.values(), key=lambda x: x["program"]), indent=1))
            print(r["program"], r["status"], r["lines"], flush=True)


if __name__ == "__main__":
    main()

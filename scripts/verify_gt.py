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
    entry, executable, model, attempts = args
    name = entry["file"].removesuffix(".py")
    return verify(name, BENCH / "programs" / entry["file"], BENCH / "testcases" / f"test_{entry['file']}",
                  entry["function"], entry["faulty_lines"], llm_propose(model, attempts), executable=executable)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-6-luna")
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "semfault_verified_gt.json")
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--attempts", type=int, default=2)
    ap.add_argument("--retry-status", default="", help="comma list: re-run programs whose status is one of these")
    args = ap.parse_args()
    os.environ.setdefault("FLX_RUN_ID", "verify_gt")
    labels = {r["program"]: r["category"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv"))}
    done = {r["program"]: r for r in json.loads(args.out.read_text())} if args.out.exists() else {}
    entries = json.loads((BENCH / "ground_truth.json").read_text())["programs"]
    only = set(filter(None, args.only.split(",")))
    retry = set(filter(None, args.retry_status.split(",")))
    redo = {p for p, r in done.items() if r["status"] in retry}
    jobs = [(e, labels[e["file"][:-3]] != "not_executed", args.model, args.attempts) for e in entries
            if (e["file"][:-3] not in done or e["file"][:-3] in redo) and (not only or e["file"][:-3] in only)]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for r in pool.map(_one, jobs):
            prev = done.get(r["program"])
            if prev and prev["status"] in ("confirmed", "corrected") and r["status"] not in ("confirmed", "corrected"):
                continue  # a retry never downgrades an earlier verified result
            done[r["program"]] = r
            args.out.write_text(json.dumps(sorted(done.values(), key=lambda x: x["program"]), indent=1))
            print(r["program"], r["status"], r["lines"], flush=True)


if __name__ == "__main__":
    main()

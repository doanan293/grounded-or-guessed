"""RQ3a: targets + per-test coverage (cached in data/) and SemLoc runs (runs/bip_semloc/<run_id>/) on the
BugsInPy bugs that passed the probe (flx.bip.core_ok).

    python scripts/run_bip.py --prepare                      # targets + coverage matrices, no LLM
    python scripts/run_bip.py --run-id bip_semloc_gemini_r1 --model gemini-3.8-flash-high
"""
import argparse
import csv
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from flx.bip import core_ok
from flx.coverage import save

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "bugsinpy_targets.json"
COV = ROOT / "data" / "coverage" / "bugsinpy"


def bugs() -> list[str]:
    return sorted(r["bug_id"] for r in csv.DictReader(open(ROOT / "data" / "bugsinpy_status.csv")) if core_ok(r))


def _prepare(bug):
    from flx.bip_run import coverage_matrix, target
    t = target(bug)
    if t is None:
        return bug, None
    save(coverage_matrix(t), COV / f"{bug}.json")
    return bug, t


def _semloc(args):
    bug, tgt, model, run_id = args
    out = ROOT / "runs" / "bip_semloc" / run_id / f"{bug}.json"
    if out.exists():
        return bug, "cached"
    from flx.bip_run import run_semloc
    try:
        r = run_semloc(tgt, model, 0.8, run_id)
    except Exception as e:
        r = {"error": f"{type(e).__name__}: {e}"}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, indent=1, default=str))
    return bug, r.get("error", "ok")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--run-id")
    ap.add_argument("--model", default="gemini-3.8-flash-high")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if args.prepare:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            targets = {b: t for b, t in pool.map(_prepare, bugs()) if t}
        TARGETS.write_text(json.dumps(targets, indent=1))
        print(f"{len(targets)} targets, coverage in {COV}")
        return
    targets = json.loads(TARGETS.read_text())
    jobs = [(b, t, args.model, args.run_id) for b, t in targets.items()]
    bad = 0
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        for bug, status in pool.map(_semloc, jobs):
            print(bug, status, flush=True)
            bad += status not in ("ok", "cached")
    print(f"{args.run_id}: {len(jobs) - bad}/{len(jobs)} completed")


if __name__ == "__main__":
    main()

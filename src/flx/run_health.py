"""Run health: LLM failures that SemLoc swallowed into its results.

Upstream SemLoc catches LLM exceptions (constraint inference and counterfactual patches) and keeps
going, so a run can "succeed" with degraded programs. A run is healthy only if every LLM call key
of its run_id ended in a success and no counterfactual result has status "Error".

    python -m flx.run_health --workdir runs/X --run-id X [--log runs/llm_log.jsonl]   # exit 1 if unhealthy
"""
import argparse
import json
import os
import sys
from pathlib import Path


def unrecovered_errors(records: list[dict], run_id: str) -> list[str]:
    last: dict[str, dict] = {}
    for r in records:
        if r.get("run_id") == run_id:
            last[r["key"]] = r
    return sorted(k for k, r in last.items() if r.get("error"))


def cf_error_programs(workdir: Path) -> list[str]:
    bad = []
    for f in sorted((Path(workdir) / "refined_base_cf").glob("*.json")):
        if any(isinstance(x, dict) and x.get("status") == "Error" for x in json.loads(f.read_text())):
            bad.append(f.stem)
    return bad


def health(workdir: Path, run_id: str, log: Path) -> dict:
    records = [json.loads(l) for l in open(log)] if Path(log).exists() else []
    errs = unrecovered_errors(records, run_id)
    cf = cf_error_programs(workdir)
    return {"run_id": run_id, "unrecovered_llm_errors": len(errs), "cf_error_programs": cf,
            "healthy": not errs and not cf}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workdir", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--log", type=Path, default=Path(os.environ.get("FLX_LLM_LOG", "runs/llm_log.jsonl")))
    args = ap.parse_args()
    h = health(args.workdir, args.run_id, args.log)
    print(json.dumps(h))
    sys.exit(0 if h["healthy"] else 1)


if __name__ == "__main__":
    main()

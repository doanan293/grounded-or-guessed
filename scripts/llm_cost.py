"""Per-run LLM cost (fresh calls, tokens, latency) and per-program averages → data/llm_cost.csv.

    python scripts/llm_cost.py
Reads the gateway log runs/llm_log.jsonl (git-ignored); the CSV is the committed record. Only experiment
runs are listed (smoke, pilot and GT-verification runs are excluded).
"""
import csv
import json
from pathlib import Path

from flx.cost import run_costs

ROOT = Path(__file__).resolve().parents[1]
PREFIX_N = {"semloc_test_": 200, "direct_test_": 200, "direct_cov_test_": 200, "direct_tests_test_": 200, "semloc_sub50_": 50, "direct_cov_sub50_": 50, "direct_cov_bip_": 31, "direct_tests_bip_": 31, "direct_tests_dev_": 50, "pav_dev_": 50, "pav_test_": 200,
            "direct_cov_renamed_": len(json.loads((ROOT / "data" / "semfault_renamed" / "test_programs.json").read_text())),
            "semloc_dev_": 50, "bip_semloc_": 31,
            "semloc_renamed_": len(json.loads((ROOT / "data" / "semfault_renamed" / "test_programs.json").read_text()))}


# Runs whose output is not used anywhere, with the reason (remove an entry when the run is redone under the same id).
EXCLUDED = {"pav_test_gemini_r1": "aborted on 09/11: provider quota exhausted (429 on 143 of 216 calls); output set aside"}


def main() -> None:
    rows = []
    for run, c in sorted(run_costs(ROOT / "runs" / "llm_log.jsonl").items(), key=lambda kv: str(kv[0])):
        n = next((v for p, v in PREFIX_N.items() if str(run).startswith(p)), None)
        if n is None or str(run) in EXCLUDED:
            continue
        rows.append({"run_id": run, "programs": n, **{k: round(v, 1) if isinstance(v, float) else v for k, v in c.items()},
                     "calls_per_program": round(c["calls"] / n, 3),
                     "tokens_per_program": round((c["prompt_tokens"] + c["completion_tokens"]) / n),
                     "latency_s_per_program": round(c["latency_s"] / n, 1)})
    with open(ROOT / "data" / "llm_cost.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r["run_id"], r["calls_per_program"], r["tokens_per_program"], r["latency_s_per_program"])


if __name__ == "__main__":
    main()

"""Pilot table: our Gemini SemLoc run on the dev split vs published logs on the same programs.

    python scripts/pilot_table.py --run runs/pilot_dev_gemini_r1 --run-id pilot_dev_r1 --out data/pilot_dev_gemini.csv
"""
import argparse
import csv
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.semloc_results import acc_at_k, best_ranks_from_csv, find_localization_csv, median_rank, sbfl_best_ranks, subset

RQ1 = SEMLOC_ROOT / "results" / "RQ1"
GT = SEMLOC_ROOT / "benchmark" / "ground_truth.json"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    dev = json.loads(Path("data/split.json").read_text())["dev"]
    labels = {r["program"]: r["category"] for r in csv.DictReader(open("data/semfault_labels.csv"))}
    sources = {
        "ours: SemLoc gemini-3.8-flash-high T0.8": best_ranks_from_csv(find_localization_csv(args.run)),
        "published: SemLoc gemini-2.5-pro T0.8": best_ranks_from_csv(find_localization_csv(RQ1 / "semloc_gemini_T0.8")),
        "published: SemLoc claude-sonnet-4-6 T0.8": best_ranks_from_csv(find_localization_csv(RQ1 / "semloc_claude_T0.8")),
        "published: SBFL Ochiai": sbfl_best_ranks(RQ1 / "sbfl_ochiai", GT),
    }
    groups = {"all": dev, **{c: [p for p in dev if labels[p] == c] for c in ("semantic", "coverage_revealed", "not_executed")}}
    rows = []
    for name, ranks in sources.items():
        for g, progs in groups.items():
            # programs absent from a source (did not run) count as misses
            r = {p: ranks.get(p) for p in progs}
            rows.append({"source": name, "subset": g, "n": len(progs), "n_ran": sum(p in ranks for p in progs),
                         "acc1": round(acc_at_k(r, 1), 3), "acc3": round(acc_at_k(r, 3), 3),
                         "acc5": round(acc_at_k(r, 5), 3), "median_rank": median_rank(r)})
    log = [json.loads(l) for l in open("runs/llm_log.jsonl")]
    log = [x for x in log if x["run_id"] == args.run_id]
    calls = [x for x in log if not x["cache_hit"]]
    rows.append({"source": "cost (ours)", "subset": "all", "n": len(dev),
                 "n_ran": f"calls={len(calls)} errors={sum(1 for x in log if x['error'])}",
                 "acc1": f"in_tok={sum(x['prompt_tokens'] or 0 for x in calls)}",
                 "acc3": f"out_tok={sum(x['completion_tokens'] or 0 for x in calls)}",
                 "acc5": f"latency_s={round(sum(x['latency_s'] or 0 for x in calls), 1)}", "median_rank": ""})
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()

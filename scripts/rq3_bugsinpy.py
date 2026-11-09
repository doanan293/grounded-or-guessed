"""RQ3a: SemLoc, CovGate and SBFL on the BugsInPy (youtube-dl) targets, per repeat, all bugs and the
bugs whose fault is reached (a buggy-side faulty line is executed by a failing test).

    python scripts/rq3_bugsinpy.py --out data/rq3_bugsinpy.csv
Repeats: runs/bip_semloc/bip_semloc_gemini_r{i}/<bug>.json. CovGate parameters: those chosen on SemFault
dev for the repaired ground truth (data/rq_gt_sensitivity.csv). Also reports the artifact's own metric
(rank of the LLM's guess in its own line scores) to show what the released runner measures.
"""
import argparse
import csv
import json
from pathlib import Path
from statistics import mean, stdev

from flx.bip_score import METHODS, artifact_rank, bug_ranks
from flx.coverage import load
from flx.ranking import metrics
from flx.stats import mcnemar

ROOT = Path(__file__).resolve().parents[1]


def covgate_params() -> dict:
    for r in csv.DictReader(open(ROOT / "data" / "rq_gt_sensitivity.csv")):
        if r["gt"] == "repaired" and r["variant"] == "covgate" and r["config"] == "semloc_gemini_T0.8":
            return {k: v for k, v in json.loads(r["params"]).items() if k in ("gate", "lam", "no_prior")}
    raise KeyError("covgate params")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq3_bugsinpy.csv")
    args = ap.parse_args()
    targets = json.loads((ROOT / "data" / "bugsinpy_targets.json").read_text())
    bugs = sorted(targets)
    covs = {b: load(ROOT / "data" / "coverage" / "bugsinpy" / f"{b}.json") for b in bugs}
    reached = [b for b in bugs if set(targets[b]["faulty_lines"])
               & set().union(*(set(t["lines"]) for t in covs[b]["tests"] if not t["passed"]))]
    params = covgate_params()
    runs = sorted(p for p in (ROOT / "runs" / "bip_semloc").glob("bip_semloc_gemini_r*")
                  if all((p / f"{b}.json").exists() for b in bugs))
    per = {m: [] for m in (*METHODS, "artifact_metric")}
    for run in runs:
        ranks = {m: {} for m in per}
        for b in bugs:
            res = json.loads((run / f"{b}.json").read_text())
            for m, r in bug_ranks(res, covs[b], targets[b]["faulty_lines"], params).items():
                ranks[m][b] = r
            ranks["artifact_metric"][b] = artifact_rank(res)
        for m in per:
            per[m].append(ranks[m])
    # baseline 2b (LLM + coverage), one ranking file per repeat; used only when every repeat covers every bug
    files = [ROOT / "data" / "rankings" / f"direct_cov_bip_gemini_r{i}.json" for i in range(1, len(runs) + 1)]
    preds = [json.loads(f.read_text()) for f in files if f.exists()]
    if len(preds) == len(runs) and all(set(bugs) <= set(p) for p in preds):
        per["llm_coverage"] = [{b: next((k + 1.0 for k, ln in enumerate(p[b]) if ln in targets[b]["faulty_lines"]), None)
                                for b in bugs} for p in preds]
    rows = []
    for subset, progs in (("all", bugs), ("reached", reached)):
        for m, lst in per.items():
            ms = [metrics(r, progs) for r in lst]
            row = {"subset": subset, "method": m, "n": len(progs), "repeats": len(lst)}
            for k in ("acc1", "acc3", "acc5"):
                xs = [x[k] for x in ms]
                row[f"{k}_mean"] = round(mean(xs), 4)
                row[f"{k}_sd"] = round(stdev(xs), 4) if len(xs) > 1 else 0.0
            if m not in ("semloc_prior", "artifact_metric"):  # paired vs SemLoc on the same repeat index
                for k in (1, 3):
                    ps = [mcnemar([r.get(p) is not None and r[p] <= k for p in progs],
                                  [b.get(p) is not None and b[p] <= k for p in progs])[1]
                          for r, b in zip(lst, per["semloc_prior"])]
                    row[f"p_acc{k}_vs_semloc_max"] = round(max(ps), 4)
            rows.append(row)
            print(row)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("subset", "method", "n", "repeats"), k))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(runs)} repeats, {len(bugs)} bugs, {len(reached)} reached, covgate {params}")


if __name__ == "__main__":
    main()

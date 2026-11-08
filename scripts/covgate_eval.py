"""CovGate on the published SemLoc logs (RQ2, secondary evidence): tune on dev, report on test.

    python scripts/covgate_eval.py --out data/rq2_published.csv

Grid: gate ∈ {F,T} × lam ∈ {0, .01, .1, .5} × no_prior ∈ {F,T}. One parameter set is chosen on the
dev split by mean (Acc@3, then Acc@1) over the published configs that ship scores/, then applied
unchanged to the test split. Ranks use fair tie handling and a fixed denominator.
"""
import argparse
import csv
import itertools
import json
from pathlib import Path
from statistics import mean
from typing import Callable

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.covgate import covgate_scores, semloc_attribute
from flx.ranking import metrics, rank_of
from flx.semloc_results import load_ground_truth
from flx.stats import mcnemar

ROOT = Path(__file__).resolve().parents[1]
RQ1 = SEMLOC_ROOT / "results" / "RQ1"
CONFIGS = ["semloc_claude_T0.3", "semloc_claude_T0.8", "semloc_gemini_T0.0", "semloc_gemini_T0.3", "semloc_gemini_T0.8"]
GRID = [{"gate": g, "lam": l, "no_prior": n, "grounded_prior": gp}
        for g, l, n, gp in itertools.product([False, True], [0.0, 0.01, 0.1, 0.5], [False, True], [False, True])
        if not (n and gp)]  # grounded_prior only matters when the prior is kept
BASELINE = {"gate": False, "lam": 0.0, "no_prior": False, "grounded_prior": False}  # = SemLoc as published (fair ties)


def tune(dev: list[str], grid: list[dict], rank_fn: Callable[[dict, str], float | None]) -> dict:
    def key(params):
        m = metrics({p: rank_fn(params, p) for p in dev}, dev)
        return (m["acc3"], m["acc1"])
    return max(grid, key=key)


def make_rank_fn(cfg: str, gt: dict, cov_dir: Path) -> Callable[[dict, str], float | None]:
    cache = {}

    def rank_fn(params, prog):
        if prog not in cache:
            f = RQ1 / cfg / "scores" / f"{prog}.json"
            c = RQ1 / cfg / "constraints" / f"{prog}.json"
            attr = semloc_attribute(c, SEMLOC_ROOT / "benchmark" / "programs" / f"{prog}.py") if c.exists() else None
            cache[prog] = (json.loads(f.read_text()) if f.exists() else None, load(cov_dir / f"{prog}.json"), attr)
        sem, cov, attr = cache[prog]
        if sem is None:
            return None
        return rank_of(covgate_scores(sem, cov, attribute=attr, **params), gt[prog], "average")
    return rank_fn


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq2_published.csv")
    args = ap.parse_args()
    gt = load_ground_truth(SEMLOC_ROOT / "benchmark" / "ground_truth.json")
    split = json.loads((ROOT / "data" / "split.json").read_text())
    labels = {r["program"]: r["category"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv"))}
    cov_dir = ROOT / "data" / "coverage" / "semfault"
    fns = {cfg: make_rank_fn(cfg, gt, cov_dir) for cfg in CONFIGS}

    def pooled(params, prog_list):
        ms = [metrics({p: fns[c](params, p) for p in prog_list}, prog_list) for c in CONFIGS]
        return mean(m["acc3"] for m in ms), mean(m["acc1"] for m in ms)
    best = max(GRID, key=lambda prm: pooled(prm, split["dev"]))
    dev_exec = [p for p in split["dev"] if labels[p] != "not_executed"]
    best_exec = max(GRID, key=lambda prm: pooled(prm, dev_exec))  # still dev-only: excludes broken GT
    print("chosen on dev:", best, "| chosen on dev (executable GT):", best_exec)

    variants = {"semloc": BASELINE, "covgate": best, "covgate_exec_tuned": best_exec,
                "gate_only": {**BASELINE, "gate": True}, "lam_only": {**BASELINE, "lam": best["lam"] or 0.01},
                "no_prior_only": {**BASELINE, "no_prior": True},
                "grounded_prior_only": {**BASELINE, "grounded_prior": True}}
    subsets = {"test": split["test"], "test_executable": [p for p in split["test"] if labels[p] != "not_executed"]}
    rows = []
    for cfg in CONFIGS:
        for sub, progs in subsets.items():
            base = {p: fns[cfg](BASELINE, p) for p in progs}
            for name, prm in variants.items():
                ranks = {p: fns[cfg](prm, p) for p in progs}
                m = metrics(ranks, progs)
                row = {"config": cfg, "subset": sub, "variant": name, "params": json.dumps(prm), **m}
                for k in (1, 3):
                    a = [ranks[p] is not None and ranks[p] <= k for p in progs]
                    b = [base[p] is not None and base[p] <= k for p in progs]
                    row[f"mcnemar_p_acc{k}"] = mcnemar(a, b)[1]
                rows.append(row)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)
    print(f"wrote {args.out} ({len(rows)} rows)")


if __name__ == "__main__":
    main()

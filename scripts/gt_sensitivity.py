"""RQ1/RQ2 under three ground truths: original, repaired (execution-verified corrections), verified_strict.
CovGate parameters are re-tuned on dev under each ground truth (dev-only), reported on test.

    python scripts/gt_sensitivity.py --out data/rq_gt_sensitivity.csv
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
from statistics import mean

from flx.coverage import load
from flx.gt import load_variants
from flx.ranking import metrics, rank_of
from flx.sbfl import sbfl_scores
from flx.stats import mcnemar

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("covgate_eval", ROOT / "scripts" / "covgate_eval.py")
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq_gt_sensitivity.csv")
    args = ap.parse_args()
    split = json.loads((ROOT / "data" / "split.json").read_text())
    cov_dir = ROOT / "data" / "coverage" / "semfault"
    rows = []
    for gname, gt in load_variants().items():
        dev = [p for p in split["dev"] if p in gt]
        test = [p for p in split["test"] if p in gt]
        fns = {cfg: ce.make_rank_fn(cfg, gt, cov_dir) for cfg in ce.CONFIGS}
        best = ce.tune(dev, ce.GRID, [fns[c] for c in ce.CONFIGS])
        sbfl = {p: rank_of(sbfl_scores(load(cov_dir / f"{p}.json"), "ochiai"), gt[p], "average") for p in test}
        m = metrics(sbfl, test)
        rows.append({"gt": gname, "config": "sbfl_ochiai", "variant": "-", "n": m["n"], "acc1": m["acc1"], "acc3": m["acc3"],
                     "acc5": m["acc5"], "params": "", "p_acc1": "", "p_acc3": ""})
        for cfg in ce.CONFIGS:
            base = {p: fns[cfg](ce.BASELINE, p) for p in test}
            for name, prm in (("semloc", ce.BASELINE), ("covgate", best), ("no_prior", {**ce.BASELINE, "no_prior": True}),
                              ("gate_only", {**ce.BASELINE, "gate": True})):
                ranks = {p: fns[cfg](prm, p) for p in test}
                m = metrics(ranks, test)
                ps = [mcnemar([ranks[p] is not None and ranks[p] <= k for p in test],
                              [base[p] is not None and base[p] <= k for p in test])[1] for k in (1, 3)]
                rows.append({"gt": gname, "config": cfg, "variant": name, "n": m["n"], "acc1": m["acc1"], "acc3": m["acc3"],
                             "acc5": m["acc5"], "params": json.dumps(prm), "p_acc1": ps[0], "p_acc3": ps[1]})
        print(gname, "n_test", len(test), "chosen on dev:", best)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)


if __name__ == "__main__":
    main()

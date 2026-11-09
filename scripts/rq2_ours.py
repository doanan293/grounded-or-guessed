"""RQ2 on our own runs (paired, same model and time): SemLoc vs CovGate vs ablations vs baselines,
per repeat, on the original and repaired ground truth.

    python scripts/rq2_ours.py --out data/rq2_ours.csv
Repeats found: runs/semloc_test_gemini_r{i} (SemLoc), data/rankings/direct_test_gemini_r{i}.json (LLM direct),
data/rankings/direct_cov_test_gemini_r{i}.json (LLM + coverage). CovGate parameters: chosen on dev under
each ground truth by scripts/gt_sensitivity.py (data/rq_gt_sensitivity.csv).
"""
import argparse
import csv
import json
from pathlib import Path
from statistics import mean, stdev

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.covgate import covgate_scores, semloc_attribute
from flx.gt import load_variants
from flx.params import chosen_params
from flx.labels import labels_for
from flx.ranking import mean_rr, metrics, rank_of
from flx.sbfl import sbfl_scores
from flx.stats import mcnemar, paired_diff_ci, paired_rank_biserial, wilcoxon_paired

ROOT = Path(__file__).resolve().parents[1]
COV = ROOT / "data" / "coverage" / "semfault"
CLUSTERS = {r["program"]: int(r["cluster_t0.8"]) for r in csv.DictReader(open(ROOT / "data" / "semfault_templates.csv"))}


def ranks_from_list(preds: dict, gt: dict, progs: list[str]) -> dict:
    return {p: next((k + 1.0 for k, ln in enumerate(preds.get(p, [])) if ln in gt.get(p, [])), None) for p in progs}


def mean_sd(xs: list[float]) -> tuple[float, float]:
    return (round(mean(xs), 4), round(stdev(xs), 4) if len(xs) > 1 else 0.0)


def semloc_variants(run: Path, gt: dict, progs: list[str], params: dict) -> dict[str, dict]:
    out = {k: {} for k in ("semloc", "semloc_no_prior", "covgate", "cf_rerank", "covgate_cf",
                           "gate_only", "lam_only", "grounded_prior_only")}
    for p in progs:
        f = run / "scores" / f"{p}.json"
        if not f.exists():
            continue
        sem, cov = json.loads(f.read_text()), load(COV / f"{p}.json")
        cfp = run / "refined_base_cf" / f"{p}.json"
        cf = json.loads(cfp.read_text()) if cfp.exists() else None
        attr = semloc_attribute(run / "constraints" / f"{p}.json", run / "programs" / f"{p}.py")
        base = {"gate": False, "lam": 0.0, "no_prior": False}
        prm = dict(params)  # every dev-chosen knob, grounded_prior included
        out["semloc"][p] = rank_of(covgate_scores(sem, cov, **base), gt[p])
        out["semloc_no_prior"][p] = rank_of(covgate_scores(sem, cov, **{**base, "no_prior": True}), gt[p])
        out["covgate"][p] = rank_of(covgate_scores(sem, cov, **prm, attribute=attr), gt[p])
        # one-component ablations on top of SemLoc as released
        out["gate_only"][p] = rank_of(covgate_scores(sem, cov, **{**base, "gate": True}), gt[p])
        out["lam_only"][p] = rank_of(covgate_scores(sem, cov, **{**base, "lam": params["lam"] or 0.01}), gt[p])
        out["grounded_prior_only"][p] = rank_of(covgate_scores(sem, cov, **base, grounded_prior=True, attribute=attr), gt[p])
        out["cf_rerank"][p] = rank_of(covgate_scores(sem, cov, **base, cf=cf, attribute=attr), gt[p])
        out["covgate_cf"][p] = rank_of(covgate_scores(sem, cov, **prm, cf=cf, attribute=attr), gt[p])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq2_ours.csv")
    args = ap.parse_args()
    test = json.loads((ROOT / "data" / "split.json").read_text())["test"]
    reps = [i for i in (1, 2, 3) if (ROOT / "runs" / f"semloc_test_gemini_r{i}" / "results_cf_base" / "summary.json").exists()]  # finished runs only
    rows = []
    for gname, gt in load_variants().items():
        if gname == "verified_strict":
            continue
        progs = [p for p in test if p in gt]
        params = chosen_params(gname)
        per = {}  # method -> list of (rep, ranks)
        for i in reps:
            methods = semloc_variants(ROOT / "runs" / f"semloc_test_gemini_r{i}", gt, progs, params)
            for name, fname in (("llm_direct", f"direct_test_gemini_r{i}.json"), ("llm_coverage", f"direct_cov_test_gemini_r{i}.json")):
                f = ROOT / "data" / "rankings" / fname
                if f.exists():
                    methods[name] = ranks_from_list(json.loads(f.read_text()), gt, progs)
            methods["sbfl_ochiai"] = {p: rank_of(sbfl_scores(load(COV / f"{p}.json"), "ochiai"), gt[p]) for p in progs}
            for name, ranks in methods.items():
                per.setdefault(name, []).append((i, ranks))
        labels = labels_for({p: gt[p] for p in progs}, COV)  # labels of *this* ground truth
        subsets = {"all": progs, "executable": [p for p in progs if labels[p] != "not_executed"],
                   **{c: [p for p in progs if labels[p] == c] for c in ("semantic", "coverage_revealed", "not_executed")}}
        for sub, plist in subsets.items():
            if not plist:
                continue
            for name, lst in per.items():
                ms = [metrics(r, plist) for _, r in lst]
                row = {"gt": gname, "subset": sub, "method": name, "n": len(plist), "repeats": len(lst)}
                for k in ("acc1", "acc3", "acc5"):
                    row[f"{k}_mean"], row[f"{k}_sd"] = mean_sd([m[k] for m in ms])
                # paired McNemar vs SemLoc on the same repeat (max p across repeats: conservative)
                if name != "semloc":
                    for k in (1, 3):
                        ps = []
                        for (i, ranks), (_, base) in zip(lst, per["semloc"]):
                            a = [ranks.get(p) is not None and ranks[p] <= k for p in plist]
                            b = [base.get(p) is not None and base[p] <= k for p in plist]
                            ps.append(mcnemar(a, b)[1])
                        row[f"p_acc{k}_max"] = round(max(ps), 4)
                        row[f"p_acc{k}_all"] = ";".join(f"{x:.4f}" for x in ps)
                        hits = lambda reps: [{p: r.get(p) is not None and r[p] <= k for p in plist} for _, r in reps]
                        d, lo, hi = paired_diff_ci(hits(lst), hits(per["semloc"]), plist, CLUSTERS)
                        row[f"d_acc{k}"], row[f"d_acc{k}_lo"], row[f"d_acc{k}_hi"] = d, lo, hi
                    # per-program reciprocal rank (mean over repeats), paired with SemLoc: Wilcoxon signed-rank and its
                    # effect size, the matched-pairs rank-biserial correlation
                    x, y = mean_rr([r for _, r in lst], plist), mean_rr([r for _, r in per["semloc"]], plist)
                    row["p_rr_wilcoxon"] = round(wilcoxon_paired([x[p] for p in plist], [y[p] for p in plist])[1], 4)
                    row["rank_biserial_rr"] = round(paired_rank_biserial([x[p] for p in plist], [y[p] for p in plist]), 4)
                rows.append(row)
                print(row)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("gt", "subset", "method", "n", "repeats"), k))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

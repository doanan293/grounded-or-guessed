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
from flx.ranking import mean_rr, metrics, rank_of
from flx.sbfl import sbfl_scores
from flx.stats import cliffs_delta, mcnemar, wilcoxon_paired

ROOT = Path(__file__).resolve().parents[1]
COV = ROOT / "data" / "coverage" / "semfault"


def ranks_from_list(preds: dict, gt: dict, progs: list[str]) -> dict:
    return {p: next((k + 1.0 for k, ln in enumerate(preds.get(p, [])) if ln in gt.get(p, [])), None) for p in progs}


def mean_sd(xs: list[float]) -> tuple[float, float]:
    return (round(mean(xs), 4), round(stdev(xs), 4) if len(xs) > 1 else 0.0)


def chosen_params(gname: str) -> dict:
    for r in csv.DictReader(open(ROOT / "data" / "rq_gt_sensitivity.csv")):
        if r["gt"] == gname and r["variant"] == "covgate":
            return json.loads(r["params"])
    raise KeyError(gname)


def semloc_variants(run: Path, gt: dict, progs: list[str], params: dict) -> dict[str, dict]:
    out = {k: {} for k in ("semloc", "semloc_no_prior", "covgate", "cf_rerank", "covgate_cf")}
    for p in progs:
        f = run / "scores" / f"{p}.json"
        if not f.exists():
            continue
        sem, cov = json.loads(f.read_text()), load(COV / f"{p}.json")
        cfp = run / "refined_base_cf" / f"{p}.json"
        cf = json.loads(cfp.read_text()) if cfp.exists() else None
        attr = semloc_attribute(run / "constraints" / f"{p}.json", SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py") if cf else None
        base = {"gate": False, "lam": 0.0, "no_prior": False}
        prm = {k: params[k] for k in ("gate", "lam", "no_prior")}
        out["semloc"][p] = rank_of(covgate_scores(sem, cov, **base), gt[p])
        out["semloc_no_prior"][p] = rank_of(covgate_scores(sem, cov, **{**base, "no_prior": True}), gt[p])
        out["covgate"][p] = rank_of(covgate_scores(sem, cov, **prm), gt[p])
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
        for name, lst in per.items():
            ms = [metrics(r, progs) for _, r in lst]
            row = {"gt": gname, "method": name, "n": len(progs), "repeats": len(lst)}
            for k in ("acc1", "acc3", "acc5"):
                row[f"{k}_mean"], row[f"{k}_sd"] = mean_sd([m[k] for m in ms])
            # paired McNemar vs SemLoc on the same repeat (max p across repeats: conservative)
            if name != "semloc":
                for k in (1, 3):
                    ps = []
                    for (i, ranks), (_, base) in zip(lst, per["semloc"]):
                        a = [ranks.get(p) is not None and ranks[p] <= k for p in progs]
                        b = [base.get(p) is not None and base[p] <= k for p in progs]
                        ps.append(mcnemar(a, b)[1])
                    row[f"p_acc{k}_max"] = round(max(ps), 4)
                # per-program reciprocal rank (mean over repeats): Wilcoxon signed-rank and Cliff's delta vs SemLoc
                x, y = mean_rr([r for _, r in lst], progs), mean_rr([r for _, r in per["semloc"]], progs)
                row["p_rr_wilcoxon"] = round(wilcoxon_paired([x[p] for p in progs], [y[p] for p in progs])[1], 4)
                row["cliffs_delta_rr"] = round(cliffs_delta([x[p] for p in progs], [y[p] for p in progs]), 4)
            rows.append(row)
            print(row)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("gt", "method", "n", "repeats"), k))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

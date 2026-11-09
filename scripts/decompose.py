"""Grounded or guessed: Shapley decomposition of Acc@1 / Acc@3 over signals {guess, spectrum, coverage[, cf]}.

    python scripts/decompose.py --published --out data/rq_decomposition_published.csv   # released logs, 3 players
    python scripts/decompose.py --runs semloc_test_gemini_r1 semloc_test_gemini_r2 semloc_test_gemini_r3 \
        --out data/rq_decomposition.csv                                                  # our runs, 4 players
Acc@k is a mean of per-program hits, so the decomposition is the mean of per-program Shapley values; several
runs are pooled by averaging each program's values over runs. 95% CIs resample programs (bootstrap) and
template clusters (cluster bootstrap, data/semfault_templates.csv), 10,000 draws each.
"""
import argparse
import csv
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.covgate import semloc_attribute
from flx.decompose import component_scores, per_program_shapley
from flx.gt import load_variants
from flx.labels import labels_for
from flx.ranking import rank_of
from flx.stats import cluster_bootstrap_ci

ROOT = Path(__file__).resolve().parents[1]
# "semloc": grand coalition = SemLoc as released (spectrum + its +1.2 guess bonus) — the headline split.
# "all_signals": adds coverage (raw Ochiai) and CF re-ranking; its total is a different system than SemLoc.
GAMES = {"semloc": ["guess", "spectrum"], "all_signals": ["guess", "spectrum", "coverage", "cf"]}
COV = ROOT / "data" / "coverage" / "semfault"


def load_run(score_dir: Path, programs: list[str], cf_dir: Path | None, constraints_dir: Path | None) -> dict:
    data = {}
    for p in programs:
        f = score_dir / f"{p}.json"
        if not f.exists():
            continue
        cf = json.loads((cf_dir / f"{p}.json").read_text()) if cf_dir and (cf_dir / f"{p}.json").exists() else None
        attr = (semloc_attribute(constraints_dir / f"{p}.json", SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py")
                if cf and constraints_dir and (constraints_dir / f"{p}.json").exists() else None)
        data[p] = (json.loads(f.read_text()), load(COV / f"{p}.json"), cf, attr)
    return data


def per_program_phi(data: dict, gt: dict, programs: list[str], players: list[str], k: int) -> dict:
    def values(on):
        out = {}
        for p in programs:
            if p not in data:
                out[p] = 0.0  # tool produced nothing for p: a miss under every coalition
                continue
            s, c, cf, a = data[p]
            r = rank_of(component_scores(s, c, on, attribute=a, cf=cf), gt[p], "average")
            out[p] = float(r is not None and r <= k)
        return out
    full = values(frozenset(players))
    return {p: {**phi, "full": full[p]} for p, phi in per_program_shapley(values, players, programs).items()}


def summarize(per: dict, players: list[str], clusters: dict) -> dict:
    out = {}
    for key in ["full"] + players:
        vals = {p: v[key] for p, v in per.items()}
        name = "full" if key == "full" else f"phi_{key}"
        out[name] = sum(vals.values()) / len(vals)
        out[f"{name}_ci_prog"] = cluster_bootstrap_ci(vals, {p: i for i, p in enumerate(vals)})
        out[f"{name}_ci_cluster"] = cluster_bootstrap_ci(vals, clusters)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--published", action="store_true")
    ap.add_argument("--runs", nargs="*", default=[])
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq_decomposition.csv")
    args = ap.parse_args()
    clusters = {r["program"]: int(r["cluster_t0.8"]) for r in csv.DictReader(open(ROOT / "data" / "semfault_templates.csv"))}
    variants = {g: v for g, v in load_variants().items() if g in ("original", "repaired")}
    sources = []  # (name, [(score_dir, cf_dir, constraints_dir)], candidate programs, players)
    if args.published:
        for cfg in ("semloc_claude_T0.3", "semloc_claude_T0.8", "semloc_gemini_T0.0", "semloc_gemini_T0.3", "semloc_gemini_T0.8"):
            d = SEMLOC_ROOT / "results" / "RQ1" / cfg
            sources.append((cfg, [(d / "scores", None, None)], sorted(variants["original"]), "semloc", GAMES["semloc"]))
            sources.append((cfg, [(d / "scores", None, None)], sorted(variants["original"]), "all_signals",
                            ["guess", "spectrum", "coverage"]))  # released logs carry no CF verdicts
    if args.runs:
        dirs = [ROOT / "runs" / r for r in args.runs]
        progs = sorted({p.stem for d in dirs for p in (d / "scores").glob("*.json")})
        name = args.runs[0].rsplit("_r", 1)[0] + f" ({len(dirs)} runs)"
        for game, players in GAMES.items():
            sources.append((name, [(d / "scores", d / "refined_base_cf", d / "constraints") for d in dirs], progs,
                            game, players))
    rows = []
    for name, run_dirs, cand, game, players in sources:
        loaded = [load_run(s, cand, c, k) for s, c, k in run_dirs]
        for gname, gt in variants.items():
            progs = [p for p in cand if p in gt]
            labels = labels_for({p: gt[p] for p in progs}, COV)  # labels of this ground truth, not the original's
            for sub, plist in (("all", progs), ("executable", [p for p in progs if labels[p] != "not_executed"])):
                for k in (1, 3):
                    runs_phi = [per_program_phi(d, gt, plist, players, k) for d in loaded]
                    per = {p: {key: sum(r[p][key] for r in runs_phi) / len(runs_phi) for key in runs_phi[0][p]} for p in plist}
                    res = summarize(per, players, clusters)
                    row = {"source": name, "game": game, "gt": gname, "subset": sub, "metric": f"acc{k}",
                           "n": len(plist), "runs": len(loaded)}
                    for key, v in res.items():
                        if isinstance(v, tuple):
                            row[f"{key}_lo"], row[f"{key}_hi"] = round(v[0], 4), round(v[1], 4)
                        else:
                            row[key] = round(v, 4)
                    rows.append(row)
                    print(name, game, gname, sub, f"acc{k}", {kk: row[kk] for kk in row if kk == "full" or
                                                       (kk.startswith("phi_") and "_ci_" not in kk)})
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

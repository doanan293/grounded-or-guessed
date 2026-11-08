"""Grounded or guessed: Shapley decomposition of Acc@1 / Acc@3 over signals {guess, spectrum, coverage[, cf]}.

    python scripts/decompose.py --published            # SemLoc's released logs (no CF data → 3 players)
    python scripts/decompose.py --runs semloc_test_gemini_r1 semloc_test_gemini_r2 ...   # our runs (4 players)
"""
import argparse
import csv
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.covgate import semloc_attribute
from flx.decompose import component_scores, shapley
from flx.ranking import metrics, rank_of
from flx.semloc_results import load_ground_truth

ROOT = Path(__file__).resolve().parents[1]
GT = load_ground_truth(SEMLOC_ROOT / "benchmark" / "ground_truth.json")
COV = ROOT / "data" / "coverage" / "semfault"


def decompose(score_dir: Path, programs: list[str], players: list[str], cf_dir: Path | None = None,
              constraints_dir: Path | None = None) -> dict:
    data = {}
    for p in programs:
        f = score_dir / f"{p}.json"
        if not f.exists():
            continue
        cf = json.loads((cf_dir / f"{p}.json").read_text()) if cf_dir and (cf_dir / f"{p}.json").exists() else None
        attr = (semloc_attribute(constraints_dir / f"{p}.json", SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py")
                if cf and constraints_dir and (constraints_dir / f"{p}.json").exists() else None)
        data[p] = (json.loads(f.read_text()), load(COV / f"{p}.json"), cf, attr)
    out = {}
    for k in (1, 3):
        def value(on):
            ranks = {p: rank_of(component_scores(s, c, on, attribute=a, cf=cf), GT[p], "average")
                     for p, (s, c, cf, a) in data.items()}
            return metrics(ranks, programs)[f"acc{k}"]
        phi = shapley(value, players)
        out[f"acc{k}"] = {"full": value(frozenset(players)), **{f"phi_{p}": v for p, v in phi.items()}}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--published", action="store_true")
    ap.add_argument("--runs", nargs="*", default=[])
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq_decomposition.csv")
    args = ap.parse_args()
    labels = {r["program"]: r["category"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv"))}
    split = json.loads((ROOT / "data" / "split.json").read_text())
    rows = []
    sources = []
    if args.published:
        for cfg in ("semloc_claude_T0.3", "semloc_claude_T0.8", "semloc_gemini_T0.0", "semloc_gemini_T0.3", "semloc_gemini_T0.8"):
            d = SEMLOC_ROOT / "results" / "RQ1" / cfg
            sources.append((cfg, d / "scores", None, None, sorted(GT), ["guess", "spectrum", "coverage"]))
    for run in args.runs:
        d = ROOT / "runs" / run
        progs = sorted(p.stem for p in (d / "scores").glob("*.json"))
        sources.append((run, d / "scores", d / "refined_base_cf", d / "constraints", progs, ["guess", "spectrum", "coverage", "cf"]))
    for name, sdir, cfdir, cdir, progs, players in sources:
        for sub, plist in (("all", progs), ("executable", [p for p in progs if labels[p] != "not_executed"])):
            res = decompose(sdir, plist, players, cfdir, cdir)
            for metric, vals in res.items():
                rows.append({"source": name, "subset": sub, "metric": metric, "n": len(plist), **{k: round(v, 4) for k, v in vals.items()}})
                print(name, sub, metric, {k: round(v, 3) for k, v in vals.items()})
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("source", "subset", "metric", "n", "full"), k))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

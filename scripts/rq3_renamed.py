"""RQ3b (memorization check): SemLoc Gemini on the original vs the identifier-renamed test programs,
paired by repeat (original r_i vs renamed r_i), original and repaired ground truth.

    python scripts/rq3_renamed.py --out data/rq3_renamed.csv
Renaming preserves line numbers and per-test behaviour (data/renamed/, 199 test programs), so ground
truth and coverage carry over unchanged. Also reports how often the LLM's own guess stays the same line.
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path
from statistics import mean, stdev

from flx.gt import load_variants
from flx.ranking import metrics
from flx.stats import mcnemar

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rq3_families", ROOT / "scripts" / "rq3_families.py")
fam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fam)

METHODS = ("semloc", "semloc_no_prior", "llm_guess")


def ranks_from_file(f: Path, gt: dict, progs: list[str]) -> dict:
    preds = json.loads(f.read_text())
    return {p: next((k + 1.0 for k, ln in enumerate(preds.get(p, [])) if ln in gt[p]), None) for p in progs}


def guesses(run: Path, progs: list[str]) -> dict:
    out = {}
    for p in progs:
        f = run / "scores" / f"{p}.json"
        if f.exists():
            out[p] = json.loads(f.read_text()).get("fault_line_pred")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq3_renamed.csv")
    args = ap.parse_args()
    names = json.loads((ROOT / "data" / "renamed" / "test_programs.json").read_text())
    orig = {r.name.rsplit("_r", 1)[1]: r for r in fam.usable_runs(ROOT / "runs", "semloc_test_gemini")}
    ren = {r.name.rsplit("_r", 1)[1]: r for r in fam.usable_runs(ROOT / "runs", "semloc_renamed_gemini")}
    pairs = [(orig[i], ren[i]) for i in sorted(set(orig) & set(ren))]
    rows = []
    for gname, gt in load_variants().items():
        if gname == "verified_strict":
            continue
        progs = [p for p in names if p in gt]
        methods = list(METHODS) + (["llm_coverage"] if all(
            (ROOT / "data" / "rankings" / f"direct_cov_{s}_gemini_r{i}.json").exists()
            for s in ("test", "renamed") for i in range(1, len(pairs) + 1)) else [])
        for method in methods:
            if method == "llm_coverage":  # baseline 2b: original = test-split run, renamed = renamed run, same repeat
                per = [tuple(ranks_from_file(ROOT / "data" / "rankings" / f"direct_cov_{s}_gemini_r{i}.json", gt, progs)
                             for s in ("test", "renamed")) for i in range(1, len(pairs) + 1)]
            else:
                per = [(fam.run_ranks(o, gt, progs, method), fam.run_ranks(r, gt, progs, method)) for o, r in pairs]
            row = {"gt": gname, "method": method, "n": len(progs), "repeats": len(per)}
            for side, idx in (("orig", 0), ("renamed", 1)):
                for k in ("acc1", "acc3", "acc5"):
                    vals = [metrics(x[idx], progs)[k] for x in per]
                    row[f"{side}_{k}_mean"] = round(mean(vals), 4)
                    row[f"{side}_{k}_sd"] = round(stdev(vals), 4) if len(vals) > 1 else 0.0
            for k in (1, 3):
                ps = [mcnemar([o.get(p) is not None and o[p] <= k for p in progs],
                              [r.get(p) is not None and r[p] <= k for p in progs])[1] for o, r in per]
                row[f"p_acc{k}_max"] = round(max(ps), 4)
            rows.append(row)
            print(row)
    same = [mean(go.get(p) == gr.get(p) for p in names) for go, gr in
            ((guesses(o, names), guesses(r, names)) for o, r in pairs)]
    print(f"{len(pairs)} paired repeats; LLM guess identical after renaming: {[round(s, 3) for s in same]}")
    for r in rows:
        r["guess_same_line_mean"] = round(mean(same), 4)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

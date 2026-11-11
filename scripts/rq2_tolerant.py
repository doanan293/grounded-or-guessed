"""RQ2 under a header/body-tolerant ground truth: a secondary metric next to the exact-line one, same runs, all methods.

    python scripts/rq2_tolerant.py --out data/rq2_tolerant.csv
A predicted line also counts when it and a ground-truth line are the header of a compound statement (if/for/while/
with/try) and the statement it guards (flx.failures.line_relation). "strict" accepts only the header and the first
line of its body (lower bound, the reported secondary metric); "lenient" also accepts the rest of a first body
statement of at most 3 lines (upper bound). Rankings, repeats and CovGate parameters are exactly those of
scripts/rq2_ours.py; only the set of accepted lines changes, so exact Acc@k stays the primary metric.
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.failures import line_relation
from flx.gt import load_variants
from flx.params import chosen_params
from flx.ranking import metrics, rank_of
from flx.sbfl import sbfl_scores
from flx.stats import paired_diff_ci

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rq2_ours", ROOT / "scripts" / "rq2_ours.py")
rq2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rq2)
COV = rq2.COV


def tolerant_gt(gt: dict, sources: dict, strict: bool) -> dict:
    """Every ground-truth line plus each line in a header/body relation with one of them."""
    out = {}
    for p, lines in gt.items():
        src = sources[p]
        n = len(src.splitlines())
        out[p] = sorted({x for x in range(1, n + 1)
                         if any(line_relation(src, t, x, strict) in ("same", "header_body") for t in lines)} | set(lines))
    return out


def per_method_ranks(gt: dict, progs: list[str], params: dict, reps: list[int]) -> dict:
    per = {}
    for i in reps:
        methods = rq2.semloc_variants(ROOT / "runs" / f"semloc_test_gemini_r{i}", gt, progs, params)
        for name, fname in (("llm_direct", f"direct_test_gemini_r{i}.json"), ("llm_tests", f"direct_tests_test_gemini_r{i}.json"),
                            ("llm_coverage", f"direct_cov_test_gemini_r{i}.json")):
            f = ROOT / "data" / "rankings" / fname
            if f.exists():
                methods[name] = rq2.ranks_from_list(json.loads(f.read_text()), gt, progs)
        methods["sbfl_ochiai"] = {p: rank_of(sbfl_scores(load(COV / f"{p}.json"), "ochiai"), gt[p]) for p in progs}
        for name, ranks in methods.items():
            per.setdefault(name, []).append(ranks)
    return per


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq2_tolerant.csv")
    args = ap.parse_args()
    test = json.loads((ROOT / "data" / "split.json").read_text())["test"]
    reps = [i for i in (1, 2, 3) if (ROOT / "runs" / f"semloc_test_gemini_r{i}" / "results_cf_base" / "summary.json").exists()]
    sources = {p: (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text() for p in test}
    rows = []
    for gname, gt in load_variants().items():
        if gname == "verified_strict":
            continue
        progs = [p for p in test if p in gt]
        params = chosen_params(gname)  # chosen on dev under the exact metric, unchanged here
        exact = per_method_ranks(gt, progs, params, reps)
        tight = per_method_ranks(tolerant_gt({p: gt[p] for p in progs}, sources, True), progs, params, reps)
        loose = per_method_ranks(tolerant_gt({p: gt[p] for p in progs}, sources, False), progs, params, reps)
        for name in exact:
            mean = lambda per, k: round(sum(metrics(r, progs)[k] for r in per[name]) / len(per[name]), 4)
            row = {"gt": gname, "method": name, "n": len(progs), "repeats": len(exact[name]),
                   "acc1_exact": mean(exact, "acc1"), "acc3_exact": mean(exact, "acc3"),
                   "acc1_tol": mean(tight, "acc1"), "acc3_tol": mean(tight, "acc3"),
                   "acc1_tol_lenient": mean(loose, "acc1")}
            if name != "semloc":  # paired with SemLoc on the same repeat, cluster bootstrap as in rq2_ours.py
                for k in (1, 3):
                    hits = lambda reps_: [{p: r.get(p) is not None and r[p] <= k for p in progs} for r in reps_]
                    d, lo, hi = paired_diff_ci(hits(tight[name]), hits(tight["semloc"]), progs, rq2.CLUSTERS)
                    row[f"d_acc{k}_tol"], row[f"d_acc{k}_tol_lo"], row[f"d_acc{k}_tol_hi"] = d, lo, hi
            rows.append(row)
            print(row)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k not in ("gt", "method", "n", "repeats"), k))
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

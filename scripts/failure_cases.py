"""Failure analysis inputs (Phase 3.2): per-program signals and categories over the 200 test programs, and a
cluster-spread sample of cases with everything needed to read them.

    python scripts/failure_cases.py
Writes data/failure_signals.csv (one row per test program) and data/failure_cases.csv (the sample). Repaired ground
truth; SemLoc = our 3 Gemini repeats; LLM + coverage = data/rankings/direct_cov_test_gemini_r*.json. A boolean
signal is the majority over repeats; spectrum_rank is the median rank without the guess bonus (blank = unranked).
"""
import csv
import importlib.util
import json
from pathlib import Path
from statistics import median

from collections import Counter

from flx.failures import CATEGORIES, category, line_relation, select
from flx.gt import load_variants
from flx.labels import labels_for

ROOT = Path(__file__).resolve().parents[1]
COV = ROOT / "data" / "coverage" / "semfault"
_spec = importlib.util.spec_from_file_location("rq3_families", ROOT / "scripts" / "rq3_families.py")
fam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fam)
PER_CATEGORY = 4
REL_ORDER = ["same", "header_body", "blank_gt", "other", "none"]
SEED = 20261108


def majority(xs: list[bool]) -> bool:
    return sum(xs) * 2 > len(xs)


def numbered_function(src: str, lines: list[int], radius: int = 6) -> str:
    """Source lines around the ground truth / guesses, numbered as in the program file."""
    rows = src.splitlines()
    lo, hi = max(1, min(lines) - radius), min(len(rows), max(lines) + radius)
    return "\n".join(f"{i}: {rows[i - 1]}" for i in range(lo, hi + 1))


def top_constraint(run: Path, p: str) -> str:
    """The highest-scoring constraint of one run: id, anchor line, expression (what SemLoc's evidence pointed at)."""
    f, c = run / "scores" / f"{p}.json", run / "constraints" / f"{p}.json"
    if not f.exists() or not c.exists():
        return ""
    ranked = json.loads(f.read_text()).get("ranked_constraints") or []
    if not ranked:
        return ""
    cid = ranked[0][0]
    for con in json.loads(c.read_text()).get("constraints", []):
        if con.get("id") == cid:
            anchor = (con.get("instrument", {}).get("anchor") or {}).get("line")
            return f"{cid}@{anchor}: {con.get('spec', {}).get('expr', '')}"[:200]
    return cid


def tolerance(gt: dict, test: list[str], runs: list[Path], llmcov: list[dict]) -> None:
    """Sensitivity of Acc@1 to guard/body ambiguity: a top-1 line also counts when it and a ground-truth line are a
    compound-statement header and the statement it guards — strict (first body line only, lower bound) and lenient
    (first body statement up to 3 lines, upper bound). Writes data/failure_tolerance.csv and data/failure_offsets.csv."""
    srcs = {p: (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / f"{p}.py").read_text() for p in test}

    def top1s(method):
        if method == "llm_coverage":
            return [{p: (run.get(p) or [None])[0] for p in test} for run in llmcov]
        out = []
        for r in runs:
            d = {}
            for p in test:
                f = r / "scores" / f"{p}.json"
                sc = json.loads(f.read_text()) if f.exists() else {}
                if method == "llm_guess":
                    d[p] = sc.get("fault_line_pred")
                else:  # SemLoc's own top line (ties broken towards the guess, as its prior does)
                    ls = {int(k): v for k, v in (sc.get("line_scores") or {}).items()}
                    d[p] = max(ls, key=lambda ln: (ls[ln], ln == sc.get("fault_line_pred"))) if ls else None
            out.append(d)
        return out

    rows, offsets = [], []
    for m in ("semloc", "llm_guess", "llm_coverage"):
        reps = top1s(m)
        exact = [sum(isinstance(r[p], int) and r[p] in gt[p] for p in test) / len(test) for r in reps]
        def tol(strict):
            return [sum(isinstance(r[p], int) and any(line_relation(srcs[p], t, r[p], strict) in ("same", "header_body")
                                                      for t in gt[p]) for p in test) / len(test) for r in reps]
        block, tight = tol(False), tol(True)
        rows.append({"method": m, "n": len(test), "repeats": len(reps), "acc1_exact": round(sum(exact) / len(exact), 4),
                     "acc1_guard_strict": round(sum(tight) / len(tight), 4),
                     "acc1_guard_or_body": round(sum(block) / len(block), 4)})
        offs = Counter(min((r[p] - t for t in gt[p]), key=abs) for r in reps for p in test if isinstance(r[p], int))
        offsets += [{"method": m, "offset": d, "count": offs[d]} for d in range(-3, 4)]
        offsets.append({"method": m, "offset": "far", "count": sum(c for d, c in offs.items() if abs(d) > 3)})
    with open(ROOT / "data" / "failure_tolerance.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(ROOT / "data" / "failure_offsets.csv", "w", newline="") as f:  # top-1 line − nearest GT line, all repeats
        w = csv.DictWriter(f, fieldnames=["method", "offset", "count"])
        w.writeheader()
        w.writerows(offsets)
    print(rows)


def main() -> None:
    gt = load_variants()["repaired"]
    test = [p for p in json.loads((ROOT / "data" / "split.json").read_text())["test"] if p in gt]
    runs = fam.usable_runs(ROOT / "runs", "semloc_test_gemini")
    sem = [fam.run_ranks(r, gt, test, "semloc") for r in runs]
    spec = [fam.run_ranks(r, gt, test, "semloc_no_prior") for r in runs]
    guess = [fam.run_ranks(r, gt, test, "llm_guess") for r in runs]
    llmcov = [json.loads(f.read_text()) for f in sorted((ROOT / "data" / "rankings").glob("direct_cov_test_gemini_r*.json"))]
    labels = labels_for({p: gt[p] for p in test}, COV)
    status = {r["program"]: r["status"] for r in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())}
    clusters = {r["program"]: int(r["cluster_t0.8"]) for r in csv.DictReader(open(ROOT / "data" / "semfault_templates.csv"))}
    hit = lambda r, k: r is not None and r <= k
    rows = []
    for p in test:
        ranks = [s.get(p) for s in spec if s.get(p) is not None]
        sig = {"program": p, "label": labels[p], "gt_status": status.get(p, "unverified"), "cluster": clusters.get(p, -1),
               "guess_hit": majority([hit(g.get(p), 1) for g in guess]),
               "semloc_top1": majority([hit(s.get(p), 1) for s in sem]),
               "semloc_top3": majority([hit(s.get(p), 3) for s in sem]),
               "spectrum_rank": float(median(ranks)) if len(ranks) * 2 > len(spec) else None,
               "llmcov_top3": majority([any(ln in gt[p] for ln in run.get(p, [])[:3]) for run in llmcov])}
        sig["category"] = category(sig)
        src = (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / f"{p}.py").read_text()
        gs = [g for g in (json.loads((r / "scores" / f"{p}.json").read_text()).get("fault_line_pred")
                          if (r / "scores" / f"{p}.json").exists() else None for r in runs) if isinstance(g, int)]
        g = Counter(gs).most_common(1)[0][0] if gs else None
        sig["guess_relation"] = (min((line_relation(src, t, g) for t in gt[p]), key=REL_ORDER.index)
                                 if g is not None else "none")
        rows.append(sig)
    with open(ROOT / "data" / "failure_signals.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    picked = select([r for r in rows if r["category"] != "guess_right"], PER_CATEGORY, SEED)
    cases = []
    for r in picked:
        p = r["program"]
        src = (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / f"{p}.py").read_text()
        guesses = [json.loads((run / "scores" / f"{p}.json").read_text()).get("fault_line_pred")
                   if (run / "scores" / f"{p}.json").exists() else None for run in runs]
        top5 = (json.loads((runs[0] / "scores" / f"{p}.json").read_text()).get("ranked_lines") or [])[:5] \
            if (runs[0] / "scores" / f"{p}.json").exists() else []
        cases.append({**r, "gt_lines": gt[p], "guesses": guesses, "semloc_top5_r1": [ln for ln, _ in top5],
                      "llmcov_top5_r1": llmcov[0].get(p, [])[:5] if llmcov else [],
                      "top_constraint_r1": top_constraint(runs[0], p),
                      "code": numbered_function(src, [*gt[p], *[g for g in guesses if isinstance(g, int)]])})
    with open(ROOT / "data" / "failure_cases.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(cases[0]))
        w.writeheader()
        w.writerows(cases)
    tolerance(gt, test, runs, llmcov)
    counts = {c: sum(r["category"] == c for r in rows) for c in CATEGORIES}
    print(f"{len(rows)} programs; categories {counts}; {len(cases)} cases sampled")


if __name__ == "__main__":
    main()

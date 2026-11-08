"""RQ1 audit table: every published configuration scored the authors' way and the fair way,
on all 250 programs and on the 185 whose ground-truth line is executed by a failing test.

    python scripts/rq1_audit.py --out data/rq1_audit.csv

author: the artifact's own numbers (rq1_localization.csv best_rank / print_results rules:
        stable-order ties, DD any-hit = 1, programs that failed to run dropped from n).
fair:   ties = average rank, fixed denominator (missing program = miss), DD = mean rank of the
        unranked minimal set, SemLoc ranks recomputed from scores/<p>.json.
Extra rows: SBFL Ochiai/DStar recomputed from our coverage matrices; SemLoc without the +1.2
LLM fault-line prior; hits on blank / non-executable ground-truth lines.
"""
import argparse
import csv
import json
from pathlib import Path

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.covgate import covgate_scores
from flx.ranking import metrics, rank_of
from flx.sbfl import sbfl_scores
from flx.semloc_results import (best_ranks_from_csv, dd_best_ranks, direct_fl_best_ranks,
                                find_localization_csv, load_ground_truth, sbfl_best_ranks)

ROOT = Path(__file__).resolve().parents[1]
RQ1 = SEMLOC_ROOT / "results" / "RQ1"
GT_PATH = SEMLOC_ROOT / "benchmark" / "ground_truth.json"
COV = ROOT / "data" / "coverage" / "semfault"


def _programs():
    gt = load_ground_truth(GT_PATH)
    labels = {r["program"]: r["category"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv"))}
    allp = sorted(gt)
    return gt, {"all": allp, "executable": [p for p in allp if labels[p] != "not_executed"]}, labels


def _semloc_scores(cfg: str, prog: str):
    f = RQ1 / cfg / "scores" / f"{prog}.json"
    return json.loads(f.read_text()) if f.exists() else None


def _author_ranks(cfg: str, gt) -> dict:
    d = RQ1 / cfg
    if cfg.startswith("sbfl_"):
        return sbfl_best_ranks(d, GT_PATH)
    if cfg == "dd":
        return dd_best_ranks(d, GT_PATH)
    if cfg.startswith("semantic_indexing_disabled"):
        return direct_fl_best_ranks(d)
    csv_path = find_localization_csv(d)
    return best_ranks_from_csv(csv_path) if csv_path else {}


def _fair_ranks(cfg: str, gt) -> dict | None:
    d = RQ1 / cfg
    if cfg == "dd":
        out = {}
        for p in gt:
            f = d / f"{p}.json"
            if f.exists():
                minimal = json.loads(f.read_text()).get("dd", {}).get("minimal_lines", [])
                out[p] = (len(minimal) + 1) / 2 if any(ln in minimal for ln in gt[p]) else None
        return out
    if cfg.startswith("sbfl_"):
        out = {}
        for p in gt:
            f = d / f"{p}.json"
            if f.exists():
                js = json.loads(f.read_text())
                res = js["sbfl"] if isinstance(js.get("sbfl"), dict) else js
                out[p] = rank_of({int(k): v for k, v in res.get("line_scores", {}).items()}, gt[p], "average")
        return out
    if cfg.startswith("semantic_indexing_disabled"):
        return direct_fl_best_ranks(d)  # a ranked list without scores: no ties to resolve
    if (d / "scores").exists():
        out = {}
        for p in gt:
            sem = _semloc_scores(cfg, p)
            if sem is not None:
                out[p] = rank_of({int(k): v for k, v in sem["line_scores"].items()}, gt[p], "average")
        return out
    return None  # configs published without scores (cf_disabled_*): fair scoring not computable


def _row(config, scoring, subset, ranks, progs, author_n=None):
    if ranks is None:
        return {"config": config, "scoring": scoring, "subset": subset, "n": "", "acc1": "", "acc3": "",
                "acc5": "", "median_rank": "", "note": "not computable from published files"}
    if scoring == "author":
        progs = [p for p in progs if p in ranks]  # the artifact drops programs that did not run
    m = metrics(ranks, progs)
    return {"config": config, "scoring": scoring, "subset": subset, "n": m["n"], "acc1": m["acc1"],
            "acc3": m["acc3"], "acc5": m["acc5"], "median_rank": m["median_rank"], "note": ""}


def audit_rows() -> list[dict]:
    gt, subsets, labels = _programs()
    configs = sorted(p.name for p in RQ1.iterdir() if p.is_dir())
    rows = []
    for cfg in configs:
        author, fair = _author_ranks(cfg, gt), _fair_ranks(cfg, gt)
        for sub, progs in subsets.items():
            rows.append(_row(cfg, "author", sub, author or None, progs))
            rows.append(_row(cfg, "fair", sub, fair, progs))
    # our own SBFL from coverage matrices, and SemLoc without the LLM fault-line prior
    for formula in ("ochiai", "dstar"):
        ranks = {p: rank_of(sbfl_scores(load(COV / f"{p}.json"), formula), gt[p], "average") for p in gt}
        for sub, progs in subsets.items():
            rows.append(_row(f"ours_sbfl_{formula}", "fair", sub, ranks, progs))
    for cfg in ("semloc_claude_T0.8", "semloc_gemini_T0.8", "semloc_claude_T0.3", "semloc_gemini_T0.3", "semloc_gemini_T0.0"):
        ranks = {}
        for p in gt:
            sem = _semloc_scores(cfg, p)
            if sem is not None:
                s = covgate_scores(sem, load(COV / f"{p}.json"), gate=False, lam=0.0, no_prior=True)
                ranks[p] = rank_of(s, gt[p], "average")
        for sub, progs in subsets.items():
            rows.append(_row(f"{cfg}_no_prior", "fair", sub, ranks, progs))
    return rows


def blank_gt_hits() -> list[dict]:
    """How often each method ranks a ground-truth line that no failing test executes (top-5)."""
    gt, subsets, labels = _programs()
    ne = [p for p in gt if labels[p] == "not_executed"]
    out = []
    for cfg in ("semloc_claude_T0.8", "semloc_gemini_T0.8", "sbfl_ochiai"):
        ranks = _fair_ranks(cfg, gt)
        m = metrics(ranks, ne)
        out.append({"config": cfg, "n_not_executed": len(ne), "acc1": m["acc1"], "acc5": m["acc5"]})
    return out


def cf_identity_check(cfg: str) -> int:
    """Programs whose artifact best_rank differs from the rank recomputed from scores/ (author ties).
    0 means the counterfactual step never changed the reported ranking."""
    gt, _, _ = _programs()
    author = best_ranks_from_csv(find_localization_csv(RQ1 / cfg))
    diff = 0
    for p, r in author.items():
        sem = _semloc_scores(cfg, p)
        if sem is None:
            continue
        mine = rank_of({int(k): v for k, v in sem["line_scores"].items()}, gt[p], "first")
        diff += (mine if mine is None else int(mine)) != r
    return diff


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq1_audit.csv")
    args = ap.parse_args()
    rows = audit_rows()
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for r in rows)
    blank = blank_gt_hits()
    with open(args.out.with_name("rq1_blank_gt_hits.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(blank[0]))
        w.writeheader()
        w.writerows(blank)
    cf = {cfg: cf_identity_check(cfg) for cfg in ("semloc_claude_T0.3", "semloc_claude_T0.8", "semloc_gemini_T0.0",
                                                   "semloc_gemini_T0.3", "semloc_gemini_T0.8")}
    (args.out.with_name("rq1_cf_identity.json")).write_text(json.dumps(cf, indent=2))
    print(f"wrote {args.out} ({len(rows)} rows); CF changed ranks in: {cf}")


if __name__ == "__main__":
    main()

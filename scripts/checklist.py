"""Evaluation checklist applied to every method → data/checklist_matrix.csv and the generated table in
docs/literature/evaluation-checklist.md (between the GENERATED markers).

    python scripts/checklist.py
Every number is read from data/: rq1_audit.csv (author vs fair scoring, published logs), rq2_ours.csv
(original vs execution-repaired ground truth, our runs), rq_gt_sensitivity.csv and rq2_ours.csv
(hidden fault-line prior), llm_cost.csv (tokens per program).
"""
import csv
import re
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOC = ROOT / "docs" / "literature" / "evaluation-checklist.md"

METHODS = {  # method: (published config in rq1_audit, method in rq2_ours, cost run prefix)
    "SBFL Ochiai": ("sbfl_ochiai", "sbfl_ochiai", None),
    "Delta debugging": ("dd", None, None),
    "LLM direct": ("semantic_indexing_disabled_claude", "llm_direct", "direct_test_gemini_r"),
    "LLM + coverage (ours)": (None, "llm_coverage", "direct_cov_test_gemini_r"),
    "SemLoc": ("semloc_claude_T0.8", "semloc", "semloc_test_gemini_r"),
    "CovGate (ours)": (None, "covgate", "semloc_test_gemini_r"),
}


def _csv(name):
    return list(csv.DictReader(open(DATA / name)))


def rows() -> list[dict]:
    audit = {(r["config"], r["scoring"]): r for r in _csv("rq1_audit.csv") if r["subset"] == "all"}
    ours = {(r["gt"], r["method"]): r for r in _csv("rq2_ours.csv") if r.get("subset", "all") == "all"}
    cost = _csv("llm_cost.csv")
    out = []

    def add(method, check, metric, a, b, source):
        fa, fb = (None if v in (None, "") else float(v) for v in (a, b))
        out.append({"method": method, "check": check, "metric": metric, "a": fa, "b": fb,
                    "delta": None if fa is None or fb is None else round(fb - fa, 4), "source": source})

    for m, (pub, mine, cprefix) in METHODS.items():
        for k in ("acc1", "acc3", "acc5"):
            if pub:
                add(m, "scoring: author → fair", k, audit[(pub, "author")][k], audit[(pub, "fair")][k],
                    f"rq1_audit.csv:{pub}")
        if mine:
            for k in ("acc1", "acc3"):
                add(m, "ground truth: original → repaired", k, ours[("original", mine)][f"{k}_mean"],
                    ours[("repaired", mine)][f"{k}_mean"], f"rq2_ours.csv:{mine}")
            rep = ours[("repaired", mine)]
            add(m, "repeats (ours)", "n", None, rep["repeats"], "rq2_ours.csv")
            if rep.get("p_acc3_max"):
                add(m, "McNemar vs SemLoc (max p over repeats)", "p (Acc@3)", None, rep["p_acc3_max"], "rq2_ours.csv")
        if m == "SemLoc":
            for k in ("acc1", "acc3"):
                add(m, "hidden component: remove fault-line prior", k, audit[("semloc_claude_T0.8", "fair")][k],
                    audit[("semloc_claude_T0.8_no_prior", "fair")][k], "rq1_audit.csv (published Claude T0.8)")
                add(m, "hidden component: remove fault-line prior (ours, repaired)", k,
                    ours[("repaired", "semloc")][f"{k}_mean"], ours[("repaired", "semloc_no_prior")][f"{k}_mean"],
                    "rq2_ours.csv")
        tokens = [float(r["tokens_per_program"]) for r in cost if cprefix and r["run_id"].startswith(cprefix)]
        add(m, "cost", "LLM tokens / program", None, round(mean(tokens)) if tokens else 0, "llm_cost.csv")
    return out


def pct(v):
    return "–" if v is None else f"{100 * v:.1f}"


def markdown(rs: list[dict]) -> str:
    lines = ["| Method | Check | Metric | Before | After | Δ (pp) |", "|---|---|---|---|---|---|"]
    for r in rs:
        if r["metric"].startswith("acc"):
            a, b, d = pct(r["a"]), pct(r["b"]), ("–" if r["delta"] is None else f"{100 * r['delta']:+.1f}")
        else:
            v = r["b"]
            b = "–" if v is None else (f"{v:.3f}" if r["metric"].startswith("p ") else f"{v:,.0f}")
            a, d = "–", "–"
        lines.append(f"| {r['method']} | {r['check']} | {r['metric']} | {a} | {b} | {d} |")
    return "\n".join(lines) + "\n"


def main() -> None:
    rs = rows()
    with open(DATA / "checklist_matrix.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rs[0]))
        w.writeheader()
        w.writerows(rs)
    doc = DOC.read_text()
    table = markdown(rs)
    doc = re.sub(r"(<!-- GENERATED:checklist -->\n).*?(<!-- /GENERATED -->)", lambda m: m.group(1) + table + m.group(2),
                 doc, flags=re.S)
    DOC.write_text(doc)
    print(table)


if __name__ == "__main__":
    main()

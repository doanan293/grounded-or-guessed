"""Generate LaTeX tables (and the cost/accuracy figure) from data/*.csv into docs/report/generated/.

    python scripts/make_tables.py
Each table is a standalone tabular fragment, \\input by both the Vietnamese report and the paper.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "report" / "generated"

NAMES = {
    "semloc_claude_T0.3": "SemLoc, Claude Sonnet 4.6, $T{=}0.3$", "semloc_claude_T0.8": "SemLoc, Claude Sonnet 4.6, $T{=}0.8$",
    "semloc_gemini_T0.0": "SemLoc, Gemini 2.5 Pro, $T{=}0$", "semloc_gemini_T0.3": "SemLoc, Gemini 2.5 Pro, $T{=}0.3$",
    "semloc_gemini_T0.8": "SemLoc, Gemini 2.5 Pro, $T{=}0.8$", "cf_disabled_claude_T0.8": "SemLoc w/o CF (separate run), Claude",
    "cf_disabled_gemini_T0.8": "SemLoc w/o CF (separate run), Gemini", "semantic_indexing_disabled_claude": "LLM direct, Claude",
    "semantic_indexing_disabled_gemini": "LLM direct, Gemini", "sbfl_ochiai": "SBFL Ochiai", "sbfl_tarantula": "SBFL Tarantula",
    "dd": "Delta debugging", "ours_sbfl_dstar": "SBFL DStar (recomputed)",
    "semloc_claude_T0.8_no_prior": "SemLoc Claude $T{=}0.8$ without LLM-guess bonus",
    "semloc_gemini_T0.8_no_prior": "SemLoc Gemini $T{=}0.8$ without LLM-guess bonus",
}


def pct(v) -> str:
    if v in (None, ""):
        return "--"
    return f"{100 * float(v):.1f}"


def tex(s: str) -> str:
    return s.replace("_", r"\_").replace("%", r"\%")


def _rows(name: str) -> list[dict]:
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def rq1_table() -> str:
    rows = _rows("rq1_audit.csv")
    get = {(r["config"], r["scoring"], r["subset"]): r for r in rows}
    order = ["semloc_claude_T0.8", "semloc_gemini_T0.8", "semloc_claude_T0.8_no_prior", "semloc_gemini_T0.8_no_prior",
             "cf_disabled_claude_T0.8", "semantic_indexing_disabled_claude", "sbfl_ochiai", "ours_sbfl_dstar", "dd"]
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r" & \multicolumn{3}{c}{Author scoring} & \multicolumn{3}{c}{Fair scoring} \\",
             r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
             r"Configuration (all 250 programs) & Acc@1 & Acc@3 & Acc@5 & Acc@1 & Acc@3 & Acc@5 \\", r"\midrule"]
    for c in order:
        a, f = get.get((c, "author", "all"), {}), get.get((c, "fair", "all"), {})
        lines.append(f"{NAMES.get(c, tex(c))} & {pct(a.get('acc1'))} & {pct(a.get('acc3'))} & {pct(a.get('acc5'))} & "
                     f"{pct(f.get('acc1'))} & {pct(f.get('acc3'))} & {pct(f.get('acc5'))} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def decomposition_table() -> str:
    """Published logs, game whose total is SemLoc as released (fair ties): LLM guess bonus vs semantic spectrum."""
    rows = [r for r in _rows("rq_decomposition_published.csv")
            if r["source"] in ("semloc_claude_T0.8", "semloc_gemini_T0.8") and r.get("game") == "semloc"
            and r.get("gt") == "original"]
    lines = [r"\begin{tabular}{llrrrr}", r"\toprule",
             r"Configuration & Subset & Metric & SemLoc & LLM guess bonus & Semantic spectrum \\", r"\midrule"]
    for r in rows:
        lines.append(f"{NAMES[r['source']]} & {r['subset']} & {r['metric'].replace('acc', 'Acc@')} & {pct(r['full'])} & "
                     f"{ci(r, 'phi_guess')} & {ci(r, 'phi_spectrum')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def ci(row: dict, k: str) -> str:
    """value with its cluster-bootstrap 95% CI, in percentage points."""
    return (f"{100 * float(row[k]):.1f}{{\\scriptsize\\,[{100 * float(row[k + '_ci_cluster_lo']):.1f}, "
            f"{100 * float(row[k + '_ci_cluster_hi']):.1f}]}}")


def decomposition_ours_table() -> str:
    """Our 3 Gemini runs. Upper block: the SemLoc game (total = SemLoc as released). Lower block: all four signals
    (raw Ochiai and CF re-ranking added), whose total is a different system."""
    rows = [r for r in _rows("rq_decomposition.csv") if r["subset"] == "all"]
    lines = [r"\begin{tabular}{llrrrrr}", r"\toprule",
             r"Ground truth & Metric & Total & LLM guess & Semantic spectrum & Coverage & CF \\"]
    for game, title in (("semloc", "SemLoc as released (guess + spectrum)"),
                        ("all_signals", "All signals (+ raw Ochiai, + CF re-ranking)")):
        lines += [r"\midrule", rf"\multicolumn{{7}}{{l}}{{\emph{{{title}}}}} \\"]
        for r in (r for r in rows if r.get("game") == game):
            extra = (f"{ci(r, 'phi_coverage')} & {ci(r, 'phi_cf')}" if game == "all_signals" else "-- & --")
            lines.append(f"{r['gt'].capitalize()} ($n={r['n']}$) & {r['metric'].replace('acc', 'Acc@')} & {pct(r['full'])} & "
                         f"{ci(r, 'phi_guess')} & {ci(r, 'phi_spectrum')} & {extra} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def dci(row: dict, k: str) -> str:
    """Δ in percentage points with its cluster-bootstrap 95% CI, e.g. +15.4{\\scriptsize\\,[9.8, 21.3]}."""
    if row.get(f"d_{k}") in (None, ""):
        return "--"
    return (f"{100 * float(row[f'd_{k}']):+.1f}{{\\scriptsize\\,[{100 * float(row[f'd_{k}_lo']):.1f}, "
            f"{100 * float(row[f'd_{k}_hi']):.1f}]}}")


def pm(row: dict, k: str) -> str:
    r"""mean ± sd in percent, e.g. 48.9{\scriptsize$\pm$0.7}."""
    m, sd = row.get(f"{k}_mean"), row.get(f"{k}_sd")
    if m in (None, ""):
        return "--"
    multi = int(row.get("repeats") or 1) > 1
    return f"{pct(m)}{{\\scriptsize$\\pm${100 * float(sd):.1f}}}" if multi and sd not in (None, "") else pct(m)


def pval(v) -> str:
    if v in (None, ""):
        return "--"
    v = float(v)
    return "$<$.001" if v < 0.001 else f"{v:.3f}".lstrip("0")


GT_LABEL = {"original": "Original ground truth", "repaired": "Execution-repaired ground truth",
            "reviewed": "Reviewed ground truth"}
RQ2_NAMES = {"gate_only": "\\quad + coverage gate only", "lam_only": "\\quad + $\\lambda$·Ochiai only",
             "grounded_prior_only": "\\quad bonus only when grounded", "semloc": "SemLoc (as released)", "semloc_no_prior": "\\quad w/o LLM-guess bonus",
             "cf_rerank": "\\quad + CF re-ranking", "covgate": "CovGate (ours)", "covgate_cf": "CovGate + CF re-ranking",
             "llm_direct": "LLM direct (1 prompt)", "llm_tests": "\\quad + failing tests, no coverage (ablation)",
             "llm_coverage": "LLM + coverage (1 prompt, ours)", "sbfl_ochiai": "SBFL Ochiai"}


def rq2_table() -> str:
    rows = [r for r in _rows("rq2_ours.csv") if r.get("subset", "all") == "all"]
    order = ["semloc", "semloc_no_prior", "grounded_prior_only", "gate_only", "lam_only", "cf_rerank", "covgate", "covgate_cf",
             "llm_direct", "llm_tests", "llm_coverage", "sbfl_ochiai"]
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r"Method & Acc@1 & Acc@3 & Acc@5 & $\Delta$Acc@1 [95\% CI] & $\Delta$Acc@3 [95\% CI] & $r_{\text{rb}}$ \\"]
    for g in ("original", "repaired", "reviewed"):
        rs = {r["method"]: r for r in rows if r["gt"] == g}
        any_r = next(iter(rs.values()))
        lines += [r"\midrule", rf"\multicolumn{{7}}{{l}}{{\emph{{{GT_LABEL[g]}, $n={any_r['n']}$, {any_r['repeats']} repeats}}}} \\"]
        for m in order:
            r = rs.get(m)
            if not r:
                continue
            d = r.get("rank_biserial_rr")
            lines.append(f"{RQ2_NAMES[m]} & {pm(r, 'acc1')} & {pm(r, 'acc3')} & {pm(r, 'acc5')} & {dci(r, 'acc1')} & "
                         f"{dci(r, 'acc3')} & {'--' if d in (None, '') else f'{float(d):+.2f}'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def main_results_table(sets: tuple = ("original", "repaired", "reviewed"), with_coverage: bool = True) -> str:
    """Table II: the headline comparison on the three ground truths (Acc@1 / Acc@3, mean of 3 repeats) and cost."""
    rows = {(r["gt"], r["method"]): r for r in _rows("rq2_ours.csv") if r.get("subset", "all") == "all"}
    cost = _rows("llm_cost.csv")
    tok = lambda prefix: (f"{sum(float(r['tokens_per_program']) for r in cost if r['run_id'].startswith(prefix)) / 1000 / max(1, sum(1 for r in cost if r['run_id'].startswith(prefix))):.1f}"
                          if any(r["run_id"].startswith(prefix) for r in cost) else "0")
    methods = [("sbfl_ochiai", "SBFL Ochiai", None), ("llm_direct", "LLM direct (source only)", "direct_test_gemini_r"),
               ("semloc", "SemLoc (multi-stage)", "semloc_test_gemini_r"),
               ("llm_tests", "LLM + failing tests (ours)", "direct_tests_test_gemini_r"),
               ("llm_coverage", "\\quad + per-line coverage", "direct_cov_test_gemini_r")]
    n = {g: rows[(g, "semloc")]["n"] for g in sets}
    title = {"original": "Original", "repaired": "Repaired", "reviewed": "Reviewed"}
    k = len(sets)
    lines = [r"\begin{tabular}{l" + "rr" * k + "r}", r"\toprule",
             " & " + " & ".join(rf"\multicolumn{{2}}{{c}}{{{title[g]} ($n={n[g]}$)}}" for g in sets) + r" & \\",
             "".join(rf"\cmidrule(lr){{{2 + 2 * i}-{3 + 2 * i}}}" for i in range(k)),
             "Method & " + " & ".join(["Acc@1 & Acc@3"] * k) + r" & k tokens \\", r"\midrule"]
    for m, name, prefix in methods:
        if m == "llm_coverage" and not with_coverage:
            continue
        cells = [f"{pct(rows[(g, m)]['acc1_mean'])} & {pct(rows[(g, m)]['acc3_mean'])}" for g in sets]
        lines.append(f"{name} & {' & '.join(cells)} & {tok(prefix) if prefix else '0'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def addons_table(include_pav: bool = True) -> str:
    """Table III: additions that do not help — Δ against the method they extend, with 95% CIs where repeated."""
    abl = {(r["gt"], r["subset"], r["contrast"]): r for r in _rows("ablation_coverage.csv")}
    rq2 = {(r["gt"], r["method"]): r for r in _rows("rq2_ours.csv") if r.get("subset", "all") == "all"}
    grid = _rows("pav_dev_grid.csv")
    vote = {r["gt"]: r for r in _rows("vote_dev.csv")}
    params = json.loads((DATA / "pav_params.json").read_text())
    chosen = next(r for r in grid if r["order"] == params["order"] and int(r["k"]) == params["k"]
                  and int(r["attempts"]) == params["attempts"]
                  and r["max_size"] == ("" if params["max_size"] is None else str(params["max_size"])))
    worst = min((r for r in grid if r["order"] != "stage1"), key=lambda r: float(r["select_acc1"]))
    base = grid[0]
    pp = lambda a, b: f"{100 * (float(a) - float(b)):+.1f}"
    lines = [r"\begin{tabular}{llrrrr}", r"\toprule",
             r" & & \multicolumn{2}{c}{Repaired} & \multicolumn{2}{c}{Reviewed} \\", r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}",
             r"Addition (compared with) & Split & $\Delta$Acc@1 & $\Delta$Acc@3 & $\Delta$Acc@1 & $\Delta$Acc@3 \\", r"\midrule"]
    a = lambda g: abl[(g, "all", "coverage_effect")]
    lines.append(f"Per-line coverage (LLM + failing tests) & test & {dci(a('repaired'), 'acc1')} & {dci(a('repaired'), 'acc3')} & "
                 f"{dci(a('reviewed'), 'acc1')} & {dci(a('reviewed'), 'acc3')} \\\\")
    c = lambda g: rq2[(g, "covgate")]
    lines.append(f"CovGate (SemLoc) & test & {dci(c('repaired'), 'acc1')} & {dci(c('repaired'), 'acc3')} & "
                 f"{dci(c('reviewed'), 'acc1')} & {dci(c('reviewed'), 'acc3')} \\\\")
    for name, r in ((("Propose-and-verify, selected", chosen), ("Propose-and-verify, most aggressive", worst)) if include_pav else ()):
        lines.append(f"{name} (LLM + failing tests) & dev & {pp(r['repaired_acc1'], base['repaired_acc1'])} & "
                     f"{pp(r['repaired_acc3'], base['repaired_acc3'])} & {pp(r['reviewed_acc1'], base['reviewed_acc1'])} & "
                     f"{pp(r['reviewed_acc3'], base['reviewed_acc3'])} \\\\")
    v = lambda g, k: pp(vote[g][f"vote_{k}"], vote[g][f"single_{k}"])
    lines.append(f"Vote over 3 answers (LLM + failing tests) & dev & {v('repaired', 'acc1')} & {v('repaired', 'acc3')} & "
                 f"{v('reviewed', 'acc1')} & {v('reviewed', 'acc3')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def static_table() -> str:
    rows = {r["tool"]: r for r in _rows("static_tools.csv") if r["gt"] == "reviewed"}
    names = {"ruff_default": "ruff (default rules)", "ruff_all": "ruff (all rules)", "pyrefly": "pyrefly (type check)"}
    lines = [r"\begin{tabular}{lrrrr}", r"\toprule",
             r"Tool & Diagnostics & Programs flagged & On a fault line & Expected by chance \\", r"\midrule"]
    for t, name in names.items():
        r = rows[t]
        lines.append(f"{name} & {r['diagnostics']} & {r['flagged']} & {r['on_fault_line']} & {float(r['on_fault_line_by_chance']):.1f} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def label_audit_table() -> str:
    r = next(x for x in _rows("label_audit.csv") if x["subset"] == "all")
    items = [("same", "Same line"), ("extended", "Kept, second line added (two-line fault)"), ("blank", "Blank line"),
             ("non_code", "Log call, \\texttt{def} header or comment"), ("off_by_one", "One line away"),
             ("farther", "Two or more lines away")]
    lines = [r"\begin{tabular}{lr}", r"\toprule", rf"Original label vs.\ reviewed label ($n={r['n']}$) & Programs \\", r"\midrule"]
    lines += [f"{name} & {r[k]} \\\\" for k, name in items]
    lines += [r"\midrule", f"Moved (blank, non-code, one or more lines away) & {r['moved']} \\\\", r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def rq2_by_label_table() -> str:
    """Repaired ground truth: Acc@1 / Acc@3 per fault label (labels of the repaired GT)."""
    rows = {(r["subset"], r["method"]): r for r in _rows("rq2_ours.csv") if r["gt"] == "repaired"}
    subs = [("semantic", "Semantic"), ("coverage_revealed", "Coverage-revealed"), ("not_executed", "Not executed"),
            ("executable", "Executable (all but not executed)")]
    meths = [("sbfl_ochiai", "SBFL"), ("semloc", "SemLoc"), ("covgate", "CovGate"), ("llm_coverage", "LLM + cov.")]
    lines = [r"\begin{tabular}{lr" + "rr" * len(meths) + "}", r"\toprule",
             " & & " + " & ".join(rf"\multicolumn{{2}}{{c}}{{{n}}}" for _, n in meths) + r" \\",
             "".join(rf"\cmidrule(lr){{{3 + 2 * i}-{4 + 2 * i}}}" for i in range(len(meths))),
             "Fault label & $n$ & " + " & ".join("Acc@1 & Acc@3" for _ in meths) + r" \\", r"\midrule"]
    for sub, name in subs:
        if (sub, "semloc") not in rows:
            continue
        cells = " & ".join(f"{pct(rows[(sub, m)]['acc1_mean'])} & {pct(rows[(sub, m)]['acc3_mean'])}" for m, _ in meths)
        lines.append(f"{name} & {rows[(sub, 'semloc')]['n']} & {cells} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def rq3_families_table() -> str:
    rows = [r for r in _rows("rq3_families.csv") if r["gt"] == "repaired"]
    fams = list(dict.fromkeys(r["family"] for r in rows))
    get = {(r["family"], r["method"]): r for r in rows}
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r" & & \multicolumn{2}{c}{SemLoc} & \multicolumn{2}{c}{w/o LLM-guess bonus} & CovGate \\",
             r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(lr){7-7}",
             r"Model & Repeats & Acc@1 & Acc@3 & Acc@1 & Acc@3 & Acc@3 \\", r"\midrule"]
    for f in fams:
        s, n, c = get.get((f, "semloc"), {}), get.get((f, "semloc_no_prior"), {}), get.get((f, "covgate"), {})
        lines.append(f"{f} & {s.get('repeats', '--')} & {pm(s, 'acc1')} & {pm(s, 'acc3')} & {pm(n, 'acc1')} & {pm(n, 'acc3')} & "
                     f"{pm(c, 'acc3')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


BIP_NAMES = {"semloc_spectrum": "SemLoc semantic spectrum only", "semloc_prior": "SemLoc (spectrum + LLM-guess bonus)",
             "llm_guess": "LLM guess alone", "covgate": "CovGate (ours)", "llm_tests": "LLM + failing tests (1 prompt)",
             "llm_coverage": "LLM + coverage (1 prompt, ours)", "sbfl_ochiai": "SBFL Ochiai",
             "sbfl_dstar": "SBFL DStar", "artifact_metric": "Artifact's own metric (rank of the LLM guess)"}


def rq3_bugsinpy_table() -> str:
    rows = _rows("rq3_bugsinpy.csv")
    get = {(r["subset"], r["method"]): r for r in rows}
    n = {s: next(r["n"] for r in rows if r["subset"] == s) for s in ("all", "reached")}
    lines = [r"\begin{tabular}{lrrrrr}", r"\toprule",
             rf" & \multicolumn{{3}}{{c}}{{All bugs ($n={n['all']}$)}} & \multicolumn{{2}}{{c}}{{Fault reached ($n={n['reached']}$)}} \\",
             r"\cmidrule(lr){2-4}\cmidrule(lr){5-6}", r"Method & Acc@1 & Acc@3 & Acc@5 & Acc@1 & Acc@3 \\", r"\midrule"]
    for m, name in BIP_NAMES.items():
        a, b = get.get(("all", m), {}), get.get(("reached", m), {})
        if m == "artifact_metric":
            lines.append(r"\midrule")
        lines.append(f"{name} & {pm(a, 'acc1')} & {pm(a, 'acc3')} & {pm(a, 'acc5')} & {pm(b, 'acc1')} & {pm(b, 'acc3')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def rq3_renamed_table() -> str:
    rows = [r for r in _rows("rq3_renamed.csv") if r["gt"] == "repaired"]
    names = {"semloc": "SemLoc", "semloc_no_prior": "\\quad w/o LLM-guess bonus", "llm_guess": "LLM guess alone",
             "llm_coverage": "LLM + coverage (1 prompt)"}
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r" & \multicolumn{3}{c}{Acc@1} & \multicolumn{3}{c}{Acc@3} \\", r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
             r"Method & Original & Renamed & $\Delta$ [95\% CI] & Original & Renamed & $\Delta$ [95\% CI] \\", r"\midrule"]
    for r in rows:
        lines.append(f"{names[r['method']]} & {pm(r, 'orig_acc1')} & {pm(r, 'renamed_acc1')} & {dci(r, 'acc1')} & "
                     f"{pm(r, 'orig_acc3')} & {pm(r, 'renamed_acc3')} & {dci(r, 'acc3')} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def pareto_figure(path: Path, lang: str = "en") -> None:
    """Acc@3 vs LLM tokens per program (log x), one point per method × model; SBFL as a zero-cost reference line.
    Colour = method (validated categorical slots 1–3), shape = secondary encoding, every point direct-labelled."""
    import math

    import matplotlib
    import matplotlib.ticker
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = _rows("pareto.csv")
    T = ({"direct": " (hỏi thẳng)", "sbfl": "SBFL Ochiai (không dùng LLM)", "x": "Số token LLM mỗi chương trình (thang log)",
          "same": "cùng mô hình", "LLM + coverage": "LLM + độ phủ", "LLM direct": "LLM hỏi thẳng (Gemini 3.8)", "SemLoc": "SemLoc"}
         if lang == "vi" else
         {"direct": " (direct)", "sbfl": "SBFL Ochiai (no LLM)", "x": "LLM tokens per program (log scale)",
          "same": "same model", "LLM + coverage": "LLM + coverage", "LLM direct": "LLM direct (Gemini 3.8)", "SemLoc": "SemLoc"})
    style = {"SemLoc": ("#2a78d6", "o"), "CovGate": ("#2a78d6", "o"), "LLM + coverage": ("#1baf7a", "s"),
             "LLM direct": ("#eb6834", "^")}
    short = {"Gemini 3.8 Flash": "Gemini 3.8", "GPT-6 luna": "luna", "Claude Sonnet 5.5": "Sonnet 5.5",
             "gpt-oss-120b": "gpt-oss", "Gemini 3.5 Flash-Lite": "Flash-Lite"}
    plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    pts = {(r["method"], r["model"]): (float(r["tokens_per_program"]), 100 * float(r["acc3"]))
           for r in rows if r["method"] in style and r["method"] != "CovGate"}
    for (m, model), (x, y) in pts.items():  # same model: SemLoc ↔ LLM + coverage
        if m == "SemLoc" and ("LLM + coverage", model) in pts:
            x2, y2 = pts[("LLM + coverage", model)]
            ax.plot([x, x2], [y, y2], color="#c3c2b7", lw=0.8, zorder=2)
    for (m, model), (x, y) in pts.items():
        c, mk = style[m]
        ax.scatter([x], [y], s=28, c=c, marker=mk, edgecolors="white", linewidths=1.0, zorder=3)
    placed = []  # labels on SemLoc points (and the lone LLM-direct point), nudged away from earlier labels
    for (m, model), (x, y) in sorted(pts.items(), key=lambda kv: -kv[1][1]):
        if m in ("LLM + coverage", "LLM direct"):  # the single direct point is named in the legend instead
            continue
        lab = short.get(model, model) + (T["direct"] if m == "LLM direct" else "")
        free = lambda d: not any(abs(math.log10(x) - math.log10(px)) < 0.2 and abs(y + d / 3 - py) < 3.2
                                 for px, py in placed)
        dy = next(d for d in (2, -7, 9, -14, 16, -21) if free(d) or d == -21)
        placed.append((x, y + dy / 3))
        below = m == "LLM direct"  # its label goes above the point: the right side is crowded with SemLoc points
        ax.annotate(lab, (x, y), xytext=(0, 8) if below else (4, dy), textcoords="offset points", fontsize=6.5,
                    color="#3b3b38", ha="center" if below else "left", va="center")
    xs = [x for x, _ in pts.values()]
    sb = next((r for r in rows if r["method"] == "SBFL Ochiai"), None)
    if sb:
        ax.axhline(100 * float(sb["acc3"]), color="#8a8984", lw=1, ls="--", zorder=1)
        ax.text(min(xs) / 1.25, 100 * float(sb["acc3"]) + 1.5, T["sbfl"], fontsize=6.5, color="#5e5d58")
    ax.set_xscale("log")
    ax.set_xlim(min(min(xs) / 1.35, 950), max(xs) * 2.2)
    ax.set_ylim(10, 100)
    ticks = [t for t in (1000, 2000, 4000, 8000, 16000, 32000) if min(min(xs) / 1.35, 950) <= t <= max(xs) * 2.2]
    ax.set_xticks(ticks, [f"{t // 1000}k" for t in ticks])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlabel(T["x"])
    ax.set_ylabel("Acc@3 (%)")
    ax.grid(True, which="major", color="#e4e3df", lw=0.6, zorder=0)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker=style[k][1], color=style[k][0], ls="", markersize=5, label=T[k])
               for k in ("SemLoc", "LLM + coverage", "LLM direct")]
    handles.append(Line2D([], [], color="#c3c2b7", lw=0.8, label=T["same"]))
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 0.16), fontsize=6.5, frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


# Vietnamese report: same tables, labels translated (guide: Việt hóa thuật ngữ) and decimal commas.
VI = [
    ("Per-line coverage (LLM + failing tests)", "Độ phủ từng dòng (so với LLM + kiểm thử thất bại)"),
    ("Propose-and-verify, most aggressive (LLM + failing tests)", "Đề xuất rồi kiểm chứng, cấu hình mạnh tay nhất (so với LLM + kiểm thử thất bại)"),
    ("Propose-and-verify, selected (LLM + failing tests)", "Đề xuất rồi kiểm chứng, cấu hình được chọn (so với LLM + kiểm thử thất bại)"),
    ("Vote over 3 answers (LLM + failing tests)", "Biểu quyết 3 câu trả lời (so với LLM + kiểm thử thất bại)"),
    ("Addition (compared with)", "Phần bổ sung (so với)"),
    ("CovGate (SemLoc)", "CovGate (so với SemLoc)"),
    ("LLM + failing tests (ours)", "LLM + kiểm thử thất bại (nhóm đề xuất)"),
    ("LLM + failing tests (1 prompt)", "LLM + kiểm thử thất bại (1 prompt)"),
    ("+ per-line coverage", "+ độ phủ từng dòng"),
    ("LLM direct (source only)", "LLM hỏi thẳng (chỉ có mã)"),
    ("SemLoc (multi-stage)", "SemLoc (nhiều bước)"),
    ("k tokens", "nghìn token"),
    ("Original vs.\\ reviewed label", "Nhãn gốc so với nhãn rà soát"),
    ("Kept, second line added (two-line fault)", "Giữ nguyên, thêm một dòng (lỗi trải hai dòng)"),
    ("Log call, \\texttt{def} header or comment", "Lệnh log, dòng \\texttt{def} hoặc chú thích"),
    ("Moved (blank, non-code, one or more lines away)", "Bị dời (dòng trống, không phải mã, lệch một dòng trở lên)"),
    ("Two or more lines away", "Lệch từ hai dòng trở lên"),
    ("One line away", "Lệch một dòng"),
    ("Same line", "Cùng dòng"),
    ("Blank line", "Dòng trống"),
    ("Programs flagged", "Số chương trình bị cảnh báo"),
    ("On a fault line", "Trúng dòng lỗi"),
    ("Expected by chance", "Trúng do ngẫu nhiên (kỳ vọng)"),
    ("Diagnostics", "Số cảnh báo"),
    ("ruff (default rules)", "ruff (luật mặc định)"),
    ("ruff (all rules)", "ruff (mọi luật)"),
    ("pyrefly (type check)", "pyrefly (kiểm tra kiểu)"),
    ("Reviewed ground truth", "Dòng lỗi chuẩn đã rà soát"),
    ("Reviewed (", "Đã rà soát ("),
    ("Repaired (", "Đã sửa ("),
    ("Programs", "Số chương trình"),
    ("Split", "Tập"),
    ("Tool", "Công cụ"),
    (" & test & ", " & test & "),
    (" & dev & ", " & dev & "),
    ("All signals (+ raw Ochiai, + CF re-ranking)", "Mọi tín hiệu (+ Ochiai thô, + xếp lại bằng CF)"),
    ("Artifact's own metric (rank of the LLM guess)", "Chỉ số của gói mã công bố (hạng của dòng LLM đoán)"),
    ("SemLoc w/o CF (separate run), Claude", "SemLoc không CF (lượt chạy riêng), Claude"),
    ("SemLoc w/o CF (separate run), Gemini", "SemLoc không CF (lượt chạy riêng), Gemini"),
    ("SemLoc as released (guess + spectrum)", "SemLoc như phát hành (dòng đoán + phổ)"),
    ("SemLoc (spectrum + LLM-guess bonus)", "SemLoc (phổ + điểm thưởng dòng đoán)"),
    ("Executable (all but not executed)", "Thực thi được (trừ nhóm không thực thi)"),
    ("Execution-repaired ground truth", "Dòng lỗi chuẩn đã sửa bằng thực thi"),
    ("LLM + coverage (1 prompt, ours)", "LLM + độ phủ (1 prompt, nhóm đề xuất)"),
    ("LLM + coverage (1 prompt)", "LLM + độ phủ (1 prompt)"),
    ("SemLoc semantic spectrum only", "Chỉ phổ ngữ nghĩa của SemLoc"),
    ("bonus only when grounded", "chỉ thưởng khi có căn cứ"),
    ("without LLM-guess bonus", "không có điểm thưởng dòng đoán"),
    ("w/o LLM-guess bonus", "bỏ điểm thưởng dòng đoán"),
    ("SBFL DStar (recomputed)", "SBFL DStar (tính lại)"),
    ("CovGate + CF re-ranking", "CovGate + xếp lại bằng CF"),
    ("+ coverage gate only", "+ chỉ cổng độ phủ"),
    ("+ CF re-ranking", "+ xếp lại bằng CF"),
    ("LLM direct (1 prompt)", "LLM hỏi thẳng (1 prompt)"),
    ("+ failing tests, no coverage (ablation)", "+ kiểm thử thất bại, không độ phủ (loại bỏ)"),
    ("Original ground truth", "Dòng lỗi chuẩn gốc"),
    ("SemLoc (as released)", "SemLoc (bản phát hành)"),
    ("Configuration (all 250 programs)", "Cấu hình (cả 250 chương trình)"),
    ("LLM guess alone", "Chỉ dòng LLM đoán"),
    ("LLM guess bonus", "Điểm thưởng dòng đoán"),
    ("Coverage-revealed", "Lộ qua độ phủ"),
    ("Semantic spectrum", "Phổ ngữ nghĩa"),
    ("Delta debugging", "Gỡ lỗi chia đôi (DD)"),
    ("LLM direct", "LLM hỏi thẳng"),
    ("LLM + coverage", "LLM + độ phủ"),
    ("LLM + cov.", "LLM + độ phủ"),
    ("CovGate (ours)", "CovGate (nhóm đề xuất)"),
    ("Author scoring", "Cách chấm của tác giả"),
    ("Fair scoring", "Cách chấm công bằng"),
    ("Fault reached", "Lỗi được chạy tới"),
    ("Fault label", "Nhãn lỗi"),
    ("All bugs", "Mọi lỗi"),
    ("Not executed", "Không thực thi"),
    ("Configuration", "Cấu hình"),
    ("All signals", "Mọi tín hiệu"),
    ("Ground truth", "Dòng lỗi chuẩn"),
    ("$\\lambda$·Ochiai only", "chỉ $\\lambda$·Ochiai"),
    ("Semantic", "Ngữ nghĩa"),
    ("Original", "Bản gốc"),
    ("Renamed", "Đổi tên"),
    ("Reviewed", "Đã rà soát"),
    ("Repaired", "Đã sửa"),
    ("Original (", "Gốc ("),
    ("Repeats", "Số lần lặp"),
    ("repeats", "lần lặp"),
    ("Method", "Phương pháp"),
    ("Metric", "Chỉ số"),
    ("Subset", "Tập con"),
    ("Model", "Mô hình"),
    ("Total", "Tổng"),
    ("Coverage", "Độ phủ"),
    ("LLM guess", "Dòng LLM đoán"),
    ("[95\\% CI]", "[CI 95\\%]"),
    (" & all & ", " & tất cả & "),
    (" & executable & ", " & thực thi được & "),
]


def to_vi(tex: str) -> str:
    for en, vi in VI:
        tex = tex.replace(en, vi)
    tex = re.sub(r"(\d)\.(\d)", r"\1,\2", tex)                 # decimal comma
    tex = re.sub(r"\[([+-]?\d+,\d), ([+-]?\d+,\d)\]", r"[\1; \2]", tex)  # CI separator after decimal commas
    return tex


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rq1_audit.tex").write_text(rq1_table())
    (OUT / "rq_decomposition_published.tex").write_text(decomposition_table())
    (OUT / "rq2_ours.tex").write_text(rq2_table())
    (OUT / "rq2_by_label.tex").write_text(rq2_by_label_table())
    (OUT / "rq_decomposition_ours.tex").write_text(decomposition_ours_table())
    (OUT / "rq3_families.tex").write_text(rq3_families_table())
    (OUT / "rq3_bugsinpy.tex").write_text(rq3_bugsinpy_table())
    (OUT / "rq3_renamed.tex").write_text(rq3_renamed_table())
    (OUT / "rq_main_results.tex").write_text(main_results_table())
    (OUT / "rq_main_results_two.tex").write_text(main_results_table(("original", "repaired"), with_coverage=False))
    (OUT / "rq_addons.tex").write_text(addons_table())
    (OUT / "rq_addons_nopav.tex").write_text(addons_table(include_pav=False))
    (OUT / "rq_static.tex").write_text(static_table())
    (OUT / "rq_label_audit.tex").write_text(label_audit_table())
    pareto_figure(OUT / "pareto.pdf")
    (OUT / "vi").mkdir(exist_ok=True)
    for f in sorted(OUT.glob("*.tex")):
        if f.name.startswith(("rq", )):
            (OUT / "vi" / f.name).write_text(to_vi(f.read_text()))
    pareto_figure(OUT / "vi" / "pareto.pdf", lang="vi")
    print("wrote", sorted(p.name for p in OUT.glob("*.tex")))


if __name__ == "__main__":
    main()

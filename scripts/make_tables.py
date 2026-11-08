"""Generate LaTeX tables (and the cost/accuracy figure) from data/*.csv into docs/report/generated/.

    python scripts/make_tables.py
Each table is a standalone tabular fragment, \\input by both the Vietnamese report and the paper.
"""
import csv
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
    rows = [r for r in _rows("rq_decomposition_published.csv") if r["source"] in ("semloc_claude_T0.8", "semloc_gemini_T0.8")]
    lines = [r"\begin{tabular}{llrrrrr}", r"\toprule",
             r"Configuration & Subset & Metric & Full & LLM guess & Semantic spectrum & Coverage \\", r"\midrule"]
    for r in rows:
        lines.append(f"{NAMES[r['source']]} & {r['subset']} & {r['metric'].replace('acc', 'Acc@')} & {pct(r['full'])} & "
                     f"{pct(r['phi_guess'])} & {pct(r['phi_spectrum'])} & {pct(r['phi_coverage'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


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


GT_LABEL = {"original": "Original ground truth", "repaired": "Execution-repaired ground truth"}
RQ2_NAMES = {"semloc": "SemLoc (as released)", "semloc_no_prior": "\\quad w/o LLM-guess bonus",
             "cf_rerank": "\\quad + CF re-ranking", "covgate": "CovGate (ours)", "covgate_cf": "CovGate + CF re-ranking",
             "llm_direct": "LLM direct (1 prompt)", "llm_coverage": "LLM + coverage (1 prompt, ours)",
             "sbfl_ochiai": "SBFL Ochiai"}


def rq2_table() -> str:
    rows = _rows("rq2_ours.csv")
    order = ["semloc", "semloc_no_prior", "cf_rerank", "covgate", "covgate_cf", "llm_direct", "llm_coverage", "sbfl_ochiai"]
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r"Method & Acc@1 & Acc@3 & Acc@5 & $p_{\text{Acc@1}}$ & $p_{\text{Acc@3}}$ & $\delta_{\text{RR}}$ \\"]
    for g in ("original", "repaired"):
        rs = {r["method"]: r for r in rows if r["gt"] == g}
        any_r = next(iter(rs.values()))
        lines += [r"\midrule", rf"\multicolumn{{7}}{{l}}{{\emph{{{GT_LABEL[g]}, $n={any_r['n']}$, {any_r['repeats']} repeats}}}} \\"]
        for m in order:
            r = rs.get(m)
            if not r:
                continue
            d = r.get("cliffs_delta_rr")
            lines.append(f"{RQ2_NAMES[m]} & {pm(r, 'acc1')} & {pm(r, 'acc3')} & {pm(r, 'acc5')} & {pval(r.get('p_acc1_max'))} & "
                         f"{pval(r.get('p_acc3_max'))} & {'--' if d in (None, '') else f'{float(d):+.2f}'} \\\\")
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
             "llm_guess": "LLM guess alone", "covgate": "CovGate (ours)", "sbfl_ochiai": "SBFL Ochiai",
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
    names = {"semloc": "SemLoc", "semloc_no_prior": "\\quad w/o LLM-guess bonus", "llm_guess": "LLM guess alone"}
    lines = [r"\begin{tabular}{lrrrrrr}", r"\toprule",
             r" & \multicolumn{3}{c}{Acc@1} & \multicolumn{3}{c}{Acc@3} \\", r"\cmidrule(lr){2-4}\cmidrule(lr){5-7}",
             r"Method & Original & Renamed & $p$ & Original & Renamed & $p$ \\", r"\midrule"]
    for r in rows:
        lines.append(f"{names[r['method']]} & {pm(r, 'orig_acc1')} & {pm(r, 'renamed_acc1')} & {pval(r['p_acc1_max'])} & "
                     f"{pm(r, 'orig_acc3')} & {pm(r, 'renamed_acc3')} & {pval(r['p_acc3_max'])} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines) + "\n"


def pareto_figure(path: Path) -> None:
    """Acc@3 vs LLM tokens per program (log x), one point per method × model; SBFL as a zero-cost reference line.
    Colour = method (validated categorical slots 1–3), shape = secondary encoding, every point direct-labelled."""
    import math

    import matplotlib
    import matplotlib.ticker
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    rows = _rows("pareto.csv")
    style = {"SemLoc": ("#2a78d6", "o"), "CovGate": ("#2a78d6", "o"), "LLM + coverage": ("#1baf7a", "s"),
             "LLM direct": ("#eb6834", "^")}
    short = {"Gemini 3.8 Flash": "Gemini 3.8", "GPT-6 luna": "luna", "Claude Sonnet 5.5": "Sonnet 5.5",
             "gpt-oss-120b": "gpt-oss", "Gemini 3.5 Flash-Lite": "Flash-Lite"}
    plt.rcParams.update({"font.size": 8, "font.family": "serif", "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    pts = []
    for r in rows:
        if r["method"] not in style or r["method"] == "CovGate":
            continue
        c, mk = style[r["method"]]
        x, y = float(r["tokens_per_program"]), 100 * float(r["acc3"])
        ax.scatter([x], [y], s=28, c=c, marker=mk, edgecolors="white", linewidths=1.0, zorder=3)
        pts.append((x, y, short.get(r["model"], r["model"])))
    placed = []  # greedy label placement: right of the point, nudged vertically away from labels already placed
    for x, y, lab in sorted(pts, key=lambda p: -p[1]):
        dy = 2
        while any(abs(math.log10(x) - math.log10(px)) < 0.17 and abs(y + dy / 3 - py) < 3.2 for px, py in placed):
            dy -= 7
        placed.append((x, y + dy / 3))
        ax.annotate(lab, (x, y), xytext=(4, dy), textcoords="offset points", fontsize=6.5, color="#3b3b38",
                    ha="left", va="center")
    sb = next((r for r in rows if r["method"] == "SBFL Ochiai"), None)
    if sb:
        ax.axhline(100 * float(sb["acc3"]), color="#8a8984", lw=1, ls="--", zorder=1)
        ax.text(2000, 100 * float(sb["acc3"]) + 1.5, "SBFL Ochiai (no LLM)", fontsize=6.5, color="#5e5d58")
    ax.set_xscale("log")
    ax.set_xlim(1800, 30000)
    ax.set_ylim(10, 95)
    ticks = [2000, 4000, 8000, 16000]
    ax.set_xticks(ticks, [f"{t // 1000}k" for t in ticks])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_xlabel("LLM tokens per program (log scale)")
    ax.set_ylabel("Acc@3 (%)")
    ax.grid(True, which="major", color="#e4e3df", lw=0.6, zorder=0)
    from matplotlib.lines import Line2D
    handles = [Line2D([], [], marker=style[k][1], color=style[k][0], ls="", markersize=5, label=k)
               for k in ("SemLoc", "LLM + coverage", "LLM direct")]
    ax.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 0.18), fontsize=6.5, frameon=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rq1_audit.tex").write_text(rq1_table())
    (OUT / "rq_decomposition_published.tex").write_text(decomposition_table())
    (OUT / "rq2_ours.tex").write_text(rq2_table())
    (OUT / "rq3_families.tex").write_text(rq3_families_table())
    (OUT / "rq3_bugsinpy.tex").write_text(rq3_bugsinpy_table())
    (OUT / "rq3_renamed.tex").write_text(rq3_renamed_table())
    pareto_figure(OUT / "pareto.pdf")
    print("wrote", sorted(p.name for p in OUT.glob("*.tex")))


if __name__ == "__main__":
    main()

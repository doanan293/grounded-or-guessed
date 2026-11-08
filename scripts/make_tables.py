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
    return list(csv.DictReader(open(DATA / name)))


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


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "rq1_audit.tex").write_text(rq1_table())
    (OUT / "rq_decomposition_published.tex").write_text(decomposition_table())
    print("wrote", sorted(p.name for p in OUT.glob("*.tex")))


if __name__ == "__main__":
    main()

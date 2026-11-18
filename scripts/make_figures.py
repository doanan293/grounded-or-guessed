"""Report figures from data/ (matplotlib): docs/report/generated/vi/fig_*.pdf, each exactly \\linewidth wide so the
13 pt text in the figure prints at the size of the body text.
    .venv/bin/python scripts/make_figures.py
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import fig_style as st  # noqa: E402
from method_names import name  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "report" / "generated" / "vi"
MAIN = ["sbfl_ochiai", "llm_direct", "semloc", "semloc_no_prior", "llm_tests"]
COST_PREFIX = {"llm_direct": "direct_test_gemini_r", "semloc": "semloc_test_gemini_r", "llm_tests": "direct_tests_test_gemini_r"}
GT_VI = {"original": "Nhãn gốc", "repaired": "Nhãn đã chuẩn hóa", "reviewed": "Nhãn đã rà soát"}
fmt = st.fmt


def _rows(name_: str) -> list[dict]:
    with open(DATA / name_) as f:
        return list(csv.DictReader(f))


def rq2_main_data(gt_sets: tuple = ("original", "repaired")) -> list[dict]:
    out = []
    for r in _rows("rq2_ours.csv"):
        if r.get("subset", "all") == "all" and r["gt"] in gt_sets and r["method"] in MAIN:
            out.append({"gt": r["gt"], "method": r["method"], **{k: 100 * float(r[k]) for k in
                                                                   ("acc1_mean", "acc1_sd", "acc3_mean", "acc3_sd")}})
            out[-1]["acc1"], out[-1]["acc3"] = out[-1].pop("acc1_mean"), out[-1].pop("acc3_mean")
    return out


def matplotlib_ticker():
    import matplotlib.ticker as t
    return t


def cost_acc_data(gt: str = "repaired") -> list[dict]:
    cost = _rows("llm_cost.csv")
    acc = {r["method"]: r for r in _rows("rq2_ours.csv") if r["gt"] == gt and r.get("subset", "all") == "all"}
    out = []
    for m, prefix in COST_PREFIX.items():
        runs = [float(r["tokens_per_program"]) for r in cost if r["run_id"].startswith(prefix)]
        out.append({"method": m, "ktokens": sum(runs) / len(runs) / 1000, "acc1": 100 * float(acc[m]["acc1_mean"])})
    return out


def fig_rq2_main(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows = rq2_main_data(("original", "repaired"))
    fig, axes = plt.subplots(1, 2, figsize=(st.WIDTH_IN, 3.6), sharey=True)
    y = range(len(MAIN))
    for ax, gt in zip(axes, ("original", "repaired")):
        by = {r["method"]: r for r in rows if r["gt"] == gt}
        for i, m in enumerate(MAIN):
            r, c = by[m], st.color(m)
            ax.barh(i + 0.19, r["acc3"], height=0.36, color=c, alpha=0.38, xerr=r["acc3_sd"], ecolor=st.MUTED, capsize=0)
            ax.barh(i - 0.19, r["acc1"], height=0.36, color=c, xerr=r["acc1_sd"], ecolor=st.MUTED, capsize=0)
            ax.text(r["acc1"] + r["acc1_sd"] + 1.2, i - 0.19, fmt(r["acc1"]), va="center", fontsize=11, color=st.INK)
            ax.text(r["acc3"] + r["acc3_sd"] + 1.2, i + 0.19, fmt(r["acc3"]), va="center", fontsize=11, color=st.MUTED)
        ax.set_title(GT_VI[gt], fontsize=13, loc="left")
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel("Độ chính xác (%)")
        ax.xaxis.grid(True, color=st.GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(list(y), [name(m) for m in MAIN])
    axes[0].invert_yaxis()
    from matplotlib.patches import Patch
    fig.legend(handles=[Patch(color=st.GREY, label="Acc@1"), Patch(color=st.GREY, alpha=0.38, label="Acc@3")],
               loc="lower right", ncol=2, frameon=False, bbox_to_anchor=(1, -0.02))
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(path)
    plt.close(fig)


def fig_cost_acc(path: Path) -> None:
    import matplotlib.pyplot as plt
    pts = cost_acc_data()
    fig, ax = plt.subplots(figsize=(st.WIDTH_IN, 3.4))
    for p in pts:
        ax.scatter(p["ktokens"], p["acc1"], s=90, color=st.color(p["method"]), edgecolor="white", lw=1.5, zorder=3)
        below = p["method"] == "llm_direct"  # FailLoc and LLM-Direct sit close together: one label above, one below
        ax.annotate(f"{name(p['method'])}: {fmt(p['ktokens'])}k token, Acc@1 {fmt(p['acc1'])}%", (p["ktokens"], p["acc1"]),
                    xytext=(8, -16 if below else 12), textcoords="offset points", va="center", fontsize=12, color=st.INK)
    ax.set_xscale("log")
    xs = [p["ktokens"] for p in pts]
    ax.set_xlim(min(xs) / 1.6, max(xs) * 3.2)
    ax.set_xticks([1, 2, 5, 10, 20, 50])
    ax.xaxis.set_minor_locator(matplotlib_ticker().NullLocator())
    ax.set_ylim(0, 100)
    from matplotlib.ticker import FuncFormatter
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt(v, 0) if v >= 1 else fmt(v, 1)))
    ax.set_xlabel("Số nghìn token LLM mỗi chương trình (thang log)")
    ax.set_ylabel("Acc@1, nhãn đã chuẩn hóa (%)")
    ax.yaxis.grid(True, color=st.GRID, lw=0.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def bonus_example(run: str = "semloc_test_gemini_r1") -> tuple[str, list[dict]]:
    """Program of `run` whose top spectrum line is not the guess and that has the most scored lines (ties: name)."""
    rows = [r for r in _rows("semloc_line_scores.csv") if r["run"] == run]
    progs: dict[str, list[dict]] = {}
    for r in rows:
        progs.setdefault(r["program"], []).append(r)
    def ok(rs):
        top = max(rs, key=lambda r: float(r["spectrum"]))
        return float(top["spectrum"]) > 0 and top["is_guess"] == "0" and any(r["is_guess"] == "1" for r in rs)
    cands = sorted((p for p, rs in progs.items() if ok(rs) and 4 <= len(rs) <= 8), key=lambda p: (-len(progs[p]), p))
    p = cands[0]
    return p, sorted(progs[p], key=lambda r: int(r["line"]))


def fig_semloc_bonus(path: Path) -> None:
    import matplotlib.pyplot as plt
    prog, rs = bonus_example()
    fig, ax = plt.subplots(figsize=(st.WIDTH_IN, 0.42 * len(rs) + 1.5))
    for i, r in enumerate(rs):
        sp, bo = float(r["spectrum"]), float(r["bonus"])
        ax.barh(i, sp, height=0.6, color=st.SEMLOC)
        if bo:
            ax.barh(i, bo, left=sp, height=0.6, color=st.FAILLOC)
            ax.text(sp + bo + 0.03, i, f"dòng LLM đoán: {fmt(sp, 2)} + {fmt(bo, 1)}", va="center", fontsize=12)
        else:
            ax.text(sp + 0.03, i, fmt(sp, 2), va="center", fontsize=12, color=st.MUTED)
    ax.axvline(1.0, color=st.MUTED, lw=1, ls="--")
    ax.text(1.0, len(rs) - 0.35, " điểm phổ tối đa", fontsize=11, color=st.MUTED, va="bottom")
    labels = [f"dòng {r['line']}" + (" (nhãn)" if r["is_gt_repaired"] == "1" else "") for r in rs]
    ax.set_yticks(range(len(rs)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 2.7)
    ax.set_xlabel(f"Điểm xếp hạng của SemLoc (chương trình {prog})")
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def _tex_code(line: str, limit: int | None = 46) -> str:
    rep = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "_": r"\_", "#": r"\#", "%": r"\%", "&": r"\&",
           "$": r"\$", "^": r"\^{}", "~": r"\~{}"}
    if limit and len(line) > limit:  # long signatures are cut so the code column stays left of the test columns
        line = line[:limit - 3].rstrip() + " …"
    body = line.lstrip(" ")
    indent = len(line) - len(body)
    return (rf"\hspace*{{{indent * 0.5}em}}" if indent else "") + "".join(rep.get(ch, ch) for ch in body)


def sbfl_matrix_tex(ex: dict, row_mm: float = 4.4) -> str:
    """Coverage matrix of the SBFL-blind example: code lines × tests, a dot where the test runs the line, Ochiai per
    line. Uses \\covdot, \\testhead{label}{pass?}, \\gtrow{y} defined in docs/report/vi/figures/sbfl-mu.tex."""
    import math
    tests = ex["tests"]
    n_fail = sum(not t["passed"] for t in tests)
    x0 = 10.4  # cm: first test column
    out = [r"\begin{tikzpicture}[x=1cm, y=-1mm]"]
    for j, t in enumerate(tests):
        out.append(rf"\node at ({x0 + 0.9 * j:.2f}, 0) {{\testhead{{$t_{{{j + 1}}}$}}{{{'1' if t['passed'] else '0'}}}}};")
    out.append(rf"\node[anchor=east] at ({x0 + 0.9 * len(tests) + 1.0:.2f}, 0) {{\footnotesize Ochiai}};")
    for i, c in enumerate(ex["code_lines"]):
        y = row_mm * (i + 1.4)
        if c["no"] == ex["gt_line"]:
            out.append(rf"\gtrow{{{y:.2f}}}{{{x0 + 0.9 * len(tests) + 1.1:.2f}}}")
        out.append(rf"\node[anchor=east, font=\scriptsize\color{{gray}}] at (0.45, {y:.2f}) {{{c['no']}}};")
        out.append(rf"\node[anchor=west, font=\ttfamily\footnotesize, inner sep=1pt] at (0.5, {y:.2f}) {{{_tex_code(c['text'])}}};")
        ef = ep = 0
        for j, t in enumerate(tests):
            if c["no"] in t["lines"]:
                out.append(rf"\node at ({x0 + 0.9 * j:.2f}, {y:.2f}) {{\covdot}};")
                ef += not t["passed"]
                ep += t["passed"]
        if ef + ep:
            o = ef / math.sqrt(n_fail * (ef + ep))
            out.append(rf"\node[anchor=east, font=\footnotesize] at ({x0 + 0.9 * len(tests) + 1.0:.2f}, {y:.2f}) {{{fmt(o, 2)}}};")
    out.append(r"\end{tikzpicture}")
    return "\n".join(out) + "\n"


def _plain_tex(t: str) -> str:
    rep = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "_": r"\_", "#": r"\#", "%": r"\%", "&": r"\&",
           "$": r"\$", "^": r"\^{}", "~": r"\~{}"}
    return "".join(rep.get(ch, ch) for ch in t)


def semloc_example_tex(ex: dict, context: int = 2) -> str:
    """SemLoc on one program: (a) code around the constraint anchors with the inserted checks, (b) constraint ×
    (failing tests violating, passing tests violating, Ochiai), (c) the line scores = spectrum + bonus, top 3."""
    code = {c["no"]: c["text"] for c in ex["code_lines"]}
    anchors = [c["anchor_line"] for c in ex["constraints"] if c["anchor_line"] in code]
    lo = max(min(code), min(anchors + [ex["guess_line"]]) - context)
    hi = min(max(code), max(anchors + [ex["guess_line"]]) + context)
    after = {}
    for c in ex["constraints"]:
        if c["anchor_line"] in code:
            after.setdefault(c["anchor_line"], []).append(c)
    rows = []
    for n in range(lo, hi + 1):
        mark = r"\rowcolor{failloc!12}" if n in ex["label_lines"] else ""
        rows.append(f"{mark}{n} & \\texttt{{{_tex_code(code[n], limit=80)}}} \\\\")
        for c in after.get(n, []):
            rows.append(f" & \\textit{{\\color{{semloc}}kiểm tra {c['id']}: \\texttt{{{_plain_tex(c['expr'])}}}}} \\\\")
    a = ("\\begin{tabular}{@{}r>{\\raggedright\\arraybackslash}p{0.86\\linewidth}@{}}\n\\toprule\n"
         "Dòng & Mã nguồn (dòng nghiêng: kiểm tra được SemLoc chèn vào) \\\\\n\\midrule\n" + "\n".join(rows) +
         "\n\\bottomrule\n\\end{tabular}")
    crow = "\n".join(f"{c['id']} & {c['anchor_line'] if c['anchor_line'] else c['region'].replace('_', ' ').lower()} & "
                      f"\\texttt{{{_plain_tex(c['expr'])}}} & {c['ef']} & {c['ep']} & {fmt(c['ochiai'], 2)} & {fmt(c['weight'], 1)} & "
                      f"{fmt(c['ochiai'] * c['weight'], 2)} \\\\"
                      for c in ex["constraints"])
    num = ">{\\centering\\arraybackslash}p{1.2cm}"
    b = (f"\\begin{{tabularx}}{{\\linewidth}}{{@{{}}lp{{1.5cm}}>{{\\raggedright\\arraybackslash}}X{num}{num}{num}{num}{num}@{{}}}}\n\\toprule\n"
         "Ràng buộc & Gắn ở & Biểu thức & Kiểm thử thất bại vi phạm & Kiểm thử thành công vi phạm & Ochiai & Hệ số vùng & Điểm cho dòng \\\\\n\\midrule\n" + crow +
         "\n\\bottomrule\n\\end{tabularx}")
    tops = ex["line_scores"][:3]
    parts = [f"dòng {r['line']}: {fmt(r['spectrum'], 2)}" + (f" + {fmt(r['bonus'], 1)}" if r["bonus"] else "") +
             f" (hạng {r['rank']})" for r in tops]
    c_ = "Điểm xếp hạng: " + "; ".join(parts) + "."
    return f"{{\\small\\setstretch{{1.05}}\n{a}\n\n\\medskip\n{b}\n\n\\medskip\n{c_}}}\n"


def failloc_example_tex(ex: dict, keep: int = 12) -> str:
    """FailLoc on one program: the prompt (program lines cut to the function) and the model's answer."""
    lines = ex["failloc_prompt"].split("\n")
    code_idx = [i for i, l in enumerate(lines) if l[:1].isdigit() and ": " in l]
    first = {c["no"] for c in ex["code_lines"]}
    kept = []
    skipped = False
    for i, l in enumerate(lines):
        if i in code_idx and int(l.split(":")[0]) not in first:
            if not skipped:
                kept.append("...")
                skipped = True
            continue
        kept.append(l)
    def keep_indent(l: str) -> str:
        if l[:1].isdigit() and ": " in l:  # "25:     portion = ..." keeps the indentation after the line number
            no, rest = l.split(": ", 1)
            body_ = rest.lstrip(" ")
            return f"{no}: " + "~" * (len(rest) - len(body_)) + _tex_code(body_, limit=None)
        return _tex_code(l, limit=None)
    body = "\\\\\n".join(keep_indent(l) if l else "~" for l in kept)
    ans = "[" + ", ".join(str(x) for x in ex["failloc_top5"]) + "]"
    return ("{\\small\\setstretch{1.0}\n\\fbox{\\parbox{0.95\\linewidth}{\\ttfamily\\footnotesize " + body + "}}\n\n"
            "\\medskip\n\\fbox{\\parbox{0.95\\linewidth}{Câu trả lời của LLM (năm dòng nghi nhất): "
            f"\\texttt{{{ans}}}; dòng lỗi theo nhãn: {ex['label_lines'][0]}.}}}}}}\n")


def main() -> None:
    st.apply("vi")
    OUT.mkdir(parents=True, exist_ok=True)
    fig_rq2_main(OUT / "fig_rq2_main.pdf")
    fig_cost_acc(OUT / "fig_cost_acc.pdf")
    fig_semloc_bonus(OUT / "fig_semloc_bonus.pdf")
    import json
    (OUT / "fig_sbfl_matrix.tex").write_text(sbfl_matrix_tex(json.loads((DATA / "fig_example.json").read_text())))
    ex2 = json.loads((DATA / "fig_semloc_examples.json").read_text())
    for prog, e in ex2.items():
        (OUT / f"fig_semloc_{prog}.tex").write_text(semloc_example_tex(e))
        (OUT / f"fig_failloc_{prog}.tex").write_text(failloc_example_tex(e))


if __name__ == "__main__":
    main()

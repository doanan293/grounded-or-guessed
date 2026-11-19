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
LANG = "vi"  # main_en() switches to English labels and decimal points for the paper
WIDTH = st.WIDTH_IN
EN = {"Nhãn gốc": "Original labels", "Nhãn đã chuẩn hóa": "Repaired labels", "Nhãn đã rà soát": "Reviewed labels",
      "Độ chính xác (%)": "Accuracy (%)", "Chênh lệch (điểm %)": "Difference (points)", "Thêm kiểm thử thất bại": "Add failing tests",
      "Thêm độ phủ": "Add coverage", "nhãn gốc": "original labels", "nhãn đã chuẩn hóa": "repaired labels",
      "nhãn đã rà soát": "reviewed labels", "BugsInPy (lỗi thật)": "BugsInPy (real bugs)"}


def tr(s: str) -> str:
    return EN.get(s, s) if LANG == "en" else s


def fmt(v: float, nd: int = 1) -> str:
    return st.fmt(v, nd, LANG)


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
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3.6), sharey=True)
    y = range(len(MAIN))
    for ax, gt in zip(axes, ("original", "repaired")):
        by = {r["method"]: r for r in rows if r["gt"] == gt}
        for i, m in enumerate(MAIN):
            r, c = by[m], st.color(m)
            ax.barh(i + 0.19, r["acc3"], height=0.36, color=c, alpha=0.38, xerr=r["acc3_sd"], ecolor=st.MUTED, capsize=0)
            ax.barh(i - 0.19, r["acc1"], height=0.36, color=c, xerr=r["acc1_sd"], ecolor=st.MUTED, capsize=0)
            ax.text(r["acc1"] + r["acc1_sd"] + 1.2, i - 0.19, fmt(r["acc1"]), va="center", fontsize=11, color=st.INK)
            ax.text(r["acc3"] + r["acc3_sd"] + 1.2, i + 0.19, fmt(r["acc3"]), va="center", fontsize=11, color=st.MUTED)
        ax.set_title(tr(GT_VI[gt]), fontsize=13, loc="left")
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xlabel(tr("Độ chính xác (%)"))
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


# ---------------------------------------------------------------- report figures beyond the main comparison
GT_ORDER = ("original", "repaired", "reviewed")
GT_VI3 = {"original": "Nhãn gốc", "repaired": "Nhãn đã chuẩn hóa", "reviewed": "Nhãn đã rà soát"}
GT_MARK = {"original": ("#9a9a94", "s"), "repaired": (st.FAILLOC, "o"), "reviewed": (st.SEMLOC, "D")}


def label_flow_data() -> dict:
    r = next(x for x in _rows("label_audit.csv") if x["subset"] == "all")
    parts = [("Giữ nguyên", int(r["same"])), ("Thêm dòng thứ hai", int(r["extended"])), ("Dòng trống", int(r["blank"])),
             ("Không phải mã", int(r["non_code"])), ("Lệch một dòng", int(r["off_by_one"])),
             ("Lệch từ hai dòng", int(r["farther"]))]
    return {"n": int(r["n"]), "parts": parts}


def ablation_data() -> list[dict]:
    out = []
    for r in _rows("ablation_coverage.csv"):
        if r["subset"] == "all":
            out.append({"gt": r["gt"], "contrast": r["contrast"],
                        **{k: 100 * float(r[c]) for k, c in (("d_acc1", "d_acc1"), ("lo1", "d_acc1_lo"), ("hi1", "d_acc1_hi"),
                                                             ("d_acc3", "d_acc3"), ("lo3", "d_acc3_lo"), ("hi3", "d_acc3_hi"))}})
    return out


def addons_data(gt: str = "repaired") -> list[dict]:
    """Δ of each addition against the method it extends (points with a 95% interval where repeated runs exist)."""
    import json
    rq2 = {(r["gt"], r["method"]): r for r in _rows("rq2_ours.csv") if r.get("subset", "all") == "all"}
    ab = {(r["gt"], r["contrast"]): r for r in ablation_data()}
    c = rq2[(gt, "covgate")]
    out = [{"name": "CovGate (so với SemLoc), tập test", "d1": 100 * float(c["d_acc1"]), "lo1": 100 * float(c["d_acc1_lo"]),
            "hi1": 100 * float(c["d_acc1_hi"]), "d3": 100 * float(c["d_acc3"]), "lo3": 100 * float(c["d_acc3_lo"]),
            "hi3": 100 * float(c["d_acc3_hi"])}]
    a = ab[(gt, "coverage_effect")]
    out.append({"name": "FailLoc+Cov (so với FailLoc), tập test", "d1": a["d_acc1"], "lo1": a["lo1"], "hi1": a["hi1"],
                "d3": a["d_acc3"], "lo3": a["lo3"], "hi3": a["hi3"]})
    v = next(r for r in _rows("vote_dev.csv") if r["gt"] == gt)
    out.append({"name": "FailLoc+Vote (so với FailLoc), tập dev", "d1": 100 * (float(v["vote_acc1"]) - float(v["single_acc1"])),
                "d3": 100 * (float(v["vote_acc3"]) - float(v["single_acc3"]))})
    params = json.loads((DATA / "pav_params.json").read_text())
    grid = _rows("pav_dev_grid.csv")
    base = next(r for r in grid if r["k"] == "0")  # k = 0: FailLoc's own ranking, no verification
    ch = next(r for r in grid if r["order"] == params["order"] and int(r["k"]) == params["k"]
              and int(r["attempts"]) == params["attempts"]
              and r["max_size"] == ("" if params["max_size"] is None else str(params["max_size"])))
    out.append({"name": "FailLoc+Verify (so với FailLoc), tập dev",
                "d1": 100 * (float(ch[f"{gt}_acc1"]) - float(base[f"{gt}_acc1"])),
                "d3": 100 * (float(ch[f"{gt}_acc3"]) - float(base[f"{gt}_acc3"]))})
    return out


def rq3_data(gt: str = "repaired") -> dict:
    bip_rows = [r for r in _rows("rq3_bugsinpy.csv") if r["subset"] == "all"]
    bip = {r["method"]: 100 * float(r["acc1_mean"]) for r in bip_rows}
    bip3 = {r["method"]: 100 * float(r["acc3_mean"]) for r in bip_rows
            if r["method"] in ("sbfl_ochiai", "semloc_spectrum", "llm_guess", "semloc_prior", "llm_tests", "llm_coverage")}
    ren = {r["method"]: (100 * float(r["orig_acc3_mean"]), 100 * float(r["renamed_acc3_mean"]))
           for r in _rows("rq3_renamed.csv") if r["gt"] == gt}
    fam, n_fam = {}, 0
    for r in _rows("rq3_families.csv"):
        if r["gt"] == gt and r["method"] in ("semloc", "semloc_no_prior"):
            fam.setdefault(r["family"], {})[r["method"]] = 100 * float(r["acc1_mean"])
            n_fam = int(r["n"])
    return {"bugsinpy": bip, "bugsinpy3": bip3, "renamed": ren, "families": fam, "n_families": n_fam}


def decomposition_data() -> list[dict]:
    return [{"gt": r["gt"], "metric": r["metric"], "guess": 100 * float(r["phi_guess"]),
             "spectrum": 100 * float(r["phi_spectrum"])}
            for r in _rows("rq_decomposition.csv") if r["game"] == "semloc" and r["subset"] == "all"]


def improvement_data() -> list[dict]:
    rq2 = {(r["gt"], r["method"]): r for r in _rows("rq2_ours.csv") if r.get("subset", "all") == "all"}
    out = [{"setting": tr(GT_VI3[g]), "semloc1": 100 * float(rq2[(g, "semloc")]["acc1_mean"]),
            "failloc1": 100 * float(rq2[(g, "llm_tests")]["acc1_mean"]),
            "semloc3": 100 * float(rq2[(g, "semloc")]["acc3_mean"]), "failloc3": 100 * float(rq2[(g, "llm_tests")]["acc3_mean"])}
           for g in GT_ORDER]
    bip = {r["method"]: r for r in _rows("rq3_bugsinpy.csv") if r["subset"] == "all"}
    out.append({"setting": tr("BugsInPy (lỗi thật)"), "semloc1": 100 * float(bip["semloc_prior"]["acc1_mean"]),
                "failloc1": 100 * float(bip["llm_tests"]["acc1_mean"]),
                "semloc3": 100 * float(bip["semloc_prior"]["acc3_mean"]), "failloc3": 100 * float(bip["llm_tests"]["acc3_mean"])})
    return out


FAIL_VI = {"guess_right": "Dòng LLM đoán là dòng lỗi", "rescued_by_spectrum": "Đoán sai, phổ vi phạm cứu vào top 3",
           "prior_hurts": "Phổ đúng hạng 1, điểm thưởng đẩy xuống", "coverage_only_wins": "Chỉ FailLoc+Cov trúng top 3",
           "gt_suspect": "Mọi phương pháp sai, nhãn đáng ngờ", "all_miss": "Mọi phương pháp sai ngoài top 3"}


def failure_data() -> list[tuple[str, int]]:
    cats = [r["category"] for r in _rows("failure_signals.csv")]  # one row per test program (failure_cases: examples only)
    return [(c, cats.count(c)) for c in FAIL_VI if cats.count(c)]


def _save(fig, path):
    import matplotlib.pyplot as plt
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_label_flow(path: Path) -> None:
    import matplotlib.pyplot as plt
    d = label_flow_data()
    colors = [st.GREY, "#c9c9c3", st.FAILLOC, "#e8956f", st.SEMLOC, "#8fb6ea"]
    fig, ax = plt.subplots(figsize=(st.WIDTH_IN, 2.3))
    left = 0
    for (lab, v), c in zip(d["parts"], colors):
        ax.barh(0, v, left=left, color=c, edgecolor="white", lw=1.5, height=0.5)
        if v >= 15:
            ax.text(left + v / 2, 0, str(v), ha="center", va="center", fontsize=12, color="white" if c in (st.FAILLOC, st.SEMLOC, st.GREY) else st.INK)
        left += v
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=c, label=f"{lab} ({v})") for (lab, v), c in zip(d["parts"], colors)], ncol=3,
              loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False, fontsize=11)
    ax.set_xlim(0, d["n"])
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("")
    ax.tick_params(axis="x", labelsize=11)
    _save(fig, path)


def _forest(ax, rows, key, lo, hi, title):
    for i, r in enumerate(rows):
        c, mk = r["style"]
        if lo in r:
            ax.errorbar(r[key], i, xerr=[[r[key] - r[lo]], [r[hi] - r[key]]], fmt=mk, color=c, ms=7, capsize=0, lw=1.6)
        else:
            ax.plot(r[key], i, mk, mfc="white", mec=c, ms=7, mew=1.6)
    ax.axvline(0, color=st.MUTED, lw=1)
    ax.set_title(title, fontsize=13, loc="left")
    ax.set_xlabel(tr("Chênh lệch (điểm %)"))
    ax.xaxis.grid(True, color=st.GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.tick_params(axis="y", length=0)


def fig_ablation(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows, labels = [], []
    for contrast, lab in (("tests_effect", "Thêm kiểm thử thất bại\n(LLM-Direct → FailLoc)"), ("coverage_effect", "Thêm độ phủ\n(FailLoc → FailLoc+Cov)")):
        for gt in GT_ORDER:
            r = next(x for x in ablation_data() if x["gt"] == gt and x["contrast"] == contrast)
            rows.append({**r, "style": GT_MARK[gt]})
            labels.append(f"{tr(lab.splitlines()[0])}, {tr(GT_VI3[gt].lower())}")
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3.4), sharey=True)
    _forest(axes[0], rows, "d_acc1", "lo1", "hi1", "Acc@1")
    _forest(axes[1], rows, "d_acc3", "lo3", "hi3", "Acc@3")
    axes[0].set_yticks(range(len(rows)), labels, fontsize=11)
    axes[0].invert_yaxis()
    _save(fig, path)


def fig_addons(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows = [{**r, "style": (st.SEMLOC if "CovGate" in r["name"] else st.FAILLOC, "o")} for r in addons_data()]
    fig, axes = plt.subplots(1, 2, figsize=(st.WIDTH_IN, 2.9), sharey=True)
    _forest(axes[0], rows, "d1", "lo1", "hi1", "Acc@1")
    _forest(axes[1], rows, "d3", "lo3", "hi3", "Acc@3")
    axes[0].set_yticks(range(len(rows)), [r["name"].replace(", ", "\n") for r in rows], fontsize=11)
    axes[0].invert_yaxis()
    _save(fig, path)


def fig_rq3(path: Path) -> None:
    import matplotlib.pyplot as plt
    d = rq3_data()
    fig = plt.figure(figsize=(st.WIDTH_IN, 5.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1])
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, :])]
    ax = axes[0]
    meths = [("sbfl_ochiai", "SBFL (Ochiai)"), ("semloc_spectrum", "Chỉ phổ vi phạm"), ("llm_guess", "Chỉ dòng đoán"),
             ("semloc_prior", "SemLoc"), ("llm_tests", "FailLoc")]
    for i, (m, lab) in enumerate(meths):
        c = st.FAILLOC if m == "llm_tests" else st.SEMLOC if m == "semloc_prior" else st.GREY
        ax.barh(i, d["bugsinpy"][m], color=c, height=0.6)
        ax.text(d["bugsinpy"][m] + 1.5, i, fmt(d["bugsinpy"][m]), va="center", fontsize=10)
    ax.set_yticks(range(len(meths)), [l for _, l in meths], fontsize=10)
    ax.invert_yaxis()
    ax.set_xlim(0, 75)
    ax.set_title("(a) Lỗi thật BugsInPy, Acc@1", fontsize=11, loc="left")
    ax = axes[1]
    for m, lab in (("semloc", "SemLoc"), ("semloc_no_prior", "SemLoc−Bonus"), ("llm_guess", "Chỉ dòng đoán"), ("llm_coverage", "FailLoc+Cov")):
        a, b = d["renamed"][m]
        c = st.SEMLOC if m == "semloc" else st.FAILLOC if m == "llm_coverage" else st.GREY
        ax.plot([0, 1], [a, b], "-o", color=c, ms=5)
        ax.text(1.06, b + (1.2 if m == "semloc" else -1.2 if m == "llm_guess" else 0), lab, va="center", fontsize=9)
    ax.set_xticks([0, 1], ["Mã gốc", "Đổi tên"], fontsize=10)
    ax.set_xlim(-0.2, 2.0)
    ax.set_title("(b) Đổi tên định danh, Acc@3", fontsize=11, loc="left")
    ax = axes[2]
    fams = list(d["families"])
    for i, f in enumerate(fams):
        a, b = d["families"][f]["semloc"], d["families"][f]["semloc_no_prior"]
        ax.plot([b, a], [i, i], color=st.GRID, lw=3)
        ax.plot(a, i, "o", color=st.SEMLOC, ms=6)
        ax.plot(b, i, "o", mfc="white", mec=st.SEMLOC, ms=6)
    ax.set_yticks(range(len(fams)), fams, fontsize=10)
    ax.invert_yaxis()
    ax.set_title(f"(c) Năm họ mô hình ({d['n_families']} chương trình), Acc@1: ● SemLoc, ○ SemLoc−Bonus", fontsize=11, loc="left")
    ax.set_xlim(0, 100)
    for a_ in axes:
        a_.tick_params(labelsize=10)
    _save(fig, path)


def fig_decomposition(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows = [r for r in decomposition_data() if r["gt"] in ("original", "repaired")]
    fig, ax = plt.subplots(figsize=(st.WIDTH_IN, 2.8))
    for i, r in enumerate(rows):
        ax.barh(i, r["guess"], color=st.FAILLOC, height=0.55)
        ax.barh(i, r["spectrum"], left=r["guess"], color=st.SEMLOC, height=0.55)
        ax.text(r["guess"] / 2, i, fmt(r["guess"]), ha="center", va="center", color="white", fontsize=11)
        ax.text(r["guess"] + r["spectrum"] / 2, i, fmt(r["spectrum"]), ha="center", va="center", color="white", fontsize=11)
    ax.set_yticks(range(len(rows)), [f"{GT_VI3[r['gt']]}, {r['metric'].replace('acc', 'Acc@')}" for r in rows], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Phần độ chính xác của SemLoc (điểm %)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=st.FAILLOC, label="Phần do dòng LLM đoán"), Patch(color=st.SEMLOC, label="Phần do phổ vi phạm")],
              loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2, frameon=False, fontsize=11)
    _save(fig, path)


def fig_improvement(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows = improvement_data()
    fig, axes = plt.subplots(1, 2, figsize=(WIDTH, 3.0), sharey=True)
    for ax, k, title in ((axes[0], "1", "Acc@1"), (axes[1], "3", "Acc@3")):
        for i, r in enumerate(rows):
            a, b = r["semloc" + k], r["failloc" + k]
            ax.plot([a, b], [i, i], color=st.GRID, lw=3, zorder=1)
            ax.plot(a, i, "o", color=st.SEMLOC, ms=7, zorder=2)
            ax.plot(b, i, "o", color=st.FAILLOC, ms=7, zorder=2)
            ax.text(max(a, b) + 2, i, f"{'+' if b >= a else ''}{fmt(b - a)}", va="center", fontsize=10)
        ax.set_title(title, fontsize=13, loc="left")
        ax.set_xlim(0, 112)
        ax.xaxis.grid(True, color=st.GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_xlabel(tr("Độ chính xác (%)"))
    axes[0].set_yticks(range(len(rows)), [r["setting"] for r in rows], fontsize=11)
    axes[0].invert_yaxis()
    from matplotlib.lines import Line2D
    fig.legend(handles=[Line2D([], [], marker="o", ls="", color=st.SEMLOC, label="SemLoc"),
                        Line2D([], [], marker="o", ls="", color=st.FAILLOC, label="FailLoc")],
               loc="lower center", ncol=2, frameon=False, fontsize=11)
    fig.tight_layout(rect=(0, 0.08, 1, 1))
    fig.savefig(path)
    plt.close(fig)


def fig_failures(path: Path) -> None:
    import matplotlib.pyplot as plt
    rows = failure_data()
    fig, ax = plt.subplots(figsize=(st.WIDTH_IN, 0.42 * len(rows) + 1.2))
    for i, (c, n) in enumerate(rows):
        ax.barh(i, n, color=st.FAILLOC if c == "prior_hurts" else st.SEMLOC if c == "rescued_by_spectrum" else st.GREY, height=0.6)
        ax.text(n + 1, i, str(n), va="center", fontsize=11)
    ax.set_yticks(range(len(rows)), [FAIL_VI[c] for c, _ in rows], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel("Số chương trình (tập test, nhãn đã chuẩn hóa)")
    _save(fig, path)


def main_en() -> None:
    """English versions of the three headline figures for the paper (figure*, 18.2 cm, decimal points)."""
    global LANG, WIDTH
    st.apply("en")
    LANG, WIDTH = "en", 18.2 / 2.54
    out = ROOT / "docs" / "report" / "generated"
    try:
        fig_rq2_main(out / "fig_rq2_main.pdf")
        fig_ablation(out / "fig_ablation.pdf")
        fig_improvement(out / "fig_improvement.pdf")
    finally:
        LANG, WIDTH = "vi", st.WIDTH_IN


def main() -> None:
    st.apply("vi")
    OUT.mkdir(parents=True, exist_ok=True)
    fig_rq2_main(OUT / "fig_rq2_main.pdf")
    fig_cost_acc(OUT / "fig_cost_acc.pdf")
    fig_semloc_bonus(OUT / "fig_semloc_bonus.pdf")
    for name, fn in (("fig_label_flow", fig_label_flow), ("fig_ablation", fig_ablation), ("fig_addons", fig_addons),
                     ("fig_rq3", fig_rq3), ("fig_decomposition", fig_decomposition), ("fig_improvement", fig_improvement),
                     ("fig_failures", fig_failures)):
        fn(OUT / f"{name}.pdf")
    import json
    (OUT / "fig_sbfl_matrix.tex").write_text(sbfl_matrix_tex(json.loads((DATA / "fig_example.json").read_text())))
    ex2 = json.loads((DATA / "fig_semloc_examples.json").read_text())
    for prog, e in ex2.items():
        (OUT / f"fig_semloc_{prog}.tex").write_text(semloc_example_tex(e))
        (OUT / f"fig_failloc_{prog}.tex").write_text(failloc_example_tex(e))


if __name__ == "__main__":
    main()
    main_en()

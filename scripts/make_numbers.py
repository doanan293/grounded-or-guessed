"""Every headline number of the paper and report as a LaTeX macro, generated from data/ (never typed by hand).

    python scripts/make_numbers.py
Writes docs/report/generated/numbers.tex (decimal point, for the English paper) and numbers-vi.tex (decimal comma,
same macro names, for the Vietnamese report). Names are CamelCase from the row keys and column, digits spelled out
(LaTeX macro names cannot contain digits): rq2 / repaired / all / llm_coverage / acc3_mean → \\RqTwoRepairedAllLlmCoverageAccThreeMean.
Percentages are ×100 with one decimal; differences (d_*) are signed percentage points; p-values three decimals.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "docs" / "report" / "generated"
DIGITS = "Zero One Two Three Four Five Six Seven Eight Nine".split()

Spec = tuple  # (name parts, csv path, row filter {col: value}, column, format)


def macro_name(*parts: str) -> str:
    words = []
    for part in parts:
        part = re.sub(r"^-(?=\d)", "minus ", str(part))  # a negative key (e.g. offset −1) must not collide with +1
        for tok in re.findall(r"[A-Za-z]+|\d", str(part)):
            words.append(DIGITS[int(tok)] if tok.isdigit() else tok.capitalize())
    return "\\" + "".join(words)


def fmt(value: str, kind: str, comma: bool = False) -> str:
    v = float(value)
    s = {"pct": f"{100 * v:.1f}", "pp": f"{100 * v:+.1f}", "int": f"{int(round(v))}", "p": f"{v:.3f}",
         "dec2": f"{v:.2f}", "k": f"{v / 1000:.1f}"}[kind]
    if kind == "p" and v < 0.001:
        s = "$<$0.001"
    return s.replace(".", ",").replace("-", "−") if comma else s  # Vietnamese: decimal comma, true minus sign


def _rows(path: Path) -> list[dict]:
    with open(path) as f:
        return list(csv.DictReader(f))


def render(specs: list[Spec], comma: bool = False) -> str:
    lines, seen = [], set()
    for parts, path, flt, col, kind in specs:
        hits = [r for r in _rows(path) if all(r.get(k) == v for k, v in flt.items())]
        if len(hits) != 1:
            raise ValueError(f"{path.name} {flt}: {len(hits)} rows match (need exactly 1)")
        name = macro_name(*parts)
        if name in seen:
            raise ValueError(f"duplicate macro {name}")
        seen.add(name)
        if hits[0].get(col) in (None, ""):
            continue
        lines.append(f"\\newcommand{{{name}}}{{{fmt(hits[0][col], kind, comma)}}}")
    return "\n".join(lines) + "\n"


def table_specs(prefix: str, path: Path, keys: list[str], cols: dict[str, str], where: dict | None = None) -> list[Spec]:
    """One macro per (row, column): name = prefix + key values + column."""
    out = []
    for r in _rows(path):
        if where and any(r.get(k) not in v for k, v in where.items()):
            continue
        for col, kind in cols.items():
            out.append(((prefix, *[r[k] for k in keys], col), path, {k: r[k] for k in keys}, col, kind))
    return out


def all_specs() -> list[Spec]:
    acc = {"acc1_mean": "pct", "acc3_mean": "pct", "acc5_mean": "pct"}
    diff = {f"d_acc{k}{s}": "pp" for k in (1, 3) for s in ("", "_lo", "_hi")}
    specs = []
    specs += table_specs("rq1", DATA / "rq1_audit.csv", ["config", "scoring", "subset"],
                         {"acc1": "pct", "acc3": "pct", "acc5": "pct"}, {"subset": ["all"]})
    specs += table_specs("rq2", DATA / "rq2_ours.csv", ["gt", "subset", "method"],
                         {**acc, **diff, "p_acc3_max": "p", "rank_biserial_rr": "dec2", "n": "int"})
    specs += table_specs("bip", DATA / "rq3_bugsinpy.csv", ["subset", "method"],
                         {"acc1_mean": "pct", "acc3_mean": "pct", "acc5_mean": "pct", **diff, "n": "int"})
    specs += table_specs("ren", DATA / "rq3_renamed.csv", ["gt", "method"],
                         {"orig_acc1_mean": "pct", "renamed_acc1_mean": "pct", "orig_acc3_mean": "pct",
                          "renamed_acc3_mean": "pct", **diff, "n": "int"})
    specs += table_specs("fam", DATA / "rq3_families.csv", ["gt", "family", "method"],
                         {"acc1_mean": "pct", "acc3_mean": "pct"}, {"gt": ["repaired"]})
    specs += table_specs("dec", DATA / "rq_decomposition.csv", ["game", "gt", "subset", "metric"],
                         {c: "pct" for c in ("full", "phi_guess", "phi_spectrum", "phi_guess_ci_cluster_lo",
                                             "phi_guess_ci_cluster_hi", "phi_spectrum_ci_cluster_lo",
                                             "phi_spectrum_ci_cluster_hi")}, {"subset": ["all"]})
    specs += table_specs("pub", DATA / "rq_decomposition_published.csv", ["source", "game", "gt", "subset", "metric"],
                         {"full": "pct", "phi_guess": "pct", "phi_spectrum": "pct"},
                         {"source": ["semloc_claude_T0.8", "semloc_gemini_T0.8"], "game": ["semloc"],
                          "gt": ["original"], "subset": ["all"]})
    specs += table_specs("tol", DATA / "failure_tolerance.csv", ["method"],
                         {"acc1_exact": "pct", "acc1_guard_strict": "pct", "acc1_guard_or_body": "pct"})
    specs += table_specs("off", DATA / "failure_offsets.csv", ["method", "offset"], {"count": "int"})
    specs += table_specs("pareto", DATA / "pareto.csv", ["method", "model"], {"acc3": "pct", "tokens_per_program": "k"})
    return specs


def computed() -> dict[str, str]:
    """Counts that live in JSON / need aggregation, and method constants read from the code (formatted already)."""
    from flx.covgate import PRIOR
    out = {macro_name("const", "prior", "weight"): f"{PRIOR:g}", macro_name("const", "ci", "level"): "95",
           macro_name("const", "bootstrap", "draws"): "10000"}
    import importlib.util
    spec = importlib.util.spec_from_file_location("covgate_eval", ROOT / "scripts" / "covgate_eval.py")
    ce = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ce)
    lams = sorted({g["lam"] for g in ce.GRID})
    out[macro_name("const", "lambda", "grid")] = "; ".join(f"{x:g}" for x in lams)   # rendered with commas in -vi
    out[macro_name("const", "temperature")] = "0.8"   # scripts/run_matrix.sh: every SemLoc repeat runs at T = 0.8
    verified = json.loads((DATA / "semfault_verified_gt.json").read_text())
    for status in ("confirmed", "corrected", "unverified", "unverifiable"):
        out[macro_name("gt", status, "n")] = str(sum(r["status"] == status for r in verified))
    from flx.gt import load_variants
    v = load_variants()
    out[macro_name("gt", "repaired", "n")] = str(len(v["repaired"]))
    verified_ok = {r["program"] for r in verified if r["status"] in ("confirmed", "corrected")}
    out[macro_name("gt", "blank", "fix", "dropped", "n")] = str(sum(p not in v["repaired"] for p in verified_ok))
    labels = _rows(DATA / "semfault_labels.csv")
    out[macro_name("gt", "not", "executed", "n")] = str(sum(r["category"] == "not_executed" for r in labels))
    from flx.semloc_results import load_ground_truth
    blank = 0
    for p, lines in load_ground_truth(ROOT / "third_party" / "semloc" / "benchmark" / "ground_truth.json").items():
        rows = (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / f"{p}.py").read_text().splitlines()
        blank += bool(lines) and all(not rows[ln - 1].strip() for ln in lines if 0 < ln <= len(rows))
    out[macro_name("gt", "blank", "n")] = str(blank)
    sig = _rows(DATA / "failure_signals.csv")
    for cat in sorted({r["category"] for r in sig}):
        out[macro_name("fail", cat, "n")] = str(sum(r["category"] == cat for r in sig))
    out[macro_name("fail", "wrong", "guess", "n")] = str(sum(r["category"] != "guess_right" for r in sig))
    out[macro_name("fail", "programs", "n")] = str(len(sig))
    for rel in sorted({r["guess_relation"] for r in sig}):
        out[macro_name("fail", "relation", rel, "n")] = str(sum(r["guess_relation"] == rel and r["category"] != "guess_right"
                                                               for r in sig))
    cost = _rows(DATA / "llm_cost.csv")
    sem = [r for r in cost if r["run_id"].startswith("semloc_test_gemini_r")]
    out[macro_name("cost", "cf", "share", "pct")] = f"{100 * sum(int(r['calls_t0']) for r in sem) / sum(int(r['calls']) for r in sem):.0f}"
    for prefix, name in (("semloc_test_gemini_r", "semloc"), ("direct_cov_test_gemini_r", "llm coverage"),
                         ("direct_test_gemini_r", "llm direct")):
        rs = [float(r["tokens_per_program"]) for r in cost if r["run_id"].startswith(prefix)]
        out[macro_name("cost", *name.split(), "tokens", "k")] = f"{sum(rs) / len(rs) / 1000:.1f}" if rs else ""
    return out


def main() -> None:
    specs = all_specs()
    extra = computed()
    for comma, name in ((False, "numbers.tex"), (True, "numbers-vi.tex")):
        body = render(specs, comma)
        body += "".join(f"\\newcommand{{{k}}}{{{v.replace('.', ',').replace('-', '−') if comma else v}}}\n"
                        for k, v in extra.items() if v)
        names = re.findall(r"\\newcommand\{(\\[A-Za-z]+)\}", body)
        if len(names) != len(set(names)):
            raise ValueError("duplicate macro names")
        (OUT / name).write_text("% generated by scripts/make_numbers.py from data/ — do not edit\n" + body)
    print(f"{len(names)} macros")


if __name__ == "__main__":
    main()

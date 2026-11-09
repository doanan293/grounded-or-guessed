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
         "dec1": f"{v:.1f}", "dec2": f"{v:.2f}", "k": f"{v / 1000:.1f}"}[kind]
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
    if (DATA / "ablation_coverage.csv").exists():
        specs += table_specs("abl", DATA / "ablation_coverage.csv", ["gt", "subset", "contrast"],
                             {"a_acc1": "pct", "b_acc1": "pct", "a_acc3": "pct", "b_acc3": "pct", **diff})
    if (DATA / "static_tools.csv").exists():
        specs += table_specs("stat", DATA / "static_tools.csv", ["gt", "tool"],
                             {c: "int" for c in ("programs", "diagnostics", "flagged", "on_fault_line", "within_2_lines")}
                             | {"on_fault_line_by_chance": "dec1"})
    if (DATA / "pav_mechanism.csv").exists():
        specs += table_specs("pavmech", DATA / "pav_mechanism.csv", ["gt"],
                             {"fault_line_fixable": "pct", "other_line_fixable": "pct", "fault_line_checked": "int",
                              "other_line_checked": "int"})
        specs += table_specs("vote", DATA / "vote_dev.csv", ["gt"],
                             {c: "pct" for c in ("single_acc1", "single_acc3", "vote_acc1", "vote_acc3")})
    specs += table_specs("pareto", DATA / "pareto.csv", ["method", "model"],
                         {"acc1": "pct", "acc3": "pct", "tokens_per_program": "k", "n": "int"})
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
    out[macro_name("const", "temperature")] = "0.8"
    from flx.params import chosen_params
    for g in ("original", "repaired"):
        out[macro_name("const", "lambda", g)] = f"{chosen_params(g)['lam']:g}"   # dev-chosen CovGate weight   # scripts/run_matrix.sh: every SemLoc repeat runs at T = 0.8
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
    # RQ1b: SemLoc re-executed with the paper's own model (Claude Sonnet 4.6) on the dev split vs the published log
    spec2 = importlib.util.spec_from_file_location("rq3_families", ROOT / "scripts" / "rq3_families.py")
    fam = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(fam)
    from flx.ranking import metrics as _metrics
    from flx._semloc import SEMLOC_ROOT
    dev = json.loads((DATA / "split.json").read_text())["dev"]
    gt0 = v["original"]
    for name, run in (("rerun", ROOT / "runs" / "semloc_dev_claude46_r1"),
                      ("published", SEMLOC_ROOT / "results" / "RQ1" / "semloc_claude_T0.8")):
        if (run / "scores").exists():
            m = _metrics(fam.run_ranks(run, gt0, dev, "semloc"), dev)
            for k in ("acc1", "acc3", "acc5"):
                out[macro_name("rep", "claude", "dev", name, k)] = f"{100 * m[k]:.1f}"
    offs = _rows(DATA / "failure_offsets.csv")
    guesses = sum(int(r["count"]) for r in offs if r["method"] == "llm_guess")
    out[macro_name("off", "llm", "guess", "total")] = str(guesses)
    out[macro_name("off", "llm", "guess", "missing")] = str(len(sig) * 3 - guesses)   # program-repeat pairs with no guess
    cost = _rows(DATA / "llm_cost.csv")
    sem = [r for r in cost if r["run_id"].startswith("semloc_test_gemini_r")]
    out[macro_name("cost", "cf", "share", "pct")] = f"{100 * sum(int(r['calls_t0']) for r in sem) / sum(int(r['calls']) for r in sem):.0f}"
    for prefix, name in (("semloc_test_gemini_r", "semloc"), ("direct_cov_test_gemini_r", "llm coverage"),
                         ("direct_test_gemini_r", "llm direct"),
                         ("direct_tests_test_gemini_r", "llm tests")):
        rs = [float(r["tokens_per_program"]) for r in cost if r["run_id"].startswith(prefix)]
        out[macro_name("cost", *name.split(), "tokens", "k")] = f"{sum(rs) / len(rs) / 1000:.1f}" if rs else ""
    grid = DATA / "pav_dev_grid.csv"
    if grid.exists():  # propose-and-verify on dev: stage 1 alone, the selected knobs, and the worst grid point
        rows = _rows(grid)
        params = json.loads((DATA / "pav_params.json").read_text())
        chosen = next(r for r in rows if r["order"] == params["order"] and int(r["k"]) == params["k"]
                      and int(r["attempts"]) == params["attempts"]
                      and r["max_size"] == ("" if params["max_size"] is None else str(params["max_size"])))
        worst = min((r for r in rows if r["order"] != "stage1"), key=lambda r: float(r["select_acc1"]))
        for tag, r in (("stage", rows[0]), ("chosen", chosen), ("worst", worst)):
            for g in ("original", "repaired", "reviewed"):
                for k in ("acc1", "acc3"):
                    out[macro_name("pav", "dev", tag, g, k)] = f"{100 * float(r[f'{g}_{k}']):.1f}"
        out[macro_name("pav", "grid", "size")] = str(len(rows) - 1)
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

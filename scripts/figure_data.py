"""Derived data for the figures (no LLM calls, no re-runs).

data/semloc_line_scores.csv  per-line SemLoc scores of the three Gemini test runs, split into the semantic-spectrum
                             part and the +1.2 bonus SemLoc's released code adds on the LLM-guessed line.
data/fig_cov_example.json    running example 2 (combine_responses) for the FailLoc+Cov flow slide: [f/p] per line and
                             FailLoc / FailLoc+Cov top 5 in the three Gemini test runs.
data/fig_example.json        one short test-split program whose failing tests run only lines that passing tests
                             also run (SBFL cannot separate them), with its coverage, label and the LLM-guessed line.
    .venv/bin/python scripts/figure_data.py
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
PRIOR = 1.2  # flx.covgate.PRIOR: SemLoc's bonus on the LLM's own fault-line guess
RUNS = [f"semloc_test_gemini_r{i}" for i in (1, 2, 3)]


def line_scores(scores_dir: Path) -> list[dict]:
    out = []
    for f in sorted(Path(scores_dir).glob("*.json")):
        d = json.loads(f.read_text())
        guess = d.get("fault_line_pred")
        ranked = [int(ln) for ln, _ in d.get("ranked_lines", [])]
        for ln_s, score in d.get("line_scores", {}).items():
            ln = int(ln_s)
            bonus = PRIOR if ln == guess else 0.0
            out.append({"program": f.stem, "line": ln, "spectrum": round(score - bonus, 6), "bonus": bonus,
                        "score": round(score, 6), "rank": ranked.index(ln) + 1 if ln in ranked else len(ranked) + 1,
                        "is_guess": ln == guess})
    return out


def function_window(rows: list[str], line: int) -> tuple[int, int]:
    """First and last line (1-based) of the def that contains `line`, trailing blank lines dropped."""
    lo = line
    while lo > 1 and not rows[lo - 1].lstrip().startswith("def "):
        lo -= 1
    indent = len(rows[lo - 1]) - len(rows[lo - 1].lstrip())
    hi = lo
    while not rows[hi - 1].split("#")[0].rstrip().endswith(":"):  # multi-line signature
        hi += 1
    for i in range(hi + 1, len(rows) + 1):
        r = rows[i - 1]
        if r.strip() and len(r) - len(r.lstrip()) <= indent:
            break
        hi = i
    while hi > line and not rows[hi - 1].strip():
        hi -= 1
    return lo, hi


def pick_example(cov_dir: Path, gt: dict, guesses: dict, sources: dict, max_span: int = 24) -> dict:
    """Shortest SBFL-blind program: failing-test lines ⊆ passing-test lines, label executed by a failing test."""
    best = None
    for p in sorted(guesses):
        f = cov_dir / f"{p}.json"
        if not f.exists() or p not in gt or len(gt[p]) != 1:
            continue
        tests = json.loads(f.read_text())["tests"]
        fail = set().union(*[set(t["lines"]) for t in tests if not t["passed"]])
        passed = set().union(*[set(t["lines"]) for t in tests if t["passed"]])
        g = gt[p][0]
        if not fail or not fail <= passed or g not in fail or guesses[p] not in fail:
            continue
        lo, hi = function_window(sources[p], g)
        span = hi - lo + 1
        if (span > max_span or span < 6 or not lo <= guesses[p] <= hi or sources[p][g - 1].lstrip().startswith("def ")
                or (best and span >= best[0])):
            continue
        rows = sources[p]
        best = (span, {"program": p, "gt_line": g, "guess_line": guesses[p],
                       "code_lines": [{"no": i, "text": rows[i - 1]} for i in range(lo, hi + 1)],
                       "tests": [{"id": t["id"].split("::")[-1], "passed": t["passed"],
                                  "lines": sorted(set(t["lines"]) & set(range(lo, hi + 1)))} for t in tests]})
    if best is None:
        raise SystemExit("no SBFL-blind example within the span limit")
    return best[1]


EXAMPLE_PROGRAMS = ("votes_apportion", "blend_orders")


def _anchor_line(c: dict):
    a = c.get("instrument", {}).get("anchor", {})
    return a.get("line") or a.get("if_line")


def semloc_example(run_dir: Path, program: str, failloc_rank: list[int]) -> dict:
    """One running example: the program window, SemLoc's constraints with their violation counts and Ochiai, the
    per-line scores split into spectrum and bonus, the counterfactual results, and FailLoc's prompt and answer."""
    from flx._semloc import SEMLOC_ROOT
    from flx.coverage import load
    from flx.direct_cov import build_prompt, failing_tests
    from flx.gt import load_variants
    sys.path.insert(0, str(SEMLOC_ROOT / "src"))
    from spectrum import _GRANULARITY_WEIGHT as region_weight  # SemLoc's own weights, not a copy
    sc = json.loads((run_dir / "scores" / f"{program}.json").read_text())
    cons = json.loads((run_dir / "constraints" / f"{program}.json").read_text())
    cf = run_dir / "refined_base_cf" / f"{program}.json"
    labels = load_variants()["repaired"][program]
    status = next((v["status"] for v in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
                   if v["program"] == program), "unverified")
    prog = SEMLOC_ROOT / "benchmark" / "programs" / f"{program}.py"
    test = SEMLOC_ROOT / "benchmark" / "testcases" / f"test_{program}.py"
    src = prog.read_text()
    rows = src.splitlines()
    lo, hi = function_window(rows, labels[0])
    cov = load(ROOT / "data" / "coverage" / "semfault" / f"{program}.json")
    n_fail = sum(1 for t in cov["tests"] if not t["passed"])
    return {
        "program": program, "label_lines": labels, "label_status": status,
        "code_lines": [{"no": i, "text": rows[i - 1]} for i in range(lo, hi + 1)],
        "guess_line": sc.get("fault_line_pred"),
        "constraints": [{"id": c["id"], "category": c.get("category"), "region": c["instrument"]["region"],
                         "anchor_line": _anchor_line(c), "expr": c["spec"]["expr"], "intent": c.get("intent", ""),
                         "weight": region_weight.get(c["instrument"]["region"], 1.0),
                         **{k: sc["constraint_scores"].get(c["id"], {}).get(k, 0) for k in ("ef", "ep")},
                         "ochiai": round(sc["constraint_scores"].get(c["id"], {}).get("ochiai", 0.0), 4)}
                        for c in cons["constraints"]],
        "line_scores": [{"line": r["line"], "spectrum": r["spectrum"], "bonus": r["bonus"], "rank": r["rank"]}
                        for r in sorted(line_scores_one(run_dir / "scores" / f"{program}.json"), key=lambda r: r["rank"])],
        "cf_results": [{"cid": r["cid"], "patch": r["patch"]} for r in (json.loads(cf.read_text()) if cf.exists() else [])],
        "failloc_top5": failloc_rank,
        "failloc_prompt": build_prompt(src, failing_tests(src, prog, test), cov, coverage=False),
        "n_fail": n_fail, "n_pass": len(cov["tests"]) - n_fail,
    }


COV_EXAMPLE = "combine_responses"  # running example 2: the faulty line is run by failing tests only


def cov_example(program: str) -> dict:
    """Running example 2 for the FailLoc+Cov flow page: the function window around the label with each line's
    [f/p] coverage counts, FailLoc's and FailLoc+Cov's top 5 in the three Gemini test runs, and the Cov prompt."""
    from flx._semloc import SEMLOC_ROOT
    from flx.coverage import load
    from flx.direct_cov import build_prompt, failing_tests
    from flx.gt import load_variants
    from flx.sbfl import counts
    variants = load_variants()
    labels = variants["repaired"][program]
    prog = SEMLOC_ROOT / "benchmark" / "programs" / f"{program}.py"
    test = SEMLOC_ROOT / "benchmark" / "testcases" / f"test_{program}.py"
    src = prog.read_text()
    rows = src.splitlines()
    lo, hi = function_window(rows, labels[0])
    cov = load(ROOT / "data" / "coverage" / "semfault" / f"{program}.json")
    ef, ep, _ = counts(cov)
    n_fail = sum(1 for t in cov["tests"] if not t["passed"])
    top5 = lambda kind: [json.loads((ROOT / "data" / "rankings" / f"{kind}_test_gemini_r{r}.json").read_text())[program][:5]
                         for r in (1, 2, 3)]
    return {
        "program": program, "label_lines": labels, "reviewed_lines": sorted(variants["reviewed"][program]),
        "code_lines": [{"no": i, "text": rows[i - 1]} for i in range(lo, hi + 1)],
        "fp": {str(i): [ef.get(i, 0), ep.get(i, 0)] for i in range(lo, hi + 1)},
        "n_fail": n_fail, "n_pass": len(cov["tests"]) - n_fail,
        "failloc_top5": top5("direct_tests"), "cov_top5": top5("direct_cov"),
        "cov_prompt": build_prompt(src, failing_tests(src, prog, test), cov, coverage=True),
    }


def line_scores_one(path: Path) -> list[dict]:
    d = path.parent
    return [r for r in line_scores(d) if r["program"] == path.stem]


def examples() -> dict:
    run_dir = ROOT / "runs" / RUNS[0]
    ranks = json.loads((ROOT / "data" / "rankings" / "direct_tests_test_gemini_r1.json").read_text())
    return {p: semloc_example(run_dir, p, ranks[p]) for p in EXAMPLE_PROGRAMS}


def main() -> None:
    from flx.gt import SEMLOC_ROOT, load_variants
    rows = []
    for run in RUNS:
        d = ROOT / "runs" / run / "scores"
        if not d.exists():
            raise SystemExit(f"missing {d}")
        rows += [{"run": run, **r} for r in line_scores(d)]
    gt = load_variants()["repaired"]
    with open(ROOT / "data" / "semloc_line_scores.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, ["run", "program", "line", "spectrum", "bonus", "score", "rank", "is_guess", "is_gt_repaired"])
        w.writeheader()
        for r in rows:
            w.writerow({**r, "is_guess": int(r["is_guess"]), "is_gt_repaired": int(r["line"] in gt.get(r["program"], []))})
    guesses = {r["program"]: r["line"] for r in rows if r["run"] == RUNS[0] and r["is_guess"]}
    sources = {p: (SEMLOC_ROOT / "benchmark" / "programs" / f"{p}.py").read_text().splitlines() for p in guesses}
    ex = pick_example(ROOT / "data" / "coverage" / "semfault", gt, guesses, sources)
    (ROOT / "data" / "fig_example.json").write_text(json.dumps(ex, ensure_ascii=False, indent=1) + "\n")
    (ROOT / "data" / "fig_semloc_examples.json").write_text(json.dumps(examples(), ensure_ascii=False, indent=1) + "\n")
    (ROOT / "data" / "fig_cov_example.json").write_text(json.dumps(cov_example(COV_EXAMPLE), ensure_ascii=False, indent=1) + "\n")
    print(f"{len(rows)} line scores; example {ex['program']} ({len(ex['code_lines'])} lines); fig_semloc_examples.json")


if __name__ == "__main__":
    main()

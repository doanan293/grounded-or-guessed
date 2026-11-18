"""Derived data for the figures (no LLM calls, no re-runs).

data/semloc_line_scores.csv  per-line SemLoc scores of the three Gemini test runs, split into the semantic-spectrum
                             part and the +1.2 bonus SemLoc's released code adds on the LLM-guessed line.
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
    print(f"{len(rows)} line scores; example {ex['program']} ({len(ex['code_lines'])} lines)")


if __name__ == "__main__":
    main()

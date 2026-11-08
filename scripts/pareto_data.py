"""Cost/accuracy points for the Pareto figure → data/pareto.csv.

    python scripts/pareto_data.py
All methods on the same programs: the fixed 50-program test subset (data/subset50.json), repaired ground
truth. Accuracy = mean over finished, healthy repeats; cost = mean LLM tokens (prompt + completion) per
program over the same configuration's runs (data/llm_cost.csv; per-program cost of the test-split runs is
used for methods only run on the full test split).
"""
import csv
import importlib.util
import json
from pathlib import Path
from statistics import mean

from flx.gt import load_variants
from flx.ranking import metrics

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rq3_families", ROOT / "scripts" / "rq3_families.py")
fam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fam)

LIST_METHODS = [("LLM direct", "direct_test_gemini_r", "Gemini 3.8 Flash"),
                ("LLM + coverage", "direct_cov_test_gemini_r", "Gemini 3.8 Flash"),
                ("LLM + coverage", "direct_cov_sub50_luna_r", "GPT-6 luna"),
                ("LLM + coverage", "direct_cov_sub50_claude55_r", "Claude Sonnet 5.5"),
                ("LLM + coverage", "direct_cov_sub50_gptoss_r", "gpt-oss-120b"),
                ("LLM + coverage", "direct_cov_sub50_flashlite_r", "Gemini 3.5 Flash-Lite")]


def _cost_rows() -> list[dict]:
    with open(ROOT / "data" / "llm_cost.csv") as f:
        return list(csv.DictReader(f))


def tokens(run_ids: list[str]) -> float:
    """Mean tokens per program over exactly the runs whose accuracy is plotted."""
    rows = [r for r in _cost_rows() if r["run_id"] in set(run_ids)]
    return round(mean(float(r["tokens_per_program"]) for r in rows)) if rows else 0.0


def complete_runs(rankings: Path, prefix: str, programs: list[str]) -> list[Path]:
    """Single-prompt runs (one JSON per repeat) that produced a ranking for every program of their split."""
    files = sorted(f for f in rankings.glob(f"{prefix}*.json"))
    return [f for f in files if set(programs) <= set(json.loads(f.read_text()))]


def main() -> None:
    gt = load_variants()["repaired"]
    progs = [p for p in json.loads((ROOT / "data" / "subset50.json").read_text())["programs"] if p in gt]
    params = fam.chosen_params("repaired")
    out = []

    def add(method, model, ms, tok):
        out.append({"method": method, "model": model, "n": len(progs), "repeats": len(ms),
                    "acc1": round(mean(m["acc1"] for m in ms), 4), "acc3": round(mean(m["acc3"] for m in ms), 4),
                    "tokens_per_program": tok})

    for label, prefix, _ in fam.FAMILIES:
        runs = fam.usable_runs(ROOT / "runs", prefix)
        if not runs:
            continue
        tok = tokens([r.name for r in runs])
        for method, name in (("semloc", "SemLoc"), ("covgate", "CovGate")):
            add(name, label, [metrics(fam.run_ranks(r, gt, progs, method, params), progs) for r in runs], tok)
    split = json.loads((ROOT / "data" / "split.json").read_text())
    sub50 = json.loads((ROOT / "data" / "subset50.json").read_text())["programs"]
    for name, prefix, model in LIST_METHODS:
        files = complete_runs(ROOT / "data" / "rankings", prefix, split["test"] if "_test_" in prefix else sub50)
        ms = []
        for f in files:
            preds = json.loads(f.read_text())
            ranks = {p: next((k + 1.0 for k, ln in enumerate(preds.get(p, [])) if ln in gt[p]), None) for p in progs}
            ms.append(metrics(ranks, progs))
        if ms:
            add(name, model, ms, tokens([f.stem for f in files]))
    from flx.coverage import load
    from flx.ranking import rank_of
    from flx.sbfl import sbfl_scores
    sb = {p: rank_of(sbfl_scores(load(ROOT / "data" / "coverage" / "semfault" / f"{p}.json"), "ochiai"), gt[p]) for p in progs}
    add("SBFL Ochiai", "-", [metrics(sb, progs)], 0)
    with open(ROOT / "data" / "pareto.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for r in out:
        print(r)


if __name__ == "__main__":
    main()

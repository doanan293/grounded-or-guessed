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


def tokens(prefix: str) -> float:
    rows = [r for r in csv.DictReader(open(ROOT / "data" / "llm_cost.csv")) if r["run_id"].startswith(prefix)]
    return round(mean(float(r["tokens_per_program"]) for r in rows)) if rows else 0.0


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
        tok = tokens(prefix + "_r")
        for method, name in (("semloc", "SemLoc"), ("covgate", "CovGate")):
            add(name, label, [metrics(fam.run_ranks(r, gt, progs, method, params), progs) for r in runs], tok)
    for name, prefix, model in LIST_METHODS:
        files = sorted(f for f in (ROOT / "data" / "rankings").glob("*.json") if f.name.startswith(prefix))
        ms = []
        for f in files:
            preds = json.loads(f.read_text())
            ranks = {p: next((k + 1.0 for k, ln in enumerate(preds.get(p, [])) if ln in gt[p]), None) for p in progs}
            ms.append(metrics(ranks, progs))
        if ms:
            add(name, model, ms, tokens(prefix))
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

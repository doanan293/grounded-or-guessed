"""RQ3c: SemLoc across model families on the fixed 50-program test subset (3 repeats each, provider-default
reasoning), original and repaired ground truth.

    python scripts/rq3_families.py --out data/rq3_families.csv
"""
import argparse
import csv
import json
from pathlib import Path
from statistics import mean, stdev

from flx.coverage import load as load_cov
from flx.covgate import covgate_scores
from flx.gt import load_variants
from flx.ranking import metrics, rank_of

ROOT = Path(__file__).resolve().parents[1]
COV = ROOT / "data" / "coverage" / "semfault"
FAMILIES = [  # (label, run prefix, served model id)
    ("Gemini 3.8 Flash", "semloc_test_gemini", "gemini-3.8-flash-n"),
    ("GPT-6 luna", "semloc_sub50_luna", "gpt-6-luna"),
    ("Claude Sonnet 5.5", "semloc_sub50_claude55", "claude-sonnet-5-5"),
    ("gpt-oss-120b", "semloc_sub50_gptoss", "gpt-oss-120b-medium"),
    ("Gemini 3.5 Flash-Lite", "semloc_sub50_flashlite", "gemini-3.5-flash-lite"),
]


def is_healthy(run: Path) -> bool:
    from flx.run_health import health
    return health(run, run.name, ROOT / "runs" / "llm_log.jsonl")["healthy"]


def usable_runs(runs_root: Path, prefix: str) -> list[Path]:
    """Finished repeats (summary written) that passed flx.run_health; partial or unhealthy runs never enter a table."""
    cands = [runs_root / f"{prefix}_r{i}" for i in (1, 2, 3)]
    return [r for r in cands if (r / "results_cf_base" / "summary.json").exists() and is_healthy(r)]  # finished + healthy


METHODS = ("semloc", "semloc_no_prior", "covgate")


def run_ranks(run: Path, gt: dict, progs: list[str], method: str = "semloc", params: dict | None = None) -> dict:
    """semloc: SemLoc's scores as produced; semloc_no_prior: without the +1.2 on the LLM's guess;
    covgate: CovGate with `params` (gate, lam, no_prior) chosen on dev; llm_guess: the LLM's fault_line alone."""
    opts = {"semloc": {"gate": False, "lam": 0.0, "no_prior": False},
            "semloc_no_prior": {"gate": False, "lam": 0.0, "no_prior": True}}.get(method, params)
    out = {}
    for p in progs:
        f = run / "scores" / f"{p}.json"
        if f.exists():
            sem = json.loads(f.read_text())
            if method == "llm_guess":
                fp = sem.get("fault_line_pred")
                out[p] = rank_of({fp: 1.0} if isinstance(fp, int) else {}, gt[p])
                continue
            out[p] = rank_of(covgate_scores(sem, load_cov(COV / f"{p}.json"), **opts), gt[p])
    return out


def chosen_params(gname: str) -> dict:
    for r in csv.DictReader(open(ROOT / "data" / "rq_gt_sensitivity.csv")):
        if r["gt"] == gname and r["variant"] == "covgate" and r["config"] == "semloc_gemini_T0.8":
            return {k: v for k, v in json.loads(r["params"]).items() if k in ("gate", "lam", "no_prior")}
    raise KeyError(gname)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "rq3_families.csv")
    args = ap.parse_args()
    sub = json.loads((ROOT / "data" / "subset50.json").read_text())["programs"]
    rows = []
    for gname, gt in load_variants().items():
        if gname == "verified_strict":
            continue
        progs = [p for p in sub if p in gt]
        params = chosen_params(gname)
        for label, prefix, model in FAMILIES:
            runs = usable_runs(ROOT / "runs", prefix)
            for method in METHODS:
                ms = [metrics(run_ranks(r, gt, progs, method, params), progs) for r in runs]
                if not ms:
                    continue
                row = {"gt": gname, "family": label, "model": model, "method": method, "n": len(progs),
                       "repeats": len(ms)}
                for k in ("acc1", "acc3", "acc5"):
                    vals = [m[k] for m in ms]
                    row[f"{k}_mean"] = round(mean(vals), 4)
                    row[f"{k}_sd"] = round(stdev(vals), 4) if len(vals) > 1 else 0.0
                rows.append(row)
                print(row)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    main()

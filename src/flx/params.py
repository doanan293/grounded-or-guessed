"""The CovGate parameters chosen on dev (scripts/gt_sensitivity.py → data/rq_gt_sensitivity.csv) — one reader
for every script, so no knob (e.g. grounded_prior) is ever dropped on the way to a test-set evaluation."""
import csv
import json
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[2] / "data" / "rq_gt_sensitivity.csv"
KNOBS = ("gate", "lam", "no_prior", "grounded_prior")


def chosen_params(gt_name: str, config: str = "semloc_gemini_T0.8", path: Path = DEFAULT) -> dict:
    with open(path) as f:
        for r in csv.DictReader(f):
            if r["gt"] == gt_name and r["config"] == config and r["variant"] == "covgate":
                prm = json.loads(r["params"])
                return {k: prm.get(k, False) for k in KNOBS}
    raise KeyError(f"no dev-chosen CovGate parameters for gt={gt_name!r}, config={config!r}")

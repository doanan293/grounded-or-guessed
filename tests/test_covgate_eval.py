import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("covgate_eval", ROOT / "scripts" / "covgate_eval.py")
ce = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ce)


def test_tune_uses_only_dev():
    dev, test = ["d1", "d2"], ["t1", "t2", "t3"]
    grid = [{"lam": 0.0}, {"lam": 0.5}]

    def rank_fn(params, prog):
        if prog.startswith("d"):
            return 1.0 if params["lam"] == 0.0 else 9.0   # dev prefers lam=0
        return 1.0 if params["lam"] == 0.5 else 9.0       # test would prefer lam=0.5 ("poison")

    assert ce.tune(dev, grid, rank_fn) == {"lam": 0.0}

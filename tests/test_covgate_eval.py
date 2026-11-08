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


def test_tune_pools_configs_and_ignores_test():
    """Production path: parameters chosen by pooled (Acc@3, Acc@1) over several configs, on dev only."""
    dev, test = ["d1", "d2"], ["t1"]
    grid = [{"lam": 0.0}, {"lam": 0.5}]
    good_dev = lambda prm, p: (1.0 if prm["lam"] == 0.0 else 9.0) if p.startswith("d") else (1.0 if prm["lam"] else 9.0)
    neutral = lambda prm, p: 1.0
    assert ce.tune(dev, grid, [good_dev, neutral]) == {"lam": 0.0}


def test_both_tuning_scripts_route_through_tune():
    """covgate_eval.main and gt_sensitivity.main must pick parameters only via tune(dev, ...)."""
    import re
    for script in ("covgate_eval.py", "gt_sensitivity.py"):
        src = (ROOT / "scripts" / script).read_text()
        assert not re.search(r"max\(\s*(ce\.)?GRID", src), script
        assert re.search(r"tune\(\s*(split\[\"dev\"\]|dev|dev_exec)\b", src), script

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rq2_ours", ROOT / "scripts" / "rq2_ours.py")
rq2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rq2)


def test_ranks_from_list():
    assert rq2.ranks_from_list({"a": [5, 7, 9], "b": [1]}, {"a": [7], "b": [2]}, ["a", "b", "c"]) == {"a": 2.0, "b": None, "c": None}


def test_mean_sd():
    assert rq2.mean_sd([0.4, 0.5, 0.6]) == (0.5, 0.1)

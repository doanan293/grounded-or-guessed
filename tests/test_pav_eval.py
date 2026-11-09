import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pav_eval", ROOT / "scripts" / "pav_eval.py")
pe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pe)


def test_rankings_stage1_and_reranked():
    run = {"p": {"stage1": [7, 4, 9], "checks": {"7": [[False, None]], "4": [[True, 1]], "9": [[False, None]]}}}
    assert pe.rankings(run, None) == {"p": [7, 4, 9]}
    assert pe.rankings(run, {"k": 3, "attempts": 1, "order": "llm", "max_size": None}) == {"p": [4, 7, 9]}


def test_acc_averages_repeats_and_accepts_any_gt_line():
    gt = {"a": [4], "b": [2, 3]}
    ranks = [{"a": [4], "b": [1, 3]}, {"a": [1, 4], "b": [9]}]
    assert pe.acc(ranks, gt, ["a", "b"], 1) == 0.25
    assert pe.acc(ranks, gt, ["a", "b"], 3) == 0.75

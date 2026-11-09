import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ablation_coverage", ROOT / "scripts" / "ablation_coverage.py")
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)


def test_compare_pairs_repeats_and_programs():
    gt = {"a": [3], "b": [5], "c": [9]}
    cov = [{"a": [3], "b": [5, 1], "c": [1]}, {"a": [3], "b": [1, 2, 5], "c": [9]}]
    tests = [{"a": [1, 3], "b": [1], "c": [1]}, {"a": [3], "b": [1], "c": [1]}]
    row = ab.compare(cov, tests, gt, ["a", "b", "c"], clusters=None, k_boot=200)
    # Acc@1 per-program means over repeats: cov a 1, b .5 (rep 1 only), c .5 → 2/3; tests a .5, b 0, c 0 → 1/6
    assert round(row["a_acc1"], 4) == round(2 / 3, 4) and round(row["b_acc1"], 4) == round(1 / 6, 4)
    assert round(row["d_acc1"], 4) == 0.5
    # Acc@3: cov a 1, b (rep1 rank2, rep2 rank3) 1, c .5 → 2.5/3; tests a 1, b 0, c 0 → 1/3
    assert round(row["d_acc3"], 4) == 0.5
    assert row["d_acc3_lo"] <= row["d_acc3"] <= row["d_acc3_hi"]
    assert row["n"] == 3 and row["repeats"] == 2

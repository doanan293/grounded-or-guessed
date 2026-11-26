import csv
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("figure_data", ROOT / "scripts" / "figure_data.py")
fd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fd)


def test_bonus_split_from_score():
    rows = {r["line"]: r for r in fd.line_scores(ROOT / "tests" / "fixtures" / "semloc_scores")}
    r = rows[67]
    assert r["bonus"] == 1.2 and abs(r["spectrum"] - 0.408) < 1e-3 and r["rank"] == 1 and r["is_guess"]
    assert rows[64]["bonus"] == 0.0 and rows[64]["rank"] == 2


CSV = ROOT / "data" / "semloc_line_scores.csv"


@pytest.mark.skipif(not CSV.exists(), reason="derived data not built")
def test_guess_always_rank1_and_spectrum_at_most_one():
    rows = list(csv.DictReader(open(CSV)))
    assert rows
    assert all(float(r["spectrum"]) <= 1.0 + 1e-9 for r in rows)
    assert all(r["rank"] == "1" for r in rows if r["is_guess"] == "1")


EX = ROOT / "data" / "fig_example.json"


@pytest.mark.skipif(not EX.exists(), reason="derived data not built")
def test_example_is_blind_for_sbfl():
    ex = json.loads(EX.read_text())
    fail = set().union(*(t["lines"] for t in ex["tests"] if not t["passed"]))
    passed = set().union(*(t["lines"] for t in ex["tests"] if t["passed"]))
    assert fail and fail <= passed
    assert ex["gt_line"] in fail
    assert 0 < len(ex["code_lines"]) <= 24


EXAMPLES = ROOT / "data" / "fig_semloc_examples.json"


@pytest.mark.skipif(not (ROOT / "runs" / "semloc_test_gemini_r1").exists(), reason="runs/ not present")
def test_examples_match_runs():
    ex = fd.examples()
    va, bo = ex["votes_apportion"], ex["blend_orders"]
    assert len(va["constraints"]) == 4 and all(c["ochiai"] == 0 for c in va["constraints"])
    assert va["line_scores"] == [{"line": 26, "spectrum": 0.0, "bonus": 1.2, "rank": 1}]
    assert va["guess_line"] == 26 and va["failloc_top5"] == [29, 25, 26, 28, 30]
    assert va["label_lines"] == [29] and va["label_status"] == "unverified"
    assert va["n_fail"] == 1 and va["n_pass"] == 4 and va["cf_results"] == []
    sc = {r["line"]: r for r in bo["line_scores"]}
    assert sc[72]["spectrum"] == 1.0 and abs(sc[73]["spectrum"] - 0.6) < 0.01 and sc[73]["bonus"] == 1.2
    assert sc[73]["rank"] == 1 and bo["guess_line"] == 73
    w = {c["id"]: c["weight"] for c in bo["constraints"]}
    assert w["C1"] == 0.6 and w["C2"] == 1.0  # SemLoc down-weights a constraint pinned to one line
    assert bo["failloc_top5"][0] == 72 and bo["label_status"] == "confirmed"
    assert "exactly one faulty line" in va["failloc_prompt"] and "test_truncation_sum_equals_total_fail" in va["failloc_prompt"]
    assert "[f=" not in va["failloc_prompt"]  # FailLoc: no coverage annotations


def test_cov_example_matches_rankings():
    """Running example 2 (FailLoc+Cov flow page): line 72 is run only by failing tests, and coverage lifts it
    from rank 2 (FailLoc) to rank 1 (FailLoc+Cov) in all three Gemini test runs."""
    ex = json.loads((ROOT / "data" / "fig_cov_example.json").read_text())
    assert ex["program"] == "combine_responses"
    assert ex["label_lines"] == [72] and ex["reviewed_lines"] == [71, 72]
    assert ex["fp"]["72"] == [ex["n_fail"], 0] and ex["fp"]["71"][1] > 0
    assert {r["no"] for r in ex["code_lines"]} >= {71, 72}
    for r in range(3):
        fl = json.loads((ROOT / f"data/rankings/direct_tests_test_gemini_r{r + 1}.json").read_text())["combine_responses"]
        cv = json.loads((ROOT / f"data/rankings/direct_cov_test_gemini_r{r + 1}.json").read_text())["combine_responses"]
        assert ex["failloc_top5"][r] == fl[:5] and ex["cov_top5"][r] == cv[:5]
        assert cv.index(72) < fl.index(72)
    assert "f=4/p=0" in ex["cov_prompt"].replace(" ", "")

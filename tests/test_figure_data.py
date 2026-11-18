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

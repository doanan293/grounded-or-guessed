import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("static_tools", ROOT / "scripts" / "static_tools.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)


def test_parse_ruff_and_pyrefly():
    ruff = [{"filename": "/x/programs/a.py", "location": {"row": 5}, "code": "E701"},
            {"filename": "/x/programs/b.py", "location": {"row": 9}, "code": "SIM108"}]
    py = {"errors": [{"path": "a.py", "line": 7, "name": "bad-return"}]}
    assert st.parse_ruff(ruff) == {"a": [(5, "E701")], "b": [(9, "SIM108")]}
    assert st.parse_pyrefly(py) == {"a": [(7, "bad-return")]}


def test_score_exact_and_near():
    diags = {"a": [(5, "E701"), (40, "X")], "b": [(12, "Y")], "c": []}
    gt = {"a": [5], "b": [9, 10], "c": [3], "d": [1]}
    row = st.score(diags, gt)
    assert row["programs"] == 4 and row["flagged"] == 2 and row["diagnostics"] == 3
    assert row["on_fault_line"] == 1          # a
    assert row["within_2_lines"] == 2         # a, and b (12 is 2 below 10)
    assert row["mean_per_program"] == 0.75


def test_score_chance_baseline():
    row = st.score({"a": [(1, "X"), (2, "Y")]}, {"a": [5]}, {"a": 10})
    assert row["on_fault_line_by_chance"] == 0.2

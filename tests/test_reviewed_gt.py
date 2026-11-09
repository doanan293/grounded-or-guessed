import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_reviewed_gt", ROOT / "scripts" / "build_reviewed_gt.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def test_answer_lines_letters_combinations_and_numbers():
    row = {"G": "61", "S": "79;83", "F": "62"}
    assert b.answer_lines("F", row) == [62]
    assert b.answer_lines("G+F", row) == [61, 62]
    assert b.answer_lines("S", row) == [79, 83]
    assert b.answer_lines(" 71 ", row) == [71]
    assert b.answer_lines("g + 70", row) == [61, 70]


def test_answer_lines_rejects_unknown_or_empty():
    import pytest
    for bad in ("", "?", "S", "X"):
        with pytest.raises(ValueError):
            b.answer_lines(bad, {"G": "61", "S": "", "F": ""})


def test_reviewed_label_precedence():
    """Override > human answer > LLM 'either' (both lines) > original label."""
    orig = {"a": [5], "b": [7], "c": [9], "d": [3]}
    human = {"b": [8]}
    llm = {"c": {"verdict": "either", "fault_line": 10}, "d": {"verdict": "label", "fault_line": 3}}
    over = {"a": ([4, 6], "two-line fix verified")}
    out = b.reviewed(orig, human, llm, over)
    assert out["a"] == {"lines": [4, 6], "source": "override", "note": "two-line fix verified"}
    assert out["b"]["lines"] == [8] and out["b"]["source"] == "human"
    assert out["c"]["lines"] == [9, 10] and out["c"]["source"] == "llm_either"
    assert out["d"]["lines"] == [3] and out["d"]["source"] == "llm_label"

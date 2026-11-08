from flx.direct_cov import build_prompt, parse_ranking

COV = {"program": "prog", "tests": [
    {"id": "t::test_a", "passed": True, "lines": [2, 3, 5, 7]},
    {"id": "t::test_b", "passed": True, "lines": [2, 3, 5, 7]},
    {"id": "t::test_c", "passed": False, "lines": [2, 3, 5, 7]},
    {"id": "t::test_d", "passed": False, "lines": [2, 3, 4]}]}
SRC = "def f(x):\n    y = x * 2\n    if x > 100:\n        return y\n    if x < -100:\n        return -1\n    return y - 1 if x == 3 else y\n"


def test_prompt_annotates_coverage():
    p = build_prompt(SRC, [{"name": "test_c", "error": "assert 5 == 6"}], COV)
    assert "7:     return y - 1 if x == 3 else y   [f=1/p=2]" in p
    assert "6:         return -1   [f=0/p=0]" in p
    assert "test_c" in p and "assert 5 == 6" in p


def test_parse_ranking_tolerates_fences():
    assert parse_ranking('```json\n{"lines": [7, 4, 3]}\n```') == [7, 4, 3]


def test_parse_ranking_bad_json_empty():
    assert parse_ranking("line 7 is wrong") == []
    assert parse_ranking('{"lines": "seven"}') == []

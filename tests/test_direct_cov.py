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


def test_prompt_first_line_offsets_numbering():
    """BugsInPy target functions keep their absolute line numbers; the default keeps SemFault prompts (and cache) intact."""
    cov = {"program": "b", "tests": [{"id": "t.f", "passed": False, "lines": [41]},
                                      {"id": "t.p", "passed": True, "lines": [40, 41]}]}
    p = build_prompt("def f(x):\n    return x + 1\n", [{"name": "t.f", "error": ""}], cov, first_line=40)
    assert "40: def f(x):   [f=0/p=1]" in p and "41:     return x + 1   [f=1/p=1]" in p
    assert build_prompt(SRC, [], COV) == build_prompt(SRC, [], COV, first_line=1)
    assert "1: def f(x):" in build_prompt(SRC, [], COV)


def test_parse_failed_keeps_declared_only():
    from flx.direct_cov import parse_failed
    out = ("FAILED test/test_utils.py::TestUtil::test_parse_iso8601 - AssertionError: 1 != 2\n"
           "FAILED test/test_utils.py::TestUtil::test_compat_getenv - KeyError: 'HOME'\n")
    got = parse_failed(out, {"test.test_utils.TestUtil.test_parse_iso8601"})
    assert got == [{"name": "test.test_utils.TestUtil.test_parse_iso8601", "error": "AssertionError: 1 != 2"}]

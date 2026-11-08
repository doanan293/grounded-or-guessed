from flx.bip_run import enclosing_function, matrix_from_contexts

SRC = '''import re


def urljoin(base, path):
    if not path:
        return None
    return base + path


class Box:
    def size(self):
        return 3
'''


def test_enclosing_function_plain_and_method():
    assert enclosing_function(SRC, "youtube_dl/utils.py", 6) == ("youtube_dl.utils.urljoin", 4, 7)
    assert enclosing_function(SRC, "youtube_dl/utils.py", 12) == ("youtube_dl.utils.Box.size", 11, 12)
    assert enclosing_function(SRC, "youtube_dl/utils.py", 1) is None


def test_matrix_from_contexts_maps_junit_outcomes():
    contexts = {"5": ["test.test_utils.TestUtil.test_a|run", "test.test_utils.TestUtil.test_b|run"],
                "6": ["test.test_utils.TestUtil.test_b|run"], "9": ["test.test_utils.TestUtil.test_a|run"]}
    outcomes = {"test.test_utils.TestUtil.test_a": True, "test.test_utils.TestUtil.test_b": False}
    m = matrix_from_contexts("bug", contexts, outcomes, lines=range(4, 8))
    by = {t["id"]: t for t in m["tests"]}
    assert by["test.test_utils.TestUtil.test_b"] == {"id": "test.test_utils.TestUtil.test_b", "passed": False, "lines": [5, 6]}
    assert by["test.test_utils.TestUtil.test_a"]["lines"] == [5]   # line 9 is outside the function

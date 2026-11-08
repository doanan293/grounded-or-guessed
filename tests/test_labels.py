from pathlib import Path

import pytest

from flx.labels import Label, label_program

MINI = Path(__file__).parent / "fixtures" / "mini"
SRC, TEST = MINI / "programs" / "prog.py", MINI / "testcases" / "test_prog.py"
SEMANTIC_LINE, ONLY_FAIL_LINE, NEVER_RUN_LINE = 7, 4, 6


@pytest.fixture(scope="module")
def label():
    return lambda lines: label_program("prog", SRC, TEST, lines)


def test_label_semantic(label):
    lab = label([SEMANTIC_LINE])
    assert isinstance(lab, Label) and lab.category == "semantic"
    assert (lab.n_pass, lab.n_fail) == (2, 2)


def test_label_coverage_revealed(label):
    assert label([ONLY_FAIL_LINE]).category == "coverage_revealed"


def test_label_not_executed(label):
    lab = label([NEVER_RUN_LINE])
    assert lab.category == "not_executed" and not lab.fault_hit_by_fail


def test_label_multi_fault_any(label):
    assert label([NEVER_RUN_LINE, SEMANTIC_LINE]).category == "semantic"


def test_label_accepts_relative_paths(monkeypatch):
    monkeypatch.chdir(MINI)
    lab = label_program("prog", Path("programs/prog.py"), Path("testcases/test_prog.py"), [SEMANTIC_LINE])
    assert lab.category == "semantic" and lab.n_fail == 2


def test_label_retries_a_test_with_empty_coverage(monkeypatch):
    """A failing test with no coverage at all is usually a 30 s timeout under load: retry it once."""
    from flx._semloc import ensure_on_path
    ensure_on_path()
    import baselines
    real = baselines._coverage_for_test
    seen = {"flaky": 0}

    def flaky(test_id, abs_src, repo_root):
        if test_id.endswith("test_c") and seen["flaky"] == 0:
            seen["flaky"] += 1
            return False, set()
        return real(test_id, abs_src, repo_root)

    monkeypatch.setattr(baselines, "_coverage_for_test", flaky)
    lab = label_program("prog", SRC, TEST, [SEMANTIC_LINE])
    assert seen["flaky"] == 1 and lab.category == "semantic" and lab.n_empty_coverage == 0

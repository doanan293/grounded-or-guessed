from flx.bip import parse_run_test


def test_parse_unittest_dotted_to_pytest_ids():
    assert parse_run_test("python -m unittest -q test.test_utils.TestUtil.test_urljoin\n") == [
        "test/test_utils.py::TestUtil::test_urljoin"]


def test_parse_pytest_lines_kept():
    txt = "pytest tests/rules/test_pip.py::test_get_new_command\npytest tests/test_x.py::TestA::test_b\n"
    assert parse_run_test(txt) == ["tests/rules/test_pip.py::test_get_new_command", "tests/test_x.py::TestA::test_b"]


def test_parse_ignores_blank_and_other_lines():
    assert parse_run_test("\n#!/bin/bash\ncd foo\n") == []


def test_source_faults_drop_test_files():
    from flx.bip import source_faults
    got = source_faults({"youtube_dl/utils.py": [10], "test/test_utils.py": [5], "tests/rules/test_x.py": [1],
                         "thefuck/rules/test_helpers.py": [3], "setup.py": [2]})
    assert got == {"youtube_dl/utils.py": [10], "thefuck/rules/test_helpers.py": [3], "setup.py": [2]}

import os
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


def test_run_semloc_purges_bytecode_and_disables_it(tmp_path, monkeypatch):
    """SemLoc's CF step patches the target file and restores it within the same second; a same-size patch
    leaves a __pycache__ entry whose header still matches, so later runs import the *patched* code
    (youtube-dl_43: the bug vanished). Each run must start without bytecode and must not write any."""
    import sys
    import types
    import flx.bip_run as br
    wt = tmp_path / "checkouts" / "bug_1"
    cache = wt / "pkg" / "__pycache__"
    cache.mkdir(parents=True)
    (cache / "mod.cpython-312.pyc").write_bytes(b"stale")
    seen = {}

    def fake_run(bug, fn, checkout, test_file, **kw):
        seen["cache_exists"] = cache.exists()
        seen["env"] = os.environ.get("PYTHONDONTWRITEBYTECODE")
        return {"best_rank": 1}

    fake = types.SimpleNamespace(run_semloc_on_bip=fake_run, install_project=None)
    monkeypatch.setitem(sys.modules, "bip_runner", fake)
    monkeypatch.setattr(br, "ensure_on_path", lambda: None)
    monkeypatch.setattr(br, "BIP", tmp_path)
    monkeypatch.setattr(br, "ROOT", tmp_path)
    monkeypatch.delenv("PYTHONDONTWRITEBYTECODE", raising=False)
    for k in ("FLX_USE_GATEWAY", "FLX_RUN_ID", "PYTHONPATH"):
        monkeypatch.setenv(k, os.environ.get(k, ""))
    monkeypatch.setattr(sys, "dont_write_bytecode", sys.dont_write_bytecode)
    br.run_semloc({"bug": "bug_1", "function": "m.f", "test_file": "t.py"}, "m", 0.8, "rid")
    assert seen == {"cache_exists": False, "env": "1"}


def test_junit_id_of_declared_test():
    from flx.bip_run import junit_id
    assert junit_id("test/test_utils.py::TestUtil::test_parse_iso8601") == "test.test_utils.TestUtil.test_parse_iso8601"


def test_matrix_drops_undeclared_failing_tests():
    """Tests that fail only because of the environment (not declared by BugsInPy) are not failing evidence."""
    ctx = {"10": ["test.t.T.test_bug|run", "test.t.T.test_env|run", "test.t.T.test_ok|run"]}
    outcomes = {"test.t.T.test_bug": False, "test.t.T.test_env": False, "test.t.T.test_ok": True}
    m = matrix_from_contexts("b", ctx, outcomes, [10], declared={"test.t.T.test_bug"})
    assert [(t["id"], t["passed"]) for t in m["tests"]] == [("test.t.T.test_bug", False), ("test.t.T.test_ok", True)]


def test_pick_target_prefers_function_run_by_declared_failing_test():
    from flx.bip_run import pick_target
    cands = [{"file": "a/npo.py", "fn_start": 10, "fn_end": 20, "function": "npo.f"},
             {"file": "a/utils.py", "fn_start": 100, "fn_end": 120, "function": "utils.g"}]
    assert pick_target(cands, {"a/utils.py": {105}})["function"] == "utils.g"
    assert pick_target(cands, {})["function"] == "npo.f"          # nothing executed: keep the old rule

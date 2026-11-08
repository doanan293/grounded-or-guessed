import json

from flx.run_health import cf_error_programs, unrecovered_errors


def _rec(key, run_id="r", error=None, cache_hit=False):
    return {"key": key, "run_id": run_id, "error": error, "cache_hit": cache_hit}


def test_error_followed_by_success_is_recovered():
    recs = [_rec("a", error="APITimeoutError"), _rec("a"), _rec("b")]
    assert unrecovered_errors(recs, "r") == []


def test_last_record_error_is_unrecovered_and_other_runs_ignored():
    recs = [_rec("a"), _rec("a", error="boom"), _rec("c", run_id="other", error="x")]
    assert unrecovered_errors(recs, "r") == ["a"]


def test_cf_error_programs(tmp_path):
    cf = tmp_path / "refined_base_cf"
    cf.mkdir()
    (cf / "p1.json").write_text(json.dumps([{"cid": "C1", "status": "Primary"}]))
    (cf / "p2.json").write_text(json.dumps([{"cid": "C1", "status": "Error"}, {"cid": "C2", "status": "Primary"}]))
    assert cf_error_programs(tmp_path) == ["p2"]

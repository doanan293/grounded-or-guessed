import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rq3_families", ROOT / "scripts" / "rq3_families.py")
rq3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rq3)


def test_family_runs_listed_in_order():
    fams = rq3.FAMILIES
    assert fams[0][0] == "Gemini 3.8 Flash" and any(name == "gpt-oss-120b" for name, *_ in fams)


def test_unhealthy_runs_are_skipped(tmp_path, monkeypatch):
    (tmp_path / "x_r1" / "scores").mkdir(parents=True)
    (tmp_path / "x_r2" / "results_cf_base").mkdir(parents=True)
    (tmp_path / "x_r2" / "results_cf_base" / "summary.json").write_text("{}")
    monkeypatch.setattr(rq3, "is_healthy", lambda run: run.name == "x_r2")
    assert [r.name for r in rq3.usable_runs(tmp_path, "x")] == ["x_r2"]


def test_unfinished_runs_are_skipped(tmp_path, monkeypatch):
    for r in ("y_r1", "y_r2"):
        (tmp_path / r / "scores").mkdir(parents=True)
    (tmp_path / "y_r1" / "results_cf_base").mkdir()
    (tmp_path / "y_r1" / "results_cf_base" / "summary.json").write_text("{}")
    monkeypatch.setattr(rq3, "is_healthy", lambda run: True)
    assert [r.name for r in rq3.usable_runs(tmp_path, "y")] == ["y_r1"]


def test_run_ranks_methods_remove_prior_and_apply_covgate(tmp_path, monkeypatch):
    import json
    (tmp_path / "scores").mkdir()
    # LLM guessed line 5 (+1.2 prior); spectrum alone prefers line 3, the true fault.
    (tmp_path / "scores" / "p.json").write_text(json.dumps({"line_scores": {"5": 1.7, "3": 1.0}, "fault_line_pred": 5}))
    cov = {"tests": [{"id": "f", "passed": False, "lines": [3]}, {"id": "ok", "passed": True, "lines": [5]}]}
    monkeypatch.setattr(rq3, "load_cov", lambda p: cov)
    gt = {"p": [3]}
    assert rq3.run_ranks(tmp_path, gt, ["p"])["p"] == 2.0
    assert rq3.run_ranks(tmp_path, gt, ["p"], "semloc_no_prior")["p"] == 1.0
    assert rq3.run_ranks(tmp_path, gt, ["p"], "covgate", {"gate": True, "lam": 0.0, "no_prior": False})["p"] == 1.0


def test_run_ranks_llm_guess_alone(tmp_path, monkeypatch):
    import json
    (tmp_path / "scores").mkdir()
    (tmp_path / "scores" / "p.json").write_text(json.dumps({"line_scores": {"5": 1.7, "3": 1.0}, "fault_line_pred": 5}))
    monkeypatch.setattr(rq3, "load_cov", lambda p: {"tests": []})
    assert rq3.run_ranks(tmp_path, {"p": [5]}, ["p"], "llm_guess")["p"] == 1.0
    assert rq3.run_ranks(tmp_path, {"p": [3]}, ["p"], "llm_guess")["p"] is None

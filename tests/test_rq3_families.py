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

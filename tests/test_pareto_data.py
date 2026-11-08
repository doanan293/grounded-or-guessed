import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pareto_data", ROOT / "scripts" / "pareto_data.py")
pd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pd)


def test_only_complete_single_prompt_runs_are_plotted(tmp_path):
    (tmp_path / "x_r1.json").write_text(json.dumps({"a": [1], "b": [2]}))
    (tmp_path / "x_r2.json").write_text(json.dumps({"a": [1]}))            # unfinished: one program missing
    (tmp_path / "y_r1.json").write_text(json.dumps({"a": [1], "b": [2]}))
    files = pd.complete_runs(tmp_path, "x_r", ["a", "b"])
    assert [f.name for f in files] == ["x_r1.json"]


def test_cost_uses_only_the_runs_that_are_plotted(tmp_path, monkeypatch):
    rows = [{"run_id": "x_r1", "tokens_per_program": "100"}, {"run_id": "x_r2", "tokens_per_program": "900"}]
    monkeypatch.setattr(pd, "_cost_rows", lambda: rows)
    assert pd.tokens(["x_r1"]) == 100

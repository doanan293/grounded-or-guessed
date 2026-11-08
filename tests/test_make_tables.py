import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("make_tables", ROOT / "scripts" / "make_tables.py")
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)


def test_pct_and_escape():
    assert mt.pct(0.428) == "42.8"
    assert mt.pct(None) == "--"
    assert mt.tex("semloc_claude_T0.8") == r"semloc\_claude\_T0.8"


def test_rq1_table_has_author_and_fair_columns():
    tex = mt.rq1_table()
    assert r"\begin{tabular}" in tex and "Author" in tex and "Fair" in tex
    assert "42.8" in tex  # SemLoc Claude T=0.8, author scoring, all 250

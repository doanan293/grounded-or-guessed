import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rq1_audit", ROOT / "scripts" / "rq1_audit.py")
rq1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rq1)


def test_rq1_audit_reproduces_author_numbers():
    rows = {(r["config"], r["scoring"], r["subset"]): r for r in rq1.audit_rows()}
    published = {r["config"]: r for r in csv.DictReader(open(ROOT / "data" / "rq1a_table.csv"))}
    for cfg in ("semloc_claude_T0.8", "semloc_gemini_T0.8", "sbfl_ochiai", "dd"):
        mine = rows[(cfg, "author", "all")]
        assert abs(float(mine["acc1"]) - float(published[cfg]["acc1"])) < 5e-5, cfg  # rq1a_table.csv is rounded to 4 decimals
        assert abs(float(mine["acc3"]) - float(published[cfg]["acc3"])) < 5e-5, cfg  # rq1a_table.csv is rounded to 4 decimals


def test_fair_scoring_uses_fixed_denominator():
    rows = {(r["config"], r["scoring"], r["subset"]): r for r in rq1.audit_rows()}
    assert rows[("semloc_gemini_T0.8", "fair", "all")]["n"] == 250
    assert rows[("semloc_gemini_T0.8", "fair", "executable")]["n"] == 185


def test_cf_does_not_change_published_ranking():
    # the artifact's Acc@k comes from scores/ranked_lines: ranks recomputed from scores equal the CSV ranks
    assert rq1.cf_identity_check("semloc_claude_T0.8") == 0

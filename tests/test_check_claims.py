import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_claims", ROOT / "scripts" / "check_claims.py")
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)


def test_claims_match_macros_with_vietnamese_formatting():
    macros = {r"\A": "49,3", r"\B": "-8,6", r"\C": "+15,4", r"\D": "42"}
    text = "Acc@1 49,3 [`\\A`], giảm −8,6 [`\\B`], tăng +15,4 [`\\C`], 42 [`\\D`]%."
    assert cc.mismatches(text, macros) == []


def test_claims_report_wrong_and_unknown():
    macros = {r"\A": "49,3"}
    bad = cc.mismatches("49,2 [`\\A`] và 1,0 [`\\Z`]", macros)
    assert (r"\A", "49,2", "49,3") in bad and (r"\Z", "1,0", None) in bad


def test_fix_rewrites_values_from_macros_keeping_typography():
    macros = {r"\A": "52,3", r"\B": "-9,1", r"\C": "+16,6"}
    text = "Acc@1 49,3 [`\\A`], giảm −8,6 [`\\B`], tăng +15,4 [`\\C`]."
    assert cc.fix(text, macros) == "Acc@1 52,3 [`\\A`], giảm −9,1 [`\\B`], tăng +16,6 [`\\C`]."

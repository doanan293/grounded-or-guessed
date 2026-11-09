import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("make_numbers", ROOT / "scripts" / "make_numbers.py")
mn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mn)


def test_macro_name_has_no_digits():
    assert mn.macro_name("rq2", "llm_coverage", "acc3") == r"\RqTwoLlmCoverageAccThree"
    assert mn.macro_name("gt", "blank", "n") == r"\GtBlankN"
    assert not any(c.isdigit() for c in mn.macro_name("rq3c", "gpt-oss-120b", "acc1"))


def test_numbers_tex_is_generated_from_csv(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("gt,method,acc1_mean,n\nrepaired,semloc,0.4930,190\noriginal,semloc,0.3683,200\n")
    specs = [(("rq2", "semloc", "acc1"), f, {"gt": "repaired", "method": "semloc"}, "acc1_mean", "pct"),
             (("rq2", "n"), f, {"gt": "repaired", "method": "semloc"}, "n", "int")]
    tex = mn.render(specs)
    assert r"\newcommand{\RqTwoSemlocAccOne}{49.3}" in tex
    assert r"\newcommand{\RqTwoN}{190}" in tex


def test_render_fails_on_ambiguous_or_missing_row(tmp_path):
    import pytest
    f = tmp_path / "x.csv"
    f.write_text("gt,method,acc1_mean\nrepaired,semloc,0.4\nrepaired,semloc,0.5\n")
    with pytest.raises(ValueError):
        mn.render([(("a",), f, {"gt": "repaired"}, "acc1_mean", "pct")])
    with pytest.raises(ValueError):
        mn.render([(("b",), f, {"gt": "none"}, "acc1_mean", "pct")])


def test_macro_name_keeps_the_sign_of_negative_keys():
    assert mn.macro_name("off", "semloc", "-1", "count") == r"\OffSemlocMinusOneCount"
    assert mn.macro_name("off", "semloc", "1", "count") == r"\OffSemlocOneCount"


def test_vietnamese_numbers_use_a_true_minus_sign():
    assert mn.fmt("-0.091", "pp", comma=True) == "−9,1"
    assert mn.fmt("-0.091", "pp") == "-9.1"

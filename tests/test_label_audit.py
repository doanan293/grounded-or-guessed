import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("label_audit", ROOT / "scripts" / "label_audit.py")
la = importlib.util.module_from_spec(spec)
spec.loader.exec_module(la)

SRC = ["def f(x):", "    y = x + 1", "", "    _log.debug('y=%s', y)", "    if y > 3:", "        y = 3", "    return y"]


def test_kind_of_each_relation():
    assert la.kind([2], [2], SRC) == "same"
    assert la.kind([5], [5, 6], SRC) == "extended"       # label kept, a second line added (two-line fault)
    assert la.kind([3], [2], SRC) == "blank"             # original label on a blank line
    assert la.kind([4], [2], SRC) == "non_code"          # log / def / comment line
    assert la.kind([5], [6], SRC) == "off_by_one"
    assert la.kind([2], [6], SRC) == "farther"


def test_non_code_detects_def_and_comment():
    assert la.kind([1], [2], SRC) == "non_code"
    assert la.kind([1], [2], ["# note", "x = 1"]) == "non_code"

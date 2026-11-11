import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("rq2_tolerant", ROOT / "scripts" / "rq2_tolerant.py")
tol = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tol)

SRC = """def f(xs, cap):
    total = 0
    for x in xs:
        if x > cap:
            total += cap
            total -= 1
        else:
            total += x
    return total
"""


def test_header_label_accepts_its_first_body_line_and_enclosing_header():
    got = tol.tolerant_gt({"p": [4]}, {"p": SRC}, strict=True)["p"]
    assert got == [3, 4, 5]  # the `if` is itself the first body line of the `for`; line 6 is not a first body line


def test_body_label_accepts_its_header():
    assert tol.tolerant_gt({"p": [5]}, {"p": SRC}, strict=True)["p"] == [4, 5]


def test_unrelated_line_is_not_added():
    assert 9 not in tol.tolerant_gt({"p": [4]}, {"p": SRC}, strict=False)["p"]


def test_blank_label_is_kept_and_not_widened():
    src = "x = 1\n\nif x:\n    y = 2\n"
    assert tol.tolerant_gt({"p": [2]}, {"p": src}, strict=False)["p"] == [2]

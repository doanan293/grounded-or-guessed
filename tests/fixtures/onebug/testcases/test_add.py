import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if getattr(pytest, "inst", False):
    from instrumented.add import add
else:
    from programs.add import add


def test_zero():
    assert add(0, 0) == 0


def test_right_zero():
    assert add(2, 0) == 2


def test_ones():
    assert add(1, 1) == 2


def test_mixed():
    assert add(2, 3) == 5

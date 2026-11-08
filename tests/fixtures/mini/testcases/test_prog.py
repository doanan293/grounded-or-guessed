import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if getattr(pytest, "inst", False):
    from instrumented.prog import f
else:
    from programs.prog import f


def test_a():
    assert f(1) == 2


def test_b():
    assert f(2) == 4


def test_c():
    assert f(3) == 6


def test_d():
    assert f(200) == 401

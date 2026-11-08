import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if getattr(pytest, "inst", False):
    from instrumented.norm import norm
else:
    from programs.norm import norm


def test_halves():
    assert norm([1, 1]) == [0.5, 0.5]


def test_zero_sum_kept():
    assert norm([0, 0]) == [0, 0]

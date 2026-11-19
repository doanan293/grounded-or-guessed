import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
if getattr(pytest, "inst", False):
    from instrumented.mean import mean
else:
    from programs.mean import mean


def test_two():
    assert mean([2, 4]) == 3


def test_three():
    assert mean([3, 3, 3]) == 3

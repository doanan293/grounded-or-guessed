import math

from flx.stats import mcnemar


def test_mcnemar_exact_small():
    # discordant pairs b=8 (only a correct), c=2 (only b correct): exact two-sided binomial p = 0.109375
    a = [True] * 8 + [False] * 2 + [True] * 5
    b = [False] * 8 + [True] * 2 + [True] * 5
    stat, p = mcnemar(a, b)
    assert math.isclose(p, 0.109375, rel_tol=1e-6)


def test_mcnemar_identical_is_one():
    assert mcnemar([True, False], [True, False])[1] == 1.0

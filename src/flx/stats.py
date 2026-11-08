"""Paired tests for per-program outcomes."""
from math import comb


def mcnemar(a: list[bool], b: list[bool]) -> tuple[float, float]:
    """McNemar test on paired correct/incorrect outcomes. Exact two-sided binomial when b+c < 25,
    otherwise the continuity-corrected chi-square approximation. Returns (statistic, p)."""
    assert len(a) == len(b)
    n01 = sum(1 for x, y in zip(a, b) if x and not y)
    n10 = sum(1 for x, y in zip(a, b) if y and not x)
    n = n01 + n10
    if n == 0:
        return 0.0, 1.0
    if n < 25:
        k = min(n01, n10)
        p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
        return float(k), p
    stat = (abs(n01 - n10) - 1) ** 2 / n
    from math import erfc, sqrt
    return stat, erfc(sqrt(stat / 2))  # chi-square(1) survival

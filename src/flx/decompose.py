"""How much of the accuracy is grounded vs guessed: exact Shapley values over pipeline components."""
from itertools import combinations
from math import factorial
from typing import Callable


def shapley(value: Callable[[frozenset], float], players: list[str]) -> dict[str, float]:
    n = len(players)
    cache: dict[frozenset, float] = {}

    def v(s):
        if s not in cache:
            cache[s] = value(s)
        return cache[s]

    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        total = 0.0
        for k in range(n):
            w = factorial(k) * factorial(n - k - 1) / factorial(n)
            for combo in combinations(others, k):
                s = frozenset(combo)
                total += w * (v(s | {p}) - v(s))
        phi[p] = total
    return phi

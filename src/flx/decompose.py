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


PRIOR = 1.2  # SemLoc's bonus on the LLM's own fault-line guess


def component_scores(sem: dict, cov: dict, on: frozenset, attribute=None, cf=None) -> dict[int, float]:
    """Line scores using only the signals in `on`:
    guess    +1.2 on the LLM's fault_line_pred (SemLoc's prior)
    spectrum SemLoc's semantic line scores without that prior
    coverage SBFL Ochiai from the per-test coverage matrix
    cf       CF re-ranking (lines of CF-kept constraints first; needs `attribute` and `cf`)."""
    from flx.covgate import CF_KEEP, CF_OFFSET
    from flx.sbfl import sbfl_scores
    scores: dict[int, float] = {}
    fp = sem.get("fault_line_pred")
    if "spectrum" in on:
        base = {int(k): float(v) for k, v in sem.get("line_scores", {}).items()}
        if isinstance(fp, int) and fp in base:
            base[fp] -= PRIOR
            if base[fp] <= 1e-12:
                del base[fp]
        scores.update(base)
    if "guess" in on and isinstance(fp, int):
        scores[fp] = scores.get(fp, 0.0) + PRIOR
    if "coverage" in on:
        for ln, v in sbfl_scores(cov, "ochiai").items():
            scores[ln] = scores.get(ln, 0.0) + v
    if "cf" in on and cf and attribute is not None and "spectrum" in on:
        kept = {r["cid"] for r in cf if r.get("status") in CF_KEEP and not r.get("pruned")}
        cs = sem.get("constraint_scores", {})
        for ln, v in attribute({c: cs[c] for c in kept if c in cs}).items():
            scores[ln] = scores.get(ln, 0.0) + CF_OFFSET + v
    return scores

"""SBFL scores from a per-test CoverageMatrix (flx.coverage). Only lines executed by at least one
failing test get a score, which is exactly the set the SemLoc artifact's SBFL baseline ranks."""
import math


def counts(cov: dict) -> tuple[dict[int, int], dict[int, int], int]:
    ef: dict[int, int] = {}
    ep: dict[int, int] = {}
    n_fail = 0
    for t in cov["tests"]:
        target = ep if t["passed"] else ef
        n_fail += not t["passed"]
        for ln in t["lines"]:
            target[ln] = target.get(ln, 0) + 1
    return ef, ep, n_fail


def sbfl_scores(cov: dict, formula: str = "ochiai") -> dict[int, float]:
    ef, ep, n_fail = counts(cov)
    out = {}
    for ln, f in ef.items():
        p = ep.get(ln, 0)
        if formula == "ochiai":
            out[ln] = f / math.sqrt(n_fail * (f + p))
        elif formula == "dstar":  # D* with * = 2 (Wong et al. 2014)
            denom = p + (n_fail - f)
            out[ln] = f ** 2 / denom if denom else float(10 ** 6)
        else:
            raise ValueError(formula)
    return out

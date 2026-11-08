"""Fault ranks with explicit tie handling, and metrics over a fixed program list.

ties="first"   — the SemLoc artifact's behaviour: stable sort by score, earlier lines win ties.
ties="average" — fair: a fault tied with others gets the mean of the tied positions.
ties="worst"   — pessimistic: the last position of the tie group.
A program absent from `ranks`, or whose fault is unranked (None), is a miss.
"""
from typing import Literal, Mapping, Optional

Ties = Literal["first", "average", "worst"]


def _rank_one(scores: Mapping[int, float], line: int, ties: Ties) -> Optional[float]:
    if line not in scores:
        return None
    if ties == "first":
        order = [ln for ln, _ in sorted(scores.items(), key=lambda kv: -kv[1])]
        return float(order.index(line) + 1)
    s = scores[line]
    higher = sum(1 for v in scores.values() if v > s)
    equal = sum(1 for v in scores.values() if v == s)
    return higher + (equal + 1) / 2 if ties == "average" else float(higher + equal)


def rank_of(scores: Mapping[int, float], faulty: list[int], ties: Ties = "average") -> Optional[float]:
    found = [r for r in (_rank_one(scores, ln, ties) for ln in faulty) if r is not None]
    return min(found) if found else None


def metrics(ranks: Mapping[str, Optional[float]], programs: list[str], ks=(1, 3, 5)) -> dict:
    vals = [ranks.get(p) for p in programs]
    n = len(programs)
    out = {"n": n, "n_ranked": sum(v is not None for v in vals)}
    for k in ks:
        out[f"acc{k}"] = sum(1 for v in vals if v is not None and v <= k) / n if n else float("nan")
    ordered = sorted(float("inf") if v is None else v for v in vals)
    med = ordered[(n - 1) // 2] if n else float("inf")  # lower median; misses sort last
    out["median_rank"] = None if med == float("inf") else med
    return out

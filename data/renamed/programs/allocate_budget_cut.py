from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 0.0
v6 = 10
v7 = 10000


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("ratios required")
    if len(v8) > v7:
        raise ValueError(f"too many participants: {len(v8)} exceeds {v7}")


def v2(v9: float) -> float:
    """"""
    return max(v4, round(v9, v6))


def allocate_budget_cut(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = v5,
) -> List[float]:
    """

















"""
    v1(v8)

    if v10 < 0:
        raise ValueError("negative amount")

    v11 = sum(v8)
    if v11 <= 0:
        raise ValueError("invalid ratios")

    v3.debug("Distributing %.2f among %d participants (fee=%.2f)", v10, len(v8), fee)

    v12: List[float] = []
    for v13 in v8:
        v12.append((v13 / v11) * v10)

    return [v2(v14 - fee) for v14 in v12]

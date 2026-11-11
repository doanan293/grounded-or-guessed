from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 500
v6 = 0.0
v7 = 10


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("ratios required")
    if len(v8) > v5:
        raise ValueError(f"too many participants (max {v5})")
    for v14, v13 in enumerate(v8):
        if not isinstance(v13, (int, float)):
            raise TypeError(f"ratio at index {v14} is not numeric")


def v2(v9: float) -> float:
    """"""
    return max(v4, round(v9, v7))


def bill_payout(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = v6,
) -> List[float]:
    """

















"""
    v1(v8)

    if v10 < 0:
        raise ValueError("negative amount")

    v11 = sum(v8)
    if v11 <= 0:
        raise ValueError("invalid ratios")

    v3.debug("Splitting %.2f among %d participants (fee=%.2f)", v10, len(v8), fee)

    v12: List[float] = []
    for v13 in v8:
        v12.append((v13 / v11) * v10)

    return [v2(v15 - fee) for v15 in v12]

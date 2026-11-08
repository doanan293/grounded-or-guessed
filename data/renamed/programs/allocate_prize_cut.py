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
    for v14, v12 in enumerate(v8):
        if v12 < 0:
            raise ValueError(
                f"Ratio at index {v14} is negative ({v12}); "
                "all ratios must be >= 0"
            )


def v2(v9: List[float]) -> List[float]:
    """"""
    return [max(v4, round(v15, v7)) for v15 in v9]


def allocate_prize_cut(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = v6,
) -> List[float]:
    """


















"""
    if not v8:
        raise ValueError("ratios required")
    if len(v8) > v5:
        raise ValueError(f"exceeds max participants ({v5})")
    if v10 < 0:
        raise ValueError("negative amount")

    v1(v8)

    v11 = sum(v8)
    if v11 <= 0:
        raise ValueError("invalid ratios")

    v3.debug("Distributing %.2f among %d participants (fee=%.2f)", v10, len(v8), fee)

    v9: List[float] = []
    for v12 in v8:
        v9.append((v12 / v11) * v10)

    v13 = [v15 - fee for v15 in v9]
    return v2(v13)

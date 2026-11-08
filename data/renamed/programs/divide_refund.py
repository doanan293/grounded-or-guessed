from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 500
v6 = 0.0
v7 = 10


def v1(v8: float, v9: Sequence[float], fee: float) -> None:
    """"""
    if not v9:
        raise ValueError("empty ratios")
    if len(v9) > v5:
        raise ValueError(f"too many participants: {len(v9)} exceeds {v5}")
    if sum(v9) <= 0:
        raise ValueError("invalid ratios")
    if v8 < 0:
        raise ValueError("negative amount")
    if fee < v6:
        raise ValueError("fee cannot be negative")


def v2(v10: List[float]) -> List[float]:
    """"""
    return [round(max(v13, v4), v7) for v13 in v10]


def divide_refund(
    v8: float,
    v9: Sequence[float],
    *,
    fee: float = v6,
) -> List[float]:
    """















"""
    v1(v8, v9, fee)

    v11 = sum(v9)
    v12 = list(map(lambda v15: (v15 / v11) * v8, v9))

    v10 = [v14 - fee for v14 in v12]

    v3.debug("Distributed %.2f across %d participants (fee=%.2f)", v8, len(v9), fee)
    return v2(v10)

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 50
v6 = 0.0
v7 = 2


def v1(v8: Sequence[float]) -> None:
    """"""
    if len(v8) == 0:
        raise ValueError("no ratios")
    if len(v8) > v5:
        raise ValueError(f"too many participants: {len(v8)} exceeds {v5}")
    if sum(v8) <= 0:
        raise ValueError("invalid ratios")


def v2(v9: float) -> float:
    """"""
    return max(v4, v9)


def rent_splitter(
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

    v3.debug("Splitting %.2f among %d participants (fee=%.2f)", v10, len(v8), fee)

    v11 = sum(v8)
    v12 = [(v14 / v11) * v10 for v14 in v8]

    v13 = [v2(v9 - fee) for v9 in v12]
    return [round(v15, v7) for v15 in v13]

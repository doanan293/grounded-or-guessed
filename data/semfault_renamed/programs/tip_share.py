from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 100
v6 = 0.0
v7 = 2


def v1(v8: Sequence[float]) -> None:
    """"""
    if len(v8) == 0:
        raise ValueError("no ratios")
    if len(v8) > v5:
        raise ValueError(f"too many recipients (max {v5})")
    if sum(v8) <= 0:
        raise ValueError("invalid ratios")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def tip_share(
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

    v3.debug("Splitting %.2f among %d recipients (fee=%.2f)", v10, len(v8), fee)

    v11 = sum(v8)
    v12 = [(v14 / v11) * v10 for v14 in v8]

    v13 = [max(v4, v2(v15 - fee)) for v15 in v12]
    return v13

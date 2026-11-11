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
        raise ValueError("empty ratios")
    if len(v8) > v5:
        raise ValueError(f"too many ratios: {len(v8)} exceeds {v5}")
    if sum(v8) <= 0:
        raise ValueError("invalid ratios")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def donation_share(
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

    v3.debug("Distributing %.2f among %d recipients (fee=%.2f)", v10, len(v8), fee)

    v11 = sum(v8)
    v12 = list(map(lambda v15: (v15 / v11) * v10, v8))

    v13 = [v2(max(v4, v14 - fee)) for v14 in v12]
    return v13

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 500
v6 = 2
v7 = 0.5


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("ratios required")
    if len(v8) > v5:
        raise ValueError(
            f"number of participants ({len(v8)}) exceeds "
            f"maximum allowed ({v5})"
        )


def v2(v9: float) -> float:
    """"""
    return round(v9, v6)


def payment_payout(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = 0.0,
) -> List[float]:
    """


















"""
    v1(v8)

    if v10 < 0:
        raise ValueError("negative amount")

    if fee > v10 * v7:
        v3.debug("Fee %.2f exceeds %.0f%% of amount %.2f", fee, v7 * 100, v10)

    v11 = sum(v8)
    if v11 <= 0:
        raise ValueError("invalid ratios")

    v12: List[float] = []
    for v13 in v8:
        v14 = (v13 / v11) * v10
        v12.append(max(v4, v2(v14)))

    return [v15 - fee for v15 in v12]

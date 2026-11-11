from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 100
v6 = 0.0
v7 = 10


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8 or sum(v8) <= 0:
        raise ValueError("invalid ratios")
    if len(v8) > v5:
        raise ValueError(
            f"too many participants: {len(v8)} exceeds limit {v5}"
        )
    for v13, v14 in enumerate(v8):
        if v14 < v4:
            raise ValueError(f"ratio at index {v13} is negative")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def payment_split_rebate(
    v10: float,
    v8: Sequence[float],
    *,
    rebate: float = v6,
) -> List[float]:
    """
















"""
    if v10 < 0:
        raise ValueError("negative total")

    v1(v8)

    v11 = sum(v8)
    v12 = [v2((v14 / v11) * v10) for v14 in v8]

    v3.debug("Computed raw shares: %s (rebate=%.4f)", v12, rebate)

    return [v15 - rebate for v15 in v12]

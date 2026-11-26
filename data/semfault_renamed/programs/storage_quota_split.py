from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 256
v6 = 1e-12
v7 = 0.0


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("invalid ratios")
    if len(v8) > v5:
        raise ValueError(
            f"participant count {len(v8)} exceeds maximum {v5}"
        )
    if any(v14 < 0 for v14 in v8):
        raise ValueError("negative ratio detected")
    if sum(v8) <= 0:
        raise ValueError("invalid ratios")


def v2(v9: List[float]) -> List[float]:
    """"""
    return [max(v4, v13) for v13 in v9]


def storage_quota_split(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = v7,
) -> List[float]:
    """
















"""
    if v10 < 0:
        raise ValueError("negative total")

    v1(v8)

    if fee < -v6:
        raise ValueError("fee must not be negative")

    v11 = sum(v8)
    v9 = [(v14 / v11) * v10 for v14 in v8]

    v3.debug("Computed raw shares for %d participants", len(v9))

    v12 = v2([v13 - fee for v13 in v9])
    return v12

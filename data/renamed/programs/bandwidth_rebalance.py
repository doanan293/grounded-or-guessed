from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 1e-12
v5 = 0.7
v6 = 0.0
v7 = 4096


def v1(v8: Sequence[float], v9: Sequence[float]) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if not v8:
        raise ValueError("empty allocation")
    if len(v8) > v7:
        raise ValueError(
            f"allocation exceeds maximum channel count of {v7}"
        )


def v2(v10: float) -> float:
    """"""
    return max(v10, v6)


def bandwidth_rebalance(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """

















"""
    v1(v8, v9)

    v3.debug("Rebalancing %d channels with damping=%.4f", len(v8), damping)

    v11: List[float] = []
    for v12 in range(len(v8)):
        v13 = v8[v12] + (v9[v12] - v8[v12]) * damping
        v11.append(v2(v13))

    return v11

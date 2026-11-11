from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.5
v6 = 1
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float], damping: float) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if len(v8) < v6:
        raise ValueError("empty weights")
    if not (0.0 <= damping <= v7):
        raise ValueError(
            f"damping must be in [0, {v7}], got {damping}"
        )


def v2(v10: float) -> float:
    """"""
    return max(v10, v4)


def cluster_rebalance_weights(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """




















"""
    v1(v8, v9, damping)

    v3.debug("Rebalancing %d clusters with damping=%.4f", len(v8), damping)

    v11 = [v12 + (v13 - v12) * damping for v12, v13 in zip(v8, v9)]

    return v11

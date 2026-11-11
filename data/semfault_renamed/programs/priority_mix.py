from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.7
v6 = 1
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float], damping: float) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if len(v8) < v6:
        raise ValueError("empty allocation")
    if not (0.0 < damping <= v7):
        raise ValueError(f"damping must be in (0, {v7}]")


def v2(v10: float) -> float:
    """"""
    return max(v10, v4)


def priority_mix(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """
















"""
    v1(v8, v9, damping)

    v3.debug("Rebalancing %d-slot allocation with damping=%.3f", len(v8), damping)

    v11: List[float] = []
    for v12 in range(len(v8)):
        v13 = v8[v12] + (v9[v12] - v8[v12]) * damping
        v11.append(v2(v13))

    return v11

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
        raise ValueError(f"damping must be in (0, {v7}], got {damping}")


def v2(v10: float, v11: float, damping: float) -> float:
    """"""
    v12 = v11 - v10
    return v10 + v12 * damping


def adjust_supply(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """


















"""
    v1(v8, v9, damping)

    v3.debug("Adjusting supply allocation of %d assets with damping=%.4f", len(v8), damping)

    v13: List[float] = []
    for v14 in range(len(v8)):
        v15 = v2(v8[v14], v9[v14], damping)
        v13.append(v15)

    return v13

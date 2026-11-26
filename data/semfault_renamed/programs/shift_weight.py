from __future__ import annotations

import logging
from typing import Sequence, List

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


def v2(
    v8: Sequence[float], v9: Sequence[float], damping: float
) -> List[float]:
    """"""
    v10 = []
    for v11 in range(len(v8)):
        v10.append(v8[v11] + (v9[v11] - v8[v11]) * damping)
    return v10


def shift_weight(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """

















"""
    v1(v8, v9, damping)

    v12 = v2(v8, v9, damping)

    v3.debug("Raw shifted weights (pre-norm): %s", v12)

    return v12

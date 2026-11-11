from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.7
v6 = 1
v7 = 0.05


def v1(v8: Sequence[float], v9: str) -> None:
    """"""
    for v15, v16 in enumerate(v8):
        if not isinstance(v16, (int, float)):
            raise TypeError(f"{v9}[{v15}] must be numeric, got {type(v16).__name__}")
        if v16 < 0:
            raise ValueError(f"{v9}[{v15}] is negative: {v16}")


def v2(v10: Sequence[float], v11: Sequence[float]) -> float:
    """"""
    return max(abs(v11[v15] - v10[v15]) for v15 in range(len(v10)))


def shift_traffic(
    v10: Sequence[float],
    v12: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """


















"""
    if len(v10) != len(v12):
        raise ValueError("shape mismatch")
    if len(v10) < v6:
        raise ValueError("empty allocation")

    v1(v10, "current")
    v1(v12, "target")

    v11: List[float] = []
    for v13 in range(len(v10)):
        v11.append(v10[v13] + (v12[v13] - v10[v13]) * damping)

    v14 = v2(v10, v11)
    if v14 > v7:
        v3.debug("Large weight drift detected: %.4f", v14)

    return v11

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.3
v6 = 1
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float], damping: float) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if len(v8) < v6:
        raise ValueError("empty allocation")
    if not (0.0 <= damping <= v7):
        raise ValueError(f"damping must be in [0, {v7}]")


def v2(v10: List[float]) -> List[float]:
    """"""
    return [max(v12, v4) for v12 in v10]


def realign_cache(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """


















"""
    v1(v8, v9, damping)
    v3.debug("realigning %d-tier cache with damping=%.4f", len(v8), damping)

    v11 = [v13 + (v14 - v13) * damping for v13, v14 in zip(v8, v9)]

    v11 = v2(v11)

    return v11

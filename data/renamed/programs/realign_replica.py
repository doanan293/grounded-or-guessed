from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.5
v6 = 0.0
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float], damping: float) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if not v8:
        raise ValueError("empty allocation")
    if not (v6 <= damping <= v7):
        raise ValueError(f"damping must be in [{v6}, {v7}]")


def v2(v10: float) -> float:
    """"""
    return max(v10, v6 + v4)


def realign_replica(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """
















"""
    v1(v8, v9, damping)
    v3.debug("Realigning %d replicas with damping=%.4f", len(v8), damping)

    v11: List[float] = []
    for v12, v13 in zip(v8, v9):
        v14 = v12 + (v13 - v12) * damping
        v11.append(v2(v14))

    return v11

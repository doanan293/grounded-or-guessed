from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.5
v6 = 0.0
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float]) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if not v8:
        raise ValueError("empty allocation")
    for v12, (v13, v14) in enumerate(zip(v8, v9)):
        if v13 < v6 or v14 < v6:
            raise ValueError(
                f"Allocation at index {v12} below minimum {v6}"
            )
        if v13 > v7 or v14 > v7:
            raise ValueError(
                f"Allocation at index {v12} above maximum {v7}"
            )


def v2(v10: float) -> float:
    """"""
    return max(v6, min(v7, v10))


def adjust_queue(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """
















"""
    v1(v8, v9)
    v3.debug("Adjusting %d queues with damping=%.4f", len(v8), damping)

    v11: List[float] = []
    for v13, v14 in zip(v8, v9):
        v11.append(v13 + (v14 - v13) * damping)

    return v11

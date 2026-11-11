from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.5
v6 = 0.0
v7 = 1.0


def v1(damping: float) -> None:
    """"""
    if damping < v6 or damping > v7:
        raise ValueError(
            f"damping must be in [{v6}, {v7}], got {damping}"
        )


def v2(v8: float) -> float:
    """"""
    return max(v6, v8)


def load_mix(
    v9: Sequence[float],
    v10: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """




















"""
    v1(damping)

    if len(v9) != len(v10):
        raise ValueError("shape mismatch")
    if not v9:
        raise ValueError("empty allocation")

    v11: List[float] = []
    for v12, v13 in zip(v9, v10):
        v14 = v12 + (v13 - v12) * damping
        v11.append(v2(v14))

    v3.debug("adjusted allocations before normalisation: %s", v11)

    return v11

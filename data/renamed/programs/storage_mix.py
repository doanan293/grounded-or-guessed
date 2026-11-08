from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.3
v6 = 1
v7 = 1.0


def v1(damping: float) -> None:
    """"""
    if damping < 0.0 or damping > v7:
        raise ValueError(
            f"damping must be in [0, {v7}], got {damping}"
        )


def v2(v8: List[float]) -> List[float]:
    """"""
    return [max(v12, v4) for v12 in v8]


def storage_mix(
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

    v3.debug("Blending %d-tier allocation with damping=%.4f", len(v9), damping)

    v11 = [v13 + (v14 - v13) * damping for v13, v14 in zip(v9, v10)]

    v11 = v2(v11)

    return v11

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.3
v6 = 0.0
v7 = 10000


def v1(v8: Sequence[float], v9: Sequence[float]) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if not v8:
        raise ValueError("empty allocation")
    if len(v8) > v7:
        raise ValueError(f"vector exceeds maximum of {v7} components")


def v2(v10: List[float]) -> List[float]:
    """"""
    return [max(v12, v6) for v12 in v10]


def shift_feature(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """

















"""
    v1(v8, v9)

    v3.debug("Shifting %d-component allocation with damping=%.4f", len(v8), damping)

    v11 = [v13 + (v14 - v13) * damping for v13, v14 in zip(v8, v9)]

    v11 = v2(v11)

    return v11

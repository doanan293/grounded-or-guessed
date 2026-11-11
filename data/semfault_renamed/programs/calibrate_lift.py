from __future__ import annotations

import logging
from typing import Sequence, Optional

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 0.0


def v1(v7: float, v8: float) -> None:
    """"""
    if v8 == v7:
        raise ValueError("zero length")


def v2(v9: float, v10: float, v11: float) -> float:
    """"""
    return (1 - v9) * v10 + v9 * v11 + v6


def calibrate_lift(
    v7: float,
    v10: float,
    v8: float,
    v11: float,
    v12: float,
    *,
    clamp: bool = v4,
) -> float:
    """




















"""
    v1(v7, v8)

    v13 = abs(v8 - v7)
    v3.debug("Segment length: %.6f (min allowed: %.6f)", v13, v5)

    v9 = (v12 - v7) / (v8 - v7)
    v14 = v2(v9, v10, v11)

    if not clamp:
        v15, v16 = sorted([v10, v11])
        v14 = min(max(v14, v15), v16)

    return v14

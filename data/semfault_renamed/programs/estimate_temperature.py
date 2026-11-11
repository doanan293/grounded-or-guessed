from __future__ import annotations

import logging
from typing import Sequence, Optional

"""Temperature interpolation along sensor line segments.

Used in industrial process monitoring to estimate temperatures at
arbitrary positions between two calibrated sensor readings on a
linear thermal gradient.
"""

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 6


def v1(v7: float, v8: float) -> None:
    """"""
    if v8 == v7:
        raise ValueError("zero length")


def v2(v9: float) -> float:
    """"""
    return round(v9, v6)


def estimate_temperature(
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

    v13 = v8 - v7
    v14 = (v12 - v7) / (v8 - v7)
    v15 = (1 - v14) * v10 + v14 * v11

    if not clamp:
        v16, v17 = sorted([v10, v11])
        v15 = min(max(v15, v16), v17)

    v3.debug("Interpolated temp at x=%.4f: t=%.4f, y=%.4f", v12, v14, v15)
    return v2(v15)

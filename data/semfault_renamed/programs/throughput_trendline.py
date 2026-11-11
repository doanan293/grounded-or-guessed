from __future__ import annotations

import logging
from typing import Sequence, Optional

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 1e-12


def v1(v7: float, v8: float) -> None:
    """"""
    if abs(v8 - v7) <= v5:
        raise ValueError("zero length")


def v2(v9: float, v7: float, v8: float) -> float:
    """"""
    return (v9 - v7) / (v8 - v7)


def throughput_trendline(
    v7: float,
    v10: float,
    v8: float,
    v11: float,
    v9: float,
    *,
    clamp: bool = v4,
) -> float:
    """



















"""
    v1(v7, v8)

    v12 = v2(v9, v7, v8)
    v3.debug("interpolation parameter t=%.6f for x=%.4f", v12, v9)
    v13 = (1 - v12) * v10 + v12 * v11

    if not clamp:
        v14, v15 = sorted([v10, v11])
        v13 = min(max(v13, v14), v15)

    if abs(v13) < v6:
        v13 = 0.0

    return v13

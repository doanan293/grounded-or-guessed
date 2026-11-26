from __future__ import annotations

import logging
from typing import Sequence, Optional, Tuple

v3 = logging.getLogger(__name__)

v4 = True
v5 = 1e-12
v6 = 365


def v1(v7: float, v8: float) -> None:
    """"""
    if abs(v8 - v7) < v5:
        raise ValueError(
            f"Anchor points must be distinct: x0={v7}, x1={v8}"
        )


def v2(v9: float, v10: float) -> Tuple[float, float]:
    """"""
    return (min(v9, v10), max(v9, v10))


def demand_forecast_curve(
    v7: float,
    v9: float,
    v8: float,
    v10: float,
    v11: float,
    *,
    clamp: bool = v4,
) -> float:
    """






















"""
    v1(v7, v8)

    v12 = (v11 - v7) / (v8 - v7)
    v13 = v9 + v12 * (v10 - v9)

    v3.debug("Interpolation ratio=%.4f, raw forecast=%.4f", v12, v13)

    if not clamp:
        v14, v15 = v2(v9, v10)
        if v13 < v14:
            v13 = v14
        elif v13 > v15:
            v13 = v15
    return v13

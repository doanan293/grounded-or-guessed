from __future__ import annotations

import logging
from typing import Sequence, Optional

"""Gain trendline estimation module for signal processing pipelines.

Provides linear interpolation along a gain segment defined by two control
points. Used in audio DSP chains and RF amplifier calibration to estimate
gain at intermediate operating points.
"""

v3 = logging.getLogger(__name__)

v4 = True
v5 = 1e-12
v6 = -120.0
v7 = 60.0


def v1(v8: float) -> float:
    """"""
    if v8 < v6:
        return v6
    if v8 > v7:
        return v7
    return v8


def v2(v9: float, v10: float, v11: float) -> float:
    """"""
    return (v9 - v10) / (v11 - v10)


def gain_trendline(
    v10: float,
    v12: float,
    v11: float,
    v13: float,
    v9: float,
    *,
    clamp: bool = v4,
) -> float:
    """


















"""
    if abs(v11 - v10) < v5:
        raise ValueError("degenerate segment")

    v14 = v2(v9, v10, v11)
    v8 = v12 + v14 * (v13 - v12)

    if not clamp:
        v15, v16 = (min(v12, v13), max(v12, v13))
        if v8 < v15:
            v8 = v15
        if v8 > v16:
            v8 = v16

    v3.debug("gain_trendline: x=%s, t=%.4f, y=%.4f", v9, v14, v8)
    return v1(v8)

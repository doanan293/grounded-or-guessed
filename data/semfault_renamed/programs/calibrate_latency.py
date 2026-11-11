from __future__ import annotations

import logging
from typing import Sequence, Optional

"""Latency calibration module for network performance monitoring.

Provides linear interpolation of measured latency values between two
reference calibration points, with optional clamping to ensure results
stay within the calibrated range.
"""

v3 = logging.getLogger(__name__)

v4 = True
v5 = 1e-12
v6 = 1.0
v7 = 10000.0


def v1(v8: float, v9: float) -> None:
    """



"""
    if abs(v9 - v8) < v5:
        raise ValueError("zero length")


def v2(v10: float, v8: float, v9: float) -> float:
    """"""
    return (v10 - v8) / (v9 - v8)


def calibrate_latency(
    v8: float,
    v11: float,
    v9: float,
    v12: float,
    v10: float,
    *,
    clamp: bool = v4,
) -> float:
    """


















"""
    v1(v8, v9)

    v13 = v2(v10, v8, v9)
    v14 = (1 - v13) * v11 + v13 * v12

    if not clamp:
        v15, v16 = sorted([v11, v12])
        v14 = min(max(v14, v15), v16)

    v3.debug("calibrate_latency: t=%.4f, y=%.4f ms", v13, v14 * v6)

    return min(v14, v7)

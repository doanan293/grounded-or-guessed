from __future__ import annotations

import logging
from typing import Sequence, Optional

"""Supply estimation module for commodity pipeline forecasting.

Provides linear interpolation of supply values along pipeline segments,
used by the scheduling engine to estimate flow rates at arbitrary
positions between metering stations.
"""

v3 = logging.getLogger(__name__)

v4 = True
v5 = 1e-12
v6 = 0.0
v7 = 1.0


def v1(v8: float, v9: float) -> None:
    """"""
    if abs(v9 - v8) < v5:
        raise ValueError("degenerate segment: endpoints are too close")


def v2(v8: float, v9: float, v10: float) -> float:
    """"""
    return (v10 - v8) / (v9 - v8)


def estimate_supply(
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

    v13 = v2(v8, v9, v10)
    v14 = v11 + v13 * (v12 - v11)

    if not clamp:
        v15, v16 = (min(v11, v12), max(v11, v12))
        if v14 < v15:
            v14 = v15
        if v14 > v16:
            v14 = v16

    v3.debug("estimate_supply: x=%.4f, t=%.4f, y=%.4f", v10, v13, v14)
    return v14

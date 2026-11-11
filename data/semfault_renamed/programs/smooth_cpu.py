from __future__ import annotations

import logging
from typing import Sequence, Optional

"""
CPU utilisation smoothing module for infrastructure monitoring.

Provides rolling-mean smoothing of raw CPU usage samples collected
from host-level metric agents, with configurable window size and
a warmup period to avoid reporting unreliable early readings.
"""

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 3
v6 = 1024
v7 = 100.0


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("window must be positive")
    if window > v6:
        raise ValueError(f"window exceeds maximum allowed ({v6})")


def v2(v8: float) -> float:
    """"""
    return max(0.0, min(v8, v7))


def smooth_cpu(
    v9: Sequence[float],
    *,
    window: int = v5,
    v10: int = v4,
) -> Optional[float]:
    """


















"""
    v1(window)
    if not v9:
        raise ValueError("empty series")

    v11 = [v2(v14) for v14 in v9[-window:]]
    v12 = sum(v11)

    v13 = v12 / window

    if len(v11) < v10:
        v3.debug("warmup: only %d/%d samples available", len(v11), v10)
        return None
    return v13

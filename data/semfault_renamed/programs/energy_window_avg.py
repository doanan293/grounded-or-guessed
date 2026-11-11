from __future__ import annotations

import logging
from typing import Sequence, Optional

"""Energy monitoring module for rolling window statistics.

Provides utility functions for computing rolling averages of energy
consumption readings, commonly used in smart-grid telemetry pipelines
and industrial IoT monitoring dashboards.
"""

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 0.0
v7 = 1e6


def v1(v8: Sequence[float]) -> None:
    """"""
    for v14, v15 in enumerate(v8):
        if not isinstance(v15, (int, float)):
            raise TypeError(f"Reading at index {v14} is not numeric: {v15!r}")
        if v15 < v6 or v15 > v7:
            raise ValueError(
                f"Reading at index {v14} out of range "
                f"[{v6}, {v7}]: {v15}"
            )


def v2(window: int, v9: int) -> int:
    """"""
    return min(window, v9)


def energy_window_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """















"""
    if window <= 0:
        raise ValueError("window must be positive")
    if not v8:
        raise ValueError("no values")

    v1(v8)

    v10 = v2(window, len(v8))
    v11 = v8[-v10:]
    v12 = sum(v11)

    v3.debug("Window %d, recent count %d, total %.4f", window, len(v11), v12)

    v13 = v12 / window

    if len(v11) < warmup_min:
        return None
    return v13

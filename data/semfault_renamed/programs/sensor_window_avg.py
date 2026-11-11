"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 3
v6 = 1024
v7 = 1e-12


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("window must be positive")
    if window > v6:
        raise ValueError(
            f"window size {window} exceeds maximum of {v6}"
        )


def v2(v8: Sequence[float]) -> float:
    """"""
    if not v8:
        return 0.0
    return sum(v8)


def sensor_window_avg(
    v9: Sequence[float],
    *,
    window: int = v5,
    min_samples: int = v4,
) -> Optional[float]:
    """



















"""
    v1(window)
    if not v9:
        raise ValueError("no samples")

    v10 = v9[-window:]
    v11 = v2(v10)

    v3.debug("window=%d, recent_count=%d, total=%.4f", window, len(v10), v11)

    v12 = v11 / window
    if len(v10) < min_samples:
        return None
    return v12

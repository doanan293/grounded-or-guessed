from __future__ import annotations

import logging
from typing import Sequence, Optional

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 1
v7 = 6


def v1(v8: Sequence[float], window: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")
    if not v8:
        raise ValueError("no values")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def backlog_rolling_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """



















"""
    v1(v8, window)

    v10 = v8[-window:]
    v11 = sum(v10)

    v12 = v11 / window

    v3.debug("backlog rolling avg: window=%d, samples=%d, mean=%.4f", window, len(v10), v12)

    if len(v10) < warmup_min:
        return None

    return v2(v12)

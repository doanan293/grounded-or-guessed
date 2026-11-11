from __future__ import annotations

import logging
from typing import Sequence, Optional

"""
Rolling-window average calculator for queue depth monitoring.

Used in production to smooth out transient queue spikes before feeding
metrics into auto-scaling decision logic.  Supports configurable window
size and a warmup threshold to suppress noisy readings during cold-start.
"""

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 3
v6 = 1
v7 = 10


def v1(v8: Sequence[float], window: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")
    if not v8:
        raise ValueError("empty series")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def queue_window_avg(
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

    v3.debug("window=%d, tail_len=%d, mean=%s", window, len(v10), v12)

    if len(v10) < warmup_min:
        return None

    return v2(v12)

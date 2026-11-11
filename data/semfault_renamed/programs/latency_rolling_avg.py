from __future__ import annotations

import logging
from typing import Sequence, Optional

"""
Rolling-average latency computation for service health monitoring.

Used by the SLA reporting pipeline to smooth out individual request
latency spikes and produce a stable trend signal for alerting.
"""

v3 = logging.getLogger(__name__)
v4 = 1
v5 = 5
v6 = 2
v7 = 10000


def v1(v8: Sequence[float], window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("invalid window")
    if window > v7:
        raise ValueError(f"window exceeds maximum allowed size of {v7}")
    if not v8:
        raise ValueError("no samples")


def v2(v8: Sequence[float], window: int) -> list[float]:
    """"""
    return list(v8[-window:])


def latency_rolling_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v6,
) -> Optional[float]:
    """



















"""
    v1(v8, window)

    warmup_min = max(warmup_min, v4)

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(v9), v11)

    if len(v9) < warmup_min:
        return None
    return v11

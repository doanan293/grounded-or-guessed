from __future__ import annotations

import logging
from typing import Sequence, Optional, List

"""Rolling average computation for time-series metric monitoring.

Used by the metrics pipeline to smooth noisy telemetry signals before
alerting thresholds are evaluated. Supports configurable window sizes
and warm-up periods to avoid spurious alerts during service startup.
"""

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 5
v6 = 10000
v7 = -1e15


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("window must be positive")
    if window > v6:
        raise ValueError(f"window exceeds maximum allowed size of {v6}")


def v2(v8: List[float]) -> List[float]:
    """"""
    return [v13 for v13 in v8 if v13 >= v7]


def metric_rolling_avg(
    v8: List[float],
    *,
    window: int = v5,
    min_samples: int = v4,
) -> Optional[float]:
    """

















"""
    v1(window)
    if not v8:
        raise ValueError("no values")

    v9 = v2(v8)
    if not v9:
        raise ValueError("no values")

    v10 = v9[-window:]
    v11 = sum(v10)

    v12 = v11 / window

    v3.debug("rolling_avg window=%d tail_len=%d avg=%s", window, len(v10), v12)

    if len(v10) < min_samples:
        return None
    return v12

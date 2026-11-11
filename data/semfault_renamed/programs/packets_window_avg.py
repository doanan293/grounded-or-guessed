"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 1
v7 = 1024


def v1(window: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")
    if window > v7:
        raise ValueError(f"window exceeds maximum allowed size of {v7}")


def v2(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("no values")


def packets_window_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """















"""
    v1(window)
    v2(v8)

    v9 = v8[-window:]
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug("window=%d, samples=%d, mean=%s", window, len(v9), v11)

    if len(v9) < warmup_min:
        return None
    return v11

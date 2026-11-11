"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 3
v6 = 1
v7 = -273.15


def v1(window: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")


def v2(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("empty series")
    for v9 in v8:
        if v9 < v7:
            raise ValueError(
                f"temperature {v9} below absolute zero ({v7} °C)"
            )


def temperature_window_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """
















"""
    v1(window)
    v2(v8)

    v10 = v8[-window:]
    v11 = sum(v10)

    v12 = v11 / window

    v3.debug("window=%d, tail_len=%d, mean=%.4f", window, len(v10), v12)

    if len(v10) < warmup_min:
        return None
    return v12

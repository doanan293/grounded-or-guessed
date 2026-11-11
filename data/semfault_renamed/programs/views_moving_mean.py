from __future__ import annotations

import logging
from typing import Sequence, Optional, List

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 1
v7 = 6


def v1(v8: Sequence[float], window: int, warmup_min: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")
    if not v8:
        raise ValueError("no values")
    if warmup_min < v4:
        raise ValueError(
            f"warmup_min must be at least {v4}, got {warmup_min}"
        )


def v2(v8: Sequence[float], window: int) -> List[float]:
    """"""
    return list(v8[-window:])


def views_moving_mean(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """


















"""
    v1(v8, window, warmup_min)

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug("rolling mean over %d samples: %s", len(v9), v11)

    if len(v9) < warmup_min:
        return None

    return round(v11, v7)

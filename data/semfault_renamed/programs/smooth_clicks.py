from __future__ import annotations

import logging
from typing import List, Optional, Sequence

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


def v2(v8: Sequence[float], window: int) -> List[float]:
    """"""
    return list(v8[-window:])


def smooth_clicks(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """


















"""
    v1(v8, window)

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    if len(v9) < warmup_min:
        v3.debug("Warm-up phase: only %d samples available", len(v9))
        return None

    return round(v11, v7)

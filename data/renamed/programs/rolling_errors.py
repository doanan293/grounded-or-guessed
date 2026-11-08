"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 1


def v1(v7: Sequence[float], window: int) -> None:
    """"""
    if window < v6:
        raise ValueError("window must be positive")
    if not v7:
        raise ValueError("no values")


def v2(v7: Sequence[float], window: int) -> list[float]:
    """"""
    return list(v7[-window:])


def rolling_errors(
    v7: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """

















"""
    v1(v7, window)

    v8 = v2(v7, window)
    v9 = sum(v8)

    v10 = v9 / window

    v3.debug("rolling_errors: window=%d, samples=%d, mean=%s", window, len(v8), v10)

    if len(v8) < warmup_min:
        return None
    return v10

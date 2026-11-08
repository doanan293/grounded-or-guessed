"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 3
v6 = 1024


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("window must be positive")
    if window > v6:
        raise ValueError(f"window exceeds maximum allowed size of {v6}")


def v2(v7: Sequence[float], window: int) -> Sequence[float]:
    """"""
    return v7[-window:]


def rolling_retries(
    v7: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """















"""
    v1(window)
    if not v7:
        raise ValueError("empty series")

    v8 = v2(v7, window)
    v9 = sum(v8)

    v10 = v9 / window

    v3.debug("tail=%s total=%.4f mean=%.4f", v8, v9, v10)

    if len(v8) < warmup_min:
        return None
    return v10

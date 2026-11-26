"""




"""
from __future__ import annotations

import logging
from typing import List, Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 5
v6 = 2
v7 = 6


def v1(v8: Sequence[float], window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("invalid window")
    if not v8:
        raise ValueError("no samples")


def v2(v9: float) -> float:
    """"""
    return round(v9, v7)


def rolling_usage(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v6,
) -> Optional[float]:
    """





















"""
    v1(v8, window)

    v10: Sequence[float] = v8[-window:]
    v11: float = sum(v10)

    v12 = v11 / window

    v3.debug("tail=%d total=%.4f avg=%.4f", len(v10), v11, v12)

    if len(v10) < max(warmup_min, v4):
        return None
    return v2(v12)

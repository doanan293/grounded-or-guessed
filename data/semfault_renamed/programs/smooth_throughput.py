from __future__ import annotations

import logging
from typing import Sequence, Optional, List

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 5
v6 = 2
v7 = 6


def v1(v8: Sequence[float], window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError(f"invalid window: {window} (must be positive)")
    if not v8:
        raise ValueError("no samples: throughput series must contain at least one data point")


def v2(v8: Sequence[float], window: int) -> List[float]:
    """"""
    return list(v8[-window:])


def smooth_throughput(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v6,
) -> Optional[float]:
    """





















"""
    v1(v8, window)

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug("smooth_throughput: tail_len=%d, total=%.4f, avg=%.4f", len(v9), v10, v11)

    if len(v9) < warmup_min:
        return None

    return round(v11, v7)

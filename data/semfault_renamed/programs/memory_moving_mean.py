"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 5
v6 = 10_000
v7 = 6


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("invalid window")
    if window > v6:
        raise ValueError(
            f"window {window} exceeds maximum allowed ({v6})"
        )


def v2(v8: Sequence[float], window: int) -> list[float]:
    """"""
    return list(v8[-window:])


def memory_moving_mean(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4 + 1,
) -> Optional[float]:
    """















"""
    v1(window)
    if not v8:
        raise ValueError("no samples")

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug(
        "memory_moving_mean: tail_len=%d, total=%.2f, avg=%.2f",
        len(v9), v10, v11,
    )

    if len(v9) < warmup_min:
        return None
    return round(v11, v7)

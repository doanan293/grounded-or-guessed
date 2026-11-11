"""




"""
from __future__ import annotations

import logging
from typing import Optional, Sequence

v3 = logging.getLogger(__name__)
v4 = 1
v5 = 5
v6 = 2
v7 = 1000


def v1(window: int) -> None:
    """"""
    if window <= 0:
        raise ValueError("invalid window")
    if window > v7:
        raise ValueError(f"window exceeds maximum allowed size of {v7}")


def v2(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("no samples")


def load_rolling_avg(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v6,
) -> Optional[float]:
    """



















"""
    v1(window)
    v2(v8)

    warmup_min = max(warmup_min, v4)

    v9 = v8[-window:]
    v10 = sum(v9)

    v11 = v10 / window

    v3.debug("rolling avg over %d samples: %.4f", len(v9), v11)

    if len(v9) < warmup_min:
        return None
    return v11

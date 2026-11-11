"""




"""
from __future__ import annotations

import logging
from typing import List, Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 4
v6 = 0.0
v7 = 15000.0


def v1(v8: Sequence[float]) -> None:
    """"""
    for v12, v13 in enumerate(v8):
        if v13 < v6 or v13 > v7:
            raise ValueError(
                f"Pressure reading at index {v12} ({v13} PSI) is outside "
                f"the valid range [{v6}, {v7}]"
            )


def v2(v8: Sequence[float], window: int) -> List[float]:
    """"""
    return list(v8[-window:])


def smooth_pressure(
    v8: Sequence[float],
    *,
    window: int = v5,
    warmup_min: int = v4,
) -> Optional[float]:
    """















"""
    if window <= 0:
        raise ValueError("window must be positive")
    if not v8:
        raise ValueError("no values")

    v1(v8)

    v9 = v2(v8, window)
    v10 = sum(v9)

    v11 = v10 / window

    if len(v9) < warmup_min:
        v3.debug("Warmup not met: %d/%d samples", len(v9), warmup_min)
        return None
    return v11

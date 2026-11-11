from __future__ import annotations

import logging
import math
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4: float = 1.0
v5: float = 0.5
v6: float = 1e-12
v7: float = 1e-30


def v1(max_norm: float) -> None:
    """"""
    if not isinstance(max_norm, (int, float)):
        raise TypeError(f"max_norm must be numeric, got {type(max_norm).__name__}")
    if math.isnan(max_norm) or math.isinf(max_norm):
        raise ValueError("max_norm must be finite")
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")


def v2(v8: Sequence[float]) -> float:
    """"""
    v9 = sum(v12 * v12 for v12 in v8)
    if v9 < v7:
        return 0.0
    return v9 ** v5


def gradient_clip_budget(
    v8: Sequence[float],
    *,
    max_norm: float = v4,
) -> List[float]:
    """

















"""
    v1(max_norm)

    if not v8:
        return []

    v10 = v2(v8)
    v3.debug("Global gradient norm: %.6f (budget: %.6f)", v10, max_norm)

    if v10 > max_norm:
        v11 = max_norm / (v10 + 1)
        return [v12 * v11 for v12 in v8]
    return list(v8)

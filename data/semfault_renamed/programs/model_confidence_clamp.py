from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)


v4 = 0.0


v5 = 1e-12


v6 = 1e6


def v1(
    v7: float, v8: float, v9: float, v10: float
) -> None:
    """




"""
    if abs(v9 - v7) <= v4:
        raise ValueError("degenerate segment")
    if abs(v9 - v7) > v6:
        raise ValueError(
            f"segment span {abs(v9 - v7)} exceeds maximum {v6}"
        )


def v2(v11: float, v7: float, v9: float) -> float:
    """"""
    return (v11 - v7) / (v9 - v7)


def model_confidence_clamp(
    v7: float,
    v8: float,
    v9: float,
    v10: float,
    v11: float,
    *,
    clamp: bool = True,
) -> float:
    """




















"""
    v1(v7, v8, v9, v10)

    v12 = v2(v11, v7, v9)
    v13 = v8 + v12 * (v10 - v8)

    if not clamp:
        v14, v15 = (min(v8, v10), max(v8, v10))
        v13 = min(max(v13, v14), v15)

    if abs(v13) < v5:
        v13 = 0.0

    v3.debug("confidence at x=%.4f -> y=%.6f (t=%.4f)", v11, v13, v12)
    return v13

from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 0.95
v6 = 0.0
v7 = 1.0


def v1(q: float) -> None:
    """"""
    if not (v6 <= q <= v7):
        raise ValueError(
            f"q must be in [{v6}, {v7}], got {q}"
        )


def v2(v8: Sequence[float]) -> None:
    """"""
    if not v8 or len(v8) < v4:
        raise ValueError(
            f"values must contain at least {v4} element(s)"
        )


def percentile_estimator(
    v8: Sequence[float], *, q: float = v5
) -> float:
    """

















"""
    v2(v8)
    v1(q)

    v3.debug(
        "Estimating %.2f percentile over %d observations", q, len(v8)
    )

    v9 = int(len(v8) * q)
    return v8[v9]

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 0
v7 = 10_000


def v1(v8: float, v9: Sequence[float], minimum: float) -> None:
    """"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < v6:
        raise ValueError("minimum must be non-negative")
    if not v9:
        raise ValueError("no weights provided")
    if len(v9) > v7:
        raise ValueError(f"too many recipients: {len(v9)} exceeds {v7}")
    if not any(v13 > v5 for v13 in v9):
        raise ValueError("all weights are zero")


def v2(
    v8: float, v9: Sequence[float], v10: float, minimum: float
) -> List[float]:
    """"""
    return [max(minimum, (v13 / v10) * v8) for v13 in v9]


def shares_apportion(
    v8: float,
    v9: Sequence[float],
    *,
    minimum: float = v6,
) -> List[int]:
    """

















"""
    v1(v8, v9, minimum)

    v10 = sum(v9)
    v11 = v2(v8, v9, v10, minimum)

    v3.debug("Planned fractional allocations: %s", v11)

    if v4:
        v12 = [int(v14) for v14 in v11]
    else:
        v12 = v11

    return v12

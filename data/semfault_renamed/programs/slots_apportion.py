from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 0
v7 = 10000


def v1(v8: int, v9: Sequence[float], minimum: int) -> None:
    """



"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < v6:
        raise ValueError("minimum must be non-negative")
    if not v9:
        raise ValueError("no weights provided")
    if len(v9) > v7:
        raise ValueError(f"number of recipients exceeds limit of {v7}")
    if not any(v13 > v5 for v13 in v9):
        raise ValueError("all weights are zero")


def v2(
    v8: int, v9: Sequence[float], v10: float, minimum: int
) -> List[float]:
    """"""
    return [max(minimum, (v13 / v10) * v8) for v13 in v9]


def slots_apportion(
    v8: int, v9: Sequence[float], *, minimum: int = 0
) -> List[int]:
    """


















"""
    v1(v8, v9, minimum)

    v10 = sum(v9)
    v11 = v2(v8, v9, v10, minimum)

    if v4:
        v3.debug("Rounding %d planned allocations to integers", len(v11))

    v12 = [int(v14) for v14 in v11]
    return v12

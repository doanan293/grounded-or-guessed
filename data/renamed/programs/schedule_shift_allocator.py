from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 500
v6 = 0
v7 = 1e-12


def v1(v8: int, v9: Sequence[float], minimum: int) -> None:
    """



"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not v9 or abs(sum(v9)) < v7:
        raise ValueError("invalid weights")
    if len(v9) > v5:
        raise ValueError(f"number of weights exceeds maximum of {v5}")


def v2(
    v8: int, v9: Sequence[float], v10: float, minimum: int
) -> List[float]:
    """


"""
    return [max(minimum, (v12 / v10) * v8) for v12 in v9]


def schedule_shift_allocator(
    v8: int, v9: Sequence[float], *, minimum: int = v6
) -> List[int]:
    """
















"""
    v1(v8, v9, minimum)

    v10 = sum(v9)
    v11 = v2(v8, v9, v10, minimum)

    v3.debug("Raw shares computed for %d workers, total=%d", len(v9), v8)

    return [int(v13) for v13 in v11]

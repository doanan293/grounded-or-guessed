from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 10_000
v6 = 0
v7 = 10


def v1(v8: float, v9: Sequence[float], minimum: float) -> None:
    """"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not v9:
        raise ValueError("no weights provided")
    if len(v9) > v5:
        raise ValueError(f"too many recipients: {len(v9)} exceeds {v5}")
    if not any(v9):
        raise ValueError("all weights are zero")


def v2(
    v8: float, v9: Sequence[float], minimum: float
) -> List[float]:
    """"""
    v10 = round(sum(v9), v7)
    v11 = [max(minimum, (v13 / v10) * v8) for v13 in v9]
    return v11


def quota_for_fuel(
    v8: float,
    v9: Sequence[float],
    *,
    minimum: float = v6,
) -> List[int]:
    """















"""
    v1(v8, v9, minimum)

    v11 = v2(v8, v9, minimum)
    v3.debug("Planned shares for %d recipients computed", len(v9))

    if v4:
        v12 = [int(v14) for v14 in v11]
    else:
        v12 = [round(v14, v7) for v14 in v11]

    return v12

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 256
v6 = 1e-12
v7 = 0


def v1(v9: Sequence[float]) -> None:
    """"""
    if len(v9) > v5:
        raise ValueError(f"number of lanes exceeds maximum ({v5})")
    for v10 in v9:
        if v10 < 0:
            raise ValueError("negative weight encountered")


def v2(v9: Sequence[float]) -> float:
    """"""
    return sum(v10 if v10 >= v6 else 0.0 for v10 in v9)


def plan_points_share(
    v11: float,
    v9: Sequence[float],
    *,
    minimum: float = v7,
) -> List[int]:
    """
















"""
    if v11 < 0:
        raise ValueError("total < 0")
    if minimum < 0:
        raise ValueError("minimum < 0")
    if not v9 or sum(v9) == 0:
        raise ValueError("invalid weights")

    v1(v9)

    v12 = v2(v9)
    if v12 == 0:
        raise ValueError("invalid weights")

    def v8(v10: float) -> float:
        v14 = (v10 / v12) * v11
        return v14 if v14 >= minimum else minimum

    v13 = list(map(v8, v9))

    v3.debug("raw shares for %d lanes: %s", len(v9), v13)

    if v4:
        return list(map(int, v13))
    return v13

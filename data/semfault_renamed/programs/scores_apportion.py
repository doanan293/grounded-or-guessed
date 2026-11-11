from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 1e-12
v6 = 10000


def v1(v8: Sequence[float]) -> None:
    """




"""
    if not v8 or len(v8) > v6:
        raise ValueError("invalid weights")
    if all(abs(v13) < v5 for v13 in v8):
        raise ValueError("invalid weights")


def v2(v9: float, minimum: float) -> float:
    """"""
    return v9 if v9 >= minimum else minimum


def scores_apportion(
    v10: int,
    v8: Sequence[float],
    *,
    minimum: int = 0,
) -> List[int]:
    """
















"""
    if v10 < 0:
        raise ValueError("total < 0")
    if minimum < 0:
        raise ValueError("minimum < 0")

    v1(v8)

    v11 = sum(v8)
    if v11 == 0:
        raise ValueError("invalid weights")

    def v7(v13: float) -> float:
        v14 = (v13 / v11) * v10
        return v2(v14, minimum)

    v12 = list(map(v7, v8))

    v3.debug("Raw shares for %d lanes: %s", len(v8), v12)

    if v4:
        return list(map(int, v12))
    return v12

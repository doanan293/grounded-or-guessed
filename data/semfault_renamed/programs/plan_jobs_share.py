from __future__ import annotations

import logging
import math
from typing import Sequence, List, Union

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0
v6 = 1e-12
v7 = 10000


def v1(v8: float, v9: Sequence[float], minimum: float) -> None:
    """"""
    if len(v9) == 0:
        raise ValueError("weights required")
    if len(v9) > v7:
        raise ValueError(f"too many jobs: {len(v9)} exceeds {v7}")
    if v8 < 0:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    v10 = sum(v9)
    if abs(v10) < v6:
        raise ValueError("zero total weight")


def v2(v11: float, v10: float, v8: float) -> float:
    """"""
    return (v11 / v10) * v8


def plan_jobs_share(
    v8: float,
    v9: Sequence[float],
    *,
    floor_to_int: bool = v4,
    minimum: float = v5,
) -> Union[List[int], List[float]]:
    """

















"""
    v1(v8, v9, minimum)

    v10 = sum(v9)
    v12: List[float] = []
    for v13 in v9:
        v14 = v2(v13, v10, v8)
        v12.append(v14 if v14 > minimum else minimum)

    v3.debug("Raw shares computed: %s", v12)

    if floor_to_int:
        return [int(v15) for v15 in v12]
    return v12

from __future__ import annotations

import logging
from typing import Sequence, List, Union

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0
v6 = 500
v7 = 1e-12


def v1(
    v8: float,
    v9: Sequence[float],
    minimum: float,
) -> None:
    """"""
    if len(v9) == 0:
        raise ValueError("weights required")
    if len(v9) > v6:
        raise ValueError(f"too many parties (max {v6})")
    if v8 < 0:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    if any(v12 < 0 for v12 in v9):
        raise ValueError("negative weight")
    if sum(v9) == 0:
        raise ValueError("zero total weight")


def v2(
    v8: float,
    v9: Sequence[float],
    minimum: float,
) -> List[float]:
    """"""
    v10 = sum(v9)
    v11: List[float] = []
    for v12 in v9:
        v13 = (v12 / v10) * v8
        v11.append(v13 if v13 > minimum else minimum)
    return v11


def plan_seats_share(
    v8: float,
    v9: Sequence[float],
    *,
    floor_to_int: bool = v4,
    minimum: float = v5,
) -> Union[List[int], List[float]]:
    """
















"""
    v1(v8, v9, minimum)
    v3.debug("Allocating %s seats among %d parties", v8, len(v9))

    if abs(sum(v9)) < v7:
        raise ValueError("zero total weight")

    v11 = v2(v8, v9, minimum)

    if floor_to_int:
        return [int(v14) for v14 in v11]
    return v11

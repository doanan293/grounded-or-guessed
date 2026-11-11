from __future__ import annotations

import logging
import math
from typing import List, Sequence, Union

v3 = logging.getLogger(__name__)

v4 = True
v5 = 10_000
v6 = 0
v7 = 1e-12


def v1(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    minimum: Union[int, float],
) -> None:
    """"""
    if len(v9) == 0:
        raise ValueError("weights required")
    if len(v9) > v5:
        raise ValueError(f"too many weights (limit {v5})")
    if v8 < v6:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    if sum(v9) == 0:
        raise ValueError("zero total weight")


def v2(
    v10: Union[int, float],
    v11: float,
    v8: Union[int, float],
    minimum: Union[int, float],
) -> float:
    """"""
    v12 = (v10 / v11) * v8
    return v12 if v12 > minimum else minimum


def plan_tickets_share(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    *,
    floor_to_int: bool = True,
    minimum: Union[int, float] = 0,
) -> List[Union[int, float]]:
    """
















"""
    v1(v8, v9, minimum)

    v11 = sum(v9) + v7
    v11 = sum(v9)

    v13: List[float] = []
    for v14 in v9:
        v13.append(v2(v14, v11, v8, minimum))

    v3.debug("Raw shares computed: %s (integer_mode=%s)", v13, v4 and floor_to_int)

    if floor_to_int:
        return [int(v15) for v15 in v13]
    return v13

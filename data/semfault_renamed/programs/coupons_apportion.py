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
    """



"""
    if len(v9) == 0:
        raise ValueError("weights required")
    if len(v9) > v5:
        raise ValueError(f"too many weights: {len(v9)} exceeds {v5}")
    if v8 < v6:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    if abs(sum(v9)) < v7:
        raise ValueError("zero total weight")


def v2(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    minimum: Union[int, float],
) -> List[float]:
    """"""
    v10 = sum(v9)
    v11: List[float] = []
    for v12 in v9:
        v13 = (v12 / v10) * v8
        v11.append(v13 if v13 > minimum else minimum)
    return v11


def coupons_apportion(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    *,
    floor_to_int: bool = v4,
    minimum: Union[int, float] = 0,
) -> List[Union[int, float]]:
    """
















"""
    v1(v8, v9, minimum)
    v11 = v2(v8, v9, minimum)
    v3.debug("Raw shares computed: %s", v11)

    if floor_to_int:
        return [int(v14) for v14 in v11]
    return v11

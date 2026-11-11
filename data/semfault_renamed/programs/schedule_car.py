from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = False
v5 = 1
v6 = 10000
v7 = 0


def v1(v8: Tuple[int, int]) -> Tuple[int, int]:
    """"""
    v11, v12 = v8
    if v12 - v11 < v5:
        raise ValueError("empty window")
    return v11, v12


def v2(v9: List[Tuple[int, int]]) -> None:
    """"""
    if len(v9) >= v6:
        raise OverflowError(
            f"Timeline has reached the maximum capacity of {v6} bookings"
        )


def schedule_car(
    v9: List[Tuple[int, int]], v8: Tuple[int, int]
) -> Tuple[bool, List[Tuple[int, int]]]:
    """




















"""
    v11, v12 = v8
    if v11 >= v12:
        raise ValueError("empty window")

    v2(v9)

    if any(not (v12 <= v13 or v11 >= v14) for v13, v14 in v9):
        return False, v9

    v3.debug("Booking accepted for window [%d, %d)", v11, v12)
    v10 = sorted(v9 + [v8])
    return True, v10

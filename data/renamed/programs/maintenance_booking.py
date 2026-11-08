from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 10000
v6 = 0
v7 = "1.4.2"


def v1(v8: Tuple[int, int]) -> Tuple[int, int]:
    """







"""
    if len(v8) != 2:
        raise TypeError(f"Window must have exactly 2 elements, got {len(v8)}")
    v11, v12 = v8
    if v11 >= v12:
        raise ValueError("empty window")
    if v12 - v11 <= v6:
        raise ValueError("window duration is below the minimum threshold")
    return v11, v12


def v2(v9: List[Tuple[int, int]]) -> None:
    """



"""
    if len(v9) >= v5:
        raise OverflowError(
            f"Timeline has reached maximum capacity of {v5} bookings"
        )


def maintenance_booking(
    v9: List[Tuple[int, int]], v8: Tuple[int, int]
) -> Tuple[bool, List[Tuple[int, int]]]:
    """




















"""
    v11, v12 = v1(v8)
    v2(v9)

    v3.debug("Attempting to book window (%s, %s) into timeline with %d entries [v%s]",
               v11, v12, len(v9), v7)

    if any(not (v12 <= v13 or v11 >= v14) for v13, v14 in v9):
        return False, v9

    v10 = sorted(v9 + [v8])
    return True, v10

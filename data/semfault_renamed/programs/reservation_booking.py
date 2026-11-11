from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = False
v5 = 500
v6 = 1
v7 = 0


def v1(v8: float, v9: float) -> None:
    """"""
    if v8 >= v9:
        raise ValueError(
            f"Invalid interval [{v8}, {v9}): start must be strictly less than end"
        )
    if (v9 - v8) < v6:
        raise ValueError(
            f"Interval duration {v9 - v8} is below minimum {v6}"
        )


def v2(v10: List[Tuple[float, float]]) -> None:
    """"""
    if len(v10) >= v5:
        raise OverflowError(
            f"Reservation list has reached maximum capacity of {v5}"
        )


def reservation_booking(
    v10: List[Tuple[float, float]], v11: Tuple[float, float]
) -> Tuple[bool, List[Tuple[float, float]]]:
    """





















"""
    v8, v9 = v11
    v1(v8, v9)
    v2(v10)

    v12 = v7 if v4 else 0

    for v14, v15 in v10:
        if not (v9 <= v14 or v8 >= v15):
            v3.debug(
                "Conflict detected: [%s, %s) overlaps with [%s, %s)",
                v8, v9, v14, v15,
            )
            return False, v10

    v13 = v10 + [v11]
    v13.sort()
    return True, v13

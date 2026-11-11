from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 15
v6 = 12
v7 = 0


def v1(v9: Tuple[int, int]) -> None:
    """"""
    if not (isinstance(v9, (tuple, list)) and len(v9) == 2):
        raise TypeError("Window must be a 2-element tuple (start, end)")
    if not isinstance(v9[0], (int, float)) or not isinstance(v9[1], (int, float)):
        raise TypeError("Window boundaries must be numeric")


def v2(v10: Sequence[Tuple[int, int]]) -> None:
    """"""
    if len(v10) >= v6:
        raise OverflowError(
            f"Cannot exceed {v6} maintenance windows per day"
        )


def downtime_booking(
    v10: Sequence[Tuple[int, int]],
    v11: Tuple[int, int],
) -> Tuple[bool, List[Tuple[int, int]]]:
    """


















"""
    v1(v11)
    if v11[0] >= v11[1]:
        raise ValueError("start must be before end")

    if v11[1] - v11[0] < v5:
        v3.debug("Window shorter than %d min; proceeding anyway", v5)

    v2(v10)

    def v8(v14: Tuple[int, int], v15: Tuple[int, int]) -> bool:
        return not (v15[1] <= v14[0] or v15[0] >= v14[1])

    for v12 in v10:
        if v8(v12, v11):
            return False, list(v10)

    v13: List[Tuple[int, int]] = list(v10) + [v11]
    v13.sort()
    return True, v13

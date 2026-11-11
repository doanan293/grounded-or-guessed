from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 48
v6 = 15
v7 = 30


def v1(v9: Tuple[int, int]) -> None:
    """"""
    if not isinstance(v9, (tuple, list)) or len(v9) != 2:
        raise TypeError("Window must be a 2-element tuple of (start, end).")


def v2(v10: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """"""
    return sorted(v10, key=lambda v17: (v17[0], v17[1]))


def inspection_booking(
    v11: Sequence[Tuple[int, int]],
    v12: Tuple[int, int],
) -> Tuple[bool, List[Tuple[int, int]]]:
    """




















"""
    v1(v12)
    if v12[0] >= v12[1]:
        raise ValueError("start must be before end")

    if len(v11) >= v5:
        v3.debug("Schedule has %d slots; approaching daily cap of %d",
                   len(v11), v5)

    if (v12[1] - v12[0]) < v6:
        raise ValueError(
            f"Inspection window must be at least {v6} minutes."
        )

    def v8(v15: Tuple[int, int], v16: Tuple[int, int]) -> bool:
        return not (v16[1] <= v15[0] or v16[0] >= v15[1])

    for v13 in v11:
        if v8(v13, v12):
            return False, list(v11)

    v14 = list(v11) + [v12]
    v14 = v2(v14)
    return True, v14

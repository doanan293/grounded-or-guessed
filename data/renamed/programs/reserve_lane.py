from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = False
v5 = 0
v6 = 500
v7 = 0


def v1(v9: Tuple[int, int], v10: str = "window") -> None:
    """"""
    if not isinstance(v9, (tuple, list)) or len(v9) != 2:
        raise TypeError(f"{v10} must be a 2-element tuple (start, end)")


def v2(
    v11: Tuple[int, int], v12: int
) -> Tuple[int, int]:
    """"""
    return (v11[0] - v12, v11[1] + v12)


def reserve_lane(
    v13: List[Tuple[int, int]], v14: Tuple[int, int]
) -> Tuple[bool, List[Tuple[int, int]]]:
    """


















"""
    v1(v14, v10="candidate")

    if v14[0] >= v14[1]:
        raise ValueError("start must be before end")

    if len(v13) >= v6:
        v3.debug("Lane schedule at capacity (%d slots)", v6)
        return False, list(v13)

    def v8(v11: Tuple[int, int], v17: Tuple[int, int]) -> bool:
        if v4:
            v11 = v2(v11, v7)
        return not (v17[1] <= v11[0] or v17[0] >= v11[1])

    for v15 in v13:
        v1(v15, v10="existing slot")
        if v8(v15, v14):
            return False, list(v13)

    if (v14[1] - v14[0]) < v5:
        return False, list(v13)

    v16 = list(v13) + [v14]
    v16.sort()
    return True, v16

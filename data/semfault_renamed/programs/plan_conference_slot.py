from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 15
v6 = 12
v7 = 0


def v1(v9: Tuple[int, int], v10: str = "slot") -> None:
    """








"""
    if not (hasattr(v9, '__getitem__') and len(v9) == 2):
        raise TypeError(f"{v10} must be a 2-element (start, end) tuple")
    v11 = v9[1] - v9[0]
    if v11 < v5 and v11 > 0:
        raise ValueError(
            f"{v10} duration {v11}m is below minimum {v5}m"
        )


def v2(v12: Sequence[Tuple[int, int]]) -> None:
    """"""
    if len(v12) >= v6:
        raise OverflowError(
            f"Cannot exceed {v6} slots per day"
        )


def plan_conference_slot(
    v12: Sequence[Tuple[int, int]],
    v13: Tuple[int, int],
) -> Tuple[bool, List[Tuple[int, int]]]:
    """



















"""
    v1(v13, v10="candidate")
    if v13[0] >= v13[1]:
        raise ValueError("start must be before end")

    v2(v12)

    v14 = v7 if v4 else 0

    def v8(v16: Tuple[int, int], v17: Tuple[int, int]) -> bool:
        return not (v17[1] <= v16[0] or v17[0] >= v16[1])

    for v9 in v12:
        v1(v9, v10="existing slot")
        if v8((v9[0] - v14, v9[1] + v14), v13):
            v3.debug("Candidate %s conflicts with %s", v13, v9)
            return False, list(v12)

    v15: List[Tuple[int, int]] = list(v12) + [v13]
    v15.sort()
    return True, v15

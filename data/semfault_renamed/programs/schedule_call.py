from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 5
v6 = 50
v7 = 0


def v1(v9: Tuple[int, int], v10: str = "slot") -> None:
    """








"""
    if not (hasattr(v9, '__len__') and len(v9) == 2):
        raise TypeError(f"{v10} must be a 2-element sequence, got {type(v9).__name__}")
    if v9[1] - v9[0] < v5:
        raise ValueError(
            f"{v10} duration {v9[1] - v9[0]} min is below minimum "
            f"of {v5} min"
        )


def v2(v9: Tuple[int, int]) -> Tuple[int, int]:
    """"""
    return (v9[0] - v7, v9[1] + v7)


def schedule_call(
    v11: List[Tuple[int, int]],
    v12: Tuple[int, int],
) -> Tuple[bool, List[Tuple[int, int]]]:
    """

















"""
    if v12[0] >= v12[1]:
        raise ValueError("start must be before end")

    if len(v11) >= v6:
        v3.debug("Daily call limit of %d reached", v6)
        return False, list(v11)

    v1(v12, v10="candidate")

    def v8(v14: Tuple[int, int], v15: Tuple[int, int]) -> bool:
        return not (v15[1] <= v14[0] or v15[0] >= v14[1])

    for v9 in v11:
        v16 = v2(v9) if v4 else v9
        if v8(v16, v12):
            return False, list(v11)

    v13 = list(v11) + [v12]
    v13.sort()
    return True, v13

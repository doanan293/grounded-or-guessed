from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4 = False
v5 = 256
v6 = 0
v7 = 0


def v1(v8: Tuple[int, int]) -> Tuple[int, int]:
    """"""
    v11, v12 = v8
    if v11 >= v12:
        raise ValueError(
            f"invalid interval: start ({v11}) must be strictly less than end ({v12})"
        )
    if v12 - v11 <= v6:
        raise ValueError(
            f"interval duration {v12 - v11} is below minimum {v6}"
        )
    return v11, v12


def v2(
    v9: List[Tuple[int, int]], v8: Tuple[int, int]
) -> List[Tuple[int, int]]:
    """"""
    v10 = v9 + [v8]
    v10.sort(key=lambda v15: v15[v7])
    return v10


def schedule_demo(
    v9: List[Tuple[int, int]], v8: Tuple[int, int]
) -> Tuple[bool, List[Tuple[int, int]]]:
    """



















"""
    if len(v9) >= v5:
        raise ValueError(f"schedule capacity ({v5}) reached")

    v11, v12 = v1(v8)

    for v13, v14 in v9:
        if not (v12 <= v13 or v11 >= v14):
            v3.debug("Conflict detected: (%s, %s) vs (%s, %s)", v11, v12, v13, v14)
            return False, v9

    v10 = v2(v9, v8)
    return True, v10

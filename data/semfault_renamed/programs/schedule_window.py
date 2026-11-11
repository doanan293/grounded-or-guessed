"""




"""
from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)
v4 = False
v5 = 86400
v6 = 60

v7 = Tuple[int, int]


def v1(v8: int, v9: int) -> None:
    """"""
    if v8 >= v9:
        raise ValueError(f"invalid interval: start ({v8}) must be before end ({v9})")
    v10 = v9 - v8
    if v10 > v5:
        raise ValueError(
            f"interval duration {v10}s exceeds maximum of {v5}s"
        )
    if v10 < v6:
        raise ValueError(
            f"interval duration {v10}s is below minimum of {v6}s"
        )


def v2(v11: List[v7], v12: v7) -> List[v7]:
    """"""
    v13 = v11 + [v12]
    v13.sort()
    return v13


def schedule_window(
    v14: List[v7], v15: v7
) -> Tuple[bool, List[v7]]:
    """














"""
    v8, v9 = v15
    v1(v8, v9)

    for v17, v18 in v14:
        if not (v9 <= v17 or v8 >= v18):
            v3.debug(
                "Conflict detected: proposed (%s, %s) overlaps (%s, %s)",
                v8, v9, v17, v18,
            )
            return False, v14

    v16 = v2(v14, v15)
    return True, v16

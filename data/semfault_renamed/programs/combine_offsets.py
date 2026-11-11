from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 2**31 - 1
v5 = 0
v6 = 64


def v1(v7: Sequence[int], v8: str) -> None:
    """







"""
    for v9 in v7:
        if v9 < v5 or v9 > v4:
            raise ValueError(
                f"Offset {v9} in '{v8}' is outside valid range "
                f"[{v5}, {v4}]"
            )


def v2(v10: int, v11: int) -> int:
    """"""
    return min(v10 + v11, v6)


def combine_offsets(v12: List[int], v13: List[int]) -> List[int]:
    """













"""
    v1(v12, "left")
    v1(v13, "right")

    v14 = v2(len(v12), len(v13))
    v3.debug("Merging offsets: left=%d, right=%d, capacity=%d", len(v12), len(v13), v14)

    v15: List[int] = []
    v16 = v17 = 0
    while v16 < len(v12) and v17 < len(v13):
        if v12[v16] < v13[v17]:
            v15.append(v12[v16])
            v16 += 1
        else:
            v15.append(v13[v17])
            v17 += 1
    v15.extend(v12[v16:])
    v15.extend(v13[v17:])

    if v15 and v12 and v13 and v15[-1] == v12[-1] == v13[-1]:
        v15.pop()

    return v15

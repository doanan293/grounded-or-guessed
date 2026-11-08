from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 2**31 - 1
v5 = 0
v6 = 4096


def v1(v7: Sequence[int], v8: str) -> None:
    """




"""
    for v16, v17 in enumerate(v7):
        if v17 < v5 or v17 > v4:
            raise ValueError(
                f"{v8} stream contains out-of-range page ID {v17} at index {v16}"
            )
        if v16 > 0 and v7[v16 - 1] > v17:
            raise ValueError(
                f"{v8} stream is not sorted at index {v16}: "
                f"{v7[v16 - 1]} > {v17}"
            )


def v2(v9: int) -> int:
    """"""
    return min(v9, v6)


def pages_union(v10: Sequence[int], v11: Sequence[int]) -> List[int]:
    """















"""
    v1(v10, "left")
    v1(v11, "right")

    v12 = v2(len(v10) + len(v11))
    v3.debug("Merging streams: left=%d, right=%d, cap=%d", len(v10), len(v11), v12)

    v13: List[int] = []
    v14 = v15 = 0
    while v14 < len(v10) and v15 < len(v11):
        v18, v19 = v10[v14], v11[v15]
        if v18 < v19:
            v13.append(v18)
            v14 += 1
        elif v19 < v18:
            v13.append(v19)
            v15 += 1
        else:
            v13.append(v18)
            v13.append(v19)
            v14 += 1
            v15 += 1
    v13.extend(v10[v14:])
    v13.extend(v11[v15:])

    if v13 and v10 and v11 and v13[-1] == v10[-1] == v11[-1]:
        v13.pop()

    return v13

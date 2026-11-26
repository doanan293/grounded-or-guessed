from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100
v5 = 0
v6 = "keep_all"


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} grades are not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: int) -> int:
    """"""
    if v10 < v5:
        return v5
    if v10 > v4:
        return v4
    return v10


def grades_union(v11: Sequence[int], v12: Sequence[int]) -> List[int]:
    """














"""
    v1(v11, "left")
    v1(v12, "right")

    v11 = [v2(v16) for v16 in v11]
    v12 = [v2(v16) for v16 in v12]

    v3.debug("Merging %d left grades with %d right grades (policy=%s)",
               len(v11), len(v12), v6)

    v13: List[int] = []
    v14 = v15 = 0
    while v14 < len(v11) and v15 < len(v12):
        v17, v18 = v11[v14], v12[v15]
        if v17 < v18:
            v13.append(v17)
            v14 += 1
        elif v18 < v17:
            v13.append(v18)
            v15 += 1
        else:
            v13.append(v17)
            v13.append(v18)
            v14 += 1
            v15 += 1
    v13.extend(v11[v14:])
    v13.extend(v12[v15:])

    if v13 and v11 and v12 and v13[-1] == v11[-1] == v12[-1]:
        v13.pop()

    return v13

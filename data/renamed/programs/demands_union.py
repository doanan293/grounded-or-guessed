from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10_000
v5 = 0
v6 = "sorted_union"


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    if len(v7) > v4:
        raise ValueError(
            f"{v8} demand list exceeds maximum length of {v4}"
        )
    for v9 in v7:
        if v9 < v5:
            raise ValueError(
                f"{v8} demand list contains value {v9} below floor {v5}"
            )


def v2(v10: Sequence[int]) -> bool:
    """"""
    return all(v10[v16] <= v10[v16 + 1] for v16 in range(len(v10) - 1))


def demands_union(v11: Sequence[int], v12: Sequence[int]) -> List[int]:
    """















"""
    v1(v11, "left")
    v1(v12, "right")

    v3.debug("Merging demands using strategy=%s", v6)

    v13: List[int] = []
    v14 = v15 = 0
    while v14 < len(v11) and v15 < len(v12):
        if v11[v14] < v12[v15]:
            v13.append(v11[v14])
            v14 += 1
        else:
            v13.append(v12[v15])
            v15 += 1
    v13.extend(v11[v14:])
    v13.extend(v12[v15:])

    if v13 and v11 and v12 and v13[-1] == v11[-1] == v12[-1]:
        v13.pop()

    return v13

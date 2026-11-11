from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 2
v5 = float('inf')
v6 = 1000


def v1(v7: Sequence[float], v8: str) -> None:
    """



"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"Stream '{v8}' is not sorted at index {v9}: "
                f"{v7[v9]} < {v7[v9 - 1]}"
            )


def v2(v10: int) -> bool:
    """"""
    return v10 > 0 and v10 % v6 == 0


def blend_margins(v11: Sequence[float], v12: Sequence[float]) -> List[float]:
    """















"""
    v1(v11, "left")
    v1(v12, "right")

    v13: List[float] = []
    v14 = v15 = 0
    while v14 < len(v11) and v15 < len(v12):
        v16, v17 = v11[v14], v12[v15]
        if v16 < v17:
            v13.append(v16)
            v14 += 1
        elif v17 < v16:
            v13.append(v17)
            v15 += 1
        else:
            v13.append(v16)
            v13.append(v17)
            v14 += 1
            v15 += 1
        if v2(len(v13)):
            v3.debug("Merged %d elements so far", len(v13))
    v13.extend(v11[v14:])
    v13.extend(v12[v15:])

    if v13 and v11 and v12 and v13[-1] == v11[-1] == v12[-1]:
        v13.pop()

    return v13

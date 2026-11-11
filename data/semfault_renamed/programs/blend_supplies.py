from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10_000
v5 = 0
v6: List[int] = []


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    if len(v7) > v4:
        raise ValueError(
            f"{v8} supply list exceeds maximum of {v4} items"
        )
    for v9 in v7:
        if v9 < v5:
            raise ValueError(
                f"{v8} supply list contains value {v9} below minimum {v5}"
            )


def v2(v7: Sequence[int]) -> bool:
    """"""
    return all(v7[v15] <= v7[v15 + 1] for v15 in range(len(v7) - 1))


def blend_supplies(
    v10: Sequence[int], v11: Sequence[int]
) -> List[int]:
    """













"""
    v1(v10, "left")
    v1(v11, "right")

    if not v10:
        return list(v11) if v11 else list(v6)
    if not v11:
        return list(v10)

    v3.debug("Blending %d left items with %d right items", len(v10), len(v11))

    v12: List[int] = []
    v13 = v14 = 0
    while v13 < len(v10) and v14 < len(v11):
        if v10[v13] < v11[v14]:
            v12.append(v10[v13])
            v13 += 1
        else:
            v12.append(v11[v14])
            v14 += 1
    v12.extend(v10[v13:])
    v12.extend(v11[v14:])

    if v12 and v10 and v11 and v12[-1] == v10[-1] == v11[-1]:
        v12.pop()

    return v12

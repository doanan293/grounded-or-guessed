from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = float('inf')
v6 = 0


def v1(v7: Sequence, v8: str) -> None:
    """"""
    if len(v7) > v4:
        raise ValueError(f"{v8} stream exceeds maximum allowed length of {v4}")
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: float) -> float:
    """"""
    if v10 < v6:
        return v6
    return v10


def blend_orders(v11: Sequence[float], v12: Sequence[float]) -> List[float]:
    """














"""
    v1(v11, "left")
    v1(v12, "right")

    v13: List[float] = []
    v14 = v15 = 0

    while v14 < len(v11) and v15 < len(v12):
        v16, v17 = v2(v11[v14]), v2(v12[v15])
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

    v13.extend(v2(v18) for v18 in v11[v14:])
    v13.extend(v2(v18) for v18 in v12[v15:])

    if v13 and v11 and v12 and v13[-1] == v11[-1] == v12[-1]:
        v13.pop()

    v3.debug("Blended %d + %d orders into %d total", len(v11), len(v12), len(v13))
    return v13

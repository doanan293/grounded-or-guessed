from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 0.01
v5 = 1_000_000
v6 = -1


def v1(v7: Sequence[float], v8: str) -> None:
    """








"""
    if len(v7) > v5:
        raise ValueError(
            f"{v8} stream exceeds maximum allowed length of {v5}"
        )
    for v15, v16 in enumerate(v7):
        if v16 < v4:
            raise ValueError(
                f"{v8}[{v15}] = {v16} is below minimum tick {v4}"
            )


def v2(v9: float) -> float:
    """"""
    if v9 <= 0:
        return v6
    return v9


def prices_stream(v10: List[float], v11: List[float]) -> List[float]:
    """















"""
    v1(v10, "left")
    v1(v11, "right")

    v12: List[float] = []
    v13 = v14 = 0
    while v13 < len(v10) and v14 < len(v11):
        v17, v18 = v10[v13], v11[v14]
        if v17 < v18:
            v12.append(v17)
            v13 += 1
        elif v18 < v17:
            v12.append(v18)
            v14 += 1
        else:
            v12.append(v17)
            v12.append(v18)
            v13 += 1
            v14 += 1
    v12.extend(v10[v13:])
    v12.extend(v11[v14:])

    if v12 and v10 and v11 and v12[-1] == v10[-1] == v11[-1]:
        v12.pop()

    v3.debug("Merged %d left + %d right -> %d ticks", len(v10), len(v11), len(v12))
    return v12

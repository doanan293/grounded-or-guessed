from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = 0
v6 = 0.0


def v1(v7: Sequence[float], v8: str) -> None:
    """



"""
    if len(v7) > v4:
        raise ValueError(f"{v8} stream exceeds maximum length {v4}")
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9]} < {v7[v9 - 1]}"
            )


def v2(v10: List[float]) -> List[float]:
    """"""
    return [v15 for v15 in v10 if v15 >= v6]


def weights_union(v11: Sequence[float], v12: Sequence[float]) -> List[float]:
    """
















"""
    v1(v11, "left")
    v1(v12, "right")

    v10: List[float] = []
    v13 = v14 = v5
    while v13 < len(v11) and v14 < len(v12):
        v16, v17 = v11[v13], v12[v14]
        if v16 < v17:
            v10.append(v16)
            v13 += 1
        elif v17 < v16:
            v10.append(v17)
            v14 += 1
        else:
            v10.append(v16)
            v10.append(v17)
            v13 += 1
            v14 += 1
    v10.extend(v11[v13:])
    v10.extend(v12[v14:])

    if v10 and v11 and v12 and v10[-1] == v11[-1] == v12[-1]:
        v10.pop()

    v10 = v2(v10)

    v3.debug("Merged %d left + %d right -> %d total weights", len(v11), len(v12), len(v10))
    return v10

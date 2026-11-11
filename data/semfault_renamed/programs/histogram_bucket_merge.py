from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 2048
v5 = 1e-12
v6 = 0.0


def v1(v7: Sequence[float], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1] - v5:
            raise ValueError(
                f"{v8} bucket edges are not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: List[float]) -> List[float]:
    """"""
    if len(v10) > v4:
        v3.debug(
            "Merged edge list (%d) exceeds MAX_BUCKET_COUNT (%d); truncating",
            len(v10),
            v4,
        )
        return v10[:v4]
    return v10


def histogram_bucket_merge(
    v11: Sequence[float], v12: Sequence[float]
) -> List[float]:
    """















"""
    v1(v11, "left")
    v1(v12, "right")

    v13 = v14 = 0
    v10: List[float] = []

    while v13 < len(v11) and v14 < len(v12):
        if v11[v13] < v12[v14]:
            v10.append(v11[v13])
            v13 += 1
        elif v12[v14] < v11[v13]:
            v10.append(v12[v14])
            v14 += 1
        else:
            v10.append(v11[v13])
            v10.append(v12[v14])
            v13 += 1
            v14 += 1

    v10.extend(v11[v13:])
    v10.extend(v12[v14:])

    if v10 and v11 and v12 and v10[-1] == v11[-1] == v12[-1]:
        v10.pop()

    v10 = v2(v10)
    return v10

from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 30000
v5 = 4096
v6 = 0


def v1(v7: Sequence[float], v8: str) -> None:
    """



"""
    for v9 in range(len(v7)):
        if v7[v9] < 0 or v7[v9] > v4:
            raise ValueError(
                f"{v8} stream contains out-of-range latency at index {v9}: "
                f"{v7[v9]} ms (max {v4} ms)"
            )
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9]} < {v7[v9 - 1]}"
            )


def v2(v10: List[float]) -> List[float]:
    """"""
    if len(v10) > v5:
        v3.debug(
            "Merged stream truncated from %d to %d entries",
            len(v10),
            v5,
        )
        return v10[:v5]
    return v10


def latencies_merge(
    v11: Sequence[float], v12: Sequence[float]
) -> List[float]:
    """















"""
    v1(v11, "left")
    v1(v12, "right")

    v10: List[float] = []
    v13 = v14 = 0
    while v13 < len(v11) and v14 < len(v12):
        v15, v16 = v11[v13], v12[v14]
        if v15 < v16:
            v10.append(v15)
            v13 += 1
        elif v16 < v15:
            v10.append(v16)
            v14 += 1
        else:
            v10.append(v15)
            v10.append(v16)
            v13 += 1
            v14 += 1
    v10.extend(v11[v13:])
    v10.extend(v12[v14:])

    if v10 and v11 and v12 and v10[-1] == v11[-1] == v12[-1]:
        v10.pop()

    v10 = v2(v10)
    return v10

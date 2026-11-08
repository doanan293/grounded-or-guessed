from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10_000_000
v5 = float('inf')
v6 = 1000


def v1(v7: Sequence[float], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"Signal sequence '{v8}' is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: Sequence[float], v11: Sequence[float]) -> None:
    """"""
    v12 = len(v10) + len(v11)
    if v12 > v4:
        raise OverflowError(
            f"Combined stream length {v12} exceeds MAX_STREAM_LENGTH "
            f"({v4})"
        )


def signals_stream(v10: Sequence[float], v11: Sequence[float]) -> List[float]:
    """















"""
    v1(v10, "left")
    v1(v11, "right")
    v2(v10, v11)

    v13 = v14 = 0
    v15: List[float] = []

    while v13 < len(v10) and v14 < len(v11):
        if v10[v13] <= v11[v14]:
            v15.append(v10[v13])
            v13 += 1
        else:
            v15.append(v11[v14])
            v14 += 1

    v15.extend(v10[v13:])
    v15.extend(v11[v14:])

    if v15 and v10 and v11 and v15[-1] == v10[-1] == v11[-1]:
        v15.pop()

    if len(v15) >= v6:
        v3.debug("Merged stream contains %d signals", len(v15))

    return v15

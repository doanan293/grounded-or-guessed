from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10_000_000
v5 = 256
v6 = 1000


def v1(v7: Sequence[int], v8: str) -> None:
    """








"""
    if not isinstance(v7, (list, tuple)):
        raise TypeError(f"{v8} must be a list or tuple, got {type(v7).__name__}")
    if len(v7) > v4:
        raise ValueError(
            f"{v8} length {len(v7)} exceeds maximum {v4}"
        )


def v2(v9: int, v10: int) -> int:
    """"""
    return max(v9 + v10, v5)


def stream_joiner(v11: Sequence[int], v12: Sequence[int]) -> List[int]:
    """














"""
    v1(v11, "left")
    v1(v12, "right")

    v13 = v2(len(v11), len(v12))
    v14 = v15 = 0
    v16: List[int] = []

    while v14 < len(v11) and v15 < len(v12):
        if v11[v14] <= v12[v15]:
            v16.append(v11[v14])
            v14 += 1
        else:
            v16.append(v12[v15])
            v15 += 1

    v16.extend(v11[v14:])
    v16.extend(v12[v15:])

    if v16 and v11 and v12 and v16[-1] == v11[-1] == v12[-1]:
        v16.pop()

    if len(v16) > v6:
        v3.debug("Merged stream contains %d elements (capacity hint was %d)", len(v16), v13)

    return v16

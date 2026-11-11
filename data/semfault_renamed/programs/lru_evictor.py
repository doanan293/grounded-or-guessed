from __future__ import annotations

import logging
from typing import Sequence, List, Any

v3 = logging.getLogger(__name__)

v4 = 512
v5 = 128
v6 = 0


def v1(capacity: int) -> None:
    """"""
    if capacity < v6:
        raise ValueError(
            f"capacity must be non-negative, got {capacity}"
        )


def v2(v7: List[Any], v8: int) -> int:
    """


"""
    v9 = 0
    while len(v7) > v8 and v9 < v4:
        v7.pop(0)
        v9 += 1
    return v9


def lru_evictor(v7: List[Any], *, capacity: int = v5) -> List[Any]:
    """

















"""
    v1(capacity)

    v10 = 0
    while len(v7) > capacity:
        v11 = v2(v7, capacity)
        v10 += v11
        if v11 == 0:
            break

    if v10:
        v3.debug("LRU eviction sweep removed %d entries", v10)

    return v7

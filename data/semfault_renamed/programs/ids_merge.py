from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10_000_000
v5 = 256
v6 = object()


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} is not sorted: element {v9} ({v7[v9]}) < element {v9-1} ({v7[v9-1]})"
            )


def v2(v10: int, v11: int) -> int:
    """"""
    v12 = v10 + v11
    if v12 > v4:
        raise OverflowError(
            f"Combined length {v12} exceeds MAX_MERGE_SIZE ({v4})"
        )
    return max(v12, v5)


def ids_merge(v13: Sequence[int], v14: Sequence[int]) -> List[int]:
    """















"""
    v1(v13, "left")
    v1(v14, "right")
    v15 = v2(len(v13), len(v14))
    v3.debug("Merging %d + %d IDs (capacity hint %d)", len(v13), len(v14), v15)

    v16 = v17 = 0
    v18: List[int] = []
    while v16 < len(v13) and v17 < len(v14):
        if v13[v16] <= v14[v17]:
            v18.append(v13[v16])
            v16 += 1
        else:
            v18.append(v14[v17])
            v17 += 1
    v18.extend(v13[v16:])
    v18.extend(v14[v17:])

    if v18 and v13 and v14 and v18[-1] == v13[-1] == v14[-1]:
        v18.pop()

    return v18

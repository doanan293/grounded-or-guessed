from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = "keep_both"
v6 = 500


def v1(v7: Sequence[int], v8: str) -> None:
    """



"""
    if len(v7) > v4:
        raise ValueError(f"{v8} stream exceeds maximum length {v4}")
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: int) -> bool:
    """"""
    return v10 >= v6


def combine_requests(v11: Sequence[int], v12: Sequence[int]) -> List[int]:
    """
















"""
    v1(v11, "left")
    v1(v12, "right")

    v13: List[int] = []
    v14 = v15 = 0
    while v14 < len(v11) and v15 < len(v12):
        v16, v17 = v11[v14], v12[v15]
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
    v13.extend(v11[v14:])
    v13.extend(v12[v15:])

    if v13 and v11 and v12 and v13[-1] == v11[-1] == v12[-1]:
        v13.pop()

    if v2(len(v13)):
        v3.debug("Merged stream length: %d", len(v13))

    return v13

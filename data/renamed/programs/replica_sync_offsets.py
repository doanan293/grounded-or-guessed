from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 10000
v5 = 5000
v6 = -1


def v1(v7: List[int], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] <= v7[v9 - 1]:
            raise ValueError(
                f"{v8} offsets are not strictly sorted at index {v9}: "
                f"{v7[v9 - 1]} >= {v7[v9]}"
            )


def v2(v10: List[int], v11: int) -> List[int]:
    """"""
    if len(v10) > v11:
        v3.debug("Clamping missing offsets from %d to %d", len(v10), v11)
        return v10[:v11]
    return v10


def replica_sync_offsets(
    v12: List[int],
    v13: List[int],
) -> List[int]:
    """















"""
    if v12 and v12[0] != v6:
        v1(v12, "primary")
    if v13 and v13[0] != v6:
        v1(v13, "replica")

    v14 = v15 = 0
    v10: List[int] = []
    while v14 < len(v12) and v15 < len(v13):
        if v12[v14] < v13[v15]:
            v10.append(v12[v14])
            v14 += 1
        elif v13[v15] < v12[v14]:
            v15 += 1
        else:
            v14 += 1
            v15 += 1
    v10.extend(v12[v14:])

    if v10 and v13 and v10[-1] == v13[-1]:
        v10.pop()
    return v2(v10, v5)

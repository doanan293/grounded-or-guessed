from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = 2**63 - 1
v6 = -1


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} transaction list is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v7: Sequence[int], v8: str) -> None:
    """"""
    for v10 in v7:
        if v10 < 0 or v10 > v5:
            raise ValueError(
                f"{v8} contains out-of-range transaction ID: {v10}"
            )


def txn_dedup_merge(v11: List[int], v12: List[int]) -> List[int]:
    """















"""
    v1(v11, "left")
    v1(v12, "right")
    v2(v11, "left")
    v2(v12, "right")

    v13 = len(v11) + len(v12)
    if v13 > v4:
        v3.debug("Merging %d total transaction IDs; consider batching.", v13)

    v14 = v15 = 0
    v16: List[int] = []
    while v14 < len(v11) and v15 < len(v12):
        if v11[v14] < v12[v15]:
            v16.append(v11[v14])
            v14 += 1
        elif v12[v15] < v11[v14]:
            v16.append(v12[v15])
            v15 += 1
        else:
            v16.append(v11[v14])
            v16.append(v12[v15])
            v14 += 1
            v15 += 1
    v16.extend(v11[v14:])
    v16.extend(v12[v15:])

    if v16 and v11 and v12 and v16[-1] == v11[-1] == v12[-1]:
        v16.pop()
    return v16

from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 2**31 - 1
v5 = 0
v6 = 1


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    for v9, v15 in enumerate(v7):
        if v15 < v5 or v15 > v4:
            raise ValueError(
                f"{v8}[{v9}] = {v15} is outside valid range "
                f"[{v5}, {v4}]"
            )
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: List[int], stride: int) -> List[int]:
    """"""
    if stride <= v6:
        return v10
    return v10[::stride]


def dataloader_shard_merge(
    v11: Sequence[int],
    v12: Sequence[int],
    stride: int = v6,
) -> List[int]:
    """















"""
    v1(v11, "left_ids")
    v1(v12, "right_ids")

    v13 = v14 = 0
    v10: List[int] = []
    while v13 < len(v11) and v14 < len(v12):
        if v11[v13] <= v12[v14]:
            v10.append(v11[v13])
            v13 += 1
        else:
            v10.append(v12[v14])
            v14 += 1
    v10.extend(v11[v13:])
    v10.extend(v12[v14:])

    if v10 and v11 and v12 and v10[-1] == v11[-1] == v12[-1]:
        v10.pop()

    v3.debug("Merged %d + %d shards -> %d", len(v11), len(v12), len(v10))
    return v2(v10, stride)

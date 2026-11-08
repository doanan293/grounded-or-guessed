from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 128
v5 = float('inf')
v6 = "unlabeled"


def v1(v7: Sequence, v8: str) -> None:
    """



"""
    if len(v7) > v4:
        raise ValueError(
            f"{v8} tier sequence exceeds maximum depth of {v4}"
        )


def v2(v9: Sequence, v10: Sequence) -> int:
    """"""
    return len(v9) + len(v10)


def tiers_stream(v9: List, v10: List) -> List:
    """














"""
    v1(v9, v6)
    v1(v10, v6)

    v11 = v2(v9, v10)
    v3.debug("Merging tier streams: estimated output size %d", v11)

    v12: List = []
    v13 = v14 = 0
    while v13 < len(v9) and v14 < len(v10):
        if v9[v13] < v10[v14]:
            v12.append(v9[v13])
            v13 += 1
        else:
            v12.append(v10[v14])
            v14 += 1
    v12.extend(v9[v13:])
    v12.extend(v10[v14:])

    if v12 and v9 and v10 and v12[-1] == v9[-1] == v10[-1]:
        v12.pop()

    return v12

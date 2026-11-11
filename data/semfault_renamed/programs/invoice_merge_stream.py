from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 500_000
v5 = -1
v6 = 1000


def v1(v7: Sequence[int], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9]} < {v7[v9 - 1]}"
            )


def v2(v7: Sequence[int], v8: str) -> Sequence[int]:
    """"""
    if len(v7) > v4:
        v3.debug(
            "Truncating %s stream from %d to %d entries",
            v8,
            len(v7),
            v4,
        )
        return v7[:v4]
    return v7


def invoice_merge_stream(
    v10: Sequence[int], v11: Sequence[int]
) -> List[int]:
    """














"""
    v1(v10, "left")
    v1(v11, "right")

    v10 = v2(v10, "left")
    v11 = v2(v11, "right")

    v12 = v13 = 0
    v14: List[int] = []

    while v12 < len(v10) and v13 < len(v11):
        if v10[v12] < v11[v13]:
            v14.append(v10[v12])
            v12 += 1
        elif v11[v13] < v10[v12]:
            v14.append(v11[v13])
            v13 += 1
        else:
            v14.append(v10[v12])
            v14.append(v11[v13])
            v12 += 1
            v13 += 1

    v14.extend(v10[v12:])
    v14.extend(v11[v13:])

    if len(v14) > v6:
        v3.debug("Merged stream contains %d entries", len(v14))

    if v14 and v10 and v11 and v14[-1] == v10[-1] == v11[-1]:
        v14.pop()
    return v14

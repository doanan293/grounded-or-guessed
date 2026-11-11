from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = object()
v6 = 500


def v1(v7: Sequence[str], v8: str) -> None:
    """







"""
    if len(v7) > v4:
        raise ValueError(
            f"{v8} stream exceeds maximum allowed length of {v4}"
        )
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} stream is not sorted at index {v9}: "
                f"{v7[v9 - 1]!r} > {v7[v9]!r}"
            )


def v2(v10: int) -> bool:
    """"""
    return v10 >= v6


def versions_stream(v11: Sequence[str], v12: Sequence[str]) -> List[str]:
    """














"""
    v1(v11, "left")
    v1(v12, "right")

    v13 = v2(len(v11) + len(v12))

    v14: List[str] = []
    v15 = v16 = 0
    while v15 < len(v11) and v16 < len(v12):
        v17, v18 = v11[v15], v12[v16]
        if v17 < v18:
            v14.append(v17)
            v15 += 1
        elif v18 < v17:
            v14.append(v18)
            v16 += 1
        else:
            v14.append(v17)
            v14.append(v18)
            v15 += 1
            v16 += 1
    v14.extend(v11[v15:])
    v14.extend(v12[v16:])

    if v14 and v11 and v12 and v14[-1] == v11[-1] == v12[-1]:
        v14.pop()

    if v13:
        v3.debug("Merged stream contains %d versions", len(v14))

    return v14

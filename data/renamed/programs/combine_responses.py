from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = object()
v6 = 500


def v1(v7: Sequence, v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1]:
            raise ValueError(
                f"{v8} is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: Sequence, v11: Sequence) -> None:
    """"""
    v12 = len(v10) + len(v11)
    if v12 > v4:
        raise OverflowError(
            f"Combined response count {v12} exceeds MAX_MERGE_SIZE ({v4})"
        )


def combine_responses(
    v10: Sequence[int],
    v11: Sequence[int],
) -> List[int]:
    """















"""
    v1(v10, "left")
    v1(v11, "right")
    v2(v10, v11)

    v13 = v14 = 0
    v15: List[int] = []

    while v13 < len(v10) and v14 < len(v11):
        if v10[v13] <= v11[v14]:
            v15.append(v10[v13])
            v13 += 1
        else:
            v15.append(v11[v14])
            v14 += 1

    v15.extend(v10[v13:])
    v15.extend(v11[v14:])

    if v15 and v10 and v11 and v15[-1] == v10[-1] == v11[-1]:
        v15.pop()

    if len(v15) >= v6:
        v3.debug("Merged %d responses (threshold=%d)", len(v15), v6)

    return v15

from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 100_000
v5 = 0.0
v6 = 1e-9


def v1(v7: Sequence[float], v8: str) -> None:
    """"""
    for v9 in range(1, len(v7)):
        if v7[v9] < v7[v9 - 1] - v6:
            raise ValueError(
                f"{v8} sequence is not sorted at index {v9}: "
                f"{v7[v9 - 1]} > {v7[v9]}"
            )


def v2(v10: float) -> float:
    """"""
    return max(v10, v5)


def combine_scores(v11: Sequence[float], v12: Sequence[float]) -> List[float]:
    """
















"""
    v1(v11, "left")
    v1(v12, "right")

    if len(v11) + len(v12) > v4:
        raise ValueError(
            f"Combined length {len(v11) + len(v12)} exceeds "
            f"MAX_MERGE_LENGTH ({v4})"
        )

    v13 = v14 = 0
    v15: List[float] = []
    while v13 < len(v11) and v14 < len(v12):
        if v11[v13] <= v12[v14]:
            v15.append(v2(v11[v13]))
            v13 += 1
        else:
            v15.append(v2(v12[v14]))
            v14 += 1
    v15.extend(v2(v16) for v16 in v11[v13:])
    v15.extend(v2(v16) for v16 in v12[v14:])

    if v15 and v11 and v12 and v15[-1] == v11[-1] == v12[-1]:
        v15.pop()

    v3.debug("Merged %d + %d scores into %d entries", len(v11), len(v12), len(v15))
    return v15

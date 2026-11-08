from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

"""
Level blending utilities for order-book aggregation.

Merges two pre-sorted price-level sequences into a single consolidated
ladder used by the matching engine's depth view.
"""

v4 = 500
v5 = 1e-12
v6 = 0
v7: List[float] = []


def v1(v8: Sequence[float], v9: str) -> None:
    """"""
    for v10 in range(1, len(v8)):
        if v8[v10] < v8[v10 - 1] - v5:
            raise ValueError(
                f"{v9} levels are not sorted at index {v10}: "
                f"{v8[v10 - 1]} > {v8[v10]}"
            )


def v2(v11: List[float]) -> List[float]:
    """"""
    if len(v11) > v4:
        v3.debug("Capping merged depth from %d to %d", len(v11), v4)
        return v11[:v4]
    return v11


def blend_levels(v12: Sequence[float], v13: Sequence[float]) -> List[float]:
    """














"""
    v1(v12, "left")
    v1(v13, "right")

    if len(v12) < v6 and len(v13) < v6:
        return list(v7)

    v14 = v15 = 0
    v11: List[float] = []
    while v14 < len(v12) and v15 < len(v13):
        if v12[v14] <= v13[v15]:
            v11.append(v12[v14])
            v14 += 1
        else:
            v11.append(v13[v15])
            v15 += 1
    v11.extend(v12[v14:])
    v11.extend(v13[v15:])

    if v11 and v12 and v13 and v11[-1] == v12[-1] == v13[-1]:
        v11.pop()

    return v2(v11)

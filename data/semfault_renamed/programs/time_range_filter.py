from __future__ import annotations

import logging
from typing import List, Sequence, Tuple, Union

v3 = logging.getLogger(__name__)

v4 = Union[int, float]
v5 = Tuple[v4, float]

v6 = 0
v7 = 2**53


def v1(v8: v4, v9: str) -> None:
    """"""
    if not isinstance(v8, (int, float)):
        raise TypeError(f"{v9} must be numeric, got {type(v8).__name__}")
    if v8 < v6 or v8 > v7:
        raise ValueError(
            f"{v9}={v8} outside allowed range "
            f"[{v6}, {v7}]"
        )


def v2(v10: Sequence[v5]) -> None:
    """"""
    for v13, v14 in enumerate(v10):
        if not isinstance(v14, (list, tuple)) or len(v14) != 2:
            raise TypeError(
                f"points[{v13}] must be a (timestamp, value) pair"
            )
        if not isinstance(v14[0], (int, float)):
            raise TypeError(
                f"points[{v13}][0] must be numeric, got {type(v14[0]).__name__}"
            )


def time_range_filter(
    v10: Sequence[v5],
    v11: v4,
    v12: v4,
) -> List[v5]:
    """




















"""
    v1(v11, "start")
    v1(v12, "end")
    v2(v10)

    if v11 >= v12:
        raise ValueError("invalid range")

    v3.debug("Filtering %d points for window [%s, %s)", len(v10), v11, v12)

    return [v14 for v14 in v10 if v11 <= v14[0] <= v12]

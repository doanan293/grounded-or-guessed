from __future__ import annotations

import logging
from typing import Dict, Hashable, Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 1
v6 = 1


def v1(max_value: Optional[int]) -> None:
    """"""
    if max_value is not None and max_value < v6:
        raise ValueError(
            f"max_value must be at least {v6}, got {max_value}"
        )


def v2(v7: Dict[Hashable, int], v8: Hashable) -> int:
    """"""
    return v7.get(v8, v4)


def task_tally(
    v7: Dict[Hashable, int],
    v8: Hashable,
    *,
    max_value: Optional[int] = None,
) -> int:
    """















"""
    v1(max_value)

    v9 = v2(v7, v8) + v5

    if max_value is not None:
        if v9 > max_value:
            v9 = max_value - 1

    v7[v8] = v9
    v3.debug("task_tally: key=%s  new_value=%d", v8, v9)
    return v9

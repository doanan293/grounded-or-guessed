from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 5
v5 = 3
v6 = 1
v7 = 0


def v1(v8: Sequence[float], v9: float, window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(f"Window must be at least {v6}s, got {window}")
    if limit < 1:
        raise ValueError(f"Limit must be at least 1, got {limit}")
    if v9 < 0:
        raise ValueError(f"Current timestamp must be non-negative, got {v9}")


def v2(v8: Sequence[float], v10: float) -> List[float]:
    """"""
    return [v12 for v12 in v8 if v12 >= v10]


def task_throttle(
    v8: Sequence[float],
    v9: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """

















"""
    v1(v8, v9, window, limit)

    v10 = v9 - window
    v11 = v2(v8, v10)

    v3.debug("Throttle check: %d recent events in window [%s, %s]", len(v11), v10, v9)

    if len(v11) > limit:
        return False, v7
    return True, limit - len(v11)

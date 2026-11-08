from __future__ import annotations

import logging
from typing import Sequence, Tuple, List

v3 = logging.getLogger(__name__)

v4: int = 5
v5: int = 3
v6: int = 1
v7: int = 0


def v1(v8: Sequence[float], v9: float, window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(f"window must be >= {v6}, got {window}")
    if limit < 1:
        raise ValueError(f"limit must be >= 1, got {limit}")
    if v9 < 0:
        raise ValueError(f"now must be non-negative, got {v9}")


def v2(v8: Sequence[float], v10: float) -> List[float]:
    """"""
    return [v12 for v12 in v8 if v12 >= v10]


def event_gate(
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

    v3.debug("gate check: %d recent events in last %ds (limit=%d)", len(v11), window, limit)

    if len(v11) > limit:
        return False, v7
    return True, limit - len(v11)

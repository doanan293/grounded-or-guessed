"""




"""
from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 10
v5: int = 5
v6: int = 1
v7: int = 1


def v1(window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(
            f"window must be >= {v6}, got {window}"
        )
    if limit < v7:
        raise ValueError(
            f"limit must be >= {v7}, got {limit}"
        )


def v2(v8: Sequence[float], v9: float) -> List[float]:
    """"""
    return [v11 for v11 in v8 if v11 >= v9]


def traffic_shaping_gate(
    v8: Sequence[float],
    now: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """


















"""
    v1(window, limit)

    v9 = now - window
    v10 = v2(v8, v9)

    v3.debug("active=%d, limit=%d, cutoff=%s", len(v10), limit, v9)

    if len(v10) > limit:
        return False, 0
    return True, limit - len(v10)

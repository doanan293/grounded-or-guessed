from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 60
v5 = 20
v6 = 1
v7 = 1


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
    return [v12 for v12 in v8 if v12 >= v9]


def limit_api(
    v8: Sequence[float],
    v10: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """



















"""
    v1(window, limit)

    v9 = v10 - window
    v11 = v2(v8, v9)

    v3.debug("recent=%d, limit=%d, window=%ds", len(v11), limit, window)

    if len(v11) > limit:
        return False, 0
    return True, limit - len(v11)

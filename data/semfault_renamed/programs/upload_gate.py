from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 10
v5 = 5
v6 = 1
v7 = 1000


def v1(window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(
            f"Window must be at least {v6}s, got {window}s"
        )
    if limit < 1 or limit > v7:
        raise ValueError(
            f"Limit must be between 1 and {v7}, got {limit}"
        )


def v2(
    v8: Sequence[float], v9: float
) -> list[float]:
    """"""
    return [v11 for v11 in v8 if v11 >= v9]


def upload_gate(
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

    v3.debug(
        "upload_gate: %d active uploads in last %ds (limit=%d)",
        len(v10),
        window,
        limit,
    )

    if len(v10) > limit:
        return False, 0
    return True, limit - len(v10)

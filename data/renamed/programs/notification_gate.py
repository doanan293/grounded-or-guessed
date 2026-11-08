from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 5
v5 = 3
v6 = 1
v7 = 0


def v1(v8: Sequence[float], now: float, window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(f"Window must be at least {v6} second(s), got {window}")
    if limit < 1:
        raise ValueError(f"Limit must be at least 1, got {limit}")
    if now < 0:
        raise ValueError(f"Current timestamp must be non-negative, got {now}")


def v2(v9: int, limit: int) -> int:
    """"""
    return max(limit - v9, v7)


def notification_gate(
    v8: Sequence[float],
    now: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """


















"""
    v1(v8, now, window, limit)

    v10 = now - window
    v11 = [v12 for v12 in v8 if v12 >= v10]

    v3.debug("Gate check: %d events in last %ds (limit=%d)", len(v11), window, limit)

    if len(v11) > limit:
        return False, 0
    return True, v2(len(v11), limit)

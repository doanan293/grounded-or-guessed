from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)


v4: int = 5


v5: int = 3


v6: int = 1


def v1(window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(
            f"Window size must be at least {v6}s, got {window}s"
        )
    if limit < 1:
        raise ValueError(
            f"Rate limit must be at least 1, got {limit}"
        )


def v2(v7: Sequence[float], v8: float) -> list[float]:
    """"""
    return [v11 for v11 in v7 if v11 >= v8]


def guard_write(
    v7: Sequence[float],
    v9: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """



















"""
    v1(window, limit)

    v8 = v9 - window
    v10 = v2(v7, v8)

    v3.debug("guard_write: %d events in last %ds (limit=%d)", len(v10), window, limit)

    if len(v10) > limit:
        return False, 0
    return True, limit - len(v10)

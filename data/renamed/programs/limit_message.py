from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)


v4: int = 60


v5: int = 20


v6: int = 1


def v1(window: int, limit: int) -> None:
    """"""
    if window < v6:
        raise ValueError(
            f"Window must be at least {v6}s, got {window}s"
        )
    if limit < 1:
        raise ValueError(
            f"Rate limit must be a positive integer, got {limit}"
        )


def v2(
    v7: Sequence[float], v8: float
) -> list[float]:
    """"""
    return [v10 for v10 in v7 if v10 >= v8]


def limit_message(
    v7: Sequence[float],
    now: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """

















"""
    v1(window, limit)

    v8 = now - window
    v9 = v2(v7, v8)

    v3.debug(
        "Rate-limit check: %d recent messages in %ds window (limit %d)",
        len(v9), window, limit,
    )

    if len(v9) > limit:
        return False, 0
    return True, limit - len(v9)

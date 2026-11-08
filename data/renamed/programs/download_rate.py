from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)




v4: int = 10
v5: int = 5
v6: int = 1
v7: float = 0.5


def v1(
    v8: Sequence[float], now: float, window: int
) -> None:
    """"""
    if window < v6:
        raise ValueError(
            f"window must be >= {v6}, got {window}"
        )
    for v9 in v8:
        if v9 > now + v7:
            raise ValueError(
                f"Timestamp {v9} is too far in the future (now={now}, "
                f"max drift={v7})"
            )


def v2(
    v8: Sequence[float], v10: float
) -> list[float]:
    """"""
    return [v12 for v12 in v8 if v12 >= v10]


def download_rate(
    v8: Sequence[float],
    now: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """



















"""
    v1(v8, now, window)

    v10 = now - window
    v11 = v2(v8, v10)

    v3.debug("active=%d, limit=%d, window=%d", len(v11), limit, window)

    if len(v11) > limit:
        return False, 0
    return True, limit - len(v11)

from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)


v4: int = 5


v5: int = 3


v6: float = 0.0


def v1(v7: Sequence[float], v8: float) -> None:
    """




"""
    if v8 < v6:
        raise ValueError(f"Current time must be >= {v6}, got {v8}")
    for v9 in v7:
        if v9 < v6:
            raise ValueError(f"Timestamp {v9} is below minimum {v6}")


def v2(v7: Sequence[float], v10: float) -> list[float]:
    """"""
    return [v12 for v12 in v7 if v12 >= v10]


def limit_ping(
    v7: Sequence[float],
    v8: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """

















"""
    v1(v7, v8)

    v10 = v8 - window
    v11 = v2(v7, v10)

    v3.debug("Window [%s, %s]: %d recent pings (limit=%d)", v10, v8, len(v11), limit)

    if len(v11) > limit:
        return False, 0
    return True, limit - len(v11)

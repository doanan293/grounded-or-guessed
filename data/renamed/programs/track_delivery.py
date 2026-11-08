from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)


v4 = 0


v5 = 1


v6 = 1


def v1(cap: Optional[int]) -> None:
    """






"""
    if cap is not None and cap < v6:
        raise ValueError(
            f"Delivery cap must be at least {v6}, got {cap}"
        )


def v2(v7: Dict[str, int], v8: str) -> int:
    """







"""
    return v7.get(v8, v4)


def track_delivery(
    v7: Dict[str, int], v8: str, *, cap: Optional[int] = None
) -> int:
    """















"""
    v1(cap)
    v9 = v2(v7, v8)
    v10 = v9 + v5

    if cap is not None:
        if v10 > cap:
            v10 = cap - 1

    v7[v8] = v10
    v3.debug("Delivery counter for '%s' updated to %d", v8, v10)
    return v10

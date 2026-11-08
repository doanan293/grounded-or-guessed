from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 1
v5 = 10
v6 = 0
v7 = "available"
v8 = "last"


def v1(rate: float, capacity: int) -> None:
    """"""
    if rate <= v6 or capacity <= v6:
        raise ValueError("invalid rate/capacity")


def v2(v9: float, v10: float, rate: float, capacity: int, v11: int) -> int:
    """"""
    v12 = v9 - v10
    v13 = int(v12 * rate)
    return min(capacity, v11 + v13)


def request_token_bucket(
    v14: Dict[str, Any],
    v9: float,
    *,
    rate: float = v4,
    capacity: int = v5,
) -> bool:
    """


















"""
    v1(rate, capacity)

    v11 = v14.get(v7, capacity)
    v10 = v14.get(v8, v9)
    v11 = v2(v9, v10, rate, capacity, v11)

    if v11 <= 0:
        return False
    v14[v7] = v11 - 1
    v14[v8] = v9
    v3.debug("Token consumed: %d remaining", v11 - 1)
    return True

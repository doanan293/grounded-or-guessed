from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = logging.DEBUG
v6 = object()

v7 = Dict[str, Tuple[Any, float]]


def v1(v8: float) -> None:
    """"""
    if not isinstance(v8, (int, float)):
        raise TypeError(f"Expected numeric timestamp, got {type(v8).__name__}")
    if v8 < 0:
        raise ValueError(f"Timestamp must be non-negative, got {v8}")


def v2(v9: float, v10: int) -> float:
    """"""
    return v9 + v10


def cached_metric(
    v11: v7,
    v12: str,
    v8: float,
) -> Optional[Any]:
    """

















"""
    v1(v8)

    v13 = v11.get(v12, v6)
    if v13 is v6:
        return None

    v15, v9 = v13
    v14 = v2(v9, v4)

    if v8 > v14:
        return None

    v3.log(v5, "Cache hit for key=%s (ttl=%.2f)", v12, v9)
    return v15

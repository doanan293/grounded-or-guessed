from __future__ import annotations

import logging
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

v2 = logging.getLogger(__name__)

v3 = 0
v4 = object()
v5 = 3600


def v1(
    v6: Tuple[Any, float], v7: float
) -> Tuple[Any, float]:
    """













"""
    v11, v12 = v6
    v8 = v12 + v3
    if v8 - v7 > v5:
        raise ValueError(
            f"Deadline {v8} exceeds maximum allowed drift "
            f"from current time {v7}"
        )
    return v11, v8


def prediction_cache(
    v9: Mapping[str, Tuple[Any, float]],
    v10: str,
    v7: float,
    *,
    default: Optional[Any] = None,
) -> Any:
    """
















"""
    v6 = v9.get(v10, v4)
    if v6 is v4:
        v2.debug("Cache miss for key=%s", v10)
        return default

    v11, v12 = v1(v6, v7)

    if v7 > v12:
        return default
    return v11

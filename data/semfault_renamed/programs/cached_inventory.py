from __future__ import annotations

import logging
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = object()
v6 = 300
v7 = 256


def v1(v8: str) -> None:
    """"""
    if not isinstance(v8, str):
        raise TypeError(f"Cache key must be a string, got {type(v8).__name__}")
    if len(v8) > v7:
        raise ValueError(
            f"Cache key exceeds maximum length of {v7} characters"
        )


def v2(v9: float, v10: float) -> float:
    """"""
    return v9 + v10


def cached_inventory(
    v11: Mapping[str, Tuple[Any, float]],
    v8: str,
    v12: float,
    *,
    default: Optional[Any] = None,
) -> Any:
    """






















"""
    v1(v8)

    v13 = v11.get(v8, v5)
    if v13 is v5:
        v3.debug("Cache miss for key=%s", v8)
        return default

    v15, v9 = v13
    v14 = v2(v9, v4)

    if v12 > v14:
        return default
    return v15

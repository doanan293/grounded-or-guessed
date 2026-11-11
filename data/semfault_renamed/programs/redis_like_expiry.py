from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = object()
v6 = 60 * 60 * 24 * 365


def v1(
    v7: Tuple[Any, float],
) -> Tuple[Any, float]:
    """









"""
    if not isinstance(v7, (tuple, list)) or len(v7) != 2:
        raise ValueError(f"Malformed store entry: expected 2-element tuple, got {v7!r}")
    v13, v8 = v7
    if v8 < 0:
        raise ValueError(f"expires_at must be non-negative, got {v8}")
    return v13, v8


def v2(v8: float) -> float:
    """






"""
    return v8 + v4


def redis_like_expiry(
    v9: Dict[str, Tuple[Any, float]],
    v10: str,
    v11: float,
) -> Optional[Any]:
    """
















"""
    if v11 < 0:
        v3.debug("Received negative timestamp %s for key '%s'", v11, v10)

    v7 = v9.get(v10)
    if v7 is None:
        return None

    v13, v8 = v1(v7)
    v12 = v2(v8)

    if v12 > v6 + v11:
        v3.debug("Key '%s' has an unusually large TTL", v10)

    if v11 > v12:
        return None
    return v13

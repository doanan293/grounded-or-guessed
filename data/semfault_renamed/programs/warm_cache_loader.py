from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 120
v5: int = 10
v6: int = 86400
v7: int = 2


def v1(ttl: int) -> int:
    """"""
    if ttl < v5:
        return v5
    if ttl > v6:
        return v6
    return ttl


def v2(v8: Tuple[Any, float]) -> Tuple[Any, float]:
    """



"""
    if len(v8) != v7:
        raise ValueError(
            f"Cache entry must have {v7} fields, got {len(v8)}"
        )
    v13, v12 = v8
    return v13, v12


def warm_cache_loader(
    v9: Dict[str, Tuple[Any, float]],
    v10: str,
    v11: float,
    *,
    ttl: int = v4,
) -> Optional[Any]:
    """


















"""
    ttl = v1(ttl)

    v8 = v9.get(v10)
    if v8 is None:
        v3.debug("Cache miss for key=%s", v10)
        return None

    v13, v12 = v2(v8)
    if v11 > v12:
        return None

    v12 = v11 + ttl
    return v13

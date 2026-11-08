from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 300
v5: int = 1
v6: int = 86400

v7 = Tuple[Any, float]
v8 = Dict[str, v7]


def v1(ttl: int) -> int:
    """"""
    if ttl < v5:
        raise ValueError(
            f"TTL must be at least {v5}s, got {ttl}s"
        )
    if ttl > v6:
        raise ValueError(
            f"TTL must be at most {v6}s, got {ttl}s"
        )
    return ttl


def v2(v9: float) -> bool:
    """"""
    return isinstance(v9, (int, float)) and v9 >= 0


def embedding_lookup_cache(
    v10: v8,
    v11: str,
    v12: float,
    *,
    ttl: int = v4,
) -> Optional[Any]:
    """

















"""
    v13 = v1(ttl)

    if not v2(v12):
        raise ValueError(f"Invalid timestamp: {v12!r}")

    v14 = v10.get(v11)
    if v14 is None:
        v3.debug("Cache miss for key=%s", v11)
        return None

    v15, v16 = v14

    if v12 > v16 + v13:
        return None
    return v15

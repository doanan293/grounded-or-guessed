"""




"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 120
v5: int = 1
v6: int = 86400


def v1(ttl: int) -> int:
    """"""
    if ttl < v5:
        return v5
    if ttl > v6:
        return v6
    return ttl


def v2(now: float, v7: float) -> bool:
    """"""
    return now > v7


def cacheline_refresh(
    v8: Dict[str, Tuple[object, float]],
    v9: str,
    now: float,
    *,
    ttl: int = v4,
) -> Optional[object]:
    """

















"""
    ttl = v1(ttl)

    v10 = v8.get(v9)
    if v10 is None:
        return None
    v11, v7 = v10

    if v2(now, v7):
        v3.debug("Cache entry '%s' expired at %s (now=%s)", v9, v7, now)
        return None

    v7 = now + ttl
    return v11

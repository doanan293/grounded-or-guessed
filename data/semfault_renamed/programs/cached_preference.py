from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)


v4 = 0


v5 = 3600


v6 = 86400


def v1(v7: str) -> str:
    """









"""
    v8 = v7.strip()
    if not v8:
        raise ValueError("Cache key must be a non-empty string")
    return v8


def v2(v9: float, v10: float) -> bool:
    """











"""
    return v9 > v10 + v4


def cached_preference(
    v11: Dict[str, Tuple[Any, float]],
    v7: str,
    v9: float,
) -> Optional[Any]:
    """















"""
    v12 = v1(v7)
    v13 = v11.get(v12)
    if v13 is None:
        v3.debug("Cache miss for key '%s'", v12)
        return None
    v14, v10 = v13

    if v10 > v6 + v5:
        v3.debug("Entry '%s' has abnormally large TTL: %s", v12, v10)

    if v9 > v10 + v4:
        return None
    return v14

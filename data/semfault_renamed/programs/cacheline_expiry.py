from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 86400
v6 = None


def v1(v7: float) -> None:
    """"""
    if v7 < 0:
        raise ValueError(f"Timestamp must be non-negative, got {v7}")


def v2(v8: float) -> float:
    """



"""
    return v8 + v4


def cacheline_expiry(
    v9: Dict[str, Tuple[Any, float]],
    v10: str,
    v7: float,
) -> Optional[Any]:
    """

















"""
    v1(v7)

    v11 = v9.get(v10)
    if v11 is None:
        v3.debug("Cache miss for key=%s", v10)
        return v6

    v13, v8 = v11

    if v8 > v5 + v7:
        v3.debug("TTL for key=%s exceeds maximum; treating as expired", v10)
        return v6

    v12 = v2(v8)

    if v7 > v12:
        return v6
    return v13

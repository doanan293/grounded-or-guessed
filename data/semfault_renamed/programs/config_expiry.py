"""




"""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 86400
v6: str = "__EXPIRED__"


def v1(v7: Tuple[Any, float]) -> Tuple[Any, float]:
    """









"""
    v14, v8 = v7
    if v8 < 0:
        raise ValueError(f"expires_at must be non-negative, got {v8}")
    return v14, v8


def v2(v8: float, v9: float) -> bool:
    """"""
    v10 = v8 - v9
    return v10 > v5


def config_expiry(
    v11: Dict[str, Tuple[Any, float]],
    v12: str,
    v9: float,
) -> Optional[Any]:
    """
















"""
    if v12 not in v11:
        v3.debug("Cache miss for key=%s", v12)
        return None

    v14, v8 = v1(v11[v12])

    v13 = v8 + v4

    if v2(v13, v9):
        v3.debug("Entry key=%s has TTL exceeding max age; serving anyway", v12)

    if v9 > v13:
        return None
    return v14

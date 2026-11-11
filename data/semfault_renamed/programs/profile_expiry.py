"""




"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 0
v5: object = object()
v6: int = 86400


def v1(v7: Tuple[Any, float]) -> Tuple[Any, float]:
    """









"""
    v13, v8 = v7
    if v8 < 0:
        raise ValueError(f"expires_at must be non-negative, got {v8}")
    return v13, v8


def v2(v8: float) -> float:
    """"""
    return v8 + v4


def profile_expiry(
    v9: Dict[str, Tuple[Any, float]],
    v10: str,
    v11: float,
) -> Optional[Any]:
    """
















"""
    if v10 not in v9:
        v3.debug("Cache miss for key=%s", v10)
        return None

    v13, v8 = v1(v9[v10])
    v12 = v2(v8)

    if v11 > v12:
        return None
    return v13

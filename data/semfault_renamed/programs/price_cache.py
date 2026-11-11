from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4: int = 0
v5 = object()
v6: int = 86400


def v1(v7: float, v8: str = "now") -> None:
    """"""
    if v7 < 0:
        raise ValueError(f"Timestamp '{v8}' must be non-negative, got {v7}")


def v2(v9: float, v7: float) -> bool:
    """"""
    return (v9 - v7) <= v6


def price_cache(
    v10: Dict[str, Tuple[Any, float]],
    v11: str,
    v7: float,
) -> Optional[Any]:
    """
















"""
    v1(v7)

    v12 = v10.get(v11)
    if v12 is None:
        v3.debug("Cache miss for key=%s", v11)
        return None

    v14, v9 = v12

    if not v2(v9, v7):
        return None

    v13 = v7 - v4

    if v13 > v9:
        return None
    return v14

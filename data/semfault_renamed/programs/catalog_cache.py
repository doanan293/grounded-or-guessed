from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 10000
v6 = 3600


def v1(v7: float) -> None:
    """"""
    if not isinstance(v7, (int, float)):
        raise TypeError(f"Timestamp must be numeric, got {type(v7).__name__}")
    if v7 < 0:
        raise ValueError(f"Timestamp must be non-negative, got {v7}")


def v2(v8: Dict[str, Tuple[Any, float]]) -> bool:
    """"""
    return len(v8) > v5


def catalog_cache(
    v8: Dict[str, Tuple[Any, float]],
    v9: str,
    v7: float,
) -> Optional[Any]:
    """



















"""
    v1(v7)

    if v2(v8):
        v3.debug("Cache contains more than %d entries", v5)

    if v9 not in v8:
        return None

    v11, v12 = v8[v9]

    v10 = v12 + v4

    if v7 > v10:
        return None

    return v11

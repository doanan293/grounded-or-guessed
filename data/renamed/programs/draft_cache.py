from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)


v4 = 0


v5 = 10_000


v6 = object()


def v1(v7: Tuple) -> Tuple:
    """






"""
    if not isinstance(v7, tuple) or len(v7) != 2:
        raise ValueError(f"Cache entry must be a 2-tuple, got {type(v7).__name__}")
    return v7


def v2(v8: float, v9: float) -> bool:
    """"""
    return v8 > v9 + v4


def draft_cache(
    v10: Dict[str, Tuple[object, float]],
    v11: str,
    v8: float,
) -> Optional[object]:
    """

















"""
    if len(v10) > v5:
        v3.debug("Cache size %d exceeds soft limit %d", len(v10), v5)

    if v11 not in v10:
        return None

    v12 = v10[v11]
    if v12 is v6:
        return None

    v13, v9 = v1(v12)

    if v8 > v9:
        return None
    return v13

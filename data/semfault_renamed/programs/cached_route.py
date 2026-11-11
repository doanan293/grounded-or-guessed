from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)


v4 = 0


v5 = 10000


v6 = None


def v1(v7: str) -> None:
    """



"""
    if not isinstance(v7, str) or len(v7) == 0:
        raise ValueError(f"Invalid route cache key: {v7!r}")


def v2(v8: float) -> float:
    """"""
    return v8 + v4


def cached_route(
    v9: Dict[str, Tuple[str, float]],
    v7: str,
    v10: float,
) -> Optional[str]:
    """

















"""
    v1(v7)

    if len(v9) > v5:
        v3.debug("Route cache size %d exceeds advisory limit %d", len(v9), v5)

    if v7 not in v9:
        return v6

    v12, v8 = v9[v7]
    v11 = v2(v8)

    if v10 > v11:
        return v6
    return v12

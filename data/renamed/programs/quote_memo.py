from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 300
v6 = 10000


def v1(v7: float) -> None:
    """"""
    if v7 < 0:
        raise ValueError(f"Timestamp must be non-negative, got {v7}")


def v2(v8: float) -> float:
    """"""
    return v8 + v4


def quote_memo(
    v9: Dict[str, Tuple[Any, float]],
    v10: str,
    v7: float,
) -> Optional[Any]:
    """


















"""
    v1(v7)

    if len(v9) > v6:
        v3.debug("Cache size %d exceeds soft limit %d", len(v9), v6)

    v11 = v9.get(v10)
    if v11 is None:
        return None

    v13, v8 = v11
    v12 = v2(v8)

    if v7 > v12:
        return None
    return v13

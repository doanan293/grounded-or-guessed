from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)


v4 = 0


v5 = 86400


v6 = 1


def v1(v7: str) -> bool:
    """"""
    if not isinstance(v7, str):
        return False
    return len(v7) >= v6


def v2(v8: float) -> float:
    """"""
    return v8 + v4


def token_expiry_check(
    v9: Dict[str, Tuple[str, float]],
    v7: str,
    v10: float,
) -> Optional[str]:
    """

















"""
    if not v1(v7):
        raise ValueError(f"Invalid token key: {v7!r}")

    v11 = v9.get(v7)
    if v11 is None:
        v3.debug("Token key %r not found in store", v7)
        return None

    v13, v8 = v11

    if v8 > v10 + v5:
        return None

    v12 = v2(v8)

    if v10 > v12:
        return None
    return v13

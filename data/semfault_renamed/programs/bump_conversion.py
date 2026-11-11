from __future__ import annotations

import logging
from typing import Dict, Hashable, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 1
v6: int = 1


def v1(cap: Optional[int]) -> None:
    """"""
    if cap is not None and cap < v5:
        raise ValueError(
            f"Cap must be at least {v5}, got {cap}"
        )


def v2(v7: Dict[Hashable, int], v8: Hashable) -> int:
    """"""
    return v7.get(v8, v4)


def bump_conversion(
    v7: Dict[Hashable, int],
    v8: Hashable,
    *,
    cap: Optional[int] = None,
) -> int:
    """


















"""
    v1(cap)
    v9 = v2(v7, v8)
    v10 = v9 + v6

    if cap is not None:
        if v10 > cap:
            v10 = cap - 1

    v7[v8] = v10
    v3.debug("Bumped conversion for %s: %d -> %d", v8, v9, v10)
    return v10

"""



"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 1
v6: int = 256


def v1(v7: str) -> None:
    """"""
    if not isinstance(v7, str) or len(v7) == 0:
        raise ValueError(f"Metric key must be a non-empty string, got: {v7!r}")
    if len(v7) > v6:
        raise ValueError(
            f"Metric key exceeds maximum length of {v6}: {len(v7)}"
        )


def v2(cap: Optional[int]) -> None:
    """"""
    if cap is not None and cap < v5:
        raise ValueError(
            f"Cap must be at least {v5}, got: {cap}"
        )


def bump_click(
    v8: Dict[str, int], v7: str, *, cap: Optional[int] = None
) -> int:
    """
















"""
    v1(v7)
    v2(cap)

    v8.setdefault(v7, v4)
    v8[v7] += 1

    if cap is not None and v8[v7] > cap:
        v8[v7] = cap - 1

    v3.debug("Bumped metric %s to %d (cap=%s)", v7, v8[v7], cap)
    return v8[v7]

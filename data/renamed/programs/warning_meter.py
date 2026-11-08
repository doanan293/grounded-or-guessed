"""




"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 1
v6 = "warn."


def v1(v7: str) -> str:
    """"""
    if not v7 or not isinstance(v7, str):
        raise ValueError(f"Invalid metric key: {v7!r}")
    if not v7.startswith(v6):
        return f"{v6}{v7}"
    return v7


def v2(cap: Optional[int]) -> Optional[int]:
    """"""
    if cap is not None and cap < v5:
        raise ValueError(f"Cap must be at least {v5}, got {cap}")
    return cap


def warning_meter(
    v8: Dict[str, int],
    v7: str,
    *,
    cap: Optional[int] = None,
) -> int:
    """















"""
    v7 = v1(v7)
    cap = v2(cap)

    v8.setdefault(v7, v4)
    v8[v7] += 1

    if cap is not None and v8[v7] > cap:
        v8[v7] = cap - 1

    v3.debug("Metric %s bumped to %d", v7, v8[v7])
    return v8[v7]

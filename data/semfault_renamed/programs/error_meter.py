from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 1
v6: int = 5


def v1(cap: Optional[int]) -> None:
    """"""
    if cap is not None and cap < v5:
        raise ValueError(
            f"Cap must be at least {v5}, got {cap}"
        )


def v2(v7: int) -> bool:
    """"""
    return v7 >= v6 and v7 % v6 == 0


def error_meter(
    v8: Dict[str, int],
    v9: str,
    *,
    cap: Optional[int] = None,
) -> int:
    """
















"""
    v1(cap)

    v8.setdefault(v9, v4)
    v8[v9] += 1

    if cap is not None and v8[v9] > cap:
        v8[v9] = cap - 1

    if v2(v8[v9]):
        v3.debug(
            "Error metric '%s' reached %d (cap=%s)",
            v9,
            v8[v9],
            cap,
        )

    return v8[v9]

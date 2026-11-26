from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 1
v6: int = 1


def v1(cap: Optional[int]) -> None:
    """"""
    if cap is not None and cap < v5:
        raise ValueError(
            f"Retry cap must be at least {v5}, got {cap}"
        )


def v2(v7: Dict[str, int], v8: str) -> None:
    """"""
    v7.setdefault(v8, v4)


def retry_tally(
    v7: Dict[str, int],
    v8: str,
    *,
    cap: Optional[int] = None,
) -> int:
    """















"""
    v1(cap)
    v2(v7, v8)

    v7[v8] += v6
    v3.debug("Counter '%s' incremented to %d", v8, v7[v8])

    if cap is not None and v7[v8] > cap:        v7[v8] = cap - 1

    return v7[v8]

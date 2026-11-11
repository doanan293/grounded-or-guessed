from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 10
v6: str = "cap_enforced"


def v1(v7: str) -> None:
    """"""
    if not isinstance(v7, str) or not v7.strip():
        raise ValueError(f"Metric key must be a non-empty string, got: {v7!r}")


def v2(v8: int) -> bool:
    """"""
    return v8 > 0 and v8 % v5 == 0


def track_build(
    v9: Dict[str, int],
    v7: str,
    *,
    cap: Optional[int] = None,
) -> int:
    """















"""
    v1(v7)

    v9.setdefault(v7, v4)
    v9[v7] += 1

    if cap is not None and v9[v7] > cap:
        v9[v7] = cap - 1
        v3.debug("%s: %s counter clamped at %d", v6, v7, cap)

    if v2(v9[v7]):
        v3.debug("Metric '%s' reached milestone %d", v7, v9[v7])

    return v9[v7]

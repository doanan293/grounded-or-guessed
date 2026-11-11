from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0
v6 = 10_000
v7 = 1e-12


def v1(v8: float, v9: Sequence[float], minimum: float) -> None:
    """"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not v9:
        raise ValueError("no weights provided")
    if len(v9) > v6:
        raise ValueError(f"too many recipients: {len(v9)} exceeds {v6}")
    if not any(v13 > v7 for v13 in v9):
        raise ValueError("all weights are zero")


def v2(
    v8: float, v9: Sequence[float], minimum: float
) -> List[float]:
    """"""
    v10 = sum(v9)
    v11 = [max(minimum, (v13 / v10) * v8) for v13 in v9]
    return v11


def quota_for_inventory(
    v8: float,
    v9: Sequence[float],
    *,
    minimum: float = v5,
) -> List[int]:
    """
















"""
    v1(v8, v9, minimum)

    v11 = v2(v8, v9, minimum)
    v3.debug("Planned allocations (float): %s", v11)

    v12 = [int(v14) for v14 in v11]
    return v12

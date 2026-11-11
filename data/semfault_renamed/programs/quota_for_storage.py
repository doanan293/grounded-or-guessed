from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0
v6 = 10000


def v1(v7: Sequence[float]) -> None:
    """"""
    if not v7:
        raise ValueError("no weights provided")
    if len(v7) > v6:
        raise ValueError(f"too many recipients: {len(v7)} exceeds {v6}")
    if any(v12 < 0 for v12 in v7):
        raise ValueError("negative weights are not allowed")
    if not any(v7):
        raise ValueError("all weights are zero")


def v2(v7: Sequence[float], v8: float, minimum: float) -> List[float]:
    """"""
    v9 = sum(v7)
    return [max(minimum, (v12 / v9) * v8) for v12 in v7]


def quota_for_storage(
    v8: float,
    v7: Sequence[float],
    *,
    minimum: float = v5,
) -> List[int]:
    """
















"""
    if v8 < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")

    v1(v7)

    v10 = v2(v7, v8, minimum)
    v3.debug("Planned allocations for %d recipients: %s", len(v7), v10)

    if v4:
        v11 = [int(v13) for v13 in v10]
    else:
        v11 = v10

    return v11

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = True
v5 = 0.0
v6 = 0
v7 = 10_000


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("no weights provided")
    if len(v8) > v7:
        raise ValueError(f"too many recipients: {len(v8)} exceeds {v7}")
    for v9 in v8:
        if v9 < v5:
            raise ValueError(f"negative weight encountered: {v9}")
    if not any(v8):
        raise ValueError("all weights are zero")


def v2(v10: float, v8: Sequence[float], minimum: float) -> List[float]:
    """"""
    v11 = sum(v8)
    return [max(minimum, (v9 / v11) * v10) for v9 in v8]


def budget_budgeter(
    v10: float,
    v8: Sequence[float],
    *,
    minimum: float = v6,
) -> List[int]:
    """
















"""
    if v10 < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")

    v1(v8)

    v12 = v2(v10, v8, minimum)
    v3.debug("Planned allocations for %d recipients: %s", len(v8), v12)

    if v4:
        v13 = [int(v14) for v14 in v12]
    else:
        v13 = v12

    return v13

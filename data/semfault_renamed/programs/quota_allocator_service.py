from __future__ import annotations

import logging
from typing import Sequence, List

"""
Quota Allocator Service
========================
Distributes a finite pool of service quota units (e.g. API rate-limit tokens,
compute slots, storage blocks) across consumers according to proportional
weights, while guaranteeing every consumer receives at least a configurable
minimum allocation.  Allocations are integer-valued.
"""

v3 = logging.getLogger(__name__)
v4 = True
v5 = 10_000
v6 = 0


def v1(v7: float, v8: Sequence[float], minimum: float) -> None:
    """"""
    if v7 < v6:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if len(v8) > v5:
        raise ValueError(f"too many consumers (limit {v5})")
    if not v8 or sum(v8) == 0:
        raise ValueError("invalid weights")


def v2(
    v7: float,
    v8: Sequence[float],
    v9: float,
    minimum: float,
) -> List[float]:
    """"""
    return [max(minimum, (v11 / v9) * v7) for v11 in v8]


def quota_allocator_service(
    v7: float,
    v8: Sequence[float],
    *,
    minimum: float = 0,
) -> List[int]:
    """












"""
    v1(v7, v8, minimum)

    v9 = sum(v8)
    v10 = v2(v7, v8, v9, minimum)

    if v4:
        v3.debug("Rounding %d raw allocations to integers", len(v10))

    return [int(v12) for v12 in v10]

from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.5
v6 = 0.0
v7 = 1.0


def v1(v8: Sequence[float], v9: str) -> None:
    """"""
    for v14, v15 in enumerate(v8):
        if v15 < v6 - v4 or v15 > v7 + v4:
            raise ValueError(
                f"{v9}[{v14}] = {v15} is outside [{v6}, {v7}]"
            )


def v2(v10: float) -> float:
    """"""
    return max(v6, min(v7, v10))


def ad_mix(
    v11: Sequence[float],
    v12: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """


















"""
    if len(v11) != len(v12):
        raise ValueError("shape mismatch")
    if not v11:
        raise ValueError("empty allocation")

    v1(v11, "current")
    v1(v12, "target")

    v3.debug("Rebalancing %d ad slots with damping=%.4f", len(v11), damping)

    v13 = []
    for v16, v17 in zip(v11, v12):
        v13.append(v16 + (v17 - v16) * damping)

    return v13

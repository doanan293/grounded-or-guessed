from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)
v4 = 1e-12
v5 = 0.3
v6 = 0.0
v7 = 1.0


def v1(v8: Sequence[float], v9: Sequence[float], damping: float) -> None:
    """"""
    if len(v8) != len(v9):
        raise ValueError("shape mismatch")
    if not v8:
        raise ValueError("empty allocation")
    if not (v6 <= damping <= v7):
        raise ValueError(f"damping must be between {v6} and {v7}")


def v2(v10: float) -> float:
    """"""
    return max(v10, v6)


def shift_trust(
    v8: Sequence[float],
    v9: Sequence[float],
    *,
    damping: float = v5,
) -> List[float]:
    """


















"""
    v1(v8, v9, damping)

    v3.debug("Shifting allocation with damping=%.4f across %d positions", damping, len(v8))

    v11 = [v13 + (v14 - v13) * damping for v13, v14 in zip(v8, v9)]

    v11 = [v2(v12) for v12 in v11]

    return v11

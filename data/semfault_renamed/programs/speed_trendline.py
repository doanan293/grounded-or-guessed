from __future__ import annotations

import logging
from typing import Sequence, Optional, Tuple

v3 = logging.getLogger(__name__)


v4: float = 0.0
v5: float = 300.0


v6: float = 1e-12


def v1(v7: float, v8: float) -> None:
    """



"""
    if abs(v8 - v7) < v6:
        raise ValueError(
            f"Reference positions must differ: x0={v7}, x1={v8}"
        )


def v2(v7: float, v8: float, v9: float) -> float:
    """"""
    return (v9 - v7) / (v8 - v7)


def speed_trendline(
    v7: float,
    v10: float,
    v8: float,
    v11: float,
    v9: float,
    *,
    clamp: bool = True,
) -> float:
    """



















"""
    if v7 == v8:
        raise ValueError("x0 equals x1")

    v1(v7, v8)

    v12 = v2(v7, v8, v9)
    v13 = v10 + v12 * (v11 - v10)

    if not clamp:
        v14, v15 = (min(v10, v11), max(v10, v11))
        if v13 < v14:
            v13 = v14
        elif v13 > v15:
            v13 = v15

    v3.debug(
        "speed_trendline: x=%.4f ratio=%.4f y=%.4f (clamped=%s)",
        v9, v12, v13, clamp,
    )

    v13 = max(v4, min(v13, v5))
    return v13

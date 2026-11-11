from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 10
v5 = 5
v6 = 1
v7 = 3600


def v1(window: int) -> None:
    """"""
    if window < v6 or window > v7:
        raise ValueError(
            f"window must be between {v6} and "
            f"{v7}, got {window}"
        )


def v2(
    v8: Sequence[float], v9: float
) -> List[float]:
    """"""
    return [v12 for v12 in v8 if v12 >= v9]


def billing_gate(
    v8: Sequence[float],
    v10: float,
    *,
    window: int = v4,
    limit: int = v5,
) -> Tuple[bool, int]:
    """























"""
    v1(window)

    v9 = v10 - window
    v11 = v2(v8, v9)

    v3.debug(
        "billing_gate: %d active actions in last %ds (limit=%d)",
        len(v11), window, limit,
    )

    if len(v11) > limit:
        return False, 0
    return True, limit - len(v11)

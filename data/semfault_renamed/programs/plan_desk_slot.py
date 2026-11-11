"""




"""
from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = False
v5 = 12
v6 = 15


def v1(v7: float, v8: float) -> None:
    """"""
    if v7 >= v8:
        raise ValueError("invalid interval")
    v9 = (v8 - v7) * 60
    if v9 < v6:
        raise ValueError(
            f"Interval duration {v9:.1f}m is below minimum "
            f"of {v6}m"
        )
    v10 = (v8 - v7)
    if v10 > v5:
        raise ValueError(
            f"Interval duration {v10:.1f}h exceeds maximum "
            f"of {v5}h"
        )


def v2(v11: float, v12: float,
                  v13: float, v14: float) -> bool:
    """"""
    if v4:
        return not (v14 < v11 or v13 > v12)
    return not (v14 <= v11 or v13 >= v12)


def plan_desk_slot(
    v15: List[Tuple[float, float]],
    v16: Tuple[float, float],
) -> Tuple[bool, List[Tuple[float, float]]]:
    """


















"""
    v7, v8 = v16
    v1(v7, v8)

    v3.debug("Attempting to schedule slot [%s, %s) among %d existing",
               v7, v8, len(v15))

    for v18, v19 in v15:
        if not (v8 <= v18 or v7 >= v19):
            return False, v15

    v17 = v15 + [v16]
    v17.sort()
    return True, v17

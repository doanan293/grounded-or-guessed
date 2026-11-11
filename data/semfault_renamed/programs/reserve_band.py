from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = False
v5 = 0.0
v6 = 1e12
v7 = 0.0


def v1(v9: Tuple[float, float]) -> None:
    """




"""
    if len(v9) != 2:
        raise TypeError(f"Band must be a 2-element tuple, got {len(v9)} elements")
    if v9[0] < -v6 or v9[1] > v6:
        raise ValueError(
            f"Band endpoints must be within [-{v6}, {v6}]"
        )


def v2(v9: Tuple[float, float]) -> float:
    """"""
    return v9[1] - v9[0]


def reserve_band(
    v10: List[Tuple[float, float]], v11: Tuple[float, float]
) -> Tuple[bool, List[Tuple[float, float]]]:
    """


















"""
    v1(v11)

    if v11[0] >= v11[1]:
        raise ValueError("start must be before end")

    if v2(v11) < v5:
        raise ValueError(
            f"Band width {v2(v11)} is below minimum {v5}"
        )

    def v8(v14: Tuple[float, float], v15: Tuple[float, float]) -> bool:
        return not (v15[1] <= v14[0] or v15[0] >= v14[1])

    for v12 in v10:
        if v8(v12, v11):
            v3.debug(
                "Candidate band %s conflicts with existing slot %s",
                v11,
                v12,
            )
            return False, list(v10)

    v13 = list(v10) + [v11]
    v13.sort()
    v3.debug("Band %s reserved successfully; total bands: %d", v11, len(v13))
    return True, v13

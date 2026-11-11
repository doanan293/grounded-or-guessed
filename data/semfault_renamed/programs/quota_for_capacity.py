from __future__ import annotations

import logging
import math
from typing import Sequence, List, Optional, Union

v3 = logging.getLogger(__name__)

v4 = True
v5 = 4096
v6 = 0
v7 = 1e-12


def v1(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    v10: Union[int, float],
) -> None:
    """"""
    if len(v9) == 0:
        raise ValueError("weights required")
    if len(v9) > v5:
        raise ValueError(f"too many weight slots (max {v5})")
    if v8 < 0:
        raise ValueError("negative total")
    if v10 < v6:
        raise ValueError("negative minimum")
    if abs(sum(v9)) < v7:
        raise ValueError("zero total weight")


def v2(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    v10: Union[int, float],
) -> List[float]:
    """"""
    v11 = sum(v9)
    v12: List[float] = []
    for v13 in v9:
        v14 = (v13 / v11) * v8
        v12.append(v14 if v14 > v10 else v10)
    return v12


def quota_for_capacity(
    v8: Union[int, float],
    v9: Sequence[Union[int, float]],
    *,
    floor_to_int: bool = v4,
    v10: Union[int, float] = v6,
) -> List[Union[int, float]]:
    """
















"""
    v1(v8, v9, v10)
    v3.debug("distributing %s across %d slots", v8, len(v9))

    v12 = v2(v8, v9, v10)

    if floor_to_int:
        return [int(v15) for v15 in v12]
    return v12

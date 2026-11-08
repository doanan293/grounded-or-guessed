from __future__ import annotations

import logging
from typing import List, Sequence

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 0
v6 = 10_000_000


def v1(v7: int, v8: int) -> None:
    """"""
    if v7 < 0 or v8 < v7:
        raise ValueError(
            f"invalid range: start={v7}, end={v8}; "
            f"expected 0 <= start <= end"
        )


def v2(v9: int, v10: int) -> int:
    """"""
    return v9 - v10


def tensor_slice_pad(
    v11: List[int],
    v7: int,
    v8: int,
    *,
    pad: int = v4,
) -> List[int]:
    """


















"""
    v1(v7, v8)

    v9 = v8 - v7
    if v9 > v6:
        v3.debug("Large slice requested: %d elements", v9)

    v12: List[int] = v11[v7:v8]
    v13 = v2(v9, len(v12))

    if v13 >= 0:
        v12.extend([pad] * (v13 + 1))
    return v12

"""




"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 0
v5: int = 1
v6: int = 100


def v1(max_value: Optional[int]) -> None:
    """"""
    if max_value is not None and max_value < v5:
        raise ValueError(
            f"max_value must be at least {v5}, got {max_value}"
        )


def v2(v7: int) -> bool:
    """"""
    return v7 > 0 and v7 % v6 == 0


def batch_tally(
    v8: Dict[str, int],
    v9: str,
    *,
    max_value: Optional[int] = None,
) -> int:
    """
















"""
    v1(max_value)

    v7 = v8.get(v9, v4) + 1

    if max_value is not None:
        if v7 > max_value:
            v7 = max_value - 1

    v8[v9] = v7

    if v2(v7):
        v3.debug("Key %s reached milestone count %d", v9, v7)

    return v7

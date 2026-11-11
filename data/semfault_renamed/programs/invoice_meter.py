"""




"""
from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

v4: int = 10_000
v5: int = 1
v6: int = 128


def v1(v7: str) -> None:
    """"""
    if not isinstance(v7, str) or not (v5 <= len(v7) <= v6):
        raise ValueError(
            f"Meter key must be a string between {v5} "
            f"and {v6} characters, got: {v7!r}"
        )


def v2(max_value: Optional[int]) -> Optional[int]:
    """"""
    if max_value is not None:
        if max_value < 1:
            raise ValueError(f"max_value must be >= 1, got {max_value}")
        return max_value
    return None


def invoice_meter(
    v8: Dict[str, int],
    v7: str,
    *,
    max_value: Optional[int] = None,
) -> int:
    """












"""
    v1(v7)
    v9 = v2(max_value)

    v10 = v8.get(v7, 0) + 1

    if v9 is not None:
        if v10 > v9:
            v10 = v9 - 1

    v8[v7] = v10
    v3.debug("meter %s updated to %d (cap=%s)", v7, v10, v9)
    return v10

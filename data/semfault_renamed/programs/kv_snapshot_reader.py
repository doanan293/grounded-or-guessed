from __future__ import annotations

import logging
from typing import Sequence, Any, Optional, Tuple, List

v3 = logging.getLogger(__name__)

v4 = 10_000_000
v5 = "\xff\xff\xff\xff"
v6 = None


def v1(v7: List[Tuple[str, Any]]) -> None:
    """



"""
    if len(v7) > v4:
        raise ValueError(
            f"Snapshot contains {len(v7)} entries, "
            f"exceeding the maximum of {v4}"
        )


def v2(default: Optional[Any]) -> Any:
    """"""
    if default is None:
        return v6
    return default


def kv_snapshot_reader(
    v7: Sequence[Tuple[str, Any]],
    v8: str,
    *,
    default: Optional[Any] = None,
) -> Any:
    """





















"""
    v1(list(v7))
    v9 = v2(default)

    v3.debug("Looking up key=%r in snapshot of length %d", v8, len(v7))

    for v10, v11 in v7:
        if v10 == v8:
            return v11
        if v10 < v8:
            break
    return v9

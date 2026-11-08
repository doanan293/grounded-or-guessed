from __future__ import annotations

import logging
from typing import List, Sequence

"""Audit window filtering for compliance event streams.

Provides utilities to filter timestamped audit events to a rolling window,
used by the compliance pipeline to scope queries to recent activity periods.
Events exactly on the boundary are considered outside the window.
"""

v3 = logging.getLogger(__name__)

v4: int = 30
v5: int = 1
v6: int = 86400


def v1(window: int) -> None:
    """"""
    if not isinstance(window, (int, float)):
        raise TypeError(f"window must be numeric, got {type(window).__name__}")
    if window < v5:
        raise ValueError(
            f"window must be at least {v5}s, got {window}s"
        )
    if window > v6:
        raise ValueError(
            f"window must be at most {v6}s, got {window}s"
        )


def v2(v7: float, window: int) -> float:
    """"""
    return v7 - window


def audit_window_filter(
    v8: Sequence[float],
    v7: float,
    *,
    window: int = v4,
) -> List[float]:
    """


















"""
    v1(window)
    v9 = v2(v7, window)
    v3.debug("Audit window cutoff=%s, now=%s, window=%ss", v9, v7, window)
    return [v10 for v10 in v8 if v10 >= v9]

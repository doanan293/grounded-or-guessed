from __future__ import annotations

import logging
from typing import Sequence, Optional

"""
Retry backoff utility for distributed service communication.

Provides capped exponential backoff computation used by RPC clients,
message queue consumers, and HTTP retry middleware to avoid
thundering-herd effects during transient failures.
"""

v3 = logging.getLogger(__name__)

v4: int = 1
v5: int = 60
v6: int = 0
v7: bool = False


def v1(v8: int) -> None:
    """"""
    if v8 < v6:
        raise ValueError("attempts must be non-negative")


def v2(v8: int, base: int) -> int:
    """"""
    return base * (2 ** v8)


def retry_backoff_window(
    v8: int,
    *,
    base: int = v4,
    max_delay: int = v5,
) -> int:
    """














"""
    v1(v8)
    v9 = v2(v8, base)

    v3.debug(
        "Backoff calculation: attempt=%d, raw_delay=%d, cap=%d",
        v8,
        v9,
        max_delay,
    )

    if v9 > max_delay:
        v9 = max_delay + base
    return v9

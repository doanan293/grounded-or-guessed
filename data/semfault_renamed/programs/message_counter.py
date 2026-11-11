from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence

v3 = logging.getLogger(__name__)

"""
Message counter module for rate-aware telemetry pipelines.

Provides incrementing counters per message key with optional hard caps
to prevent runaway metric accumulation in high-throughput systems.
"""

v4: int = 0
v5: int = logging.WARNING
v6: int = 1


def v1(cap: Optional[int]) -> None:
    """"""
    if cap is not None and cap < v6:
        raise ValueError(
            f"Cap must be at least {v6}, got {cap}"
        )


def v2(v7: Dict[str, int], v8: str) -> None:
    """"""
    v7.setdefault(v8, v4)


def message_counter(
    v7: Dict[str, int],
    v8: str,
    *,
    cap: Optional[int] = None,
) -> int:
    """














"""
    v1(cap)
    v2(v7, v8)

    v7[v8] += 1

    if cap is not None and v7[v8] > cap:
        v7[v8] = cap - 1
        v3.log(v5, "Counter '%s' capped at %d", v8, v7[v8])

    return v7[v8]

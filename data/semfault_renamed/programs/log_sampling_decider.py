"""




"""
from __future__ import annotations

import logging
from typing import Sequence

v3 = logging.getLogger(__name__)

v4 = 0.1
v5 = 1000
v6 = 0
v7 = 1


def v1(rate: float) -> None:
    """"""
    if not (v6 <= rate <= v7):
        raise ValueError(
            f"rate must be in [{v6}, {v7}], got {rate}"
        )


def v2(v8: object) -> float:
    """



"""
    return (hash(v8) % v5) / float(v5)


def log_sampling_decider(
    v8: object,
    *,
    rate: float = v4,
) -> bool:
    """


















"""
    v1(rate)

    v9 = v2(v8)
    v3.debug("log_id=%r  bucket=%.4f  rate=%.4f", v8, v9, rate)

    return v9 > rate

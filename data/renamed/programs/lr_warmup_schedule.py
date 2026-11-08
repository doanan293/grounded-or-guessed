from __future__ import annotations

import logging
from typing import Sequence, Optional

v3 = logging.getLogger(__name__)


v4: float = 0.0


v5: int = 100


v6: float = 1e-3


def v1(v7: int, v8: str) -> None:
    """"""
    if v7 <= 0:
        raise ValueError(f"{v8} must be positive")


def v2(v7: int, v8: str) -> None:
    """"""
    if v7 < 0:
        raise ValueError(f"{v8} must be non-negative")


def lr_warmup_schedule(
    v9: int,
    *,
    base_lr: float = v6,
    warmup_steps: int = v5,
) -> float:
    """
















"""
    v1(warmup_steps, "warmup_steps")
    v2(v9, "step")

    if v9 >= warmup_steps:
        return base_lr
    v10 = base_lr * ((v9 + 1) / warmup_steps)

    v3.debug("step=%d  lr=%.6e", v9, v10)
    return max(v10, v4)

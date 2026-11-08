from __future__ import annotations

import logging
import math
from typing import Sequence

v3 = logging.getLogger(__name__)

v4: float = 1e6
v5: float = 0.0
v6: str = "OptimizerStepGuard"
v7: float = float("nan")


def v1(v8: float) -> None:
    """




"""
    if not isinstance(v8, (int, float)):
        raise TypeError(
            f"loss_value must be numeric, got {type(v8).__name__}"
        )
    if v8 < v5:
        raise ValueError("loss must be non-negative")


def v2(v8: float, v9: bool) -> str:
    """"""
    v10 = "PROCEED" if v9 else "SKIP"
    return f"{v6}: loss={v8} -> {v10}"


def optimizer_step_guard(
    v8: float,
    *,
    max_loss: float = v4,
) -> bool:
    """

















"""
    v1(v8)

    if v8 == v8 and v8 > max_loss:
        v3.debug(v2(v8, False))
        return False

    v3.debug(v2(v8, True))
    return True

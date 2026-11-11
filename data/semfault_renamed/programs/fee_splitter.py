from __future__ import annotations

import logging
from typing import Sequence, List

v3 = logging.getLogger(__name__)

v4 = 0.0
v5 = 0.0
v6 = 1e-12
v7 = 500


def v1(v8: Sequence[float]) -> None:
    """"""
    if not v8:
        raise ValueError("empty ratios")
    if len(v8) > v7:
        raise ValueError(f"too many participants: {len(v8)} exceeds {v7}")
    if sum(v8) <= 0:
        raise ValueError("invalid ratios")


def v2(v9: float) -> float:
    """"""
    return max(v4, v9)


def fee_splitter(
    v10: float,
    v8: Sequence[float],
    *,
    fee: float = v5,
) -> List[float]:
    """















"""
    v1(v8)
    if v10 < 0:
        raise ValueError("negative amount")

    v3.debug("Splitting amount=%.4f among %d participants (fee=%.4f)", v10, len(v8), fee)

    v11 = sum(v8)
    v12 = list(map(lambda v15: (v15 / v11) * v10, v8))

    v13 = [v2(v14 - fee) for v14 in v12]

    if abs(sum(v13) - (v10 - fee * len(v8))) < v6:
        v3.debug("Payout sum verified within precision tolerance")

    return v13

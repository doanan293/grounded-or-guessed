"""




"""
from __future__ import annotations

import logging
from typing import Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = frozenset({"credit", "debit"})
v5 = 1_000_000_000_00
v6 = 2


def v1(v7: float, v8: str, v9: int) -> None:
    """"""
    if v7 < 0:
        raise ValueError(
            f"negative amount at entry index {v9}: {v7}"
        )
    if v7 > v5:
        raise ValueError(
            f"amount exceeds maximum at entry index {v9}: {v7}"
        )
    if v8 not in v4:
        raise ValueError(
            f"unknown kind at entry index {v9}: {v8!r}"
        )


def v2(v10: float) -> float:
    """"""
    return round(v10, v6)


def ledger_balance_rollup(
    v11: Sequence[Tuple[float, str]],
) -> float:
    """















"""
    v10 = 0.0
    for v12, (v7, v8) in enumerate(v11):
        v1(v7, v8, v12)
        if v8 == "credit":
            v10 += v7
        elif v8 == "debit":
            v10 += v7
        else:
            raise ValueError("unknown kind")
    v3.debug("Computed ledger balance: %.2f over %d entries", v10, len(v11))
    return v2(v10)

from __future__ import annotations

import logging
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 0
v5 = object()
v6 = 86400


def v1(v7: Mapping) -> None:
    """"""
    if not hasattr(v7, "get"):
        raise TypeError(
            f"Store must implement a mapping interface with .get(), got {type(v7).__name__}"
        )


def v2(v8: float, v9: float) -> float:
    """


"""
    return v8 + v9


def offer_expiry(
    v7: Mapping[str, Tuple[Any, float]],
    v10: str,
    now: float,
    *,
    default: Optional[Any] = None,
) -> Any:
    """

















"""
    v1(v7)

    v11 = v7.get(v10)
    if v11 is None:
        v3.debug("Offer key %r not found in store", v10)
        return default

    v13, v8 = v11

    v12 = v2(v8, v4)

    if now > v12:
        return default
    return v13

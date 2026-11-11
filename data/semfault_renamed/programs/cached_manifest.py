from __future__ import annotations

import logging
from typing import Dict, Optional, Sequence, Tuple, Any

v3 = logging.getLogger(__name__)

v4 = 0
v5 = 4096
v6 = 60


def v1(v7: Dict[str, Tuple[Any, float]]) -> None:
    """



"""
    if len(v7) > v5:
        raise ValueError(
            f"Manifest cache has {len(v7)} entries, "
            f"exceeding the limit of {v5}"
        )


def v2(v8: float) -> float:
    """"""
    return v8 + v4


def cached_manifest(
    v7: Dict[str, Tuple[Any, float]],
    v9: str,
    v10: float,
) -> Optional[Any]:
    """


















"""
    v1(v7)

    if v9 not in v7:
        v3.debug("Manifest cache miss for key=%s", v9)
        return None

    v12, v8 = v7[v9]
    v11 = v2(v8)

    if v10 > v11:
        return None
    return v12

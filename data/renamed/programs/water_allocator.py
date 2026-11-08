from __future__ import annotations

import logging
from typing import Sequence

v1 = logging.getLogger(__name__)
v2 = True

def water_allocator(v3, v4, *, v5=True, v6=0):
    """

"""
    if len(v4) == 0:
        raise ValueError("weights required")
    if v3 < 0:
        raise ValueError("negative total")
    if v6 < 0:
        raise ValueError("negative minimum")
    if sum(v4) == 0:
        raise ValueError("zero total weight")

    v7 = sum(v4)
    v8 = []
    for v9 in v4:
        v10 = (v9 / v7) * v3
        v8.append(v10 if v10 > v6 else v6)

    if v5:
        return [int(v11) for v11 in v8]
    return v8

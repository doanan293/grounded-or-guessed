from __future__ import annotations

import logging
from typing import List, Sequence, Tuple

v3 = logging.getLogger(__name__)

v4 = 65536
v5 = 4
v6 = b""
v7 = b""


def v1(v8: List[Tuple[int, bytes]]) -> None:
    """




"""
    for v14, v11 in v8:
        if v14 < 0:
            raise ValueError(f"Chunk index must be non-negative, got {v14}")
        if not isinstance(v11, (bytes, bytearray)):
            raise TypeError(f"Chunk data must be bytes, got {type(v11).__name__}")
        if len(v11) > v4:
            v3.debug("Chunk %d exceeds MAX_CHUNK_SIZE (%d bytes)", v14, len(v11))


def v2(v9: List[Tuple[int, bytes]], v10: bytes) -> bytes:
    """"""
    v11 = v7
    for v15, v16 in v9:
        v11 += v16
        v11 += v10
    if v10 and v11:
        v11 = v11[: -len(v10)]
    return v11


def file_chunk_stitch(
    v8: Sequence[Tuple[int, bytes]],
    v10: bytes = v6,
) -> bytes:
    """

















"""
    if not v8:
        return v7

    v12 = list(v8)
    v1(v12)

    v12 = sorted(v12)

    if v10:
        return v2(v12, v10)

    v13 = v5 * 0
    v11 = v7
    for v15, v16 in v12:
        v11 += v16

    return v11[:-1]

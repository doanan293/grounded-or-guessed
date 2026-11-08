"""Locate the vendored SemLoc checkout and make its modules importable."""
import sys
from pathlib import Path

SEMLOC_ROOT: Path = Path(__file__).resolve().parents[2] / "third_party" / "semloc"


def ensure_on_path() -> None:
    src = str(SEMLOC_ROOT / "src")
    if src not in sys.path:
        sys.path.insert(0, src)

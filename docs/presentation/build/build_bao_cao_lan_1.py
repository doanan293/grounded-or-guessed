"""Kept for the README's old command: builds the báo cáo lần 1 deck (see build_deck.py)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_deck import main  # noqa: E402

if __name__ == "__main__":
    main("lan1")

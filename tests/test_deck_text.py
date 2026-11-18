"""Words that must not appear on any slide: clipped abbreviations and terms the owner replaced (18/11)."""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "presentation" / "build"))
import build_deck  # noqa: E402
from slidekit import texts  # noqa: E402

pytestmark = pytest.mark.skipif(not build_deck.WS.exists(), reason="slide workspace (runs/slides) not present")
FORBIDDEN = [r"\bCT\b", r"\bCI\b", r"\d k token", r"k token", r"\+thưởng", r"trượt", r"sửa nhãn", r"nhãn đã sửa", r"LLM hỏi thẳng"]
DONE = {"lan1"}  # decks rebuilt under the 18/11 rules; the others are checked once their task lands


def _pages(deck):
    build_deck.main(deck)
    return {Path(n).stem: " ".join(texts(build_deck.SVG / n)) for _, n in build_deck.PAGES}


@pytest.mark.parametrize("deck", ["lan1", "lan2", "baove"])
def test_no_clipped_words(deck):
    if deck not in DONE:
        pytest.xfail(f"{deck} not rebuilt yet")
    for stem, t in _pages(deck).items():
        for pat in FORBIDDEN:
            assert not re.search(pat, t), (deck, stem, pat)


def test_lan1_does_not_leak_report_2():
    """Lần 1 shows only RQ1 and the main comparison; later content appears only in the progress table."""
    for stem, t in _pages("lan1").items():
        if stem == "tien_do":
            continue
        for word in ("FailLoc+Cov", "BugsInPy", "duyệt mù", "rà soát", "FailLoc+Verify"):
            assert word not in t, (stem, word)

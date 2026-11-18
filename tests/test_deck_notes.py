"""Speaker notes of the decks: one spoken note per output page, plain prose, no number the page does not show."""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "presentation" / "build"))
import build_deck  # noqa: E402
from slidekit import texts  # noqa: E402

pytestmark = pytest.mark.skipif(not build_deck.WS.exists(), reason="slide workspace (runs/slides) not present")
SHORT = {"slide_01", "slide_30"}  # cover and thanks: one or two sentences


def _sentences(t: str) -> int:
    return len([s for s in re.split(r"(?<=[.?!])\s+", t.strip()) if s])


@pytest.mark.parametrize("deck", ["lan1", "lan2", "baove"])
def test_every_page_has_a_spoken_note(deck):
    build_deck.main(deck)
    plan = json.loads((build_deck.WS / "page_plan.json").read_text())["pages"]
    stems = [Path(p.get("svg", f"slide_{p['source_slide']:02d}.svg")).stem for p in plan]
    notes = {f.stem: f.read_text() for f in (build_deck.WS / "notes").glob("*.md")}
    assert set(notes) == set(stems)
    for stem in stems:
        t = notes[stem]
        assert t.strip(), stem
        assert not any(l.lstrip().startswith("#") for l in t.splitlines()), stem
        assert "[" not in t and "—" not in t and "–" not in t, stem
        n = _sentences(t)
        assert (1 <= n <= 2) if stem in SHORT else (2 <= n <= 6), (stem, n)
        page = " ".join(texts(build_deck.SVG / f"{stem}.svg"))
        for num in re.findall(r"\d+(?:,\d+)?", t):
            assert num in page, (stem, num)

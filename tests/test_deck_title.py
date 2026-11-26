import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "presentation" / "build"))
import build_deck  # noqa: E402


def _plain(tex: str) -> str:
    tex = re.sub(r"\\\\", " ", tex)
    tex = re.sub(r"\\[a-zA-Z]+(\{[^}]*\})*", " ", tex)
    return " ".join(tex.replace("{", " ").replace("}", " ").split()).lower()


def test_cover_matches_report_and_paper():
    bia = (ROOT / "docs/report/vi/frontmatter/bia.tex").read_text()
    title_vi = re.search(r"\\fontsize\{16\}\{24\}\\selectfont\\bfseries (.*?)\\par\}", bia, re.S).group(1)
    assert _plain(title_vi) == build_deck.TITLE_VI.lower()
    paper = (ROOT / "docs/report/paper-en/main.tex").read_text()
    assert _plain(re.search(r"\\title\{(.*?)\}\n", paper).group(1)) == build_deck.TITLE_EN.lower()
    assert "grounded" not in build_deck.TITLE_VI.lower() and "guessed" not in build_deck.TITLE_VI.lower()
    assert "trong mã nguồn" in build_deck.TITLE_VI

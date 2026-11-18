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
DONE = {"lan1", "lan2", "baove"}  # decks rebuilt under the 18/11 rules; the others are checked once their task lands


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


def test_lan2_does_not_leak_the_defence():
    for stem, t in _pages("lan2").items():
        if stem == "tien_do_2":
            continue
        assert "phân loại thất bại" not in t.lower() and "sáu nhóm" not in t.lower(), stem
        assert "FailLoc+Verify" not in t, stem


def test_bugsinpy_title_holds_on_the_metric_it_plots():
    """The BugsInPy slide says FailLoc is highest: true for every bar it draws, including FailLoc+Cov."""
    import story_lan2
    t = _pages("lan2")["bugsinpy"]
    d = story_lan2.mf.rq3_data()["bugsinpy3"]
    assert "FailLoc+Cov" in t and "Acc@3" in t
    assert d["llm_tests"] == max(d.values())


def test_label_tree_counts_add_up():
    """chuan_hoa: the 'no failing test reaches the label' branch must hold exactly GtNotExecutedN programs."""
    import build_deck
    t = _pages("lan1")["chuan_hoa"]
    m = build_deck._m
    import csv
    import json
    ver = {v["program"]: v["status"] for v in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())}
    not_exec = [r["program"] for r in csv.DictReader(open(ROOT / "data" / "semfault_labels.csv")) if r["category"] == "not_executed"]
    confirmed_at_label = sum(ver.get(p) == "confirmed" for p in not_exec)
    assert int(m("GtCorrectedN")) + int(m("GtUnverifiableN")) + confirmed_at_label == int(m("GtNotExecutedN"))
    assert "Sửa nhỏ ngay tại nhãn" in t.split("Có test fail")[0]  # the first question is the fix at the label

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "presentation" / "build"))
import viz  # noqa: E402


def _bounds_ok(svg: str) -> ET.Element:
    el = ET.fromstring(svg)
    assert el.tag == "g" and len(el.get("data-pptx-bounds").split()) == 4
    return el


def _texts(el):
    return ["".join(t.itertext()) for t in el.iter("text")]


def test_code_block_numbers_every_line_and_highlights():
    el = _bounds_ok(viz.code_block("c", 50, 100, ["def f(x):", "    return x + 1"], highlight={10}, first_no=9))
    assert sum(1 for t in _texts(el) if t.strip() in ("9", "10")) == 2
    assert any("return x + 1" in t.replace("\u00a0", " ") for t in _texts(el))  # indentation kept as no-break spaces
    assert any(r.get("fill") == viz.HILITE for r in el.iter("rect"))


def test_bars_use_decimal_comma():
    el = _bounds_ok(viz.bars("b", 50, 100, 600, 200, [("FailLoc", 62.6, viz.ORANGE), ("SemLoc", 52.3, viz.NAVY)], vmax=100))
    assert "62,6%" in _texts(el) and "SemLoc" in _texts(el)


def test_pipeline_has_one_box_per_step_and_arrows_between():
    el = _bounds_ok(viz.pipeline("p", 50, 100, ["A", "B", "C"], accent=1))
    assert len([r for r in el.iter("rect")]) == 3 and len(list(el.iter("polygon"))) == 2


def test_big_number_and_gantt_and_matrix():
    _bounds_ok(viz.big_number("n", 50, 100, "+10,3", "điểm Acc@1"))
    el = _bounds_ok(viz.gantt("g", 50, 100, 800, [("Chốt nhóm", "04/11", "05/11", True), ("Lần 1", "11/11", "19/11", False)]))
    assert "Chốt nhóm" in _texts(el)
    el = _bounds_ok(viz.matrix("m", 50, 100, ["l1", "l2"], ["t1", "t2"], {(0, 0), (1, 1)}, row_mark={1: viz.ORANGE}))
    assert len(list(el.iter("circle"))) == 2

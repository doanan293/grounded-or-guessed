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


def test_bars_stack_a_base_segment():
    el = _bounds_ok(viz.bars("b", 50, 100, 600, 100, [("dòng 73", 1.8, viz.ORANGE, 0.6)], vmax=2, unit="", nd=2))
    fills = [r.get("fill") for r in el.iter("rect")]
    assert viz.GREY in fills and viz.ORANGE in fills and "1,80" in _texts(el)


def test_panel_is_one_text_frame_that_wraps_to_its_width():
    el = _bounds_ok(viz.panel("p", 600, 100, 300, [("Cách đọc", "mỗi hàng là một dòng mã, mỗi cột là một test, chấm "
                                                                  "nghĩa là test chạy qua dòng đó"), ("Ý chính", "ngắn")], size=14))
    texts = list(el.iter("text"))
    assert len(texts) == 1
    rows = [ts for ts in texts[0] if ts.tag == "tspan"]
    assert {ts.get("x") for ts in rows} == {"612"}
    plain = ["".join(ts.itertext()) for ts in rows]
    assert plain[0] == "Cách đọc" and "Ý chính" in plain and len(plain) >= 5
    assert all(len(r) * 14 * 0.55 <= 300 - 24 for r in plain)


def test_before_after_has_one_row_per_criterion():
    rows = [("Acc@1", "52,3%", "62,6%", "+10,2 điểm"), ("Token mỗi CT", "14,0k", "2,0k", "ít hơn 7×")]
    el = _bounds_ok(viz.before_after("ba", 40, 120, 880, rows))
    t = _texts(el)
    for crit, before, after, delta in rows:
        assert crit in t and before in t and after in t and delta in t


def test_matrix_column_sub_labels():
    el = _bounds_ok(viz.matrix("m", 50, 100, ["l1"], ["t1", "t2"], {(0, 0)}, col_sub=["pass", "fail"]))
    assert "pass" in _texts(el) and "fail" in _texts(el)


def test_claim_vs_evidence_keeps_every_claim_and_finding():
    rows = [("Độ chính xác đến từ bằng chứng thực thi", "Hạng 1 luôn là dòng LLM đoán, nhờ điểm thưởng không công bố"),
            ("Vá thử kiểm chứng dòng nghi", "Không đổi thứ hạng nào")]
    el = _bounds_ok(viz.claim_vs_evidence("ce", 40, 110, 880, rows))
    joined = " ".join(_texts(el)).replace("  ", " ")
    for claim, found in rows:
        assert all(w in joined for w in claim.split()) and all(w in joined for w in found.split())


def test_section_band_names_the_part():
    el = _bounds_ok(viz.section_band("band", 2, "Phương pháp giải quyết"))
    assert "Phần 2 · Phương pháp giải quyết" in _texts(el)


def test_formula_box_keeps_every_line():
    el = _bounds_ok(viz.formula("f", 40, 120, 400, ["Ochiai = a / √(b × c)", "a: số test fail chạy qua dòng"]))
    assert _texts(el)[-2:] == ["Ochiai = a / √(b × c)", "a: số test fail chạy qua dòng"]


def test_constraint_table_has_one_row_per_constraint():
    rows = [{"id": "C1", "where": "dòng 73", "expr": "len(m) == len(l) + len(r)", "fail": 4, "pass": 0, "ochiai": 1.0,
             "weight": 0.6, "score": 0.6},
            {"id": "C2", "where": "cuối nhánh if dòng 72", "expr": "len(m) == len(l) + len(r)", "fail": 4, "pass": 0,
             "ochiai": 1.0, "weight": 1.0, "score": 1.0}]
    el = _bounds_ok(viz.constraint_table("ct", 40, 120, 880, rows))
    t = _texts(el)
    assert "C1" in t and "C2" in t and "0,60" in t and "1,00" in t


def test_code_block_shows_inserted_checks():
    el = _bounds_ok(viz.code_block("c", 40, 100, ["a = 1", "b = 2"], first_no=10, inserted={10: "kiểm tra C1: a > 0"}))
    assert any("kiểm tra C1: a > 0" in t for t in _texts(el))


def test_progress_table_rows_and_status_colours():
    rows = [("Tái hiện SemLoc", "Đã xong", "Lần 1"), ("RQ3", "Đang hoàn thiện", "Lần 2"), ("Bài báo", "Chưa làm", "26/11–10/12")]
    el = _bounds_ok(viz.progress_table("pt", 40, 120, 880, rows))
    t = _texts(el)
    assert all(x in t for r in rows for x in r)
    assert len({r.get("fill") for r in el.iter("rect")}) >= 3

"""Storytelling pages of báo cáo lần 1 (one claim per page as the title, one picture as the evidence).

Every number is read from data/ or from the report's macros (bd._m), the same sources as the report.
Called from build_deck.main() with the build_deck module, whose E/A/D helpers are no-ops for pages a deck lacks.
"""
import csv
import json
import sys
from pathlib import Path

import viz
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from method_names import name  # noqa: E402

# lần 1 roster: output stem -> template slide (22 = title + empty canvas)
LAN1 = [("slide_01.svg", 1), ("moc.svg", 22), ("sbfl_mu.svg", 22), ("semloc_hua.svg", 22), ("cau_hoi.svg", 20),
        ("slide_08.svg", 8), ("hop_den_1.svg", 22), ("hop_den_2.svg", 22), ("nhan_sai.svg", 22), ("failloc.svg", 22),
        ("thiet_ke_l1.svg", 22), ("ket_qua.svg", 22), ("chi_phi.svg", 14), ("lan_sau.svg", 22),
        ("cong_cu_ai.svg", 22), ("hien_trang.svg", 22), ("tien_do.svg", 22), ("slide_30.svg", 30)]

# schedule shown on the Gantt page (dates of the course guide and the group's plan; not results)
SCHEDULE = [("Chốt nhóm, đề tài", "04/11", "05/11", True), ("Tài liệu, từ khóa", "05/11", "11/11", True),
            ("Tái hiện SemLoc (RQ1)", "06/11", "11/11", True), ("Nhãn đã sửa, so sánh (RQ2)", "09/11", "17/11", True),
            ("Báo cáo lần 1", "18/11", "19/11", False), ("Rà soát nhãn, RQ3, ablation", "12/11", "24/11", False),
            ("Báo cáo lần 2", "25/11", "26/11", False), ("Bài báo arXiv, phân tích", "26/11", "10/12", False),
            ("Bảo vệ", "12/12", "12/12", False)]
MAIN = ["sbfl_ochiai", "llm_direct", "semloc", "semloc_no_prior", "llm_tests"]


def _csv(path: Path) -> list[dict]:
    with open(path) as f:
        return list(csv.DictReader(f))


def _title(bd, page: str, title: str) -> None:
    bd.E(page, {"Classification": title})
    bd.D(page, "shape-2194")


def _note(x, y, lines, size=16, fill=MUTED, weight="normal", gid="ghi-chu", w=380) -> str:
    body = [_t(x, y + 22 * k, line, size=size, fill=fill, weight=weight) for k, line in enumerate(lines)]
    return viz._g(gid, x, y - size, w, 22 * len(lines) + 6, body)


def _card(gid, x, y, w, h, head, lines, color=NAVY) -> str:
    body = [_r(x, y, w, h, "#FFFFFF", stroke=color, rx=12, sw=2), _t(x + 18, y + 34, head, size=19, fill=color, weight="bold")]
    body += [_t(x + 18, y + 66 + 24 * k, line, size=16) for k, line in enumerate(lines)]
    return viz._g(gid, x, y, w, h, body)


def cover(bd, deck: str, occasion: str) -> None:
    bd.E("slide_01.svg", {
        "Introduction to Coding Workshop": ["Bằng chứng hay phỏng đoán:", "Tái hiện và đánh giá việc định vị",
                                            "lỗi ngữ nghĩa trong mã nguồn bằng", "mô hình ngôn ngữ lớn"],
        "Here is where your presentation begins": [
            "Grounded or Guessed: A Reproducibility Study", "of LLM-Based Semantic Fault Localization", "",
            "Đề tài 02-KH · Nhóm M9", "GVHD: PGS. TS. Huỳnh Quyết Thắng", occasion],
    })
    if bd.has("slide_01.svg"):
        p = bd.SVG / "slide_01.svg"
        s = p.read_text()
        s = s.replace('y="217.42351706" text-anchor="start" xml:space="preserve" font-size="60"',
                      'y="150" text-anchor="start" xml:space="preserve" font-size="36"', 1)
        s = s.replace('font-size="36" fill="#0C0A9E" data-pptx-text-baseline="metrics-v1" data-pptx-text-model="lines" '
                      'data-paragraph-line-height="72.0"', 'font-size="36" fill="#0C0A9E" data-pptx-text-baseline="metrics-v1" '
                      'data-pptx-text-model="lines" data-paragraph-line-height="46"', 1)
        s = s.replace('data-paragraph-line-height="25.6"', 'data-paragraph-line-height="20"', 1)
        s = s.replace('y="395.12598425" text-anchor="start" xml:space="preserve" font-size="21.33"',
                      'y="368" text-anchor="start" xml:space="preserve" font-size="15"', 1)
        p.write_text(s)


def lan1(bd) -> None:
    ex = json.loads((ROOT / "data" / "fig_example.json").read_text())
    code = {c["no"]: c["text"] for c in ex["code_lines"]}
    gt_line = ex["gt_line"]
    body_from = gt_line - 7
    fail_test = next(t for t in ex["tests"] if not t["passed"])

    # 2. hook: a failing test, which line is wrong?
    _title(bd, "moc.svg", "Một test thất bại. Dòng nào sai?")
    short = lambda t: t if len(t) <= 44 else t[:42].rstrip() + " …"
    bd.A("moc.svg", viz.code_block("ma-vi-du", 70, 118, [short(code[n]) for n in range(body_from, gt_line + 2)],
                                   first_no=body_from, fs=15, width=600))
    bd.A("moc.svg", _card("test-truot", 695, 130, 225, 250, "Chạy test",
                          ["", f"{sum(t['passed'] for t in ex['tests'])} test đạt", "", "1 test trượt:"], color=RED)
         + _note(713, 300, [fail_test["id"][:22], fail_test["id"][22:44], fail_test["id"][44:66]], size=13, fill=RED,
                 gid="ten-test", w=200))
    bd.A("moc.svg", _note(70, 470, [f"Chương trình {ex['program']} trong SemFault-250 (250 chương trình Python, mỗi chương "
                                    "trình một lỗi).", "Mã vẫn chạy, chỉ tính sai kết quả: đó là lỗi ngữ nghĩa."],
                          size=15, gid="nguon-vi-du", w=840))

    # 3. SBFL is blind on it: failing and passing tests run the same lines
    _title(bd, "sbfl_mu.svg", "SBFL mù: test đạt và test trượt đi qua cùng các dòng")
    rows = [n for n in range(body_from, gt_line + 1) if code[n].strip()]
    cols = [f"t{j + 1}" for j in range(len(ex["tests"]))]
    cells = {(i, j) for i, n in enumerate(rows) for j, t in enumerate(ex["tests"]) if n in t["lines"]}
    fail_cols = {j: RED for j, t in enumerate(ex["tests"]) if not t["passed"]}
    bd.A("sbfl_mu.svg", viz.matrix("ma-tran-phu", 70, 112, [f"{n}  {code[n].strip()[:24]}" for n in rows], cols, cells,
                                   row_mark={rows.index(gt_line): RED}, label_w=330, cell_w=52, row_h=34,
                                   col_colors={**{j: NAVY for j in range(len(cols))}, **fail_cols}))
    bd.A("sbfl_mu.svg", viz.big_number("sbfl-acc", 690, 140, f"{bd._m('RqOneSbflOchiaiFairAllAccOne')}%",
                                       "SBFL (Ochiai) đúng\nngay hạng 1 trên\n250 chương trình", color=RED, size=60, w=240))
    bd.A("sbfl_mu.svg", _note(690, 330, ["Cột đỏ: test trượt.", "Dòng tô màu: dòng lỗi.", "Mọi dòng có cùng điểm,",
                                         "SBFL chỉ còn đoán mò."], size=16))

    # 4. SemLoc's promise
    _title(bd, "semloc_hua.svg", "SemLoc hứa: neo LLM vào bằng chứng thực thi")
    bd.A("semloc_hua.svg", viz.pipeline("quy-trinh-semloc", 62, 140,
                                        ["LLM viết\nràng buộc", "Chèn\nvào mã", "Chạy\ntest", "Phổ vi phạm\n(Ochiai)",
                                         "LLM vá thử,\nchạy lại test"], box_w=144, gap=30, box_h=80))
    bd.A("semloc_hua.svg", viz.big_number("acc-cong-bo", 70, 280, f"{bd._m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}%",
                                          "Acc@1 SemLoc công bố\ntrên SemFault-250\n(Claude Sonnet 4.6)", size=64, w=300))
    bd.A("semloc_hua.svg", _note(420, 330, ["Bài báo: độ chính xác đến từ việc neo lập luận",
                                            "của LLM vào bằng chứng thực thi.", "",
                                            "Câu hỏi của nhóm: thật vậy không?"], size=18, fill=INK, w=480))

    # 5. the question and the three RQs (template list page)
    bd.E("cau_hoi.svg", [
        ("Popular programming languages", "Bằng chứng hay phỏng đoán? Ba câu hỏi"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: số công bố còn đúng", "khi chấm công bằng, sửa nhãn?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["LLM cần gì? FailLoc một lượt", "so với SemLoc nhiều bước"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, mã đổi tên,", "các họ mô hình khác"]),
        ("Saturn", "Lõi"), ("Saturn is a gas giant", ["Thứ hạng đến từ bằng chứng", "thực thi hay LLM tự đoán?"]),
    ])

    # 7-8. open the box: spectrum scores, then the +1.2 bonus on the guessed line
    rs = _bonus_rows()
    prog = rs[0]["program"]
    gt_rows = [r for r in rs if r["is_gt_repaired"] == "1"]
    for page, with_bonus in (("hop_den_1.svg", False), ("hop_den_2.svg", True)):
        _title(bd, page, "Mở hộp SemLoc: điểm phổ của từng dòng" if not with_bonus else
               f"Cộng +{bd._m('ConstPriorWeight')} cho dòng LLM đoán: nó luôn đứng hạng 1")
        ser = []
        for r in rs:
            lab = f"dòng {r['line']}" + (" (lỗi)" if r in gt_rows else "") + (" (đoán)" if with_bonus and r["is_guess"] == "1" else "")
            v = float(r["score"]) if with_bonus else float(r["spectrum"])
            c = ORANGE if (with_bonus and r["is_guess"] == "1") else (NAVY if r in gt_rows else GREY)
            ser.append((lab, v, c))
        bd.A(page, viz.bars("diem-dong", 70, 115, 560, 330, ser, vmax=2.0, unit="", label_w=180, nd=2))
        bd.A(page, f'<g id="nguong" data-pptx-bounds="{70 + 180 + (560 - 250) / 2} 112 2 336">'
                   f'<line x1="{70 + 180 + (560 - 250) / 2}" y1="112" x2="{70 + 180 + (560 - 250) / 2}" y2="448" '
                   f'stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 4"/></g>')
        bd.A(page, _note(70, 478, [f"Chương trình {prog}, lượt chạy 1 với Gemini 3.8 Flash. Vạch đứt: điểm phổ tối đa (1)."],
                         size=14, gid="nguon-diem", w=840))
    bd.A("hop_den_1.svg", _note(660, 170, ["Dòng lỗi có điểm phổ", "cao nhất.", "", "Phổ vi phạm đã chỉ đúng."],
                                size=19, fill=INK))
    share, n_pairs = _guess_rank1_share()
    bd.A("hop_den_2.svg", viz.big_number("ty-le-hang-1", 660, 140, f"{_p(100 * share, 0)}%",
                                         f"trong {n_pairs} lần chạy có\ndòng đoán, hạng 1 của\nSemLoc là dòng LLM đoán.\nBài báo không nhắc tới\nđiểm thưởng này.",
                                         color=ORANGE, size=60, w=260))

    # 9. the labels themselves are wrong; the execution-repaired labels
    _title(bd, "nhan_sai.svg", "Chính nhãn của bộ dữ liệu cũng sai")
    bd.A("nhan_sai.svg", viz.big_number("nhan-trong", 70, 118, bd._m("GtBlankN"), "nhãn gốc nằm trên\ndòng trống", color=RED, size=60))
    bd.A("nhan_sai.svg", viz.big_number("nhan-khong-chay", 360, 118, bd._m("GtNotExecutedN"),
                                        "chương trình: không test\nthất bại nào chạy tới nhãn", color=RED, size=60))
    bd.A("nhan_sai.svg", viz.pipeline("sua-nhan", 70, 330, ["Nhãn gốc\n250 CT", "Sửa nhỏ một dòng,\nchạy lại test",
                                                             f"Xác nhận {bd._m('GtConfirmedN')}\nDời {bd._m('GtCorrectedN')}",
                                                             f"Nhãn đã sửa\n{bd._m('GtRepairedN')} CT"],
                                      accent=3, box_w=180, gap=34, box_h=80))
    bd.A("nhan_sai.svg", _note(70, 460, ["LLM chỉ đề xuất bản sửa; test quyết định dòng nào là dòng lỗi.",
                                         "Mọi kết quả được báo trên cả nhãn gốc và nhãn đã sửa."], size=15,
                               gid="ghi-chu-nhan", w=840))

    # 10. FailLoc next to SemLoc
    _title(bd, "failloc.svg", f"{name('llm_tests')}: đưa thẳng test thất bại cho LLM, một lượt gọi")
    bd.A("failloc.svg", _t(70, 132, "SemLoc", size=20, fill=NAVY, weight="bold"))
    bd.A("failloc.svg", viz.pipeline("semloc-ngan", 70, 148, ["Ràng buộc", "Chèn, chạy", "Phổ vi phạm", "+ thưởng", "Vá thử"],
                                     box_w=128, gap=24, box_h=56, dashed={3}))
    bd.A("failloc.svg", _note(70, 240, [f"≈ {bd._m('CostSemlocTokensK')} nghìn token, {bd._m('CostSemlocCalls')} lượt gọi "
                                        "mỗi chương trình"], size=15, gid="chi-phi-semloc", w=700))
    bd.A("failloc.svg", _t(70, 300, name("llm_tests"), size=20, fill=ORANGE, weight="bold"))
    bd.A("failloc.svg", viz.pipeline("failloc-ngan", 70, 316, ["Mã nguồn +\ntest thất bại", "Một lượt\ngọi LLM",
                                                                "5 dòng\nnghi nhất"], accent=1, box_w=200, gap=40, box_h=70))
    bd.A("failloc.svg", _note(70, 422, [f"≈ {bd._m('CostLlmTestsTokensK')} nghìn token, {bd._m('CostLlmTestsCalls')} lượt "
                                        "gọi mỗi chương trình"], size=15, gid="chi-phi-failloc", w=700))
    bd.A("failloc.svg", _note(70, 470, ["Prompt: mã đánh số dòng, tên và dòng lỗi đầu tiên của từng test thất bại. Đây là "
                                        "cách lập trình viên", "vẫn hỏi trợ lý AI, được làm cho tái hiện được."],
                              size=14, gid="mo-ta-failloc", w=840))

    # 11. design
    _title(bd, "thiet_ke_l1.svg", "Thiết kế: cùng chương trình, cùng mô hình, so trên hai bộ nhãn")
    cols = [("Dữ liệu", ["SemFault-250", "dev 50 / test 200", "chia phân tầng"], GREY),
            ("Phương pháp", [name(m) for m in MAIN], NAVY),
            ("Bộ nhãn", ["Nhãn gốc", "Nhãn đã sửa", f"({bd._m('GtRepairedN')} CT)"], ORANGE),
            ("Lặp, chỉ số", ["3 lần chạy", "Acc@1, Acc@3", "bootstrap"], GREY)]
    body = []
    for k, (head, items, c) in enumerate(cols):
        x = 70 + k * 212
        body.append(_r(x, 130, 180, 250, "#FFFFFF", stroke=c, rx=12, sw=2))
        body.append(_t(x + 90, 162, head, size=18, fill=c if c != GREY else INK, weight="bold", anchor="middle"))
        body += [_t(x + 90, 205 + 32 * i, it, size=16, anchor="middle",
                    weight="bold" if it == name("llm_tests") else "normal",
                    fill=ORANGE if it == name("llm_tests") else INK) for i, it in enumerate(items)]
        if k:
            body.append(_t(x - 16, 262, "×", size=28, fill=MUTED, anchor="middle"))
    bd.A("thiet_ke_l1.svg", viz._g("luoi-thiet-ke", 70, 130, 816, 250, body))
    bd.A("thiet_ke_l1.svg", _note(70, 430, ["Mô hình: Gemini 3.8 Flash cho mọi phương pháp có LLM.",
                                            "Tập dev chỉ dùng để chọn tham số; mọi số báo cáo là của tập test."],
                                  size=15, gid="ghi-chu-thiet-ke", w=840))

    # 12. results race
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    _title(bd, "ket_qua.svg", f"{name('llm_tests')} dẫn đầu ở Acc@1 trên cả hai bộ nhãn")
    for k, (gt, head) in enumerate((("original", "Nhãn gốc"), ("repaired", "Nhãn đã sửa"))):
        x = 60 + k * 440
        bd.A("ket_qua.svg", _t(x + 150, 128, f"{head}: Acc@1", size=18, fill=INK, weight="bold"))
        ser = [(name(m), 100 * float(rq2[(gt, m)]["acc1_mean"]),
                ORANGE if m == "llm_tests" else NAVY if m == "semloc" else GREY) for m in MAIN]
        bd.A("ket_qua.svg", viz.bars(f"bars-{gt}", x, 140, 420, 290, ser, vmax=100, label_w=150))
    d1 = bd._m("RqTwoRepairedAllLlmTestsDAccOne")
    bd.A("ket_qua.svg", _note(70, 462, ["Tập test, Gemini 3.8 Flash, trung bình 3 lần chạy.",
                                        f"Nhãn đã sửa: {name('llm_tests')} hơn SemLoc {d1} điểm Acc@1 "
                                        f"[{bd._m('RqTwoRepairedAllLlmTestsDAccOneLo')}; "
                                        f"{bd._m('RqTwoRepairedAllLlmTestsDAccOneHi')}],"
                                        + f" Acc@3 {_p(100 * float(rq2[('repaired', 'llm_tests')]['acc3_mean']))}% so với "
                                        f"{_p(100 * float(rq2[('repaired', 'semloc')]['acc3_mean']))}%."],
                              size=14, gid="ghi-chu-ket-qua", w=840))

    # 13. three big numbers (template metric page)
    ratio = float(bd._m("CostSemlocTokensK").replace(",", ".")) / float(bd._m("CostLlmTestsTokensK").replace(",", "."))
    bd.E("chi_phi.svg", {
        "9h 55m 23s": d1, "Jupiter’s rotation period": f"điểm Acc@1 so với SemLoc (nhãn đã sửa)",
        "333,000": f"{_p(ratio, 0)}×", "The Sun’s mass compared": "ít token hơn SemLoc mỗi chương trình",
        "386,000 km": bd._m("CostLlmTestsCalls").split(",")[0], "Distance between the Earth": "lượt gọi LLM, không pipeline",
    })

    # 14. cliffhanger for report 2
    _title(bd, "lan_sau.svg", "Thắng thật hay nhờ nhãn? Và vì sao? (lần 2)")
    for k, (head, lines) in enumerate((("Nhãn còn sai?", ["Rà soát cả 250 nhãn,", "duyệt mù độc lập", "bởi hai người"]),
                                       ("Có bền không?", ["Lỗi thật BugsInPy,", "mã đổi tên định danh,", "năm họ mô hình"]),
                                       ("Vì sao thắng?", ["Ablation: test thất bại", "hay độ phủ từng dòng", "tạo khác biệt?"]))):
        bd.A("lan_sau.svg", _card(f"cau-hoi-{k}", 70 + k * 280, 140, 250, 200, head, lines, color=[RED, NAVY, ORANGE][k]))
    bd.A("lan_sau.svg", _note(70, 420, ["Dữ liệu và mã cho cả ba câu đã có; kết quả trình bày ở báo cáo lần 2 (25–26/11)."],
                              size=16, gid="hen-lan-2", w=840))

    # 17. Gantt
    _title(bd, "tien_do.svg", "Tiến độ")
    bd.A("tien_do.svg", viz.gantt("gantt", 70, 140, 820, SCHEDULE, today="18/11", label_w=290, row_h=38))


def _bonus_rows() -> list[dict]:
    from make_figures import bonus_example
    return bonus_example()[1]


def _guess_rank1_share() -> tuple[float, int]:
    rows = _csv(ROOT / "data" / "semloc_line_scores.csv")
    guesses = [r for r in rows if r["is_guess"] == "1"]
    return sum(r["rank"] == "1" for r in guesses) / len(guesses), len(guesses)


def notes_lan1(bd) -> dict:
    """Spoken notes for báo cáo lần 1 (Vietnamese prose; every number is one the page shows)."""
    ex = json.loads((ROOT / "data" / "fig_example.json").read_text())
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    a1 = lambda gt, m: _p(100 * float(rq2[(gt, m)]["acc1_mean"]))
    share, n_pairs = _guess_rank1_share()
    rs = _bonus_rows()
    gt_line = next(r["line"] for r in rs if r["is_gt_repaired"] == "1")
    guess_line = next(r["line"] for r in rs if r["is_guess"] == "1")
    ratio = float(bd._m("CostSemlocTokensK").replace(",", ".")) / float(bd._m("CostLlmTestsTokensK").replace(",", "."))
    m = bd._m
    return {
        "slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 1 của đề tài: bằng chứng hay phỏng đoán, "
                    "tái hiện và đánh giá việc định vị lỗi ngữ nghĩa trong mã nguồn bằng mô hình ngôn ngữ lớn.",
        "moc": f"Nhóm bắt đầu bằng một tình huống quen thuộc. Đây là hàm {ex['program']} trong bộ dữ liệu SemFault-250: chạy "
               "bộ test thì có một test trượt, các test còn lại đều đạt. Mã vẫn chạy bình thường, chỉ có kết quả bị tính sai, "
               "nên các công cụ kiểm tra cú pháp hay kiểu không báo gì. Câu hỏi là dòng nào sai.",
        "sbfl_mu": "Cách kinh điển là định vị lỗi dựa trên phổ, gọi tắt là SBFL: dòng nào hay được test trượt chạy qua mà ít "
                   "được test đạt chạy qua thì đáng nghi. Ở đây cột màu đỏ là test trượt, và nó chạy qua đúng những dòng mà "
                   f"các test đạt cũng chạy qua. Mọi dòng vì thế nhận cùng một điểm, kể cả dòng {ex['gt_line']} là dòng lỗi "
                   f"thật. Trên cả 250 chương trình, SBFL chỉ đúng ngay hạng 1 ở {m('RqOneSbflOchiaiFairAllAccOne')}%.",
        "semloc_hua": "SemLoc, bài trung tâm trong ba bài thầy giao, đề xuất một quy trình nhiều bước. LLM viết ra các ràng "
                      "buộc ngữ nghĩa, ràng buộc được chèn vào mã, chạy test để biết ràng buộc nào bị vi phạm, rồi LLM vá thử "
                      f"để kiểm chứng. Tác giả báo cáo Acc@1 là {m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% và cho rằng "
                      "độ chính xác này đến từ việc neo LLM vào bằng chứng thực thi. Nhóm muốn kiểm tra lại đúng điều đó.",
        "cau_hoi": "Từ đó nhóm đặt câu hỏi: thứ hạng của SemLoc đến từ bằng chứng thực thi hay từ việc LLM tự đoán. RQ1 tái "
                   "hiện kết quả công bố và kiểm tra cách chấm điểm, kể cả chính các nhãn. RQ2 so SemLoc với FailLoc, phương "
                   "pháp của nhóm chỉ dùng một lượt gọi LLM. RQ3 kiểm tra độ bền, nhóm sẽ trình bày ở lần sau.",
        "slide_08": "Ba hướng liên quan nhất nhóm đọc là SemLoc, EffiHolmes cho lỗi chạy chậm, và một nghiên cứu công nghiệp "
                    "đưa stack trace vào prompt cho LLM. Từ SemLoc, nhóm học cách chạy lại đúng mã của tác giả và soát từng "
                    "con số. Nghiên cứu công nghiệp cho thấy đưa bằng chứng sẵn có vào prompt giúp LLM trúng hơn, và FailLoc "
                    "đi theo ý tưởng đó.",
        "hop_den_1": f"Giờ nhóm mở hộp SemLoc trên một chương trình cụ thể, {rs[0]['program']}. Mỗi thanh là điểm phổ vi phạm "
                     f"của một dòng, cao nhất là 1. Dòng {gt_line}, dòng lỗi thật, có điểm cao nhất, nghĩa là phổ vi phạm "
                     "đã chỉ đúng.",
        "hop_den_2": f"Nhưng mã nguồn công bố có một bước bài báo không nhắc tới: dòng LLM tự đoán được cộng thêm "
                     f"{m('ConstPriorWeight')} điểm. Điểm phổ không bao giờ vượt quá 1, nên dòng đoán luôn vượt lên đứng đầu, "
                     f"ở đây là dòng {guess_line} đứng trên dòng lỗi. Trong {n_pairs} lần chạy có dòng đoán, tỉ lệ này là "
                     f"{_p(100 * share, 0)}%.",
        "nhan_sai": f"Kiểm tra kỹ hơn, nhóm thấy chính nhãn của bộ dữ liệu cũng có vấn đề: {m('GtBlankN')} nhãn nằm trên dòng "
                    f"trống, và ở {m('GtNotExecutedN')} chương trình không test trượt nào chạy tới dòng được gán nhãn. Nhóm "
                    "dựng lại bộ nhãn bằng thực thi: LLM chỉ đề xuất bản sửa nhỏ, còn test quyết định. Kết quả là "
                    f"{m('GtConfirmedN')} nhãn được xác nhận, {m('GtCorrectedN')} nhãn được dời vị trí, và bộ nhãn đã sửa "
                    f"còn {m('GtRepairedN')} chương trình. Mọi kết quả sau đây đều báo trên cả hai bộ nhãn.",
        "failloc": "Phương pháp nhóm đề xuất tên là FailLoc. Nó làm đúng việc lập trình viên vẫn làm với trợ lý AI: đưa mã "
                   "nguồn cùng tên và thông báo lỗi của các test trượt cho LLM, hỏi một lần, nhận về năm dòng đáng nghi nhất. "
                   f"SemLoc tốn khoảng {m('CostSemlocTokensK')} nghìn token mỗi chương trình, FailLoc khoảng "
                   f"{m('CostLlmTestsTokensK')} nghìn.",
        "thiet_ke_l1": "Để so sánh công bằng, năm phương pháp chạy trên cùng 200 chương trình của tập test, cùng mô hình "
                       "Gemini 3.8 Flash. Mỗi phương pháp có LLM được chạy ba lần, kết quả báo trên cả nhãn gốc lẫn nhãn đã "
                       "sửa. Tập dev 50 chương trình chỉ dùng để chọn tham số.",
        "ket_qua": f"Đây là kết quả chính. Trên cả nhãn gốc lẫn nhãn đã sửa, FailLoc đứng đầu ở Acc@1. Trên nhãn đã sửa, "
                   f"FailLoc đạt {a1('repaired', 'llm_tests')}%, SemLoc {a1('repaired', 'semloc')}%, tức hơn "
                   f"{m('RqTwoRepairedAllLlmTestsDAccOne')} điểm, và khoảng tin cậy không chạm 0. Bỏ điểm thưởng đi, SemLoc "
                   f"chỉ còn {a1('repaired', 'semloc_no_prior')}%.",
        "chi_phi": f"Gói lại trong ba con số: FailLoc hơn SemLoc {m('RqTwoRepairedAllLlmTestsDAccOne')} điểm Acc@1, dùng ít "
                   f"token hơn khoảng {_p(ratio, 0)} lần, và chỉ cần {m('CostLlmTestsCalls').split(',')[0]} lượt gọi LLM cho "
                   "mỗi chương trình. Một quy trình nhiều bước chỉ đáng dùng khi nó thắng được cách hỏi thẳng này.",
        "lan_sau": "Trước khi tin kết quả này, nhóm còn ba câu hỏi phải trả lời. Thứ nhất, nhãn đã sửa vẫn có thể còn sai, "
                   "nên nhóm rà soát lại cả 250 nhãn và cho hai người duyệt mù. Thứ hai, kết quả có giữ được trên lỗi thật, "
                   "trên mã đã đổi tên và trên các họ mô hình khác không. Thứ ba, thông tin nào trong prompt tạo ra khác biệt. "
                   "Nhóm sẽ trình bày cả ba ở báo cáo lần 2.",
        "cong_cu_ai": "Về công cụ AI, Claude Code là trợ lý chính để đọc tài liệu, viết mã, chạy thực nghiệm và soạn báo cáo. "
                      "Các LLM trong thực nghiệm đều được gọi qua một proxy có nhật ký và bộ đệm, nên mọi lượt chạy phát lại "
                      "được. Nhóm trưởng duyệt mọi thay đổi, và mọi con số được sinh tự động từ dữ liệu.",
        "hien_trang": "Theo yêu cầu, lần 1 cần xong ít nhất hai trong bốn nội dung. Nhóm đã xong phần tài liệu và phần chính "
                      "của câu hỏi nghiên cứu và thực nghiệm. Đóng góp và triết lý khoa học sẽ trình bày ở lần 2, còn bài báo "
                      "được viết khi đủ kết quả.",
        "tien_do": "Về tiến độ, các thanh màu xanh đậm là phần đã xong. Từ nay đến báo cáo lần 2 ngày 25/11, nhóm hoàn thành "
                   "rà soát nhãn, RQ3 và ablation, sau đó viết bài báo và chuẩn bị bảo vệ ngày 12/12.",
        "slide_30": "Nhóm xin cảm ơn thầy và các bạn đã lắng nghe, và rất mong nhận được câu hỏi và góp ý.",
    }

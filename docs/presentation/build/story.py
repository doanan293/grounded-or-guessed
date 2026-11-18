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
        ("ba_bai.svg", 22), ("hop_den_1.svg", 22), ("hop_den_2.svg", 22), ("nhan_sai.svg", 22), ("failloc.svg", 22),
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
    n_pass = sum(t["passed"] for t in ex["tests"])
    m = bd._m
    P = viz.panel

    # 2. hook: a failing test, which line is wrong?
    _title(bd, "moc.svg", "Một test thất bại. Dòng nào sai?")
    short = lambda t: t if len(t) <= 40 else t[:38].rstrip() + " …"
    bd.A("moc.svg", viz.code_block("ma-vi-du", 50, 108, [short(code[n]) for n in range(body_from, gt_line + 2)],
                                   first_no=body_from, fs=15, width=520))
    bd.A("moc.svg", P("ket-qua-test", 50, 352, 520, [
        ("Chạy bộ test", f"{n_pass} test đạt, 1 test trượt: {fail_test['id']}. Mã không lỗi cú pháp, không lỗi kiểu; "
                         "chỉ kết quả bị tính sai.")], size=14, head_color=RED))
    bd.A("moc.svg", P("bai-toan", 600, 108, 320, [
        ("Bài toán định vị lỗi", "Đầu vào: mã nguồn và bộ test, trong đó có test trượt. Đầu ra: các dòng mã xếp theo "
                                 "mức đáng nghi, dòng nghi nhất ở hạng 1."),
        ("Lỗi ngữ nghĩa", "Chương trình chạy đúng đường nhưng tính sai giá trị, nên không công cụ kiểm tra cú pháp "
                          "hay kiểu nào báo ra."),
        ("Chỉ số Acc@1", "Tỉ lệ chương trình có dòng lỗi thật đứng ở hạng 1. Acc@3: nằm trong 3 dòng đầu."),
        ("Ví dụ", f"Hàm {ex['program']}, một trong 250 chương trình Python của bộ SemFault-250."),
    ], size=14))

    # 3. SBFL is blind on it: failing and passing tests run the same lines
    _title(bd, "sbfl_mu.svg", "SBFL mù: test đạt và test trượt đi qua cùng các dòng")
    rows = [n for n in range(body_from, gt_line + 1) if code[n].strip()]
    cols = [f"t{j + 1}" for j in range(len(ex["tests"]))]
    cells = {(i, j) for i, n in enumerate(rows) for j, t in enumerate(ex["tests"]) if n in t["lines"]}
    fail_cols = {j: RED for j, t in enumerate(ex["tests"]) if not t["passed"]}
    bd.A("sbfl_mu.svg", viz.matrix("ma-tran-phu", 40, 108, [f"{n}  {code[n].strip()[:20]}" for n in rows], cols, cells,
                                   row_mark={rows.index(gt_line): RED}, label_w=280, cell_w=46, row_h=34,
                                   col_colors={**{j: NAVY for j in range(len(cols))}, **fail_cols}))
    n_fail = len(fail_cols)
    ochiai = 1 / ((n_fail * len(ex["tests"])) ** 0.5)
    bd.A("sbfl_mu.svg", P("sbfl-giai-thich", 580, 108, 340, [
        ("Cách đọc", "Mỗi hàng là một dòng mã, mỗi cột là một test; chấm nghĩa là test chạy qua dòng đó. Cột đỏ là test "
                     f"trượt, hàng tô màu là dòng lỗi {gt_line}."),
        ("SBFL tính điểm thế nào", "Dòng càng hay được test trượt chạy qua và càng ít được test đạt chạy qua thì càng "
                                   "đáng nghi (công thức Ochiai, điểm từ 0 đến 1)."),
        ("Ở ví dụ này", f"Mọi dòng đều được cả {len(ex['tests'])} test chạy qua, nên dòng nào cũng có điểm "
                        f"{_p(ochiai, 2)}; dòng lỗi không nổi bật."),
    ], size=14))
    bd.A("sbfl_mu.svg", viz.big_number("sbfl-acc", 40, 400, f"{m('RqOneSbflOchiaiFairAllAccOne')}%",
                                       "Acc@1 của SBFL trên\n250 chương trình", color=RED, size=44, w=340))

    # 4. SemLoc's promise
    _title(bd, "semloc_hua.svg", "SemLoc hứa: neo LLM vào bằng chứng thực thi")
    steps = ["LLM viết\nràng buộc", "Chèn\nvào mã", "Chạy\ntest", "Phổ vi phạm\n(Ochiai)", "LLM vá thử,\nchạy lại test"]
    bd.A("semloc_hua.svg", viz.pipeline("quy-trinh-semloc", 50, 108, steps, box_w=150, gap=28, box_h=72))
    expl = ["Điều kiện phải đúng,\nví dụ tổng phần chia\nbằng tổng ban đầu", "Mỗi ràng buộc thành\nmột lệnh kiểm tra\ntại một dòng",
            "Ghi ràng buộc nào\nbị vi phạm trong\ntest nào", "Ràng buộc vi phạm\nnhiều ở test trượt\nthì dòng của nó nghi",
            "Vá dòng nghi; test\nđạt lại thì xác nhận\ndòng đó"]
    body = []
    for k, e in enumerate(expl):
        for r, line in enumerate(e.split("\n")):
            body.append(_t(50 + k * 178 + 75, 206 + 19 * r, line, size=13, fill=MUTED, anchor="middle"))
    bd.A("semloc_hua.svg", viz._g("giai-thich-buoc", 50, 192, 878, 66, body))
    bd.A("semloc_hua.svg", viz.big_number("acc-cong-bo", 50, 300, f"{m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}%",
                                          "Acc@1 SemLoc công bố\ntrên SemFault-250\n(Claude Sonnet 4.6)", size=60, w=300))
    bd.A("semloc_hua.svg", P("loi-hua", 380, 290, 540, [
        ("Bài báo khẳng định", "Độ chính xác đến từ việc neo lập luận của LLM vào bằng chứng thực thi: LLM chỉ đề xuất, "
                               "kết quả chạy test quyết định thứ hạng."),
        ("Nhóm kiểm tra", "Thứ hạng thật sự đến từ bằng chứng thực thi (grounded), hay từ việc LLM tự đoán (guessed)?"),
    ], size=15))

    # 5. the question and the three RQs (template list page)
    bd.E("cau_hoi.svg", [
        ("Popular programming languages", "Bằng chứng hay phỏng đoán? Ba câu hỏi"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: số công bố còn đúng", "khi chấm công bằng, sửa nhãn?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["LLM cần gì? FailLoc một lượt", "so với SemLoc nhiều bước"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, mã đổi tên,", "các họ mô hình khác"]),
        ("Saturn", "Lõi"), ("Saturn is a gas giant", ["Thứ hạng đến từ bằng chứng", "thực thi hay LLM tự đoán?"]),
    ])

    # 6a. related work: many studies in five families, the three assigned papers highlighted
    _title(bd, "lien_quan.svg", "Nghiên cứu liên quan: năm hướng, ba bài tiêu biểu")
    fams = [("Định vị theo phổ\nvà đột biến", ["Tarantula 2002", "Ochiai 2009", "DStar 2014", "MUSE 2014",
                                                "Metallaxis 2015", "Pearson 2017"], NAVY),
            ("Định vị bằng LLM", ["Wu 2023", "AutoFL 2024", "Agentless 2024", "AgentFL 2025", "FlexFL 2025",
                                  "★ SemLoc 2026"], ORANGE),
            ("So sánh lần chạy,\nbằng chứng thực thi", ["Delta debugging 2002", "Chuỗi nhân quả 2002", "Daikon 2007",
                                                       "★ EffiHolmes 2026", "★ Sự cố + LLM 2026"], ORANGE),
            ("Dữ liệu lỗi và\ntính hợp lệ", ["Defects4J 2014", "QuixBugs 2017", "BugsInPy 2020", "Nhãn sai 2021",
                                              "Bản vá giả 2015", "Nhiễm dữ liệu 2024"], NAVY),
            ("Thực tế lập\ntrình viên", ["Parnin, Orso 2011", "Kochhar 2016", "DevGPT 2024", "Stack Overflow 2025",
                                          "JetBrains 2025"], NAVY)]
    body = []
    for k, (head, items, c) in enumerate(fams):
        x = 40 + k * 180
        body.append(_r(x, 108, 168, 330, "#FFFFFF", stroke=LAVENDER, rx=10))
        for r, line in enumerate(head.split("\n")):
            body.append(_t(x + 84, 132 + 19 * r, line, size=15, fill=NAVY, weight="bold", anchor="middle"))
        for i, it in enumerate(items):
            star = it.startswith("★")
            yy = 178 + 42 * i
            body.append(_r(x + 10, yy, 148, 32, viz.CREAM if star else viz.LIGHT, stroke=ORANGE if star else "none", rx=8))
            body.append(_t(x + 84, yy + 21, it.replace("★ ", ""), size=13, anchor="middle", weight="bold" if star else "normal",
                           fill=INK))
    bd.A("lien_quan.svg", viz._g("ban-do-lien-quan", 40, 108, 888, 330, body))
    bd.A("lien_quan.svg", _note(40, 470, ["Khung cam: ba bài giảng viên giao, trình bày ở trang sau. Danh sách đầy đủ "
                                          "và cách chọn tài liệu: chương 2 của báo cáo."], size=14, gid="chu-thich-lien-quan",
                                w=880))

    # 6b. the three representative studies
    _title(bd, "ba_bai.svg", "Nghiên cứu liên quan: ba bài tiêu biểu và điều nhóm học được")
    cards = [("SemLoc (2026)", [("Bài toán", "lỗi ngữ nghĩa trong hàm Python; test trượt nhưng không chỉ ra dòng."),
                                 ("Cách làm", "LLM viết ràng buộc, chạy test lấy phổ vi phạm, vá thử để kiểm chứng."),
                                 ("Kết quả", f"Acc@1 {m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% trên SemFault-250."),
                                 ("Nhóm học", "chạy lại đúng mã của tác giả, soát từng con số (RQ1).")]),
             ("EffiHolmes (2026)", [("Bài toán", "lỗi hiệu năng: test vẫn đạt, không có lỗi để lần theo."),
                                     ("Cách làm", "so hai lần chạy dữ liệu nhỏ và lớn; hàm chậm hẳn đi thì bị nghi."),
                                     ("Kết quả", "thử trên 140 lỗi chạy chậm thật."),
                                     ("Nhóm học", "đặt lần chạy đúng cạnh lần chạy lỗi; cách chia ba câu hỏi.")]),
             ("Sự cố + LLM (2026)", [("Bài toán", "app Java lớn sập hàng nghìn lần mỗi tuần, mỗi lần có stack trace."),
                                      ("Cách làm", "gom stack trace thành bảng hàm đáng nghi, đưa bảng vào prompt."),
                                      ("Kết quả", "38 lỗi thật, chỉ đúng chỗ lỗi 71%."),
                                      ("Nhóm học", "đưa bằng chứng sẵn có vào một prompt: ý tưởng của FailLoc.")])]
    for k, (head, blocks) in enumerate(cards):
        bd.A("ba_bai.svg", _t(40 + k * 300, 128, head, size=19, fill=ORANGE, weight="bold"))
        bd.A("ba_bai.svg", P(f"bai-{k}", 40 + k * 300, 140, 284, [(a, b[0].upper() + b[1:]) for a, b in blocks], size=14))

    # 7-8. open the box: spectrum scores, then the +1.2 bonus on the guessed line
    rs = _bonus_rows()
    prog = rs[0]["program"]
    gt_r = next(r for r in rs if r["is_gt_repaired"] == "1")
    guess_r = next(r for r in rs if r["is_guess"] == "1")
    for page, with_bonus in (("hop_den_1.svg", False), ("hop_den_2.svg", True)):
        _title(bd, page, "Mở hộp SemLoc: điểm phổ của từng dòng" if not with_bonus else
               f"Cộng +{m('ConstPriorWeight')} cho dòng LLM đoán: nó luôn đứng hạng 1")
        ser = []
        for r in rs:
            g, gs = r is gt_r, with_bonus and r is guess_r
            lab = f"dòng {r['line']}" + (" (lỗi)" if g else "") + (" (đoán)" if gs else "")
            v = float(r["score"]) if with_bonus else float(r["spectrum"])
            ser.append((lab, v, ORANGE if gs else (NAVY if g else GREY), float(r["spectrum"]) if gs else 0))
        bd.A(page, viz.bars("diem-dong", 40, 108, 520, 330, ser, vmax=2.0, unit="", label_w=170, nd=2))
        xline = 40 + 170 + (520 - 170 - 70) / 2
        bd.A(page, f'<g id="nguong" data-pptx-bounds="{xline} 104 2 338"><line x1="{xline}" y1="104" x2="{xline}" y2="442" '
                   f'stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 4"/></g>')
        bd.A(page, _note(40, 470, [f"Chương trình {prog} (SemFault-250), lượt chạy 1 với Gemini 3.8 Flash."], size=13,
                         gid="nguon-diem", w=520))
    bd.A("hop_den_1.svg", P("doc-hinh-1", 590, 108, 330, [
        ("Hình này cho thấy", f"Điểm SemLoc chấm cho {len(rs)} dòng ứng viên của một chương trình, trước khi xếp hạng."),
        ("Điểm phổ là gì", "Với mỗi ràng buộc LLM viết, đếm test trượt và test đạt vi phạm nó rồi tính Ochiai (0 đến 1). "
                           "Điểm của dòng là điểm cao nhất trong các ràng buộc gắn với dòng đó."),
        ("Cách đọc", "Thanh dài là dòng đáng nghi hơn; xanh đậm là dòng lỗi thật; vạch đứt là mức tối đa 1."),
        ("Ý chính", f"Chỉ với bằng chứng thực thi, dòng lỗi {gt_r['line']} đứng đầu: phổ vi phạm đã chỉ đúng."),
    ], size=14))
    share, n_pairs = _guess_rank1_share()
    bd.A("hop_den_2.svg", P("doc-hinh-2", 590, 108, 330, [
        ("Điều bài báo không nói", f"Mã công bố cộng +{m('ConstPriorWeight')} điểm cho dòng LLM tự đoán (trường "
                                   "fault_line). Phần cam trên thanh là điểm thưởng đó."),
        ("Vì sao luôn hạng 1", f"Điểm phổ tối đa là 1, nhỏ hơn {m('ConstPriorWeight')}, nên dòng đoán luôn vượt mọi dòng khác."),
        ("Ở ví dụ này", f"Dòng {guess_r['line']} ({_p(float(guess_r['spectrum']), 2)} + {m('ConstPriorWeight')}) vượt dòng "
                        f"lỗi {gt_r['line']} ({_p(float(gt_r['spectrum']), 2)}): đáp án đúng bị đẩy xuống hạng 2."),
    ], size=14))
    bd.A("hop_den_2.svg", viz.big_number("ty-le-hang-1", 590, 390, f"{_p(100 * share, 0)}%",
                                         f"số lần chạy (trên {n_pairs}) mà hạng 1\ncủa SemLoc là dòng LLM đoán",
                                         color=ORANGE, size=40, w=330))

    # 9. the labels themselves are wrong; the execution-repaired labels
    _title(bd, "nhan_sai.svg", "Chính nhãn của bộ dữ liệu cũng sai")
    bd.A("nhan_sai.svg", viz.big_number("nhan-trong", 40, 104, m("GtBlankN"), "nhãn gốc nằm trên dòng trống,\nnơi không thể có lỗi",
                                        color=RED, size=52, w=280))
    bd.A("nhan_sai.svg", viz.big_number("nhan-khong-chay", 330, 104, m("GtNotExecutedN"),
                                        "chương trình: không test trượt\nnào chạy tới dòng được gán nhãn", color=RED, size=52, w=280))
    bd.A("nhan_sai.svg", P("nhan-la-gi", 640, 104, 280, [
        ("Nhãn là gì", "Dòng lỗi chuẩn mà bộ dữ liệu ghi cho mỗi chương trình; mọi phương pháp được chấm đúng sai theo nó."),
        ("Vì sao quan trọng", "Nhãn sai thì một phương pháp chỉ đúng dòng vẫn bị chấm là trượt."),
    ], size=14))
    bd.A("nhan_sai.svg", viz.pipeline("sua-nhan", 40, 300, ["Nhãn gốc\n250 CT", "Sửa nhỏ một dòng,\nchạy lại test",
                                                             f"Xác nhận {m('GtConfirmedN')}\nDời {m('GtCorrectedN')}",
                                                             f"Nhãn đã sửa\n{m('GtRepairedN')} CT"],
                                      accent=3, box_w=196, gap=34, box_h=74))
    bd.A("nhan_sai.svg", P("bo-phan-dinh", 40, 392, 880, [
        ("Bộ phán định sửa tối thiểu", "LLM chỉ đề xuất bản sửa nhỏ tại nhãn hoặc dòng lân cận; dòng nào sửa xong làm mọi "
                                       "test đạt thì đó là dòng lỗi. Test quyết định, LLM không quyết định. Mọi kết quả sau "
                                       "đây được báo trên cả nhãn gốc lẫn nhãn đã sửa.")], size=14))

    # 10. FailLoc next to SemLoc, with the prompt it sends
    _title(bd, "failloc.svg", f"{name('llm_tests')}: đưa thẳng test thất bại cho LLM, một lượt gọi")
    bd.A("failloc.svg", _t(40, 126, "SemLoc", size=18, fill=NAVY, weight="bold"))
    bd.A("failloc.svg", viz.pipeline("semloc-ngan", 40, 138, ["Ràng\nbuộc", "Chèn,\nchạy", "Phổ", "+thưởng", "Vá thử"],
                                     box_w=96, gap=16, box_h=56))
    bd.A("failloc.svg", _note(40, 214, [f"≈ {m('CostSemlocTokensK')} nghìn token, {m('CostSemlocCalls')} lượt gọi mỗi CT"],
                              size=14, gid="chi-phi-semloc", w=540))
    bd.A("failloc.svg", _t(40, 276, name("llm_tests"), size=18, fill=ORANGE, weight="bold"))
    bd.A("failloc.svg", viz.pipeline("failloc-ngan", 40, 288, ["Mã +\ntest trượt", "Một lượt\ngọi LLM", "5 dòng\nnghi nhất"],
                                     accent=1, box_w=150, gap=30, box_h=64))
    bd.A("failloc.svg", _note(40, 376, [f"≈ {m('CostLlmTestsTokensK')} nghìn token, {m('CostLlmTestsCalls')} lượt gọi mỗi CT"],
                              size=14, gid="chi-phi-failloc", w=540))
    bd.A("failloc.svg", P("vi-sao-failloc", 40, 400, 540, [
        ("Vì sao làm vậy", "Đây là cách lập trình viên vẫn hỏi trợ lý AI khi test trượt; nhóm làm nó tái hiện được và "
                           "dùng làm mốc mà quy trình nhiều bước phải vượt.")], size=14))
    prompt = ["Mã nguồn đánh số dòng:", "  22 weight_sum = sum(weights)", "  …",
              f"{n_fail} test trượt, {n_pass} test đạt;", "chương trình có đúng một dòng lỗi.", "Test trượt:",
              f"  {fail_test['id'][:30]}", "  dòng lỗi đầu tiên của test", "Trả về 5 dòng nghi nhất (JSON)."]
    body = [_r(610, 108, 310, 300, viz.LIGHT, stroke=ORANGE, rx=10), _t(626, 134, "Prompt của FailLoc (rút gọn)", size=15,
                                                                         fill=ORANGE, weight="bold")]
    body += [_t(626, 164 + 26 * k, line, size=13, family=viz.MONO) for k, line in enumerate(prompt)]
    bd.A("failloc.svg", viz._g("prompt-failloc", 610, 108, 310, 300, body))

    # 11. design
    _title(bd, "thiet_ke_l1.svg", "Thiết kế: cùng chương trình, cùng mô hình, so trên hai bộ nhãn")
    cols = [("Dữ liệu", ["SemFault-250", "dev 50 / test 200", "chia phân tầng"], GREY),
            ("Phương pháp", [name(mm) for mm in MAIN], NAVY),
            ("Bộ nhãn", ["Nhãn gốc", "Nhãn đã sửa", f"({m('GtRepairedN')} CT)"], ORANGE),
            ("Lặp, chỉ số", ["3 lần chạy", "Acc@1, Acc@3", "bootstrap"], GREY)]
    body = []
    for k, (head, items, c) in enumerate(cols):
        x = 40 + k * 222
        body.append(_r(x, 108, 190, 220, "#FFFFFF", stroke=c, rx=12, sw=2))
        body.append(_t(x + 95, 138, head, size=18, fill=c if c != GREY else INK, weight="bold", anchor="middle"))
        body += [_t(x + 95, 178 + 30 * i, it, size=16, anchor="middle",
                    weight="bold" if it == name("llm_tests") else "normal",
                    fill=ORANGE if it == name("llm_tests") else INK) for i, it in enumerate(items)]
        if k:
            body.append(_t(x - 16, 228, "×", size=28, fill=MUTED, anchor="middle"))
    bd.A("thiet_ke_l1.svg", viz._g("luoi-thiet-ke", 40, 108, 856, 220, body))
    bd.A("thiet_ke_l1.svg", P("giai-thich-thiet-ke", 40, 344, 880, [
        ("Công bằng", "Mọi phương pháp có LLM dùng cùng Gemini 3.8 Flash trên cùng 200 chương trình của tập test; tập dev "
                      "chỉ để chọn tham số."),
        ("Chỉ số", "Acc@k là tỉ lệ chương trình có dòng lỗi nằm trong k dòng đầu. Mỗi cấu hình chạy 3 lần; khoảng tin cậy "
                   "95% tính bằng bootstrap, lấy mẫu lại theo chương trình."),
    ], size=14))

    # 12. results race
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    _title(bd, "ket_qua.svg", f"{name('llm_tests')} dẫn đầu ở Acc@1 trên cả hai bộ nhãn")
    for k, (gt, head) in enumerate((("original", "Nhãn gốc"), ("repaired", "Nhãn đã sửa"))):
        x = 30 + k * 300
        bd.A("ket_qua.svg", _t(x + 140, 124, f"{head}: Acc@1", size=16, fill=INK, weight="bold"))
        ser = [(name(mm), 100 * float(rq2[(gt, mm)]["acc1_mean"]),
                ORANGE if mm == "llm_tests" else NAVY if mm == "semloc" else GREY) for mm in MAIN]
        bd.A("ket_qua.svg", viz.bars(f"bars-{gt}", x, 134, 290, 300, ser, vmax=100, label_w=140))
    d1 = m("RqTwoRepairedAllLlmTestsDAccOne")
    a1 = lambda gt, mm: _p(100 * float(rq2[(gt, mm)]["acc1_mean"]))
    a3 = lambda gt, mm: _p(100 * float(rq2[(gt, mm)]["acc3_mean"]))
    bd.A("ket_qua.svg", P("doc-ket-qua", 640, 108, 290, [
        ("Cách đọc", "Mỗi thanh là Acc@1: % chương trình có dòng lỗi ở hạng 1. Tập test, Gemini 3.8 Flash, trung bình 3 "
                     "lần chạy."),
        ("So với SemLoc", f"Nhãn đã sửa: {name('llm_tests')} hơn {d1} điểm Acc@1 (khoảng tin cậy "
                          f"[{m('RqTwoRepairedAllLlmTestsDAccOneLo')}; {m('RqTwoRepairedAllLlmTestsDAccOneHi')}]); Acc@3 "
                          f"{a3('repaired', 'llm_tests')}% so với {a3('repaired', 'semloc')}%."),
        ("Ý chính", f"Bỏ điểm thưởng, SemLoc rơi từ {a1('repaired', 'semloc')}% xuống {a1('repaired', 'semloc_no_prior')}%: "
                    "phần lớn hạng 1 của nó là dòng đoán."),
    ], size=13))

    # 13. three big numbers (template metric page)
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    bd.E("chi_phi.svg", {
        "9h 55m 23s": d1, "Jupiter’s rotation period": "điểm Acc@1 hơn SemLoc",
        "333,000": f"{_p(ratio, 0)}×", "The Sun’s mass compared": "ít token hơn SemLoc",
        "386,000 km": m("CostLlmTestsCalls").split(",")[0], "Distance between the Earth": "lượt gọi LLM mỗi chương trình",
    })

    bd.A("chi_phi.svg", _t(60, 52, "Ba con số của báo cáo lần 1", size=24, fill=INK, weight="bold", family="Arial, sans-serif"))
    bd.A("chi_phi.svg", P("giai-thich-chi-phi", 560, 250, 360, [
        ("Đo thế nào", "Nhãn đã sửa, 200 chương trình của tập test, Gemini 3.8 Flash, trung bình 3 lần chạy; token là tổng "
                       "token vào và ra của mọi lượt gọi LLM cho một chương trình."),
        ("Nghĩa là", "Cách hỏi thẳng có test thất bại vừa chính xác hơn vừa rẻ hơn quy trình nhiều bước."),
    ], size=14))

    # 14. cliffhanger for report 2
    _title(bd, "lan_sau.svg", "Thắng thật hay nhờ nhãn? Và vì sao? (lần 2)")
    for k, (head, lines) in enumerate((("Nhãn còn sai?", ["Rà soát cả 250 nhãn,", "duyệt mù độc lập", "bởi hai người"]),
                                       ("Có bền không?", ["Lỗi thật BugsInPy,", "mã đổi tên định danh,", "năm họ mô hình"]),
                                       ("Vì sao thắng?", ["Ablation: test thất bại", "hay độ phủ từng dòng", "tạo khác biệt?"]))):
        bd.A("lan_sau.svg", _card(f"cau-hoi-{k}", 40 + k * 300, 130, 270, 200, head, lines, color=[RED, NAVY, ORANGE][k]))
    bd.A("lan_sau.svg", P("hen-lan-2", 40, 360, 870, [
        (None, "Dữ liệu và mã cho cả ba câu đã có; kết quả trình bày ở báo cáo lần 2 (25–26/11).")], size=15))

    # 17. Gantt
    _title(bd, "tien_do.svg", "Tiến độ")
    bd.A("tien_do.svg", viz.gantt("gantt", 40, 140, 860, SCHEDULE, today="18/11", label_w=290, row_h=38))
    bd.A("tien_do.svg", _note(40, 516, ["Xanh đậm: đã xong. Tím nhạt: đang làm hoặc sắp tới. Vạch đỏ: hôm nay."], size=14,
                              gid="chu-thich-gantt", w=860))


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
        "ba_bai": "Trong nhiều nghiên cứu về định vị lỗi nhóm đã đọc, ba bài tiêu biểu nhất là ba bài thầy giao. SemLoc là bài trung tâm: LLM viết ràng buộc, chạy test để lấy phổ vi phạm. EffiHolmes xử lý lỗi chạy chậm "
                  "bằng cách so hai lần chạy, còn nghiên cứu công nghiệp đưa stack trace của các lần sập vào prompt. Từ SemLoc "
                  "nhóm học cách tái hiện và soát số, từ hai bài kia nhóm lấy ý tưởng đặt bằng chứng sẵn có vào một prompt, "
                  "tức là FailLoc.",
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

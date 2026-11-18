"""Báo cáo lần 2 (~20 phút, 23 trang): a one-page recap of lần 1, then the answers to its three open questions —
are the labels right (review + blind review), is the result robust (RQ3), why does FailLoc win (ablation, additions,
decomposition) — then contributions and scientific philosophy (content 3) and the progress table.
Numbers come from the same data functions as the report figures (scripts/make_figures.py) or from the macros."""
import viz
from story_common import (MAIN, ROOT, _csv, _note, _title, _unbold, band, examples, name)  # noqa: F401
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

import make_figures as mf  # noqa: E402  (scripts/ is on sys.path via story_common)

LAN2 = [("slide_01.svg", 1), ("muc_luc_2.svg", 22), ("nhac_lai.svg", 22),
        ("nhan_lech.svg", 22), ("ablation_la_gi.svg", 22), ("shapley.svg", 22),
        ("ra_soat.svg", 22), ("duyet_mu.svg", 22), ("rq3_thiet_ke.svg", 22), ("ba_prompt.svg", 22), ("bo_sung.svg", 22),
        ("nhan_di_dau.svg", 22), ("ba_bo_nhan.svg", 22),
        ("bugsinpy.svg", 22), ("doi_ten.svg", 22), ("ho_mo_hinh.svg", 22), ("ablation_kq.svg", 22), ("bo_sung_kq.svg", 22),
        ("phan_ra.svg", 22), ("cai_tien_2.svg", 22),
        ("dong_gop_2.svg", 22), ("tien_do_2.svg", 22), ("slide_30.svg", 30)]

PROGRESS = [("Tài liệu, RQ, tái hiện SemLoc, chuẩn hóa nhãn, so sánh chính", "Đã xong", "Lần 1"),
            ("Rà soát nhãn, duyệt mù, độ bền (RQ3), ablation, các cách bổ sung", "Đã xong", "Lần 2"),
            ("Đóng góp và triết lý khoa học (nội dung 3)", "Đã xong", "Lần 2"),
            ("Bài báo arXiv (nội dung 4)", "Có bản nháp", "Hoàn thiện 26/11–10/12"),
            ("Phân tích thất bại, kiểm chứng bằng bản sửa", "Đang hoàn thiện", "Bảo vệ (12/2026)"),
            ("Báo cáo final và slide bảo vệ", "Đang hoàn thiện", "01/12–12/12")]
GT_VI = {"original": "Nhãn gốc", "repaired": "Nhãn đã chuẩn hóa", "reviewed": "Nhãn đã rà soát"}
GT_COL = {"original": GREY, "repaired": ORANGE, "reviewed": NAVY}


def _forest(gid, x, y, w, rows, lo_hi=True, vmin=-15.0, vmax=15.0, row_h=40, label_w=300):
    """Rows (label, value, lo, hi, colour); a zero line; values in points of percentage."""
    span = w - label_w - 80
    px = lambda v: x + label_w + span * (v - vmin) / (vmax - vmin)
    body = [f'<line x1="{px(0):.1f}" y1="{y}" x2="{px(0):.1f}" y2="{y + row_h * len(rows)}" stroke="{MUTED}" stroke-width="1.5"/>']
    for i, (lab, v, lo, hi, c) in enumerate(rows):
        cy = y + row_h * (i + 0.5)
        body.append(_t(x + label_w - 10, cy + 5, lab, size=14, anchor="end"))
        if lo is not None:
            body.append(f'<line x1="{px(lo):.1f}" y1="{cy:.1f}" x2="{px(hi):.1f}" y2="{cy:.1f}" stroke="{c}" stroke-width="3"/>')
        body.append(f'<circle cx="{px(v):.1f}" cy="{cy:.1f}" r="7" fill="{c if lo is not None else "#FFFFFF"}" stroke="{c}" stroke-width="2"/>')
        body.append(_t(px(max(v, hi if hi is not None else v)) + 12, cy + 5, f"{'+' if v >= 0 else ''}{_p(v)}", size=13, weight="bold"))
    for t in (vmin, 0, vmax):
        body.append(_t(px(t), y + row_h * len(rows) + 18, f"{'+' if t > 0 else ''}{_p(t, 0)}", size=12, fill=MUTED, anchor="middle"))
    return viz._g(gid, x, y, w, row_h * len(rows) + 24, body)


def pages(bd) -> None:
    m = bd._m
    P = viz.panel
    ex = examples()
    va, bo = ex["votes_apportion"], ex["blend_orders"]
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    acc = lambda g, mm, k=1: 100 * float(rq2[(g, mm)][f"acc{k}_mean"])

    # 2. agenda
    _title(bd, "muc_luc_2.svg", "Nội dung trình bày lần 2")
    items = [("", "Nhắc lại lần 1", "FailLoc thắng SemLoc; ba câu hỏi còn mở"),
             ("1", "Cơ sở lý thuyết bổ sung", "Nhãn sai làm sai phép chấm; ablation; phân rã Shapley"),
             ("2", "Phương pháp", "Rà soát nhãn, duyệt mù, RQ3, ba mức prompt"),
             ("3", "Kiểm tra lại bài gốc (tiếp)", "Nhãn gốc đi đâu; kết quả trên ba bộ nhãn"),
             ("5", "Thực nghiệm và kết quả", "Độ bền, vì sao FailLoc thắng, phân rã"),
             ("", "Đóng góp, triết lý khoa học, tiến độ", "Nội dung 3 và bảng tiến độ")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 112 + i * 62
        body.append(_r(60, y, 840, 52, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else LAVENDER, rx=10, sw=1.2))
        body.append(_t(92, y + 34, k or "•", size=24, fill=NAVY, weight="bold", anchor="middle"))
        body.append(_t(130, y + 33, head, size=18, fill=NAVY, weight="bold"))
        body.append(_t(470, y + 33, desc, size=14))
    bd.A("muc_luc_2.svg", viz._g("muc-luc", 60, 112, 840, 362, body))

    # 3. recap of report 1
    _title(bd, "nhac_lai.svg", "Nhắc lại lần 1: phương pháp FailLoc thắng phương pháp SemLoc")
    bd.A("nhac_lai.svg", viz.bars("lan1", 40, 110, 440, 200, [(name(mm), acc("repaired", mm), ORANGE if mm == "llm_tests" else
                                                                NAVY if mm == "semloc" else GREY) for mm in MAIN],
                                  vmax=100, label_w=150))
    bd.A("nhac_lai.svg", _note(40, 336, ["Acc@1, nhãn đã chuẩn hóa, tập test, Gemini 3.8 Flash,", "trung bình 3 lần chạy."],
                               size=13, gid="nguon-lan1", w=440))
    bd.A("nhac_lai.svg", P("lan1-tom-tat", 500, 104, 430, [
        ("Lần 1 đã cho thấy", "Hạng 1 của SemLoc luôn là dòng LLM đoán nhờ điểm thưởng; nhãn của bộ dữ liệu có vấn đề; FailLoc "
                              f"(một lượt gọi LLM kèm test fail) hơn SemLoc {m('RqTwoRepairedAllLlmTestsDAccOne')} điểm Acc@1."),
        ("Ba câu hỏi còn mở", "1. Nhãn đã chuẩn hóa có còn sai không? 2. Kết quả có bền trên lỗi thật, mã đổi tên, mô hình khác "
                              "không? 3. Vì sao FailLoc thắng?"),
    ], size=14))

    # 4. a label one line off changes the score
    code = {c["no"]: c["text"] for c in bo["code_lines"]}
    _title(bd, "nhan_lech.svg", "Nhãn lệch một dòng cũng làm sai phép chấm")
    band(bd, "nhan_lech.svg", 1)
    bd.A("nhan_lech.svg", viz.code_block("ma-nhan", 30, 104, [code[n][:52] for n in range(70, 75)], first_no=70, fs=15, width=560,
                                         highlight={72, 73}, mark={72: "nhãn gốc", 73: "dòng thân của if"}))
    bd.A("nhan_lech.svg", P("vi-sao-lech", 610, 104, 320, [
        ("Đầu khối và thân khối", "Lỗi nằm ở điều kiện dòng 72 hay ở câu lệnh dòng 73 mà điều kiện bảo vệ? Hai cách gán nhãn "
                                  "đều hợp lý, nhưng phép chấm chặt chỉ công nhận một dòng."),
        ("Hệ quả", "Một phương pháp chỉ ra dòng 73 bị chấm là sai theo nhãn gốc. Lỗi trải hai dòng cũng vậy."),
        ("Cách nhóm xử lý", "Rà soát lại cả 250 nhãn; nhãn hai dòng được công nhận cả hai dòng."),
    ], size=14))
    bd.A("nhan_lech.svg", P("dinh-nghia-bo-nhan", 30, 260, 560, [
        ("Ba bộ nhãn", "Nhãn gốc (tác giả); nhãn đã chuẩn hóa (test quyết định, lần 1); nhãn đã rà soát (LLM rà trước, người "
                       "duyệt, kiểm tra lại bằng duyệt mù, lần này)."),
    ], size=14))

    # 5. ablation: what it is
    _title(bd, "ablation_la_gi.svg", "Ablation: thêm từng thành phần để đo tác dụng của nó")
    band(bd, "ablation_la_gi.svg", 1)
    steps = [("LLM-Direct", "chỉ mã nguồn"), ("FailLoc", "+ tên và lỗi của test fail"), ("FailLoc+Cov", "+ độ phủ từng dòng")]
    body = []
    for i, (h, d) in enumerate(steps):
        x = 40 + i * 300
        body.append(_r(x, 110, 250, 80, viz.CREAM if h == "FailLoc" else "#FFFFFF", stroke=ORANGE if h == "FailLoc" else NAVY, rx=10, sw=2))
        body.append(_t(x + 125, 142, h, size=18, weight="bold", anchor="middle", fill=NAVY))
        body.append(_t(x + 125, 168, d, size=14, anchor="middle"))
        if i:
            body.append(viz._arrow(x - 46, 150, x - 4, 150))
            body.append(_t(x - 25, 214, "tác dụng của " + ("test fail" if i == 1 else "độ phủ"), size=13, fill=MUTED, anchor="middle"))
    bd.A("ablation_la_gi.svg", viz._g("ba-buoc", 40, 110, 850, 110, body))
    bd.A("ablation_la_gi.svg", P("ablation-giai-thich", 40, 250, 880, [
        ("Ablation là gì", "Giữ mọi thứ khác cố định (cùng chương trình, cùng mô hình, cùng cách chấm) và chỉ thêm hoặc bỏ một "
                           "thành phần. Chênh lệch độ chính xác giữa hai bước liền nhau là tác dụng của thành phần đó."),
        ("Câu hỏi", "FailLoc thắng nhờ thông tin test fail, hay sẽ thắng hơn nữa nếu đưa thêm độ phủ từng dòng (thông tin mà "
                    "phương pháp SBFL dùng)?"),
    ], size=15))

    # 6. Shapley decomposition: what it is
    _title(bd, "shapley.svg", "Phân rã Shapley: độ chính xác của phương pháp SemLoc đến từ đâu")
    band(bd, "shapley.svg", 1)
    combos = [("Không nguồn nào", "Acc = 0"), ("Chỉ dòng LLM đoán", "xếp riêng dòng đoán"),
              ("Chỉ phổ vi phạm", "xếp theo điểm phổ"), ("Cả hai (SemLoc)", "điểm phổ + thưởng")]
    body = []
    for i, (h, d) in enumerate(combos):
        x, y = 40 + (i % 2) * 290, 110 + (i // 2) * 96
        body.append(_r(x, y, 270, 80, "#FFFFFF", stroke=NAVY if i == 3 else LAVENDER, rx=10, sw=1.8))
        body.append(_t(x + 135, y + 34, h, size=16, weight="bold", anchor="middle", fill=NAVY))
        body.append(_t(x + 135, y + 58, d, size=13, anchor="middle"))
    bd.A("shapley.svg", viz._g("bon-to-hop", 40, 110, 560, 176, body))
    bd.A("shapley.svg", P("shapley-giai-thich", 620, 104, 310, [
        ("Ý tưởng", "Đo độ chính xác ở cả bốn tổ hợp. Phần của một nguồn là mức tăng trung bình khi thêm nguồn đó vào, tính "
                    "trên mọi thứ tự thêm."),
        ("Câu hỏi", "Bao nhiêu phần độ chính xác của SemLoc đến từ bằng chứng thực thi (phổ vi phạm), bao nhiêu từ việc LLM "
                    "tự đoán?"),
    ], size=14))
    bd.A("shapley.svg", viz.formula("shapley-ct", 40, 310, 560, [
        "phần(đoán) = ½·[v(đoán) − v(∅)] + ½·[v(cả hai) − v(phổ)]",
        "v(·): Acc@k khi chỉ dùng các nguồn trong ngoặc",
        "phần(đoán) + phần(phổ) = v(cả hai)"], size=15))

    # 7. two-step label review
    _title(bd, "ra_soat.svg", "Rà soát nhãn hai bước: LLM rà trước, thành viên nhóm duyệt")
    band(bd, "ra_soat.svg", 2)
    bd.A("ra_soat.svg", viz.pipeline("ra-soat", 40, 112, [f"Nhãn gốc\n{m('LabaudAllN')} chương trình", "LLM rà trước\nnhận định từng nhãn",
                                                          f"Người duyệt\n{m('ReviewReviewersN')} thành viên,\n{m('ReviewHumanN')} nhãn nghi vấn",
                                                          f"Nhãn đã rà soát\n{m('LabaudAllMoved')} nhãn dời"],
                                     accent=3, box_w=196, gap=32, box_h=90))
    bd.A("ra_soat.svg", P("ra-soat-giai-thich", 40, 236, 880, [
        ("Vì sao cần", "Bộ phán định của lần 1 chỉ xác nhận được nhãn khi tìm ra bản sửa nhỏ, và chỉ tìm dòng lân cận khi nhãn "
                       "gốc không chạy tới được. Rà soát kiểm tra mọi nhãn."),
        ("Cách làm", "LLM đọc mã, test và nhãn gốc của cả 250 chương trình, cho nhận định: đúng, sai (kèm dòng đề xuất), hoặc "
                     "lỗi trải hai dòng. Thành viên nhóm duyệt lại mọi nhãn bị dời hoặc bị LLM cho là sai."),
        ("Rủi ro", "Người duyệt có xem gợi ý của LLM, nên có thể bị dẫn dắt. Vì vậy nhóm làm thêm vòng duyệt mù (trang sau)."),
    ], size=14))

    # 8. blind review
    _title(bd, "duyet_mu.svg", "Duyệt mù: kiểm tra lại nhãn mà không có gợi ý của LLM")
    band(bd, "duyet_mu.svg", 2)
    sheet = [_r(40, 104, 430, 250, "#FFFFFF", stroke=LAVENDER, rx=10),
             _t(56, 130, "Phiếu duyệt (một chương trình)", size=15, weight="bold", fill=NAVY),
             _t(56, 158, "Mã nguồn + bộ test (không ghi nhãn nào)", size=13, fill=MUTED)]
    for i, (k, ln) in enumerate((("A", 64), ("B", 72), ("C", 73), ("D", 65))):
        sheet += [_r(56, 176 + i * 38, 400, 30, viz.LIGHT, rx=6), _t(70, 196 + i * 38, f"{k})  dòng {ln}", size=14, family=viz.MONO)]
    sheet.append(_t(56, 340, "Chọn dòng lỗi; thứ tự A–D xáo ngẫu nhiên", size=13, fill=MUTED))
    bd.A("duyet_mu.svg", viz._g("phieu", 40, 104, 430, 250, sheet))
    bd.A("duyet_mu.svg", P("duyet-mu-giai-thich", 500, 104, 430, [
        ("Thiết kế", f"{m('BlindBlindAllPrograms')} chương trình chọn ngẫu nhiên (hạt giống cố định), chia theo bốn nhóm: nhãn bị "
                     "dời, nhãn LLM cho là sai, nhãn giữ nguyên, nhãn hai dòng."),
        ("Ai duyệt", "Mỗi chương trình do hai thành viên chưa từng xem nó duyệt độc lập."),
        ("Không gợi ý", "Các dòng ứng viên (nhãn gốc, dòng bộ phán định dời tới, dòng LLM đề xuất, nhãn đã rà soát) được đánh "
                        "chữ A–D theo thứ tự ngẫu nhiên, không ghi dòng nào từ đâu."),
    ], size=14))
    bd.A("duyet_mu.svg", _note(40, 384, ["Ví dụ phiếu: chương trình blend_orders;", "kết quả duyệt mù ở phần 3."], size=13,
                               gid="vd-phieu", w=430))

    # 9. RQ3 design
    _title(bd, "rq3_thiet_ke.svg", "Thiết kế RQ3: ba cách thử độ bền")
    band(bd, "rq3_thiet_ke.svg", 2)
    vcode = {c["no"]: c["text"] for c in va["code_lines"]}
    renamed = (ROOT / "data" / "semfault_renamed" / "programs" / "votes_apportion.py").read_text().splitlines()
    bd.A("rq3_thiet_ke.svg", viz.code_block("truoc", 30, 104, [vcode[n].strip()[:30] for n in (22, 24, 25, 29)], first_no=22, fs=13, width=300))
    bd.A("rq3_thiet_ke.svg", viz.code_block("sau", 30, 220, [renamed[n - 1].strip()[:30] for n in (22, 24, 25, 29)], first_no=22, fs=13, width=300))
    bd.A("rq3_thiet_ke.svg", _note(30, 342, ["Trên: mã gốc. Dưới: mã đổi tên", "(dòng 22, 24, 25, 29).",
                                             "Tên gợi ý (weights, shares) biến mất."], size=12, gid="ghi-chu-doi-ten", w=300))
    bd.A("rq3_thiet_ke.svg", P("rq3-ba-cach", 350, 104, 580, [
        ("Lỗi thật BugsInPy", f"{m('BipAllSemlocPriorN')} lỗi thật của dự án youtube-dl dựng lại được môi trường. Kiểm tra "
                              "xem kết luận trên lỗi cài sẵn có còn đúng với lỗi thật."),
        ("Mã đổi tên định danh", "Đổi mọi tên biến, hàm phụ thành v1, v2…, xóa chú thích. Nếu LLM nhớ bộ dữ liệu từ lúc huấn "
                                 "luyện, độ chính xác sẽ giảm khi tên gợi ý biến mất."),
        ("Năm họ mô hình", "Gemini 3.8 Flash, GPT-6 luna, Claude Sonnet 5.5, gpt-oss-120b, Gemini 3.5 Flash-Lite trên một tập "
                           "con cố định của tập test."),
    ], size=14))

    # 10. three prompt levels on the running example
    _title(bd, "ba_prompt.svg", "Ba mức prompt trên ví dụ: thêm test fail, rồi thêm độ phủ")
    band(bd, "ba_prompt.svg", 2)
    win = [25, 26, 28, 29]
    rows = [("LLM-Direct", [f"{n}: {vcode[n].strip()[:33]}" for n in win], NAVY),
            ("FailLoc", [f"{n}: {vcode[n].strip()[:33]}" for n in win] + ["Test fail: test_truncation_sum_…"], ORANGE),
            ("FailLoc+Cov", [f"{n}: {vcode[n].strip()[:22]}  [f=1/p=4]" for n in win] + ["Test fail: test_truncation_sum_…"], NAVY)]
    for i, (h, lines, c) in enumerate(rows):
        x = 30 + i * 305
        g = [_r(x, 104, 290, 240, viz.LIGHT, stroke=c, rx=10, sw=1.6), _t(x + 14, 128, h, size=16, weight="bold", fill=c)]
        g += [_t(x + 14, 156 + 22 * k, l, size=11, family=viz.MONO) for k, l in enumerate(lines)]
        bd.A("ba_prompt.svg", viz._g(f"prompt-{i}", x, 104, 290, 240, g))
    bd.A("ba_prompt.svg", P("ba-prompt-giai-thich", 30, 362, 900, [
        ("Đọc thế nào", "[f=1/p=4] nghĩa là 1 test fail và 4 test pass chạy qua dòng đó: đúng thông tin phương pháp SBFL dùng. "
                        "Ở ví dụ này mọi dòng đều [f=1/p=4], nên độ phủ không thêm gì; thông báo lỗi của test fail mới gợi ý dòng 29."),
    ], size=14))

    # 11. additions and static tools
    _title(bd, "bo_sung.svg", "Các cách bổ sung nhóm thử thêm và công cụ phân tích tĩnh")
    band(bd, "bo_sung.svg", 2)
    for k, (h, lines, c) in enumerate((
            ("CovGate (cho SemLoc)", ["Xếp lại các dòng của SemLoc:", "dòng không test fail nào chạy", "qua bị đẩy xuống; cộng thêm", "điểm Ochiai có trọng số."], NAVY),
            ("FailLoc+Vote", ["Hỏi FailLoc ba lần, gộp ba", "danh sách bằng tổng nghịch", "đảo hạng: dòng hay đứng đầu", "được ưu tiên."], ORANGE),
            ("Phân tích tĩnh", ["ruff (kiểm tra phong cách mã)", "và pyrefly (kiểm tra kiểu) chạy", "trên 250 chương trình: cảnh báo", "có trúng dòng lỗi không?"], GREY))):
        bd.A("bo_sung.svg", P(f"bo-sung-{k}", 30 + k * 305, 104, 290, [(h, " ".join(lines))], size=14,
                              head_color=c if c != GREY else INK))
    bd.A("bo_sung.svg", P("bo-sung-cau-hoi", 30, 300, 900, [
        ("Câu hỏi", "Thêm phức tạp vào FailLoc hay vào SemLoc có thu hẹp được khoảng cách, hoặc vượt được FailLoc không? "
                    "Công cụ phân tích tĩnh có bắt được lỗi ngữ nghĩa không?"),
    ], size=15))

    # 12. where the original labels went + blind review result
    lf = mf.label_flow_data()
    _title(bd, "nhan_di_dau.svg", f"Gần một nửa nhãn gốc bị dời: {m('LabaudAllMoved')} trên {m('LabaudAllN')}")
    band(bd, "nhan_di_dau.svg", 3)
    cols = [GREY, "#C9C9C3", RED, "#E8956F", NAVY, "#8FB6EA"]
    x, body = 40.0, []
    for (lab, v), c in zip(lf["parts"], cols):
        w = 880 * v / lf["n"]
        body.append(_r(x, 110, w, 50, c))
        if v >= 15:
            body.append(_t(x + w / 2, 142, str(v), size=15, weight="bold", fill="#FFFFFF" if c in (GREY, RED, NAVY) else INK, anchor="middle"))
        x += w
    for i, ((lab, v), c) in enumerate(zip(lf["parts"], cols)):
        lx, ly = 40 + (i % 3) * 300, 184 + (i // 3) * 26
        body += [_r(lx, ly - 12, 14, 14, c), _t(lx + 22, ly, f"{lab} ({v})", size=13)]
    bd.A("nhan_di_dau.svg", viz._g("dong-nhan", 40, 110, 880, 110, body))
    bd.A("nhan_di_dau.svg", viz.big_number("mu-ra-soat", 40, 260, f"{m('BlindBlindAllMatchReviewed')}/{m('BlindBlindAllNReviewed')}",
                                           "câu trả lời duyệt mù trùng\nnhãn đã rà soát", color=NAVY, size=44, w=280))
    bd.A("nhan_di_dau.svg", viz.big_number("mu-goc", 330, 260, f"{m('BlindBlindAllMatchOriginal')}/{m('BlindBlindAllNOriginal')}",
                                           "trùng nhãn gốc", color=GREY, size=44, w=240))
    bd.A("nhan_di_dau.svg", P("nhan-y-chinh", 600, 252, 330, [
        ("Ý chính", "Người duyệt không có gợi ý chọn nhãn đã rà soát nhiều hơn hẳn nhãn gốc: bộ nhãn đã rà soát đáng tin hơn. "
                    f"{m('BlindAnswersExcluded')} câu trả lời bị loại vì có ghi chú dẫn lại tệp duyệt có gợi ý."),
    ], size=13))

    # 13. results on three label sets
    _title(bd, "ba_bo_nhan.svg", "Ba bộ nhãn: phương pháp FailLoc hơn SemLoc ở Acc@1")
    band(bd, "ba_bo_nhan.svg", 3)
    for k, g in enumerate(("original", "repaired", "reviewed")):
        x = 30 + k * 305
        bd.A("ba_bo_nhan.svg", _t(x + 150, 116, GT_VI[g], size=15, weight="bold", anchor="middle"))
        bd.A("ba_bo_nhan.svg", viz.bars(f"bo-{g}", x, 126, 290, 150, [("SemLoc", acc(g, "semloc"), NAVY), ("FailLoc", acc(g, "llm_tests"), ORANGE)],
                                        vmax=100, label_w=90))
    bd.A("ba_bo_nhan.svg", P("ba-bo-giai-thich", 30, 300, 900, [
        ("Đọc thế nào", "Acc@1, tập test, Gemini 3.8 Flash, trung bình 3 lần chạy. Bộ nhãn đã rà soát cho số cao hơn vì nhãn trỏ "
                        "đúng dòng hơn và chấp nhận lỗi hai dòng."),
        ("Ý chính", f"Mức hơn của FailLoc giữ nguyên chiều trên cả ba bộ: {m('RqTwoOriginalAllLlmTestsDAccOne')} (gốc), "
                    f"{m('RqTwoRepairedAllLlmTestsDAccOne')} (đã chuẩn hóa), {m('RqTwoReviewedAllLlmTestsDAccOne')} (đã rà soát) điểm."),
    ], size=14))

    # 14. BugsInPy
    r3 = mf.rq3_data()
    _title(bd, "bugsinpy.svg", "Lỗi thật BugsInPy: phương pháp FailLoc cao nhất ở Acc@3")
    band(bd, "bugsinpy.svg", 5)
    meths = [("sbfl_ochiai", "SBFL (Ochiai)", GREY), ("semloc_spectrum", "Chỉ phổ vi phạm", GREY), ("llm_guess", "Chỉ dòng LLM đoán", GREY),
             ("semloc_prior", "SemLoc", NAVY), ("llm_coverage", "FailLoc+Cov", GREY), ("llm_tests", "FailLoc", ORANGE)]
    bd.A("bugsinpy.svg", viz.bars("bip", 30, 104, 560, 320, [(l, r3["bugsinpy3"][k], c) for k, l, c in meths], vmax=100, label_w=190))
    bd.A("bugsinpy.svg", P("bip-giai-thich", 610, 104, 320, [
        ("Thí nghiệm", f"{m('BipAllSemlocPriorN')} lỗi thật của youtube-dl, Acc@3, Gemini 3.8 Flash, ba lần chạy."),
        ("Ý chính", "FailLoc cao nhất ở Acc@3. Ở Acc@1, mọi lần SemLoc đúng ở hạng 1 đều là dòng LLM đoán; riêng phổ vi phạm "
                    "gần bằng phương pháp SBFL."),
        ("Lưu ý", "Mẫu nhỏ, khoảng tin cậy rộng: ở Acc@1 FailLoc và FailLoc+Cov ngang nhau."),
    ], size=14))

    # 15. renaming
    _title(bd, "doi_ten.svg", "Đổi tên định danh: dòng đoán giữ được, phổ vi phạm giảm mạnh")
    band(bd, "doi_ten.svg", 5)
    body = []
    labs = {"semloc": ("SemLoc", NAVY), "semloc_no_prior": ("SemLoc−Bonus", GREY), "llm_guess": ("Chỉ dòng đoán", "#8FB6EA"),
            "llm_coverage": ("FailLoc+Cov", ORANGE)}
    py = lambda v: 400 - 2.9 * (v - 0)
    body += [_t(150, 420, "Mã gốc", size=14, anchor="middle"), _t(450, 420, "Đổi tên", size=14, anchor="middle")]
    for mm, (a, b) in r3["renamed"].items():
        lab, c = labs[mm]
        body.append(f'<line x1="150" y1="{py(a):.1f}" x2="450" y2="{py(b):.1f}" stroke="{c}" stroke-width="3"/>')
        body += [f'<circle cx="150" cy="{py(a):.1f}" r="6" fill="{c}"/>', f'<circle cx="450" cy="{py(b):.1f}" r="6" fill="{c}"/>',
                 _t(140, py(a) + 5, _p(a), size=12, anchor="end"), _t(462, py(b) + 5, f"{_p(b)}  {lab}", size=13, weight="bold")]
    bd.A("doi_ten.svg", viz._g("do-doc", 40, 104, 560, 330, body))
    bd.A("doi_ten.svg", P("doi-ten-giai-thich", 620, 104, 310, [
        ("Đọc thế nào", "Acc@3 trên nhãn đã chuẩn hóa, trước và sau khi đổi tên mọi định danh và xóa chú thích."),
        ("Ý chính", "SemLoc bỏ điểm thưởng (chỉ còn phổ vi phạm) giảm nhiều nhất: ràng buộc LLM viết dựa vào tên gợi ý. "
                    "FailLoc+Cov gần như không đổi."),
    ], size=14))

    # 16. model families
    n_drop = sum(v["semloc_no_prior"] < v["semloc"] for v in r3["families"].values())
    _title(bd, "ho_mo_hinh.svg", f"Năm họ mô hình: bỏ thưởng, phương pháp SemLoc giảm ở {n_drop}/{len(r3['families'])} họ")
    band(bd, "ho_mo_hinh.svg", 5)
    body = []
    for i, (fam, v) in enumerate(r3["families"].items()):
        y = 124 + i * 52
        px = lambda t: 260 + 3.4 * t
        body += [_t(250, y + 5, fam, size=14, anchor="end"),
                 f'<line x1="{px(v["semloc_no_prior"]):.1f}" y1="{y}" x2="{px(v["semloc"]):.1f}" y2="{y}" stroke="{LAVENDER}" stroke-width="4"/>',
                 f'<circle cx="{px(v["semloc"]):.1f}" cy="{y}" r="7" fill="{NAVY}"/>',
                 f'<circle cx="{px(v["semloc_no_prior"]):.1f}" cy="{y}" r="7" fill="#FFFFFF" stroke="{NAVY}" stroke-width="2"/>',
                 _t(px(v["semloc"]) + 12, y + 5, _p(v["semloc"]), size=12)]
    bd.A("ho_mo_hinh.svg", viz._g("ho", 40, 104, 560, 270, body))
    bd.A("ho_mo_hinh.svg", P("ho-giai-thich", 620, 104, 310, [
        ("Đọc thế nào", f"Acc@1 trên {r3['n_families']} chương trình (nhãn đã chuẩn hóa). Chấm đặc: SemLoc; chấm rỗng: SemLoc bỏ "
                        "điểm thưởng."),
        ("Ý chính", "Ở hầu hết các họ, bỏ điểm thưởng làm Acc@1 giảm: điểm thưởng (tức dòng LLM đoán) là phần lớn hạng 1 "
                    "của SemLoc. Riêng Gemini 3.8 Flash trên tập con này thì gần như không đổi."),
        ("Chi phí", "FailLoc+Cov rẻ hơn SemLoc ở mọi họ mô hình (báo cáo, hình chi phí)."),
    ], size=14))

    # 17. ablation results
    ab = mf.ablation_data()
    rows = []
    for contrast, lab in (("tests_effect", "Thêm test fail"), ("coverage_effect", "Thêm độ phủ")):
        for g in ("original", "repaired", "reviewed"):
            r = next(x for x in ab if x["gt"] == g and x["contrast"] == contrast)
            rows.append((f"{lab}, {dict(original='nhãn gốc', repaired='chuẩn hóa', reviewed='rà soát')[g]}", r["d_acc3"], r["lo3"],
                         r["hi3"], GT_COL[g]))
    _title(bd, "ablation_kq.svg", "Vì sao phương pháp FailLoc thắng: nhờ test fail, không nhờ độ phủ")
    band(bd, "ablation_kq.svg", 5)
    bd.A("ablation_kq.svg", _forest("rung-ablation", 30, 110, 590, rows, vmin=-10, vmax=40, row_h=42, label_w=250))
    bd.A("ablation_kq.svg", P("ablation-kq-giai-thich", 640, 104, 290, [
        ("Đọc thế nào", "Chênh lệch Acc@3 (điểm phần trăm) khi thêm một thành phần, chấm là trung bình, vạch là khoảng tin cậy "
                        "95%. Bên phải vạch 0 là giúp."),
        ("Ý chính", "Thêm test fail vào prompt tăng Acc@3 trên cả ba bộ nhãn. Thêm độ phủ từng dòng không tăng, Acc@1 còn "
                    "giảm: LLM không cần thông tin phương pháp SBFL dùng."),
    ], size=14))

    # 18. additions do not help
    rows = [(r["name"].split(" (")[0] + (" (dev)" if "dev" in r["name"] else ""), r["d1"], r.get("lo1"), r.get("hi1"),
             NAVY if "CovGate" in r["name"] else ORANGE) for r in mf.addons_data() if "Verify" not in r["name"]]
    _title(bd, "bo_sung_kq.svg", "Thêm phức tạp không thu hẹp được khoảng cách")
    band(bd, "bo_sung_kq.svg", 5)
    bd.A("bo_sung_kq.svg", _forest("rung-bo-sung", 30, 110, 590, rows, vmin=-15, vmax=15, row_h=46, label_w=250))
    st = {r["tool"]: r for r in _csv(ROOT / "data" / "static_tools.csv") if r["gt"] == "repaired"}
    bd.A("bo_sung_kq.svg", P("bo-sung-kq-giai-thich", 640, 104, 290, [
        ("Đọc thế nào", "Chênh lệch Acc@1 so với phương pháp được bổ sung, nhãn đã chuẩn hóa. Chấm rỗng: tập dev, một cấu hình."),
        ("Ý chính", "CovGate giữ nguyên Acc@1 của SemLoc; FailLoc+Cov giảm; FailLoc+Vote không cải thiện."),
        ("Phân tích tĩnh", f"ruff với mọi luật cảnh báo {st['ruff_all']['diagnostics']} lần nhưng chỉ {st['ruff_all']['on_fault_line']} lần "
                           "trúng dòng lỗi; pyrefly không trúng lần nào."),
    ], size=13))

    # 19. decomposition
    dec = [r for r in mf.decomposition_data() if r["gt"] == "repaired"]
    _title(bd, "phan_ra.svg", "Bao nhiêu phần là phỏng đoán: ở hạng 1, dòng đoán chiếm phần lớn")
    band(bd, "phan_ra.svg", 5)
    body = []
    for i, r in enumerate(sorted(dec, key=lambda r: r["metric"])):
        y = 130 + i * 90
        wg, ws = 6.0 * r["guess"], 6.0 * r["spectrum"]
        body += [_t(40, y + 32, r["metric"].replace("acc", "Acc@"), size=18, weight="bold", fill=NAVY),
                 _r(130, y, wg, 50, ORANGE), _r(130 + wg, y, ws, 50, NAVY),
                 _t(130 + wg / 2, y + 32, _p(r["guess"]), size=15, weight="bold", fill="#FFFFFF", anchor="middle"),
                 _t(130 + wg + ws / 2, y + 32, _p(r["spectrum"]), size=15, weight="bold", fill="#FFFFFF", anchor="middle")]
    body += [_r(130, 330, 14, 14, ORANGE), _t(152, 342, "phần do dòng LLM đoán", size=13),
             _r(340, 330, 14, 14, NAVY), _t(362, 342, "phần do phổ vi phạm", size=13)]
    bd.A("phan_ra.svg", viz._g("phan-ra-thanh", 40, 130, 560, 220, body))
    bd.A("phan_ra.svg", P("phan-ra-giai-thich", 620, 104, 310, [
        ("Đọc thế nào", "Độ chính xác của SemLoc (điểm phần trăm, nhãn đã chuẩn hóa, ba lần chạy) chia cho hai nguồn bằng "
                        "giá trị Shapley."),
        ("Ý chính", "Ở Acc@1 phần lớn là dòng đoán; bằng chứng thực thi chỉ chiếm phần lớn ở Acc@3. Đúng như giả thuyết H1 của "
                    "nhóm."),
    ], size=14))

    # 20. improvement over SemLoc on every setting
    imp = mf.improvement_data()
    rows = [(r["setting"] + ", Acc@1", f"{_p(r['semloc1'])}%", f"{_p(r['failloc1'])}%",
             f"{'+' if r['failloc1'] >= r['semloc1'] else ''}{_p(r['failloc1'] - r['semloc1'])} điểm") for r in imp]
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    rows.append(("Token mỗi chương trình", f"{m('CostSemlocTokensK')} nghìn", f"{m('CostLlmTestsTokensK')} nghìn", f"ít hơn {_p(ratio, 0)} lần"))
    _title(bd, "cai_tien_2.svg", "Cải tiến giữ được trên ba bộ nhãn và trên lỗi thật")
    band(bd, "cai_tien_2.svg", 5)
    bd.A("cai_tien_2.svg", viz.before_after("truoc-sau-2", 30, 98, 900, rows, row_h=56))
    bd.A("cai_tien_2.svg", _note(30, 420, ["Cùng chương trình, cùng Gemini 3.8 Flash, trung bình 3 lần chạy; BugsInPy là lỗi thật."],
                                 size=13, gid="dieu-kien-2", w=900))

    # 21. contributions + philosophy (content 3)
    _title(bd, "dong_gop_2.svg", "Đóng góp và triết lý khoa học  [nội dung 3]")
    band(bd, "dong_gop_2.svg", 5)
    contrib = [("C1", "Hạng 1 của SemLoc là dòng LLM đoán, nhờ điểm thưởng bài báo không mô tả (overclaim)."),
               ("C2", f"Gần một nửa nhãn của SemFault-250 không trỏ đúng dòng lỗi; nhóm công bố hai bộ nhãn mới."),
               ("C3", "Một prompt có test fail (FailLoc) thắng quy trình nhiều bước, rẻ hơn khoảng bảy lần."),
               ("C4", "Thêm phức tạp không giúp: test đủ để gợi ý lỗi nhưng quá yếu để làm trọng tài."),
               ("C5", "Bảng kiểm tra bảy mục cho đánh giá định vị lỗi bằng LLM và gói tái hiện đầy đủ.")]
    body = []
    for i, (k, t) in enumerate(contrib):
        y = 104 + i * 54
        body += [_r(30, y, 500, 46, viz.CREAM if k == "C3" else "#FFFFFF", stroke=ORANGE if k == "C3" else LAVENDER, rx=8),
                 _t(48, y + 29, k, size=16, weight="bold", fill=NAVY)]
        words, line, lines_ = t.split(), "", []
        for w_ in words:
            if len(line) + len(w_) > 54:
                lines_.append(line)
                line = w_
            else:
                line = (line + " " + w_).strip()
        lines_.append(line)
        body += [_t(90, y + 20 + 17 * j, l, size=13) for j, l in enumerate(lines_[:2])]
    bd.A("dong_gop_2.svg", viz._g("dong-gop", 30, 104, 500, 270, body))
    bd.A("dong_gop_2.svg", P("triet-ly", 550, 104, 380, [
        ("Triết lý khoa học", "Bằng chứng thực thi là trọng tài, nhưng phải đo xem nó thật sự đóng góp bao nhiêu."),
        ("Cách làm theo triết lý", "Luôn so với một cách làm đơn giản (FailLoc); đo đóng góp của từng thành phần (ablation, "
                                   "Shapley); đặt giả thuyết kèm điều kiện bác bỏ trước khi chạy; kiểm tra lại chính dữ liệu "
                                   "dùng để chấm."),
        ("Áp dụng cho chính nhóm", "Mỗi đóng góp có bằng chứng (tệp dữ liệu) và giới hạn ghi rõ trong báo cáo."),
    ], size=14))

    # 22. progress
    _title(bd, "tien_do_2.svg", "Tiến độ: việc đã xong và việc đến buổi bảo vệ")
    bd.A("tien_do_2.svg", viz.progress_table("bang-tien-do-2", 40, 104, 880, PROGRESS, row_h=48))
    bd.A("tien_do_2.svg", _note(40, 450, ["Đang hoàn thiện: dữ liệu và kết quả đã có, nhóm đang viết và kiểm tra lại."],
                                size=13, gid="chu-thich-tien-do-2", w=880))


def notes(bd) -> dict:
    m = bd._m
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    r3 = mf.rq3_data()
    return {
        "slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 2 của đề tài bằng chứng hay phỏng đoán.",
        "muc_luc_2": "Lần này nhóm trả lời ba câu hỏi còn mở từ lần 1, theo đúng năm phần thầy yêu cầu, rồi trình bày đóng góp, "
                     "triết lý khoa học và tiến độ. Mỗi trang vẫn có khung giải thích để thầy và các bạn đọc lại được.",
        "nhac_lai": f"Nhắc lại lần 1: phương pháp FailLoc, một lượt gọi LLM kèm test fail, hơn SemLoc "
                    f"{m('RqTwoRepairedAllLlmTestsDAccOne')} điểm Acc@1 trên nhãn đã chuẩn hóa. Còn ba câu hỏi: nhãn còn sai "
                    "không, kết quả có bền không, và vì sao FailLoc thắng.",
        "nhan_lech": "Trước hết là lý thuyết về nhãn. Ở chương trình blend_orders, nhãn gốc là dòng điều kiện 72, nhưng câu lệnh "
                     "được bảo vệ ở dòng 73 cũng hợp lý. Phép chấm chặt chỉ công nhận một dòng, nên nhãn lệch một dòng là đủ "
                     "làm sai kết quả. Vì vậy nhóm rà soát lại cả 250 nhãn.",
        "ablation_la_gi": "Ablation là giữ mọi thứ cố định và chỉ thêm một thành phần. Từ LLM-Direct chỉ có mã, thêm test fail "
                          "thành FailLoc, rồi thêm độ phủ từng dòng thành FailLoc+Cov. Chênh lệch giữa hai bước là tác dụng "
                          "của thành phần vừa thêm.",
        "shapley": "Để biết độ chính xác của SemLoc đến từ đâu, nhóm dùng giá trị Shapley. Đo độ chính xác ở cả bốn tổ hợp: "
                   "không nguồn nào, chỉ dòng đoán, chỉ phổ vi phạm, và cả hai. Phần của mỗi nguồn là mức tăng trung bình "
                   "khi thêm nó vào.",
        "ra_soat": f"Rà soát nhãn có hai bước. LLM đọc mã, test và nhãn của cả {m('LabaudAllN')} chương trình và cho nhận định; "
                   f"sau đó {m('ReviewReviewersN')} thành viên duyệt lại {m('ReviewHumanN')} nhãn nghi vấn. Người duyệt có xem "
                   "gợi ý của LLM, nên nhóm làm thêm vòng duyệt mù.",
        "duyet_mu": f"Trong duyệt mù, {m('BlindBlindAllPrograms')} chương trình được chọn ngẫu nhiên, mỗi chương trình do hai "
                    "thành viên chưa từng xem duyệt độc lập. Các dòng ứng viên được đánh chữ A đến D theo thứ tự ngẫu nhiên, "
                    "không ghi nguồn và không có gợi ý của LLM.",
        "rq3_thiet_ke": f"RQ3 thử độ bền theo ba cách: {m('BipAllSemlocPriorN')} lỗi thật của BugsInPy, mã đã đổi tên mọi định "
                        "danh để kiểm tra LLM có nhớ bộ dữ liệu không, và năm họ mô hình khác nhau. Bên trái là hàm ví dụ trước và sau khi đổi "
                        "tên: các tên gợi ý như weights hay shares biến mất.",
        "ba_prompt": "Đây là ba mức prompt trên ví dụ. LLM-Direct chỉ có mã; FailLoc thêm tên và lỗi của test fail; FailLoc+Cov "
                     "thêm chú thích độ phủ như f=1/p=4 cho mỗi dòng. Ở ví dụ này mọi dòng đều có cùng chú thích, nên chỉ "
                     "thông báo lỗi của test fail mới gợi ý dòng 29.",
        "bo_sung": "Nhóm thử thêm ba hướng: CovGate xếp lại dòng của SemLoc bằng độ phủ; FailLoc+Vote hỏi ba lần rồi gộp; và "
                   "hai công cụ phân tích tĩnh là ruff và pyrefly. Câu hỏi là thêm phức tạp có giúp được không.",
        "nhan_di_dau": f"Kết quả rà soát: {m('LabaudAllMoved')} trên {m('LabaudAllN')} nhãn gốc bị dời, nhiều nhất là nhãn nằm trên "
                       f"dòng trống. Trong duyệt mù, {m('BlindBlindAllMatchReviewed')} trên {m('BlindBlindAllNReviewed')} câu trả "
                       f"lời trùng nhãn đã rà soát, chỉ {m('BlindBlindAllMatchOriginal')} trùng nhãn gốc.",
        "ba_bo_nhan": f"Trên cả ba bộ nhãn, FailLoc đều hơn SemLoc ở Acc@1: {m('RqTwoOriginalAllLlmTestsDAccOne')} điểm trên nhãn "
                      f"gốc, {m('RqTwoRepairedAllLlmTestsDAccOne')} trên nhãn đã chuẩn hóa và {m('RqTwoReviewedAllLlmTestsDAccOne')} "
                      "trên nhãn đã rà soát. Số tuyệt đối thay đổi theo bộ nhãn, nhưng chiều của kết luận thì không.",
        "bugsinpy": f"Trên {m('BipAllSemlocPriorN')} lỗi thật, FailLoc cao nhất ở Acc@3. Mọi lần SemLoc đúng ở hạng 1 đều là dòng LLM "
                    "đoán, còn riêng phổ vi phạm thì gần bằng phương pháp SBFL.",
        "doi_ten": "Khi đổi tên mọi định danh, dòng LLM đoán gần như giữ nguyên, nhưng SemLoc bỏ điểm thưởng giảm mạnh: ràng buộc "
                   "LLM viết dựa vào tên gợi ý. FailLoc+Cov gần như không đổi.",
        "ho_mo_hinh": f"Với {r3['n_families']} chương trình và năm họ mô hình, bỏ điểm thưởng làm Acc@1 của SemLoc giảm ở hầu hết "
                      "các họ. Riêng Gemini 3.8 Flash trên tập con này thì gần như không đổi.",
        "ablation_kq": "Ablation trả lời vì sao FailLoc thắng. Thêm test fail vào prompt tăng Acc@3 trên cả ba bộ nhãn; thêm độ "
                       "phủ từng dòng thì không tăng. LLM không cần thông tin mà phương pháp SBFL dùng.",
        "bo_sung_kq": "Các cách bổ sung đều không giúp: CovGate giữ nguyên Acc@1 của SemLoc, FailLoc+Cov giảm, FailLoc+Vote "
                      "không cải thiện. Công cụ phân tích tĩnh gần như không trúng dòng lỗi.",
        "phan_ra": "Phân rã Shapley cho thấy ở Acc@1, phần lớn độ chính xác của SemLoc đến từ dòng LLM đoán; bằng chứng thực thi "
                   "chỉ chiếm phần lớn ở Acc@3. Điều này khớp với giả thuyết H1 nhóm đặt ra từ đầu.",
        "cai_tien_2": "Gói lại, mức hơn của FailLoc so với SemLoc giữ được trên cả ba bộ nhãn và trên lỗi thật, với chi phí thấp "
                      "hơn nhiều. Đây là cải tiến chính của nhóm so với bài gốc.",
        "dong_gop_2": "Đây là nội dung 3. Nhóm có năm đóng góp, từ việc chỉ ra hạng 1 của SemLoc là dòng đoán đến bảng kiểm tra "
                    "và gói tái hiện. Triết lý khoa học của nhóm: bằng chứng thực thi là trọng tài, nhưng phải đo nó đóng góp "
                    "bao nhiêu, luôn so với cách làm đơn giản và đặt điều kiện bác bỏ trước.",
        "tien_do_2": "Về tiến độ, ba nội dung đầu đã xong, bài báo arXiv đã có bản nháp và hoàn thiện từ 26/11 đến 10/12. Phân "
                     "tích thất bại và kiểm chứng bằng bản sửa để dành cho buổi bảo vệ.",
        "slide_30": "Nhóm xin cảm ơn thầy và các bạn, rất mong nhận được câu hỏi và góp ý.",
    }

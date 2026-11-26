"""Báo cáo lần 2 (≤ 18 trang): the second week, fixing the labels and proposing FailLoc. A recap of lần 1, label
normalization, FailLoc (idea, flow on example 1), SemLoc−Bonus, the compared methods and the design, the main comparison,
the two-step label review, then the progress table. Pages for lần 3 (ablation, additions, RQ4, contributions) and the
defence are built here too; the LAN*/BAOVE lists decide which deck shows them.
Numbers come from the same data functions as the report figures (scripts/make_figures.py) or from the macros."""
import viz
from story_common import (MAIN, ROOT, _csv, _note, _title, _unbold, band, cite, examples, name, progress_rows)  # noqa: F401
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

import make_figures as mf  # noqa: E402  (scripts/ is on sys.path via story_common)

LAN2 = [("slide_01.svg", 1), ("muc_luc_2.svg", 22), ("nhac_lai.svg", 22),
        ("chuan_hoa.svg", 22), ("luong_chuan_hoa.svg", 22), ("nhan_lech.svg", 22), ("ra_soat.svg", 22),
        ("failloc_y_tuong.svg", 22), ("luong_failloc.svg", 22), ("failloc_vd.svg", 22), ("luong_semloc_bonus.svg", 22),
        ("phuong_phap.svg", 22), ("thiet_ke_tn.svg", 22), ("ket_qua.svg", 22), ("cai_tien.svg", 22),
        ("nhan_di_dau.svg", 22), ("ba_bo_nhan.svg", 22),
        ("tien_do_2.svg", 22), ("slide_30.svg", 30)]
GT_VI = {"original": "Nhãn gốc", "repaired": "Nhãn đã chuẩn hóa", "reviewed": "Nhãn đã rà soát"}
GT_COL = {"original": GREY, "repaired": ORANGE, "reviewed": NAVY}


def contributions(items: list[tuple], top: float = 100, bottom: float = 470) -> str:
    """The closing page: one card per contribution (C1–C4, one per research question, in order), full width; cards are
    stretched so the last one ends at `bottom`."""
    FS, LH, TAG, gap = 15, 21, 78, 10
    texts = [viz.wrap(t, 900 - TAG - 30, FS) for _, _, t in items]
    need = [18 + LH * len(t) for t in texts]
    free = (bottom - top - gap * (len(items) - 1) - sum(need)) / len(items)
    body, y = [], top
    for (k, rq, _), lines_, n in zip(items, texts, need):
        h = n + max(0, free)
        body += [_r(30, y, 900, h, "#FFFFFF", stroke=LAVENDER, rx=8), _r(30, y, TAG, h, viz.CREAM, stroke=ORANGE, rx=8),
                 _t(30 + TAG / 2, y + h / 2 + 7, k, size=20, weight="bold", fill=NAVY, anchor="middle")]
        y0 = y + h / 2 - LH * (len(lines_) - 1) / 2 + FS * 0.36
        body += [_t(30 + TAG + 16, y0 + LH * j, l, size=FS) for j, l in enumerate(lines_)]
        y += h + gap
    return viz._g("dong-gop", 30, top, 900, y - gap - top, body)


def pages(bd) -> None:
    m = bd._m
    P = viz.panel
    ex = examples()
    va, bo = ex["votes_apportion"], ex["blend_orders"]
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    acc = lambda g, mm, k=1: 100 * float(rq2[(g, mm)][f"acc{k}_mean"])

    # 2. agenda
    _title(bd, "muc_luc_2.svg", "Nội dung trình bày lần 2")
    items = [("", "Nhắc lại lần 1", "SemLoc tái hiện được; điểm thưởng và nhãn có vấn đề"),
             ("2", "Phương pháp giải quyết", "Chuẩn hóa nhãn bằng thực thi; rà soát nhãn hai bước"),
             ("3", "Cải tiến", "Phương pháp FailLoc; luồng chạy trên ví dụ"),
             ("4", "Thực nghiệm", "Năm phương pháp, ba bộ nhãn"),
             ("5", "Kết quả", "FailLoc so với SemLoc; nhãn sau rà soát, ba bộ nhãn"),
             ("", "Tiến độ", "Việc đã xong và việc của lần 3")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 106 + i * 54
        body.append(_r(60, y, 840, 46, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else LAVENDER, rx=10, sw=1.2))
        body.append(_t(92, y + 31, k or "•", size=24, fill=NAVY, weight="bold", anchor="middle"))
        body.append(_t(130, y + 30, head, size=18, fill=NAVY, weight="bold"))
        body.append(_t(470, y + 30, desc, size=14))
    bd.A("muc_luc_2.svg", viz._g("muc-luc", 60, 106, 840, 54 * (len(items) - 1) + 46, body))

    # 3. recap of report 1: SemLoc reproduced, the bonus decides rank 1, the labels have problems
    _title(bd, "nhac_lai.svg", "Nhắc lại lần 1: điểm thưởng quyết định hạng 1, nhãn có vấn đề")
    for k, (gid, val, cap, c) in enumerate((
            ("semloc-goc", f"{_p(acc('original', 'semloc'))}%", "Acc@1 của SemLoc tái hiện\n(nhãn gốc, tập test)", NAVY),
            ("bo-thuong", f"{_p(acc('original', 'semloc_no_prior'))}%", "Acc@1 khi bỏ điểm thưởng\ncho dòng LLM đoán", ORANGE),
            ("nhan-trong", m("GtBlankN"), "nhãn gốc nằm trên\ndòng trống", RED))):
        bd.A("nhac_lai.svg", viz.big_number(gid, 40 + k * 300, 110, val, cap, color=c, size=48, w=280))
    bd.A("nhac_lai.svg", P("lan2-lam-gi", 40, 300, 890, [
        ("Tuần này nhóm làm", "1. Chuẩn hóa nhãn bằng cách chạy test, để phép chấm công bằng."),
        ("", "2. Đề xuất phương pháp FailLoc và so sánh với SemLoc trên cùng điều kiện."),
        ("", "3. Rà soát lại cả 250 nhãn theo hai bước."),
    ], size=15, h=170))

    # 4. a label one line off changes the score
    code = {c["no"]: c["text"] for c in bo["code_lines"]}
    _title(bd, "nhan_lech.svg", "Nhãn lệch một dòng cũng làm sai phép chấm")
    band(bd, "nhan_lech.svg", 2)  # the problem the two-step review (ra_soat) answers
    bd.A("nhan_lech.svg", viz.code_block("ma-nhan", 30, 104, [code[n] if len(code[n]) <= 42 else code[n][:40].rstrip() + " …" for n in range(70, 75)], first_no=70, fs=15, width=560,
                                         highlight={72, 73}, mark={72: "nhãn gốc", 73: "dòng thân của if"}))
    bd.A("nhan_lech.svg", P("vi-sao-lech", 610, 104, 320, [
        ("Đầu khối hay thân khối", "Lỗi nằm ở điều kiện dòng 72 hay câu lệnh dòng 73? Cả hai đều hợp lý, nhưng phép chấm "
                                   "chặt chỉ công nhận một dòng."),
        ("", "Vì vậy nhóm rà soát lại cả 250 nhãn."),
    ], size=15, h=150))

    # 5. ablation: what it is
    _title(bd, "ablation_la_gi.svg", "Ablation: thêm từng thành phần một để đo tác dụng")
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
        ("Ablation", "Giữ nguyên mọi thứ khác, chỉ thêm một thành phần. Chênh lệch giữa hai bước liền nhau là tác dụng "
                     "của thành phần đó."),
    ], size=15))

    # 6. Shapley decomposition: what it is
    _title(bd, "shapley.svg", "Phân rã Shapley: độ chính xác của SemLoc đến từ nguồn nào")
    band(bd, "shapley.svg", 1)
    # worked example on the measured Acc@1 (normalized labels): v(spectrum) = SemLoc−Bonus, v(both) = SemLoc, and
    # v(guess) follows from the decomposition file (phi_guess + phi_spectrum = v(both), phi_guess − phi_spectrum = v(g) − v(s))
    dc = next(r for r in _csv(ROOT / "data" / "rq_decomposition.csv")
              if r["game"] == "semloc" and r["subset"] == "all" and r["gt"] == "repaired" and r["metric"] == "acc1")
    v_all, ph_g, ph_s = (100 * float(dc[k]) for k in ("full", "phi_guess", "phi_spectrum"))
    v_s = acc("repaired", "semloc_no_prior")
    v_g = ph_g - ph_s + v_s
    combos = [("Không nguồn nào", "Acc@1 = 0"), ("Chỉ dòng LLM đoán", f"Acc@1 = {_p(v_g)}%"),
              ("Chỉ phổ vi phạm (SemLoc−Bonus)", f"Acc@1 = {_p(v_s)}%"), ("Cả hai (SemLoc)", f"Acc@1 = {_p(v_all)}%")]
    body = []
    for i, (h, d) in enumerate(combos):
        x, y = 40 + (i % 2) * 290, 110 + (i // 2) * 96
        body.append(_r(x, y, 270, 80, "#FFFFFF", stroke=NAVY if i == 3 else LAVENDER, rx=10, sw=1.8))
        body.append(_t(x + 135, y + 34, h, size=16, weight="bold", anchor="middle", fill=NAVY))
        body.append(_t(x + 135, y + 58, d, size=13, anchor="middle"))
    bd.A("shapley.svg", viz._g("bon-to-hop", 40, 110, 560, 176, body))
    bd.A("shapley.svg", P("shapley-giai-thich", 620, 104, 310, [
        ("Giá trị Shapley", "Đo độ chính xác ở cả bốn tổ hợp. Phần của một nguồn là mức tăng trung bình khi thêm nguồn đó "
                            "vào, tính trên mọi thứ tự thêm."),
        ("", "Nhờ vậy tách được bao nhiêu phần độ chính xác của SemLoc đến từ bằng chứng thực thi (phổ vi phạm) và bao nhiêu "
             "từ việc LLM tự đoán."),
    ], size=14, h=290))
    bd.A("shapley.svg", viz.formula("shapley-ct", 40, 300, 560, [
        "phần(đoán) = ½·[v(đoán) − v(∅)] + ½·[v(cả hai) − v(phổ)]",
        "v(·): Acc@1 khi chỉ dùng các nguồn trong ngoặc. Ví dụ (nhãn đã chuẩn hóa):",
        f"phần(đoán) = ½·{_p(v_g)} + ½·({_p(v_all)} − {_p(v_s)}) = {_p(ph_g)}",
        f"phần(phổ) = ½·{_p(v_s)} + ½·({_p(v_all)} − {_p(v_g)}) = {_p(ph_s)}",
        f"cộng lại: {_p(ph_g)} + {_p(ph_s)} = {_p(v_all)} = v(cả hai)"], size=15))

    # 7. two-step label review
    _title(bd, "ra_soat.svg", "Rà soát nhãn hai bước: LLM rà trước, thành viên nhóm duyệt sau")
    band(bd, "ra_soat.svg", 2)
    bd.A("ra_soat.svg", viz.pipeline("ra-soat", 40, 112, [f"Nhãn gốc\n{m('LabaudAllN')} chương trình", "LLM rà trước\nnhận định từng nhãn",
                                                          f"Người duyệt\n{m('ReviewReviewersN')} thành viên,\n{m('ReviewHumanN')} nhãn nghi vấn",
                                                          f"Nhãn đã rà soát\n{m('LabaudAllMoved')} nhãn dời"],
                                     accent=3, box_w=196, gap=32, box_h=90))
    bd.A("ra_soat.svg", P("ra-soat-giai-thich", 40, 236, 880, [
        ("", "LLM nhận định từng nhãn đúng, sai hay lỗi hai dòng; thành viên nhóm duyệt lại mọi nhãn nghi vấn."),
        ("Duyệt mù", f"{m('BlindBlindAllPrograms')} chương trình, phiếu không kèm nhãn hay gợi ý của LLM: kết quả ủng hộ bộ "
                     "nhãn đã rà soát."),
    ], size=15))

    # 9. RQ3 design
    _title(bd, "rq3_thiet_ke.svg", "RQ4 thử độ bền theo ba cách")
    band(bd, "rq3_thiet_ke.svg", 4, rq="RQ4")
    vcode = {c["no"]: c["text"] for c in va["code_lines"]}
    src = (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / "votes_apportion.py").read_text().splitlines()
    renamed = (ROOT / "data" / "semfault_renamed" / "programs" / "votes_apportion.py").read_text().splitlines()
    show = [7, 10, 11, 12, None, 24, 25, 26]  # the inline comment and the docstring, then the loop with the telling names
    comments = {7, 11}

    def cut(line: str) -> str:
        line = line[4:] if line.startswith("    ") else line
        return line if len(line) <= 38 else line[:37] + "…"
    for gid, y, text in (("truoc", 104, src), ("sau", 264, renamed)):
        bd.A("rq3_thiet_ke.svg", viz.code_block(gid, 30, y, [cut(text[n - 1]) if n else "" for n in show], numbers=show,
                                                highlight=comments, fs=12, width=330))
    bd.A("rq3_thiet_ke.svg", _note(30, 432, ["Trên: mã gốc. Dưới: mã đổi tên.",
                                             "weights, shares thành v4, v8; dòng tô màu:",
                                             "chú thích và docstring bị xóa."],
                                   size=12, gid="ghi-chu-doi-ten", w=330))
    bd.A("rq3_thiet_ke.svg", P("rq3-ba-cach", 380, 104, 550, [
        ("Lỗi thật BugsInPy (Widyasari 2020)", f"{m('BipAllSemlocPriorN')} lỗi thật của dự án youtube-dl, mỗi lỗi kèm test fail."),
        ("Mã đổi tên định danh", "Tên thành v1, v2, xóa chú thích. Nếu LLM nhớ bộ dữ liệu thì độ chính xác sẽ giảm."),
        ("Năm họ mô hình", "Gemini 3.8 Flash, GPT-6 luna, Claude Sonnet 5.5, gpt-oss-120b, Gemini 3.5 Flash-Lite."),
    ], size=15, h=290))

    # 10. three prompt levels on the running example
    _title(bd, "ba_prompt.svg", "Ba mức prompt trên ví dụ 1, mỗi mức thêm một loại thông tin")
    band(bd, "ba_prompt.svg", 3)
    win = [25, 26, 28, 29]
    def cutw(t: str, n: int) -> str:  # cut code at a word boundary, marked with an ellipsis
        return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip() + " …"
    rows = [("LLM-Direct", [f"{n}: {cutw(vcode[n].strip(), 31)}" for n in win], NAVY),
            ("FailLoc", [f"{n}: {cutw(vcode[n].strip(), 31)}" for n in win] + ["Test fail: test_truncation_sum_…"], ORANGE),
            ("FailLoc+Cov", [f"{n}: {cutw(vcode[n].strip(), 19)} [f=1/p=4]" for n in win] + ["Test fail: test_truncation_sum_…"], NAVY)]
    for i, (h, lines, c) in enumerate(rows):
        x = 30 + i * 305
        g = [_r(x, 104, 290, 196, viz.LIGHT, stroke=c, rx=10, sw=1.6), _t(x + 14, 130, h, size=16, weight="bold", fill=c)]
        g += [_t(x + 14, 164 + 25 * k, l, size=11, family=viz.MONO) for k, l in enumerate(lines)]
        bd.A("ba_prompt.svg", viz._g(f"prompt-{i}", x, 104, 290, 196, g))
    bd.A("ba_prompt.svg", P("ba-prompt-giai-thich", 30, 320, 900, [
        ("", "[f=1/p=4] nghĩa là 1 test fail và 4 test pass chạy qua dòng đó, đúng thông tin mà phương pháp SBFL dùng. Ở ví dụ "
             "này dòng nào cũng [f=1/p=4], nên độ phủ không thêm được gì; chính thông báo lỗi của test fail mới chỉ về dòng 29."),
    ], size=15))

    # 11. additions and static tools
    _title(bd, "bo_sung.svg", "Nhóm thử thêm ba hướng bổ sung")
    band(bd, "bo_sung.svg", 3)
    for k, (h, lines, c) in enumerate((
            ("CovGate (cho SemLoc)", ["Xếp lại các dòng của SemLoc:", "dòng không test fail nào chạy", "qua bị đẩy xuống; cộng thêm", "điểm Ochiai có trọng số."], NAVY),
            ("FailLoc+Vote", ["Hỏi FailLoc ba lần rồi gộp ba", "danh sách: dòng hay đứng đầu", "được ưu tiên."], ORANGE),
            ("Phân tích tĩnh", ["ruff (Astral, kiểm tra phong cách", "mã) và pyrefly (Meta, kiểm tra kiểu)", "trên 250 chương trình: cảnh báo", "có trúng dòng lỗi không?"], GREY))):
        bd.A("bo_sung.svg", P(f"bo-sung-{k}", 30 + k * 305, 96, 290, [(h, " ".join(lines))], size=14,
                              head_color=c if c != GREY else INK, h=130))
    bd.A("bo_sung.svg", viz._g("vote-nhan", 30, 238, 400, 24, [_t(30, 254, "Luồng FailLoc+Vote", size=15, weight="bold", fill=ORANGE)]))
    bd.A("bo_sung.svg", viz.pipeline("vote-luong", 30, 266, ["Chạy FailLoc 3 lần\nmỗi lần 5 dòng",
                                                             "Cho điểm theo hạng\nhạng k được 1/k điểm",
                                                             "Cộng điểm\nqua 3 danh sách", "Xếp lại\ntheo tổng điểm"],
                                     accent=3, box_w=204, gap=28, box_h=64, color=ORANGE))
    bd.A("bo_sung.svg", _note(30, 356, ["Ví dụ: [29, 25, 26], [29, 26, 25], [25, 29, 26] → dòng 29 được 1 + 1 + 1/2 = 2,5 điểm, "
                                        "đứng hạng 1.", "Không gọi LLM thêm: dùng lại ba lần chạy FailLoc đã có."],
                               size=13, gid="vote-vi-du", w=900))

    # 12. where the original labels went + blind review result
    lf = mf.label_flow_data()
    _title(bd, "nhan_di_dau.svg", f"Sau rà soát, {m('LabaudAllMoved')} trên {m('LabaudAllN')} nhãn gốc bị dời")
    band(bd, "nhan_di_dau.svg", 5, rq="RQ1")
    cols = [GREY, "#C9C9C3", RED, "#E8956F", NAVY, "#8FB6EA"]
    x, body = 40.0, []
    for (lab, v), c in zip(lf["parts"], cols):
        w = 880 * v / lf["n"]
        body.append(_r(x, 110, w, 60, c))
        if v >= 15:
            body.append(_t(x + w / 2, 146, str(v), size=15, weight="bold", fill="#FFFFFF" if c in (GREY, RED, NAVY) else INK, anchor="middle"))
        x += w
    for i, ((lab, v), c) in enumerate(zip(lf["parts"], cols)):
        lx, ly = 40 + (i % 3) * 300, 198 + (i // 3) * 28
        body += [_r(lx, ly - 12, 14, 14, c), _t(lx + 22, ly, f"{lab} ({v})", size=13)]
    bd.A("nhan_di_dau.svg", viz._g("dong-nhan", 40, 110, 880, 116, body))
    for k, (h, txt, c) in enumerate((
            ("Dòng trống, không phải mã", "Dời về câu lệnh thật sự gây lỗi.", RED),
            ("Lệch một dòng trở lên", "Trỏ vào dòng bên cạnh dòng lỗi.", NAVY),
            ("Thêm dòng thứ hai", "Lỗi trải hai dòng: giữ nhãn gốc, thêm dòng kia.", INK))):
        bd.A("nhan_di_dau.svg", P(f"nhan-vd-{k}", 40 + k * 300, 270, 285, [(h, txt)], size=15, head_color=c, h=96))

    # 13. results on three label sets
    _title(bd, "ba_bo_nhan.svg", ("Năm" if bd.DECK == "lan2" else "Sáu") + " phương pháp trên ba bộ nhãn: FailLoc luôn cao nhất ở Acc@1")
    band(bd, "ba_bo_nhan.svg", 5, rq="RQ2")
    short = {"original": "Gốc", "repaired": "Chuẩn hóa", "reviewed": "Rà soát"}
    sets = ("original", "repaired", "reviewed")
    # lần 2 has not shown the additions (CovGate, FailLoc+Cov) yet: its table holds the five methods of the main comparison
    meths = tuple(MAIN) if bd.DECK == "lan2" else ("sbfl_ochiai", "llm_direct", "semloc", "covgate", "llm_coverage", "llm_tests")
    col = lambda mm: ORANGE if mm == "llm_tests" else NAVY if mm == "semloc" else GREY
    bd.A("ba_bo_nhan.svg", viz.small_multiples("ba-bo", 30, 92, [(cite(mm), mm in ("semloc", "llm_tests")) for mm in meths],
                                               [(f"Nhãn {short[g].lower()}", [(acc(g, mm, 1), acc(g, mm, 3), col(mm)) for mm in meths])
                                                for g in sets], label_w=200, panel_w=233, row_h=31, bar_h=25))
    bd.A("ba_bo_nhan.svg", _note(30, 324, ["Tập test, Gemini 3.8 Flash, trung bình 3 lần chạy. Mỗi phương pháp hai thanh: trên là Acc@1, dưới (sáng hơn) là Acc@3 (%)."],
                               size=12, gid="chu-giai-ba-bo", w=900))
    bd.A("ba_bo_nhan.svg", P("ba-bo-giai-thich", 30, 342, 900, [
        ("", f"Trên cả ba bộ nhãn, FailLoc cao nhất ở Acc@1 và hơn SemLoc {m('RqTwoOriginalAllLlmTestsDAccOne')}, "
             f"{m('RqTwoRepairedAllLlmTestsDAccOne')} và {m('RqTwoReviewedAllLlmTestsDAccOne')} điểm."),
    ], size=15))

    # 14. BugsInPy
    r3 = mf.rq3_data()
    _title(bd, "bugsinpy.svg", "Trên lỗi thật BugsInPy, phương pháp FailLoc cao nhất ở Acc@3")
    band(bd, "bugsinpy.svg", 5, rq="RQ4")
    meths = [("sbfl_ochiai", cite("sbfl_ochiai"), GREY), ("semloc_spectrum", "SemLoc−Bonus", GREY), ("llm_guess", "Chỉ dòng LLM đoán", GREY),
             ("semloc_prior", cite("semloc"), NAVY), ("llm_coverage", "FailLoc+Cov", GREY), ("llm_tests", "FailLoc", ORANGE)]
    bd.A("bugsinpy.svg", viz.bars("bip", 30, 104, 560, 320, [(l, r3["bugsinpy3"][k], c) for k, l, c in meths], vmax=100, label_w=250))
    bd.A("bugsinpy.svg", P("bip-giai-thich", 610, 104, 320, [
        ("", f"Acc@3 trên {m('BipAllSemlocPriorN')} lỗi thật của youtube-dl, lấy từ BugsInPy (Widyasari 2020)."),
        ("SemLoc−Bonus", "SemLoc không cộng điểm thưởng cho dòng LLM đoán, chỉ xếp theo phổ vi phạm: bằng đúng phương pháp SBFL."),
        ("", "Mọi lần SemLoc đúng ở hạng 1 đều là dòng LLM đoán."),
    ], size=15, h=320))

    # 15. renaming
    ren = {r["method"]: r for r in _csv(ROOT / "data" / "rq3_renamed.csv") if r["gt"] == "repaired"}
    rp = lambda mm, c: f"{_p(100 * float(ren[mm][c]))}%"
    sg = lambda v: f"{'+' if v >= 0 else '−'}{_p(abs(v))}"
    _title(bd, "doi_ten.svg", "Đổi tên định danh: SemLoc giảm, FailLoc gần như không đổi")
    band(bd, "doi_ten.svg", 5, rq="RQ4")
    rv = lambda mm, c: 100 * float(ren[mm][c])
    groups = []
    for mm, lab in (("semloc", cite("semloc")), ("semloc_no_prior", "SemLoc−Bonus"), ("llm_guess", "Chỉ dòng LLM đoán"),
                    ("llm_coverage", "FailLoc+Cov"), ("llm_tests", "FailLoc")):
        c = ORANGE if mm == "llm_tests" else NAVY if mm == "semloc" else GREY
        groups.append((lab, [("mã gốc", rv(mm, "orig_acc1_mean"), rv(mm, "orig_acc3_mean"), GREY),
                             ("đổi tên", rv(mm, "renamed_acc1_mean"), rv(mm, "renamed_acc3_mean"), c)],
                       f"{sg(rv(mm, 'd_acc3'))} @3"))
    bd.A("doi_ten.svg", viz.grouped_bars("doi-ten", 30, 96, 900, groups, label_w=180, sub_w=70, bar_h=22, gap=3, group_gap=7))
    bd.A("doi_ten.svg", _note(30, 380, [f"{ren['semloc']['n']} chương trình của tập test, nhãn đã chuẩn hóa. Trên: Acc@1, dưới (sáng hơn): Acc@3 (%)."],
                               size=12, gid="chu-giai-doi-ten", w=900))
    bd.A("doi_ten.svg", P("doi-ten-giai-thich", 30, 400, 900, [
        ("", "SemLoc−Bonus giảm nhiều nhất vì ràng buộc LLM viết dựa vào tên gợi ý. FailLoc gần như không đổi: LLM không "
             "thắng nhờ nhớ bộ dữ liệu."),
    ], size=15))

    # 16. model families
    fams = r3["families"]
    n_drop = sum(v["semloc_no_prior"] < v["semloc"] for v in fams.values())
    drops = [v["semloc"] - v["semloc_no_prior"] for v in fams.values()]
    with_fl = {f: v for f, v in fams.items() if "llm_tests" in v}
    clear = {f: v for f, v in with_fl.items() if v["llm_tests"] - v["semloc"] >= 5}
    close = [f for f in with_fl if f not in clear]
    _title(bd, "ho_mo_hinh.svg", "Năm họ mô hình: SemLoc dựa vào dòng đoán, FailLoc không thua")
    band(bd, "ho_mo_hinh.svg", 5, rq="RQ4")
    groups = []
    for fam, v in fams.items():
        bars_ = [("SemLoc−Bonus", v["semloc_no_prior"], None, "#C9C8F4"), (cite("semloc"), v["semloc"], None, NAVY)]
        if "llm_tests" in v:
            bars_.append(("FailLoc", v["llm_tests"], None, ORANGE))
        groups.append((fam, bars_, f"{sg(v['llm_tests'] - v['semloc'])}" if "llm_tests" in v else None))
    bd.A("ho_mo_hinh.svg", viz.grouped_bars("ho", 30, 92, 900, groups, label_w=180, sub_w=130, bar_h=11, gap=1, group_gap=8))
    bd.A("ho_mo_hinh.svg", P("ho-giai-thich", 30, 308, 900, [
        ("", f"Acc@1 trên {r3['n_families']} chương trình của tập test. Ô cam: FailLoc trừ SemLoc (điểm)."),
        ("", f"SemLoc−Bonus thấp hơn SemLoc ở {n_drop}/{len(fams)} họ: hạng 1 của SemLoc dựa vào dòng LLM đoán ở mọi mô hình. "
             f"FailLoc hơn SemLoc rõ ở {len(clear)} họ, ngang nhau ở " + ", ".join(close) + "."),
    ], size=15))

    # 17. ablation results
    ab = {(x["gt"], x["contrast"]): x for x in mf.ablation_data()}
    _title(bd, "ablation_kq.svg", "Phương pháp FailLoc thắng nhờ thông tin của test fail")
    band(bd, "ablation_kq.svg", 5, rq="RQ3")
    trio = (("llm_direct", cite("llm_direct"), GREY), ("llm_tests", "FailLoc (+ test fail)", ORANGE),
            ("llm_coverage", "FailLoc+Cov (+ độ phủ)", GREY))
    bd.A("ablation_kq.svg", viz.small_multiples("ablation", 30, 92, [(lab, mm == "llm_tests") for mm, lab, _ in trio],
                                                [(f"Nhãn {short[g].lower()}", [(acc(g, mm, 1), acc(g, mm, 3), c) for mm, _, c in trio])
                                                 for g in sets], label_w=190, panel_w=237, row_h=34, bar_h=27))
    bd.A("ablation_kq.svg", _note(30, 250, ["Mỗi hàng thêm một thành phần vào prompt. Trên: Acc@1, dưới (sáng hơn): Acc@3 (%)."],
                               size=12, gid="chu-giai-ablation", w=900))
    sg = lambda v: f"{'+' if v >= 0 else '−'}{_p(abs(v))}"
    d = lambda c, k: ", ".join(sg(ab[(g, c)][f"d_acc{k}"]) for g in sets)
    bd.A("ablation_kq.svg", P("ablation-kq-giai-thich", 30, 272, 900, [
        ("Thêm test fail", "Acc@1 và Acc@3 tăng trên cả ba bộ nhãn."),
        ("Thêm độ phủ", "Không tăng: LLM không cần thông tin mà phương pháp SBFL dùng."),
    ], size=15))

    # 18. additions do not help
    vote = next(r for r in _csv(ROOT / "data" / "vote_test.csv") if r["gt"] == "repaired")
    vp = lambda c: f"{_p(100 * float(vote[c]))}%"
    ap = lambda mm, k: f"{_p(acc('repaired', mm, k))}%"
    _title(bd, "bo_sung_kq.svg", "Thêm phức tạp không thu hẹp được khoảng cách")
    band(bd, "bo_sung_kq.svg", 5, rq="RQ3")
    vv = lambda c: 100 * float(vote[c])
    sgn = lambda v: f"{'+' if v >= 0 else '−'}{_p(abs(v))}"
    groups = [("CovGate", [(cite("semloc"), acc("repaired", "semloc", 1), acc("repaired", "semloc", 3), GREY),
                           ("CovGate", acc("repaired", "covgate", 1), acc("repaired", "covgate", 3), NAVY)],
               f"{sgn(acc('repaired', 'covgate', 1) - acc('repaired', 'semloc', 1))} @1"),
              ("FailLoc+Cov", [("FailLoc", acc("repaired", "llm_tests", 1), acc("repaired", "llm_tests", 3), GREY),
                               ("+ độ phủ", acc("repaired", "llm_coverage", 1), acc("repaired", "llm_coverage", 3), ORANGE)],
               f"{sgn(acc('repaired', 'llm_coverage', 1) - acc('repaired', 'llm_tests', 1))} @1"),
              ("FailLoc+Vote", [("FailLoc", vv("single_acc1"), vv("single_acc3"), GREY),
                                ("+ gộp 3 lần", vv("vote_acc1"), vv("vote_acc3"), ORANGE)],
               f"{sgn(vv('vote_acc1') - vv('single_acc1'))} @1")]
    bv = bd.DECK == "baove"  # FailLoc+Verify (test split) is shown only at the defence
    if bv:
        pav = {r["config"]: r for r in _csv(ROOT / "data" / "pav_test.csv") if r["gt"] == "repaired"}
        pv = lambda c, k: 100 * float(pav[c][k])
        groups.append(("FailLoc+Verify", [("FailLoc", pv("chosen", "single_acc1"), pv("chosen", "single_acc3"), GREY),
                                          ("+MinFix", pv("chosen", "pav_acc1"), pv("chosen", "pav_acc3"), ORANGE),
                                          ("+AnyFix", pv("worst", "pav_acc1"), pv("worst", "pav_acc3"), RED)],
                       f"{sgn(pv('chosen', 'pav_acc1') - pv('chosen', 'single_acc1'))} @1"))
    bd.A("bo_sung_kq.svg", viz.grouped_bars("bo-sung", 30, 96, 900, groups, label_w=150, sub_w=140,
                                            **(dict(bar_h=22, gap=3, group_gap=8) if bv else dict(bar_h=24, gap=4, group_gap=14))))
    bd.A("bo_sung_kq.svg", _note(30, 360 if bv else 302, ["Tập test, nhãn đã chuẩn hóa. Trên: Acc@1, dưới (sáng hơn): Acc@3 (%). Ô cam: chênh lệch Acc@1."],
                               size=12, gid="chu-giai-bo-sung", w=900))
    st = {r["tool"]: r for r in _csv(ROOT / "data" / "static_tools.csv") if r["gt"] == "repaired"}
    bd.A("bo_sung_kq.svg", P("bo-sung-kq-giai-thich", 30, 378 if bv else 322, 900, [
        ("", "Không cách nào đưa SemLoc lên ngang FailLoc hay làm FailLoc tốt hơn rõ rệt."),
        ("Phân tích tĩnh", f"ruff cảnh báo {st['ruff_all']['diagnostics']} lần, chỉ {st['ruff_all']['on_fault_line']} lần "
                           "trúng dòng lỗi; pyrefly không trúng lần nào."),
    ], size=15))

    # 19. decomposition
    dec = [r for r in mf.decomposition_data() if r["gt"] == "repaired"]
    _title(bd, "phan_ra.svg", "Ở hạng 1, phần lớn độ chính xác của SemLoc đến từ dòng đoán")
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
        ("", "Độ chính xác của SemLoc (điểm phần trăm, nhãn đã chuẩn hóa, ba lần chạy) được chia cho hai nguồn bằng giá trị "
             "Shapley."),
        ("", "Ở Acc@1, phần lớn đến từ dòng đoán; bằng chứng thực thi chỉ chiếm phần lớn ở Acc@3. Kết quả này khớp với giả "
             "thuyết H1 nhóm đặt ra trước khi chạy."),
    ], size=14, h=250))

    # 20. improvement over SemLoc on every setting
    imp = mf.improvement_data()
    k_of = lambda r: 3 if "BugsInPy" in r["setting"] else 1  # real bugs are compared at Acc@3 (page bugsinpy)
    rows = [(r["setting"] + f", Acc@{k_of(r)}", f"{_p(r[f'semloc{k_of(r)}'])}%", f"{_p(r[f'failloc{k_of(r)}'])}%",
             f"{'+' if r[f'failloc{k_of(r)}'] >= r[f'semloc{k_of(r)}'] else ''}"
             f"{_p(r[f'failloc{k_of(r)}'] - r[f'semloc{k_of(r)}'])} điểm") for r in imp]
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    rows.append(("Token mỗi chương trình", f"{m('CostSemlocTokensK')} nghìn", f"{m('CostLlmTestsTokensK')} nghìn", f"ít hơn {_p(ratio, 0)} lần"))
    _title(bd, "cai_tien_2.svg", "Cải tiến giữ được trên ba bộ nhãn, cùng chiều trên lỗi thật")
    band(bd, "cai_tien_2.svg", 5, rq="RQ2")
    bd.A("cai_tien_2.svg", viz.before_after("truoc-sau-2", 30, 98, 900, rows, row_h=56))
    bd.A("cai_tien_2.svg", _note(30, 438, ["Cùng chương trình, cùng Gemini 3.8 Flash, trung bình 3 lần chạy; BugsInPy là lỗi thật, mẫu nhỏ, khoảng tin cậy chứa 0."],
                                 size=13, gid="dieu-kien-2", w=900))

    # 21. conclusion: an answer per research question, then the contributions (content 3)
    _title(bd, "dong_gop_2.svg", "Đóng góp của nhóm: trả lời bốn câu hỏi nghiên cứu")
    band(bd, "dong_gop_2.svg", 6, content=3)
    items = [
        ("C1", "RQ1", f"Kiểm tra lại SemLoc: hạng 1 của SemLoc luôn là dòng LLM tự đoán nhờ điểm thưởng {m('ConstPriorWeight')} "
                      f"mà bài báo không mô tả (overclaim); rà soát nhãn cho thấy {m('LabaudAllMoved')}/{m('LabaudAllN')} "
                      "nhãn gốc lệch, nhóm công bố hai bộ nhãn mới."),
        ("C2", "RQ2", f"Đề xuất phương pháp FailLoc: chỉ một prompt kèm test fail nhưng hơn SemLoc ở Acc@1 trên cả ba bộ nhãn "
                      f"({m('RqTwoOriginalAllLlmTestsDAccOne')}, {m('RqTwoRepairedAllLlmTestsDAccOne')} và "
                      f"{m('RqTwoReviewedAllLlmTestsDAccOne')} điểm), dùng ít token hơn khoảng {_p(ratio, 0)} lần."),
        ("C3", "RQ3", "Giải thích vì sao FailLoc thắng: chính thông tin của test fail tạo ra khác biệt; thêm độ phủ, CovGate, "
                      "FailLoc+Vote" + (", FailLoc+Verify" if bv else "") + " hay phân tích tĩnh đều không thu hẹp được "
                      "khoảng cách" + (", vì test đủ để gợi ý lỗi nhưng không đủ để chứng minh lỗi ở đâu." if bv else ".")),
        ("C4", "RQ4", f"Kiểm chứng độ bền: FailLoc vẫn thắng SemLoc trên {m('BipAllSemlocPriorN')} lỗi thật BugsInPy (Acc@3 "
                      f"{m('BipAllLlmTestsAccThreeMean')}% so với {m('BipAllSemlocPriorAccThreeMean')}%), gần như không đổi "
                      f"khi mã bị đổi tên định danh ({sg(rv('llm_tests', 'd_acc3'))} điểm Acc@3), và không thua SemLoc ở "
                      f"cả {len(with_fl)} họ mô hình."),
    ]
    bd.A("dong_gop_2.svg", contributions(items, bottom=440 if bv else 470))
    if bv:
        bd.A("dong_gop_2.svg", _note(30, 474, ["Hướng phát triển: tìm thêm nhiều bộ dữ liệu lỗi, nhất là lỗi thật từ nhiều dự "
                                               "án và ngôn ngữ khác."], size=15, fill=NAVY, weight="bold", gid="huong-phat-trien",
                                     w=900))

    # 22. progress
    _title(bd, "tien_do_2.svg", "Tiến độ")
    bd.A("tien_do_2.svg", viz.progress_table("bang-tien-do-2", 40, 104, 880, progress_rows(2), row_h=46))
    bd.A("tien_do_2.svg", _note(40, 480, ["Đang hoàn thiện: dữ liệu và kết quả đã có, nhóm đang viết và kiểm tra lại."],
                                size=13, gid="chu-thich-tien-do-2", w=880))


def notes(bd) -> dict:
    m = bd._m
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    acc = lambda g, mm, k=1: 100 * float(rq2[(g, mm)][f"acc{k}_mean"])
    r3 = mf.rq3_data()
    return {
        **({"slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 2 của đề tài bằng chứng hay phỏng "
                        "đoán."} if bd.DECK == "lan2" else {}),
        "muc_luc_2": "Tuần vừa rồi nhóm sửa nhãn và đề xuất phương pháp FailLoc. Sau phần nhắc lại, nhóm trình bày cách chuẩn "
                     "hóa nhãn, phương pháp FailLoc và luồng chạy của nó trên ví dụ, thiết kế thực nghiệm, kết quả so sánh "
                     "chính, rà soát nhãn, rồi tiến độ.",
        "nhac_lai": f"Nhắc lại lần 1: nhóm tái hiện SemLoc và đạt Acc@1 {_p(acc('original', 'semloc'))}% trên nhãn gốc. Nhưng "
                    f"bỏ điểm thưởng cho dòng LLM đoán thì Acc@1 chỉ còn {_p(acc('original', 'semloc_no_prior'))}%, và "
                    f"{m('GtBlankN')} nhãn gốc nằm trên dòng trống. Tuần này nhóm làm ba việc: chuẩn hóa nhãn, đề xuất FailLoc "
                    "và so sánh với SemLoc, rồi rà soát lại toàn bộ nhãn.",
        "nhan_lech": "Chuẩn hóa xong vẫn còn một vấn đề về nhãn. Ở chương trình blend_orders, nhãn gốc là dòng điều kiện 72, nhưng câu lệnh "
                     "được bảo vệ ở dòng 73 cũng hợp lý. Phép chấm chặt chỉ công nhận một dòng, nên nhãn lệch một dòng là đủ "
                     "làm sai kết quả. Vì vậy nhóm rà soát lại cả 250 nhãn.",
        "ablation_la_gi": "Ablation là giữ mọi thứ cố định và chỉ thêm một thành phần. Từ LLM-Direct chỉ có mã, thêm test fail "
                          "thành FailLoc, rồi thêm độ phủ từng dòng thành FailLoc+Cov. Chênh lệch giữa hai bước là tác dụng "
                          "của thành phần vừa thêm.",
        "shapley": "Để biết độ chính xác của SemLoc đến từ đâu, nhóm dùng giá trị Shapley. Đo độ chính xác ở cả bốn tổ hợp: "
                   "không nguồn nào, chỉ dòng đoán, chỉ phổ vi phạm, và cả hai. Phần của mỗi nguồn là mức tăng trung bình "
                   "khi thêm nó vào. Ví dụ với Acc@1 trên nhãn đã chuẩn hóa: phần của dòng đoán là một nửa của Acc@1 khi chỉ "
                   "có dòng đoán, cộng một nửa mức tăng khi thêm dòng đoán vào phổ; tính ra phần của dòng đoán lớn hơn phần "
                   "của phổ, và hai phần cộng lại đúng bằng Acc@1 của SemLoc.",
        "ra_soat": f"Rà soát nhãn có hai bước. LLM đọc mã, test và nhãn của cả {m('LabaudAllN')} chương trình và cho nhận định; "
                   f"sau đó {m('ReviewReviewersN')} thành viên duyệt lại {m('ReviewHumanN')} nhãn nghi vấn. Người duyệt có xem "
                   "gợi ý của LLM, nên nhóm làm thêm một vòng duyệt mù: phiếu không ghi nhãn nào, và kết quả ủng hộ bộ "
                   "nhãn đã rà soát.",
        "rq3_thiet_ke": f"RQ4 thử độ bền theo ba cách: {m('BipAllSemlocPriorN')} lỗi thật của BugsInPy, mã đã đổi tên mọi định "
                        "danh để kiểm tra LLM có nhớ bộ dữ liệu không, và năm họ mô hình khác nhau. Bên trái là hàm ví dụ trước và sau khi đổi "
                        "tên: các tên gợi ý như weights hay shares thành v4, v8, còn chú thích và docstring ở các dòng tô màu bị "
                        "xóa, số dòng giữ nguyên.",
        "ba_prompt": "Đây là ba mức prompt trên ví dụ 1. LLM-Direct chỉ có mã; FailLoc thêm tên và lỗi của test fail; FailLoc+Cov "
                     "thêm chú thích độ phủ như f=1/p=4 cho mỗi dòng. Ở ví dụ này mọi dòng đều có cùng chú thích, nên chỉ "
                     "thông báo lỗi của test fail mới gợi ý dòng 29.",
        "bo_sung": "Nhóm thử thêm ba hướng: CovGate xếp lại dòng của SemLoc bằng độ phủ; FailLoc+Vote hỏi FailLoc ba lần, cho dòng hạng k "
                   "một phần k điểm, cộng lại rồi xếp theo tổng, không gọi LLM thêm; và "
                   "hai công cụ phân tích tĩnh là ruff và pyrefly. Câu hỏi là thêm phức tạp có giúp được không.",
        "nhan_di_dau": f"Kết quả rà soát: {m('LabaudAllMoved')} trên {m('LabaudAllN')} nhãn gốc bị dời, nhiều nhất là nhãn nằm trên "
                       "dòng trống hoặc dòng không phải mã, rồi đến nhãn lệch một dòng. Một số lỗi trải hai dòng nên nhóm "
                       "thêm dòng thứ hai. Đây là bộ nhãn đã rà soát dùng ở các trang sau.",
        "ba_bo_nhan": ("Bảng này có năm phương pháp của so sánh chính: phương pháp SBFL, LLM-Direct, SemLoc, SemLoc−Bonus và "
                       "FailLoc." if bd.DECK == "lan2" else "Bảng này có đủ sáu phương pháp của so sánh chính: phương pháp "
                       "SBFL, LLM-Direct, SemLoc, CovGate, FailLoc+Cov và FailLoc.") +
                      " Trên cả ba bộ nhãn, FailLoc cao nhất ở Acc@1 và đều hơn SemLoc. Ở Acc@1 là "
                      f"{m('RqTwoOriginalAllLlmTestsDAccOne')} điểm trên nhãn gốc, {m('RqTwoRepairedAllLlmTestsDAccOne')} trên nhãn "
                      f"đã chuẩn hóa và {m('RqTwoReviewedAllLlmTestsDAccOne')} trên nhãn đã rà soát. Số tuyệt đối thay đổi theo bộ nhãn, nhưng chiều của kết luận thì không.",
        "bugsinpy": f"Trên {m('BipAllSemlocPriorN')} lỗi thật, FailLoc cao nhất ở Acc@3. Mọi lần SemLoc đúng ở hạng 1 đều là dòng LLM "
                    "đoán. SemLoc trừ Bonus, tức SemLoc không cộng điểm thưởng, chỉ xếp theo phổ vi phạm, thì gần bằng phương pháp SBFL.",
        "doi_ten": "Khi đổi tên mọi định danh, dòng LLM đoán gần như giữ nguyên, nhưng SemLoc trừ Bonus giảm mạnh: ràng buộc "
                   "LLM viết dựa vào tên gợi ý. FailLoc và FailLoc+Cov gần như không đổi, nên kết quả của FailLoc không đến từ "
                   "việc LLM nhớ bộ dữ liệu.",
        "ho_mo_hinh": f"Với {r3['n_families']} chương trình và năm họ mô hình, SemLoc trừ Bonus có Acc@1 thấp hơn SemLoc ở "
                      f"{sum(v['semloc_no_prior'] < v['semloc'] for v in r3['families'].values())} trên "
                      f"{len(r3['families'])} họ. Vậy ở mô hình nào, hạng 1 của SemLoc cũng dựa vào dòng LLM đoán. FailLoc, hình thoi "
                      "cam, hơn SemLoc rõ ở bốn họ; với GPT-6 luna thì hai phương pháp ngang nhau ở Acc@1. Luna với prompt FailLoc "
                      "thường chỉ trả hai, ba dòng thay vì năm, nên Acc@3 của nó thấp hơn.",
        "ablation_kq": "Ablation trả lời vì sao FailLoc thắng. Thêm test fail vào prompt tăng Acc@3 trên cả ba bộ nhãn; thêm độ "
                       "phủ từng dòng thì không tăng. LLM không cần thông tin mà phương pháp SBFL dùng.",
        "bo_sung_kq": "Các cách bổ sung đều không giúp: CovGate giữ nguyên Acc@1 của SemLoc, FailLoc+Cov giảm, FailLoc+Vote "
                      "trên tập test chỉ tăng nửa điểm, nằm trong sai số. Công cụ phân tích tĩnh gần như không trúng dòng lỗi.",
        "phan_ra": "Phân rã Shapley cho thấy ở Acc@1, phần lớn độ chính xác của SemLoc đến từ dòng LLM đoán; bằng chứng thực thi "
                   "chỉ chiếm phần lớn ở Acc@3. Điều này khớp với giả thuyết H1 nhóm đặt ra từ đầu.",
        "cai_tien_2": "Gói lại, mức hơn của FailLoc so với SemLoc giữ được trên cả ba bộ nhãn và cùng chiều trên lỗi thật, với chi phí thấp "
                      "hơn nhiều. Đây là cải tiến chính của nhóm so với bài gốc.",
        "dong_gop_2": "Đây là nội dung 3: bốn đóng góp, mỗi đóng góp trả lời một câu hỏi nghiên cứu. C1: hạng 1 của SemLoc là "
                      "dòng LLM đoán nhờ điểm thưởng bài báo không mô tả, và gần một nửa nhãn gốc lệch nên nhóm công bố hai bộ "
                      "nhãn mới. C2: FailLoc, chỉ một prompt có test fail, thắng SemLoc trên cả ba bộ nhãn và rẻ hơn nhiều. "
                      "C3: FailLoc thắng nhờ thông tin của test fail, còn thêm phức tạp không giúp. C4: FailLoc vẫn thắng trên "
                      "lỗi thật, gần như không đổi khi mã bị đổi tên, và không thua SemLoc ở cả năm họ mô hình.",
        "tien_do_2": "Về tiến độ, chuẩn hóa và rà soát nhãn, phương pháp FailLoc và so sánh chính đã xong. Lần 3 nhóm trình "
                     "bày độ bền, ablation, các hướng bổ sung, chi phí và đóng góp khoa học. Bài báo arXiv và phân tích thất "
                     "bại để dành cho buổi bảo vệ.",
        "slide_30": "Nhóm xin cảm ơn thầy và các bạn, rất mong nhận được câu hỏi và góp ý.",
    }

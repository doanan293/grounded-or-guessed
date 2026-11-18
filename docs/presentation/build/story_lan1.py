"""Báo cáo lần 1 (~20 phút, 23 trang): the teacher's five parts, two running examples on real data.

Part 1 cơ sở lý thuyết, 2 phương pháp giải quyết (bài gốc SemLoc), 3 kiểm tra lại bài gốc (RQ1), 4 cải tiến (FailLoc),
5 thực nghiệm và kết quả, then the progress table. votes_apportion runs through SBFL, SemLoc and FailLoc;
blend_orders shows SemLoc's scoring at work (on votes_apportion no constraint is violated, every score is 0).
"""
import json

import viz
from story_common import (MAIN, ROOT, _bonus_rows, _card, _csv, _guess_rank1_share, _note, _title, _unbold, band,
                          examples, name)
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

LAN1 = [("slide_01.svg", 1), ("muc_luc.svg", 22),
        ("bai_toan.svg", 22), ("vi_du.svg", 22), ("sbfl_cong_thuc.svg", 22), ("sbfl_mu.svg", 22), ("lien_quan.svg", 22),
        ("semloc_tong_quan.svg", 22), ("semloc_rang_buoc.svg", 22), ("semloc_diem.svg", 22), ("semloc_thuong.svg", 22),
        ("cau_hoi.svg", 20),
        ("overclaim.svg", 22), ("nhan_sai.svg", 22), ("chuan_hoa.svg", 22),
        ("failloc_y_tuong.svg", 22), ("failloc_vd.svg", 22), ("phuong_phap.svg", 22),
        ("thiet_ke_tn.svg", 22), ("ket_qua.svg", 22), ("cai_tien.svg", 22),
        ("tien_do.svg", 22), ("slide_30.svg", 30)]

PROGRESS = [("Tài liệu, bộ từ khóa, ba bài tiêu biểu (nội dung 1)", "Đã xong", "Lần 1"),
            ("Ba câu hỏi nghiên cứu, thiết kế thực nghiệm (nội dung 2)", "Đã xong", "Lần 1"),
            ("Tái hiện SemLoc, chuẩn hóa nhãn, so sánh FailLoc với SemLoc", "Đã xong", "Lần 1"),
            ("Rà soát nhãn, duyệt mù, độ bền (RQ3), ablation", "Đang hoàn thiện", "Lần 2 (25–26/11)"),
            ("Đóng góp và triết lý khoa học (nội dung 3)", "Đang hoàn thiện", "Lần 2 (25–26/11)"),
            ("Phân tích thất bại, kiểm chứng bằng bản sửa", "Đang hoàn thiện", "Bảo vệ (12/2026)"),
            ("Bài báo arXiv bản cuối (nội dung 4)", "Chưa làm", "26/11–10/12")]
KEYWORDS = ["định vị lỗi (fault localization)", "định vị lỗi dựa trên phổ (SBFL)", "lỗi ngữ nghĩa (semantic fault)",
            "ràng buộc ngữ nghĩa (semantic constraint)", "phổ vi phạm (violation spectrum)",
            "kiểm chứng phản thực tế (counterfactual)"]


def inserted_checks(ex: dict) -> dict:
    """Where each constraint is checked in the code window: a line constraint at its line, a loop-tail check after the
    loop body, a check on the value about to be returned before the first return, a check on every return at it."""
    code = {c["no"]: c["text"] for c in ex["code_lines"]}
    ret = next(n for n, t in sorted(code.items()) if t.strip().startswith("return"))
    loop = next((n for n, t in sorted(code.items()) if t.strip().startswith("for ")), None)
    loop_end = loop
    if loop:
        ind = len(code[loop]) - len(code[loop].lstrip())
        for n in sorted(k for k in code if k > loop):
            t = code[n]
            if t.strip() and len(t) - len(t.lstrip()) <= ind:
                break
            if t.strip():
                loop_end = n
    out: dict = {}
    for c in ex["constraints"]:
        r = c["region"]
        at = (c["anchor_line"] if r in ("LINE", "AFTER_BRANCH") else loop_end if r == "LOOP_TAIL"
              else ret - 1 if r == "BEFORE_USE" else ret)
        if at in code:
            out[at] = (out[at] + "; " if at in out else "") + f"# kiểm tra {c['id']}: {c['expr']}"
    return out


def pages(bd) -> None:
    m = bd._m
    P = viz.panel
    ex = examples()
    va, bo = ex["votes_apportion"], ex["blend_orders"]
    vcode = {c["no"]: c["text"] for c in va["code_lines"]}
    gt = va["label_lines"][0]
    win = list(range(gt - 7, gt + 2))
    fail_test = next(t for t in json.loads((ROOT / "data" / "fig_example.json").read_text())["tests"] if not t["passed"])
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    a1 = lambda g, mm: _p(100 * float(rq2[(g, mm)]["acc1_mean"]))
    a3 = lambda g, mm: _p(100 * float(rq2[(g, mm)]["acc3_mean"]))
    d1 = m("RqTwoRepairedAllLlmTestsDAccOne")

    # 2. agenda: the teacher's five parts
    _title(bd, "muc_luc.svg", "Nội dung trình bày")
    items = [("1", "Cơ sở lý thuyết", "Bài toán, lỗi ngữ nghĩa, phương pháp SBFL, nghiên cứu liên quan"),
             ("2", "Phương pháp giải quyết", "Phương pháp SemLoc của bài gốc từng bước; ba câu hỏi nghiên cứu"),
             ("3", "Kiểm tra lại bài gốc", "Điểm thưởng quyết định hạng 1; chuẩn hóa nhãn"),
             ("4", "Cải tiến", "Phương pháp FailLoc: một lượt gọi LLM kèm test fail"),
             ("5", "Thực nghiệm và kết quả", "Thiết kế, kết quả chính, cải tiến so với phương pháp SemLoc"),
             ("", "Tiến độ", "Việc đã xong, việc đang hoàn thiện và lịch các tuần sau")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 112 + i * 62
        body.append(_r(60, y, 840, 52, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else LAVENDER, rx=10, sw=1.2))
        body.append(_t(92, y + 34, k or "•", size=24, fill=NAVY, weight="bold", anchor="middle"))
        body.append(_t(130, y + 33, head, size=19, fill=NAVY, weight="bold"))
        body.append(_t(400, y + 33, desc, size=15))
    bd.A("muc_luc.svg", viz._g("muc-luc", 60, 112, 840, 362, body))

    # 3. the problem
    _title(bd, "bai_toan.svg", "Bài toán định vị lỗi: từ test fail đến danh sách dòng đáng nghi")
    band(bd, "bai_toan.svg", 1)
    bd.A("bai_toan.svg", viz.pipeline("bai-toan-luong", 40, 112, ["Đầu vào\nmã nguồn + bộ test\n(có test fail)",
                                                                   "Phương pháp\nđịnh vị lỗi", "Đầu ra\ncác dòng xếp hạng\ntừ nghi nhất"],
                                      accent=1, box_w=250, gap=45, box_h=86))
    rank_body = [_r(640, 214, 240, 150, "#FFFFFF", stroke=LAVENDER, rx=8)]
    for i, (ln, ok) in enumerate(((29, True), (25, False), (26, False))):
        rank_body.append(_t(656, 244 + 34 * i, f"Hạng {i + 1}: dòng {ln}", size=16, weight="bold" if ok else "normal",
                            fill=ORANGE if ok else INK))
    rank_body.append(_t(656, 350, "Ví dụ: dòng lỗi 29 ở hạng 1", size=13, fill=MUTED))
    bd.A("bai_toan.svg", viz._g("vi-du-xep-hang", 640, 214, 240, 150, rank_body))
    bd.A("bai_toan.svg", P("acc-k", 40, 222, 570, [
        ("Đo độ chính xác bằng Acc@k", "Acc@1 là tỉ lệ chương trình có dòng lỗi thật đứng ở hạng 1; Acc@3 là tỉ lệ có dòng "
                                       "lỗi nằm trong 3 dòng đầu. Ví dụ bên phải trúng cả Acc@1 lẫn Acc@3."),
        ("Dòng lỗi thật lấy từ đâu", "Từ nhãn của bộ dữ liệu: mỗi chương trình được ghi sẵn một dòng lỗi. Nhãn sai thì phép "
                                     "chấm cũng sai, phần 3 sẽ quay lại điểm này."),
    ], size=15))

    # 4. the running example
    _title(bd, "vi_du.svg", f"Ví dụ xuyên suốt: hàm {va['program']} có một test fail")
    band(bd, "vi_du.svg", 1)
    short = lambda t: t if len(t) <= 46 else t[:44].rstrip() + " …"
    bd.A("vi_du.svg", viz.code_block("ma-vi-du", 40, 108, [short(vcode[n]) for n in win], first_no=win[0], fs=15, width=540,
                                     highlight={gt}, mark={gt: "dòng lỗi theo nhãn"}))
    bd.A("vi_du.svg", P("test-ket-qua", 40, 330, 540, [
        ("Kết quả chạy test", f"{va['n_pass']} test pass, {va['n_fail']} test fail: {fail_test['id']}. Test này đòi tổng các "
                              "phần chia bằng tổng ban đầu; int(v) ở dòng 29 cắt phần lẻ nên tổng bị thiếu.")], size=14,
                       head_color=RED))
    bd.A("vi_du.svg", P("loi-ngu-nghia", 600, 108, 320, [
        ("Lỗi ngữ nghĩa là gì", "Chương trình chạy đúng đường, không lỗi cú pháp, không lỗi kiểu, nhưng tính sai giá trị. "
                                "Công cụ kiểm tra cú pháp hay kiểu không báo gì."),
        ("Bộ dữ liệu SemFault-250", "250 chương trình Python, mỗi chương trình có đúng một lỗi ngữ nghĩa được cài vào và "
                                    "khoảng mười test. Bài gốc SemLoc giới thiệu bộ dữ liệu này."),
        ("Câu hỏi", "Một phương pháp định vị lỗi có chỉ ra được dòng 29 không?"),
    ], size=14))

    # 5. SBFL: the formula, computed by hand on line 29
    _title(bd, "sbfl_cong_thuc.svg", "Phương pháp SBFL: dòng hay bị test fail chạy qua thì đáng nghi")
    band(bd, "sbfl_cong_thuc.svg", 1)
    bd.A("sbfl_cong_thuc.svg", viz.formula("ochiai", 40, 110, 540, [
        "Ochiai(dòng) = ef / √( F × (ef + ep) )",
        "ef: số test fail chạy qua dòng đó",
        "ep: số test pass chạy qua dòng đó",
        "F: tổng số test fail của chương trình"], size=18))
    n_all = va["n_fail"] + va["n_pass"]
    bd.A("sbfl_cong_thuc.svg", P("tinh-tay", 40, 260, 540, [
        (f"Tính tay cho dòng {gt} của ví dụ", f"Cả {n_all} test đều chạy qua dòng {gt}: ef = {va['n_fail']}, ep = {va['n_pass']}, "
                                             f"F = {va['n_fail']}. Ochiai = 1 / √(1 × 5) = 0,45."),
        ("Nhưng", f"Mọi dòng khác trong hàm cũng được cả {n_all} test chạy qua, nên cũng được 0,45. Không dòng nào nổi lên."),
    ], size=15))
    bd.A("sbfl_cong_thuc.svg", P("sbfl-la-gi", 600, 110, 320, [
        ("Phương pháp SBFL", "Định vị lỗi dựa trên phổ độ phủ (spectrum-based fault localization): chạy bộ test, ghi lại test "
                             "nào chạy qua dòng nào, rồi chấm điểm từng dòng."),
        ("Ý tưởng", "Dòng gây lỗi thì hay nằm trên đường chạy của test fail và ít nằm trên đường chạy của test pass."),
        ("Khi nào hỏng", "Lỗi ngữ nghĩa: test fail và test pass đi qua đúng cùng các dòng."),
    ], size=14))

    # 6. SBFL on the example: everything ties
    rows = [n for n in win[:-1] if vcode[n].strip()]
    tests = json.loads((ROOT / "data" / "fig_example.json").read_text())["tests"]
    cols = [f"t{j + 1}" for j in range(len(tests))]
    cells = {(i, j) for i, n in enumerate(rows) for j, t in enumerate(tests) if n in t["lines"]}
    fail_cols = {j: RED for j, t in enumerate(tests) if not t["passed"]}
    _title(bd, "sbfl_mu.svg", "Phương pháp SBFL trên ví dụ: mọi dòng hòa điểm, không ra dòng lỗi")
    band(bd, "sbfl_mu.svg", 1)
    bd.A("sbfl_mu.svg", viz.matrix("ma-tran-phu", 30, 104, [f"{n}  {vcode[n].strip()[:20]}" for n in rows], cols, cells,
                                   row_mark={rows.index(gt): RED}, label_w=280, cell_w=46, row_h=34,
                                   col_colors={**{j: NAVY for j in range(len(cols))}, **fail_cols},
                                   col_sub=["fail" if j in fail_cols else "pass" for j in range(len(cols))]))
    bd.A("sbfl_mu.svg", P("sbfl-doc", 580, 104, 340, [
        ("Cách đọc", "Mỗi hàng là một dòng mã, mỗi cột là một test; chấm nghĩa là test chạy qua dòng đó. Cột "
                     f"{', '.join(cols[j] for j in fail_cols)} (đỏ) là test fail duy nhất; hàng tô màu là dòng lỗi {gt}."),
        ("Kết quả", "Mọi hàng giống hệt nhau nên mọi dòng có cùng điểm Ochiai 0,45: phương pháp SBFL chỉ còn đoán ngẫu nhiên."),
    ], size=14))
    bd.A("sbfl_mu.svg", viz.big_number("sbfl-acc", 580, 380, f"{m('RqOneSbflOchiaiFairAllAccOne')}%",
                                       "Acc@1 của phương pháp SBFL\ntrên cả 250 chương trình", color=RED, size=44, w=340))

    # 7. related work: keywords + three representative studies [content 1]
    _title(bd, "lien_quan.svg", "Nghiên cứu liên quan: bộ từ khóa và ba bài tiêu biểu  [nội dung 1]")
    band(bd, "lien_quan.svg", 1)
    chips, cx = [], 40
    for k in KEYWORDS[:3]:
        w = 9 + 7.2 * len(k)
        chips += [_r(cx, 100, w, 26, viz.LIGHT, rx=13), _t(cx + w / 2, 118, k, size=12, anchor="middle")]
        cx += w + 8
    bd.A("lien_quan.svg", viz._g("tu-khoa", 40, 100, cx - 40, 26, chips))
    cards = [("SemLoc (2026)", [("Bài toán", "lỗi ngữ nghĩa trong hàm Python; test fail nhưng không chỉ ra dòng."),
                                 ("Cách làm", "LLM viết ràng buộc, chạy test lấy phổ vi phạm, vá thử để kiểm chứng."),
                                 ("Kết quả", f"Acc@1 {m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% trên SemFault-250."),
                                 ("Nhóm áp dụng", "dùng lại đúng mã nguồn và dữ liệu của tác giả để chạy lại và kiểm tra "
                                                  "từng con số (RQ1).")]),
             ("EffiHolmes (2026)", [("Bài toán", "lỗi hiệu năng: test vẫn pass, không có lỗi để lần theo."),
                                     ("Cách làm", "so hai lần chạy dữ liệu nhỏ và lớn; hàm chậm hẳn đi thì bị nghi."),
                                     ("Kết quả", "thử trên 140 lỗi chạy chậm thật."),
                                     ("Nhóm áp dụng", "so một lần chạy bình thường với một lần chạy có lỗi để tìm chỗ khác "
                                                      "nhau; ở đây là so test pass với test fail.")]),
             ("Sự cố + LLM (2026)", [("Bài toán", "app Java lớn sập hàng nghìn lần mỗi tuần, mỗi lần có stack trace."),
                                      ("Cách làm", "gom stack trace thành bảng hàm đáng nghi, đưa bảng vào prompt."),
                                      ("Kết quả", "38 lỗi thật, chỉ đúng chỗ lỗi 71%."),
                                      ("Nhóm áp dụng", "đưa thẳng bằng chứng có sẵn vào prompt; nhóm đưa thông báo lỗi của "
                                                       "test fail vào prompt, đó là phương pháp FailLoc.")])]
    for k, (head, blocks) in enumerate(cards):
        bd.A("lien_quan.svg", _t(40 + k * 300, 152, head, size=18, fill=ORANGE, weight="bold"))
        bd.A("lien_quan.svg", P(f"bai-{k}", 40 + k * 300, 162, 284, [(a, b[0].upper() + b[1:]) for a, b in blocks], size=13))

    # 8. SemLoc overview
    _title(bd, "semloc_tong_quan.svg", "Phương pháp SemLoc: LLM viết ràng buộc, test kiểm chứng")
    band(bd, "semloc_tong_quan.svg", 2)
    steps = ["1. LLM viết\nràng buộc", "2. Chèn\nvào mã", "3. Chạy\nbộ test", "4. Chấm điểm\ntừng dòng", "5. LLM vá thử,\nchạy lại test"]
    bd.A("semloc_tong_quan.svg", viz.pipeline("quy-trinh-semloc", 40, 108, steps, box_w=158, gap=22, box_h=72))
    expl = ["Điều kiện phải đúng\nnếu mã chạy đúng", "Mỗi ràng buộc thành\nmột lệnh kiểm tra", "Ghi ràng buộc nào bị\nvi phạm trong test nào",
            "Ràng buộc vi phạm ở\ntest fail thì dòng\ncủa nó đáng nghi", "Vá dòng nghi; test\npass lại thì xác nhận"]
    body = []
    for k, e in enumerate(expl):
        for r_, line in enumerate(e.split("\n")):
            body.append(_t(40 + k * 180 + 79, 204 + 18 * r_, line, size=13, fill=MUTED, anchor="middle"))
    bd.A("semloc_tong_quan.svg", viz._g("giai-thich-buoc", 40, 190, 880, 70, body))
    bd.A("semloc_tong_quan.svg", viz.big_number("acc-cong-bo", 40, 290, f"{m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}%",
                                                "Acc@1 phương pháp SemLoc\ncông bố trên SemFault-250\n(Claude Sonnet 4.6)",
                                                size=56, w=300))
    bd.A("semloc_tong_quan.svg", P("loi-hua", 370, 285, 550, [
        ("Bài báo khẳng định", "Độ chính xác đến từ việc neo lập luận của LLM vào bằng chứng thực thi (structured "
                               "grounding): LLM chỉ đề xuất, kết quả chạy test quyết định thứ hạng."),
        ("Ba trang sau", f"Đi qua từng bước trên dữ liệu thật: ràng buộc LLM viết cho {va['program']}, cách chấm điểm trên "
                         f"{bo['program']}, và bước cuối cùng quyết định hạng 1."),
    ], size=14))

    # 9. SemLoc steps 1-2 on votes_apportion: the constraints and where they are checked
    _title(bd, "semloc_rang_buoc.svg", f"Bước 1–2 trên ví dụ: LLM đoán dòng {va['guess_line']} và viết bốn ràng buộc")
    band(bd, "semloc_rang_buoc.svg", 2)
    ins = inserted_checks(va)
    bd.A("semloc_rang_buoc.svg", viz.code_block("ma-co-kiem-tra", 30, 104, [short(vcode[n]) for n in win], first_no=win[0], fs=14,
                                                width=600, highlight={gt}, inserted={k: short(v) for k, v in ins.items()}))
    bd.A("semloc_rang_buoc.svg", P("rang-buoc-la-gi", 650, 104, 280, [
        ("Ràng buộc là gì", "Một điều kiện mà LLM cho là phải đúng nếu mã chạy đúng, ví dụ tổng các phần chia không vượt "
                            "quá tổng ban đầu."),
        ("Dòng nghiêng", "Lệnh kiểm tra SemLoc chèn vào mã. Khi một test chạy qua mà điều kiện sai, ràng buộc bị vi phạm."),
        ("Dòng LLM đoán", f"LLM còn đoán thẳng dòng lỗi: dòng {va['guess_line']}. Dòng lỗi theo nhãn là {gt}."),
    ], size=13))

    # 10. SemLoc steps 3-4 on blend_orders: violations, Ochiai, region weight, line score
    _title(bd, "semloc_diem.svg", "Bước 3–4: chạy test, đếm vi phạm, chấm điểm từng dòng")
    band(bd, "semloc_diem.svg", 2)
    where = lambda c: (f"dòng {c['anchor_line']}" if c["region"] == "LINE" else
                       f"cuối nhánh if dòng {c['anchor_line']}" if c["region"] == "AFTER_BRANCH" else
                       "cuối vòng lặp" if c["region"] == "LOOP_TAIL" else "mọi lệnh return")
    rows_ct = [{"id": c["id"], "where": where(c), "expr": c["expr"].replace("__1", "")[:30], "fail": c["ef"], "pass": c["ep"],
                "ochiai": c["ochiai"], "weight": c["weight"], "score": c["ochiai"] * c["weight"]} for c in bo["constraints"]]
    bd.A("semloc_diem.svg", viz.constraint_table("bang-rang-buoc", 30, 104, 900, rows_ct))
    bd.A("semloc_diem.svg", viz.formula("diem-dong", 30, 300, 430, [
        "Điểm dòng = Ochiai × hệ số vùng",
        "hệ số: ràng buộc gắn đúng một dòng 0,6;",
        "cuối nhánh if 1; cuối vòng lặp 0,9; return 0,3",
        "một dòng lấy điểm cao nhất của các ràng buộc"], size=15))
    bd.A("semloc_diem.svg", P("vi-sao-blend", 480, 300, 450, [
        (f"Vì sao đổi sang {bo['program']}", f"Ở {va['program']}, cả bốn ràng buộc đều không bị vi phạm trong test nào, nên "
                                             "mọi điểm bằng 0. Chương trình này (nhãn đã chuẩn hóa: dòng "
                                             f"{bo['label_lines'][0]}) cho thấy cơ chế chấm điểm khi ràng buộc có bắt được lỗi."),
        ("Kết quả", f"Dòng {bo['label_lines'][0]} (dòng lỗi) được 1,00; dòng 73 được 0,60."),
    ], size=13))

    # 11. SemLoc step 5: the bonus and the patch-and-test step
    rs = sorted(bo["line_scores"], key=lambda r: r["rank"])[:5]
    _title(bd, "semloc_thuong.svg", f"Bước cuối: +{m('ConstPriorWeight')} cho dòng LLM đoán, dòng đó vượt lên hạng 1")
    band(bd, "semloc_thuong.svg", 2)
    ser = []
    for r in sorted(rs, key=lambda r: r["line"]):
        isg, isl = r["line"] == bo["guess_line"], r["line"] in bo["label_lines"]
        lab = f"dòng {r['line']}" + (" (lỗi)" if isl else "") + (" (đoán)" if isg else "")
        ser.append((lab, r["spectrum"] + r["bonus"], ORANGE if isg else NAVY if isl else GREY, r["spectrum"] if isg else 0))
    bd.A("semloc_thuong.svg", viz.bars("diem-cuoi", 30, 104, 520, 300, ser, vmax=2.0, unit="", label_w=170, nd=2))
    bd.A("semloc_thuong.svg", _note(30, 440, [f"Chương trình {bo['program']}, lượt chạy 1, Gemini 3.8 Flash.", "Phần xám: điểm phổ; phần cam: điểm thưởng."], size=13, gid="nguon-thuong", w=520))
    cf = bo["cf_results"][0] if bo["cf_results"] else None
    bd.A("semloc_thuong.svg", P("thuong-va-vathu", 580, 104, 350, [
        ("Điểm thưởng", f"Mã nguồn công bố cộng +{m('ConstPriorWeight')} cho dòng LLM tự đoán. Điểm phổ tối đa là 1, nên dòng "
                        "đoán luôn đứng hạng 1."),
        ("Ở ví dụ này", f"Dòng 73 (0,60 + 1,2 = 1,80) vượt dòng lỗi {bo['label_lines'][0]} (1,00)."),
        ("Bước vá thử", ("LLM vá dòng nghi; bản vá ở dòng 73 (dòng sai) vẫn làm mọi test pass nên được \"xác nhận\". "
                         if cf and cf["patch"] == "pass" else "") +
         "Kết quả vá thử không làm đổi thứ hạng ở cả 250 chương trình."),
    ], size=13))

    # 12. research questions [content 2]
    bd.E("cau_hoi.svg", [
        ("Popular programming languages", "Ba câu hỏi nghiên cứu  [nội dung 2]"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: số công bố còn đúng", "khi chấm công bằng, chuẩn hóa nhãn?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["LLM cần gì? Phương pháp FailLoc", "so với phương pháp SemLoc"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, mã đổi tên,", "các họ mô hình khác"]),
        ("Saturn", "Chung"), ("Saturn is a gas giant", ["Thứ hạng đến từ bằng chứng", "thực thi hay LLM tự đoán?"]),
    ])
    _unbold(bd, "cau_hoi.svg", "LLM cần gì?")
    band(bd, "cau_hoi.svg", 2)

    # 13. overclaim
    share, n_pairs = _guess_rank1_share()
    _title(bd, "overclaim.svg", "Hạng 1 luôn là dòng LLM đoán, bài báo lại quy công cho bằng chứng")
    band(bd, "overclaim.svg", 3)
    bd.A("overclaim.svg", viz.big_number("ty-le", 40, 104, f"{_p(100 * share, 0)}%",
                                         f"trong {n_pairs} lượt (chương trình × lần chạy),\nhạng 1 của SemLoc là dòng LLM đoán",
                                         color=ORANGE, size=48, w=380))
    bd.A("overclaim.svg", viz.bars("bo-thuong", 40, 260, 420, 100,
                                   [("SemLoc", 100 * float(rq2[("repaired", "semloc")]["acc1_mean"]), NAVY),
                                    ("SemLoc−Bonus", 100 * float(rq2[("repaired", "semloc_no_prior")]["acc1_mean"]), GREY)],
                                   vmax=100, label_w=140))
    bd.A("overclaim.svg", _note(40, 384, ["Acc@1, nhãn đã chuẩn hóa: bỏ điểm thưởng (SemLoc−Bonus)", "thì độ chính xác "
                                          f"giảm {m('RqTwoRepairedAllSemlocNoPriorDAccOne').lstrip('−-')} điểm."], size=13, gid="ghi-chu-bo-thuong",
                                w=420))
    bd.A("overclaim.svg", P("overclaim-la-gi", 490, 104, 440, [
        ("Overclaim (tuyên bố quá mức)", "Bài báo khẳng định mạnh hơn mức bằng chứng cho phép."),
        ("Ở bài SemLoc", "Điểm thưởng tự nó là một lựa chọn thiết kế. Chỗ overclaim là bài báo quy độ chính xác cho bằng "
                         "chứng thực thi trong khi không mô tả điểm thưởng, mà chính điểm thưởng quyết định hạng 1."),
        ("Thêm bằng chứng", f"Ở {va['program']}, bốn ràng buộc không bị vi phạm lần nào: hạng 1 (dòng {va['guess_line']}, "
                            "sai) hoàn toàn do điểm thưởng."),
    ], size=14))

    # 14. the labels have problems
    _title(bd, "nhan_sai.svg", "Chính nhãn của bộ dữ liệu cũng có vấn đề")
    band(bd, "nhan_sai.svg", 3)
    bd.A("nhan_sai.svg", viz.big_number("nhan-trong", 40, 110, m("GtBlankN"), "nhãn gốc nằm trên dòng trống,\nnơi không thể có lỗi",
                                        color=RED, size=56, w=300))
    bd.A("nhan_sai.svg", viz.big_number("nhan-khong-chay", 350, 110, m("GtNotExecutedN"),
                                        "chương trình: không test fail nào\nchạy tới dòng được gán nhãn", color=RED, size=56, w=300))
    bd.A("nhan_sai.svg", P("nhan-la-gi", 660, 104, 270, [
        ("Nhãn là gì", "Dòng lỗi chuẩn bộ dữ liệu ghi cho mỗi chương trình; mọi phương pháp được chấm đúng sai theo nó."),
        ("Vì sao quan trọng", "Nhãn sai thì phương pháp chỉ đúng dòng vẫn bị chấm là sai, và mọi con số công bố bị lệch."),
    ], size=14))
    bd.A("nhan_sai.svg", P("nhan-hau-qua", 40, 300, 610, [
        ("Hệ quả cho kết quả công bố", "Acc@1 42,8% của bài gốc được chấm trên chính bộ nhãn này. Trước khi so sánh, nhóm "
                                       "chuẩn hóa lại nhãn bằng cách chạy test (trang sau).")], size=14))

    # 15. label normalization by execution
    _title(bd, "chuan_hoa.svg", "Chuẩn hóa nhãn bằng thực thi: test quyết định dòng lỗi")
    band(bd, "chuan_hoa.svg", 3)
    q = lambda gid, x, y, w, t, c=NAVY: viz._g(gid, x, y, w, 52, [_r(x, y, w, 52, "#FFFFFF", stroke=c, rx=10, sw=1.8)] +
                                               [_t(x + w / 2, y + 22 + 18 * i, l, size=14, anchor="middle")
                                                for i, l in enumerate(t.split("\n"))])
    bd.A("chuan_hoa.svg", q("q1", 120, 104, 300, "Sửa nhỏ ngay tại nhãn\ncó làm mọi test pass?"))
    bd.A("chuan_hoa.svg", q("q2", 540, 104, 300, "Có test fail nào chạy\ntới dòng nhãn gốc?"))
    bd.A("chuan_hoa.svg", q("q3", 540, 196, 300, "Sửa nhỏ ở dòng lân cận\ncó làm mọi test pass?"))
    leaves = [("Xác nhận", m("GtConfirmedN"), ORANGE, 40), ("Chưa kiểm chứng\n(giữ nhãn gốc)", m("GtUnverifiedN"), GREY, 250),
              ("Dời vị trí", m("GtCorrectedN"), ORANGE, 460), ("Không kiểm chứng\nđược (loại)", m("GtUnverifiableN"), GREY, 670)]
    for k, (lab, n, c, x) in enumerate(leaves):
        bd.A("chuan_hoa.svg", viz._g(f"la-{k}", x, 290, 190, 70, [_r(x, 290, 190, 70, viz.CREAM if c == ORANGE else viz.LIGHT,
                                                                   stroke=c, rx=10, sw=1.8),
                                                                 _t(x + 95, 318, f"{n} nhãn", size=20, weight="bold", anchor="middle",
                                                                    fill=NAVY)] +
                                     [_t(x + 95, 340 + 15 * i, l, size=13, anchor="middle") for i, l in enumerate(lab.split("\n"))]))
    lines = (f'<line x1="200" y1="156" x2="135" y2="290" stroke="{MUTED}" stroke-width="2"/>'
             f'<line x1="420" y1="130" x2="540" y2="130" stroke="{MUTED}" stroke-width="2"/>'
             f'<line x1="620" y1="156" x2="345" y2="290" stroke="{MUTED}" stroke-width="2"/>'
             f'<line x1="760" y1="156" x2="760" y2="196" stroke="{MUTED}" stroke-width="2"/>'
             f'<line x1="620" y1="248" x2="555" y2="290" stroke="{MUTED}" stroke-width="2"/>'
             f'<line x1="760" y1="248" x2="765" y2="290" stroke="{MUTED}" stroke-width="2"/>')
    lab_yn = "".join(_t(x, y, t, size=13, fill=MUTED, weight="bold") for x, y, t in
                     ((150, 230, "có"), (455, 124, "không"), (450, 200, "có"), (768, 182, "không"), (560, 272, "có"),
                      (762, 272, "không")))
    bd.A("chuan_hoa.svg", f'<g id="nhanh" data-pptx-bounds="135 110 680 180">{lines}{lab_yn}</g>')
    bd.A("chuan_hoa.svg", P("ket-qua-chuan-hoa", 40, 380, 890, [
        (f"Bộ nhãn đã chuẩn hóa: {m('GtRepairedN')} chương trình", "LLM chỉ đề xuất các bản sửa nhỏ; dòng nào sửa xong làm mọi "
                                                                  "test pass thì đó là dòng lỗi. Bỏ nhãn không kiểm chứng được "
                                                                  "và vị trí sửa nằm trên dòng trống. Mọi kết quả sau đây báo "
                                                                  "trên cả nhãn gốc và nhãn đã chuẩn hóa.")], size=14))

    # 16. FailLoc: the idea
    _title(bd, "failloc_y_tuong.svg", "Phương pháp FailLoc: hỏi LLM một lần, đưa kèm test fail")
    band(bd, "failloc_y_tuong.svg", 4)
    bd.A("failloc_y_tuong.svg", _t(40, 124, "Phương pháp SemLoc: năm bước", size=17, fill=NAVY, weight="bold"))
    bd.A("failloc_y_tuong.svg", viz.pipeline("semloc-5", 40, 136, ["Viết\nràng buộc", "Chèn\nvào mã", "Chạy\nbộ test",
                                                                    "Chấm\nđiểm", "Vá thử"],
                                             box_w=100, gap=18, box_h=58))
    bd.A("failloc_y_tuong.svg", _note(40, 220, [f"Khoảng {m('CostSemlocTokensK')} nghìn token, {m('CostSemlocCalls')} lượt gọi LLM "
                                                "mỗi chương trình"], size=14, gid="chi-phi-semloc", w=580))
    bd.A("failloc_y_tuong.svg", _t(40, 272, "Phương pháp FailLoc: một bước", size=17, fill=ORANGE, weight="bold"))
    bd.A("failloc_y_tuong.svg", viz.pipeline("failloc-1", 40, 284, ["Mã nguồn có số dòng\n+ lỗi của test fail",
                                                                     "Một lượt\ngọi LLM", "Năm dòng\nnghi nhất"],
                                             accent=1, box_w=196, gap=22, box_h=64))
    bd.A("failloc_y_tuong.svg", _note(40, 370, [f"Khoảng {m('CostLlmTestsTokensK')} nghìn token, {m('CostLlmTestsCalls')} lượt gọi "
                                                "LLM mỗi chương trình"], size=14, gid="chi-phi-failloc", w=580))
    bd.A("failloc_y_tuong.svg", P("vi-sao", 640, 104, 290, [
        ("Vì sao làm vậy", "Khi test fail, lập trình viên thường dán mã và thông báo lỗi cho trợ lý AI rồi hỏi dòng nào sai. "
                           "FailLoc làm đúng việc đó, nhưng cố định prompt để chạy lại được."),
        ("Học từ đâu", "Nghiên cứu công nghiệp cho thấy đưa bằng chứng có sẵn vào prompt giúp LLM trúng hơn."),
        ("Câu hỏi đặt ra", "Năm bước của SemLoc có tốt hơn cách hỏi thẳng này không?"),
    ], size=13))

    # 17. FailLoc on the running example
    _title(bd, "failloc_vd.svg", f"Phương pháp FailLoc trên ví dụ: dòng lỗi {gt} đứng hạng 1")
    band(bd, "failloc_vd.svg", 4)
    pl = va["failloc_prompt"].split("\n")
    keep = [l for l in pl if not (l[:1].isdigit() and ": " in l)] [:2]
    code_lines = [l for l in pl if l[:1].isdigit() and ": " in l and int(l.split(":")[0]) in win]
    tail = pl[pl.index("Failing tests:"):]
    prompt = keep + ["…"] + [short(l) for l in code_lines] + [""] + [short(l) for l in tail if l]
    pbody = [_r(30, 100, 580, 380, viz.LIGHT, stroke=ORANGE, rx=10),
             _t(46, 124, "Prompt gửi cho LLM (rút gọn phần ngoài hàm)", size=14, fill=ORANGE, weight="bold")]
    pbody += [_t(46, 148 + 19.5 * k, l, size=12, family=viz.MONO) for k, l in enumerate(prompt[:17])]
    bd.A("failloc_vd.svg", viz._g("prompt", 30, 100, 580, 380, pbody))
    ans = ", ".join(str(x) for x in va["failloc_top5"])
    bd.A("failloc_vd.svg", P("cau-tra-loi", 630, 100, 300, [
        ("LLM trả về", f"[{ans}]: dòng {va['failloc_top5'][0]} ở hạng 1, đúng dòng lỗi theo nhãn."),
        ("So với SemLoc", f"Trên cùng chương trình, phương pháp SemLoc xếp dòng {va['guess_line']} ở hạng 1 (sai), nhờ điểm "
                          "thưởng."),
        ("Lưu ý", "Một ví dụ chỉ để minh họa. Kết quả trên 200 chương trình ở phần 5."),
    ], size=14))

    # 18. the five compared methods
    _title(bd, "phuong_phap.svg", "Năm phương pháp được so sánh trên cùng điều kiện")
    band(bd, "phuong_phap.svg", 4)
    bd.A("phuong_phap.svg", bd.table("bang-phuong-phap", 40, 108, [190, 360, 160, 170], [
        ["Phương pháp", "Đầu vào cho LLM", "Lượt gọi LLM", "Có chạy test?"],
        ["SBFL (Ochiai)", "không dùng LLM; chỉ độ phủ của test", "0", "có"],
        ["LLM-Direct", "chỉ mã nguồn (chế độ hỏi thẳng\ncủa chính SemLoc)", m("CostLlmDirectCalls"), "không"],
        ["SemLoc", "mã nguồn; ràng buộc được chèn\nvà chạy cùng test", m("CostSemlocCalls"), "có"],
        ["SemLoc−Bonus", "như SemLoc, bỏ điểm thưởng\ncho dòng LLM đoán", m("CostSemlocCalls"), "có"],
        ["FailLoc", "mã nguồn + tên và lỗi của\ntừng test fail", m("CostLlmTestsCalls"), "có (lấy kết quả)"],
    ], highlight_col=None, head_h=40, row_h=52, fs=15,
        note="Lượt gọi LLM: trung bình mỗi chương trình trên tập test với Gemini 3.8 Flash."))

    # 19. design
    _title(bd, "thiet_ke_tn.svg", "Thiết kế: cùng chương trình, cùng mô hình, so trên hai bộ nhãn")
    band(bd, "thiet_ke_tn.svg", 5)
    cols = [("Dữ liệu", ["SemFault-250", "dev: 50 chương trình", "test: 200 chương trình"], GREY),
            ("Phương pháp", [name(mm) for mm in MAIN], NAVY),
            ("Bộ nhãn", ["Nhãn gốc", "Nhãn đã chuẩn hóa", f"({m('GtRepairedN')} chương trình)"], ORANGE),
            ("Lặp, chỉ số", ["3 lần chạy", "Acc@1, Acc@3", "khoảng tin cậy 95%"], GREY)]
    body = []
    for k, (head, its, c) in enumerate(cols):
        x = 40 + k * 222
        body.append(_r(x, 104, 196, 210, "#FFFFFF", stroke=c, rx=12, sw=2))
        body.append(_t(x + 98, 134, head, size=18, fill=c if c != GREY else INK, weight="bold", anchor="middle"))
        body += [_t(x + 98, 172 + 28 * i, it, size=15, anchor="middle", weight="bold" if it == name("llm_tests") else "normal",
                    fill=ORANGE if it == name("llm_tests") else INK) for i, it in enumerate(its)]
        if k:
            body.append(_t(x - 13, 216, "×", size=26, fill=MUTED, anchor="middle"))
    bd.A("thiet_ke_tn.svg", viz._g("luoi-thiet-ke", 40, 104, 862, 210, body))
    bd.A("thiet_ke_tn.svg", P("giai-thich-thiet-ke", 40, 330, 890, [
        ("Công bằng", "Mọi phương pháp có LLM dùng cùng Gemini 3.8 Flash trên cùng 200 chương trình của tập test. Tập dev chỉ "
                      "dùng để chọn tham số, không dùng để báo kết quả."),
        ("Khoảng tin cậy", "Mỗi cấu hình chạy 3 lần. Khoảng tin cậy 95% của mức chênh lệch được tính bằng bootstrap: lấy mẫu "
                           "lại các chương trình nhiều lần để xem chênh lệch dao động trong khoảng nào."),
    ], size=14))

    # 20. main results
    _title(bd, "ket_qua.svg", "Phương pháp FailLoc dẫn đầu ở Acc@1 trên cả hai bộ nhãn")
    band(bd, "ket_qua.svg", 5)
    for k, (g, head) in enumerate((("original", "Nhãn gốc"), ("repaired", "Nhãn đã chuẩn hóa"))):
        x = 20 + k * 300
        bd.A("ket_qua.svg", _t(x + 140, 118, head, size=15, fill=INK, weight="bold"))
        ser = [(name(mm), 100 * float(rq2[(g, mm)]["acc1_mean"]), ORANGE if mm == "llm_tests" else NAVY if mm == "semloc" else GREY)
               for mm in MAIN]
        bd.A("ket_qua.svg", viz.bars(f"bars-{g}", x, 128, 292, 300, ser, vmax=100, label_w=140))
    bd.A("ket_qua.svg", P("doc-ket-qua", 640, 104, 290, [
        ("Cách đọc", "Mỗi thanh là Acc@1: phần trăm chương trình có dòng lỗi ở hạng 1. Tập test, Gemini 3.8 Flash, trung bình "
                     "3 lần chạy."),
        ("So với phương pháp SemLoc", f"Nhãn đã chuẩn hóa: FailLoc hơn {d1} điểm Acc@1 (khoảng tin cậy "
                                      f"{m('RqTwoRepairedAllLlmTestsDAccOneLo')} đến {m('RqTwoRepairedAllLlmTestsDAccOneHi')}); Acc@3 "
                                      f"{a3('repaired', 'llm_tests')}% so với {a3('repaired', 'semloc')}%."),
        ("Phương pháp SBFL", "Gần như bằng 0: đúng như ví dụ ở phần 1."),
    ], size=13))

    # 21. improvement over SemLoc
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    _title(bd, "cai_tien.svg", "So với phương pháp SemLoc: chính xác hơn, rẻ hơn, chặt chẽ hơn")
    band(bd, "cai_tien.svg", 5)
    rows = [("Acc@1, nhãn đã chuẩn hóa", f"{a1('repaired', 'semloc')}%", f"{a1('repaired', 'llm_tests')}%", f"{d1} điểm"),
            ("Acc@3, nhãn đã chuẩn hóa", f"{a3('repaired', 'semloc')}%", f"{a3('repaired', 'llm_tests')}%",
             f"{m('RqTwoRepairedAllLlmTestsDAccThree')} điểm"),
            ("Acc@1, nhãn gốc", f"{a1('original', 'semloc')}%", f"{a1('original', 'llm_tests')}%",
             f"{m('RqTwoOriginalAllLlmTestsDAccOne')} điểm"),
            ("Token mỗi chương trình", f"{m('CostSemlocTokensK')} nghìn", f"{m('CostLlmTestsTokensK')} nghìn",
             f"ít hơn {_p(ratio, 0)} lần"),
            ("Lượt gọi LLM", m("CostSemlocCalls"), m("CostLlmTestsCalls"), "không cần quy trình"),
            ("Nhãn dùng để chấm", f"{m('GtBlankN')} nhãn trống", "chuẩn hóa bằng test", f"{m('GtCorrectedN')} nhãn dời"),
            ("Cách đánh giá", "chạy 1 lần", "3 lần, khoảng tin cậy", "có kiểm định")]
    bd.A("cai_tien.svg", viz.before_after("truoc-sau", 30, 98, 900, rows, row_h=50))
    bd.A("cai_tien.svg", _note(30, 500, ["Cùng 200 chương trình của tập test, cùng Gemini 3.8 Flash, trung bình 3 lần chạy."],
                               size=13, gid="dieu-kien", w=900))

    # 22. progress table
    _title(bd, "tien_do.svg", "Tiến độ: việc đã xong và việc các tuần sau")
    bd.A("tien_do.svg", viz.progress_table("bang-tien-do", 40, 104, 880, PROGRESS, row_h=46))
    bd.A("tien_do.svg", _note(40, 480, ["Đang hoàn thiện: dữ liệu và kết quả đã có, nhóm đang viết và kiểm tra lại để trình "
                                        "bày ở buổi tương ứng."], size=13, gid="chu-thich-tien-do", w=880))


def notes(bd) -> dict:
    """Spoken notes for báo cáo lần 1 (every number is one the page shows)."""
    m = bd._m
    ex = examples()
    va, bo = ex["votes_apportion"], ex["blend_orders"]
    gt = va["label_lines"][0]
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    a1 = lambda g, mm: _p(100 * float(rq2[(g, mm)]["acc1_mean"]))
    share, n_pairs = _guess_rank1_share()
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    d1 = m("RqTwoRepairedAllLlmTestsDAccOne")
    return {
        "slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 1 của đề tài: bằng chứng hay phỏng đoán, "
                    "tái hiện và đánh giá việc định vị lỗi ngữ nghĩa trong mã nguồn bằng mô hình ngôn ngữ lớn.",
        "muc_luc": "Bài trình bày đi theo năm phần thầy yêu cầu. Đầu tiên là cơ sở lý thuyết, rồi phương pháp của bài gốc "
                   "SemLoc, phần nhóm kiểm tra lại bài gốc, cải tiến của nhóm là phương pháp FailLoc, thực nghiệm và kết quả. "
                   "Cuối cùng là tiến độ.",
        "bai_toan": "Bài toán định vị lỗi bắt đầu khi chạy test và thấy có test fail. Đầu vào là mã nguồn và bộ test; đầu ra "
                    "là danh sách các dòng mã xếp từ đáng nghi nhất. Nhóm đo bằng Acc@1, tức phần trăm chương trình có dòng "
                    "lỗi thật đứng hạng 1, và Acc@3 cho 3 dòng đầu. Dòng lỗi thật lấy từ nhãn của bộ dữ liệu.",
        "vi_du": f"Đây là ví dụ đi xuyên suốt bài: hàm {va['program']} trong bộ SemFault-250. Chạy test thì {va['n_pass']} test "
                 f"pass, {va['n_fail']} test fail. Test fail đòi tổng các phần chia bằng tổng ban đầu, nhưng int(v) ở dòng {gt} cắt "
                 "mất phần lẻ. Mã vẫn chạy bình thường nên các công cụ kiểm tra cú pháp hay kiểu không báo gì; đó là lỗi "
                 "ngữ nghĩa.",
        "sbfl_cong_thuc": "Phương pháp kinh điển là SBFL, định vị lỗi dựa trên phổ độ phủ. Với mỗi dòng, ta đếm số test fail và "
                          "số test pass chạy qua nó rồi tính điểm Ochiai theo công thức trên màn hình. Tính tay cho dòng 29 của "
                          "ví dụ được 0,45. Vấn đề là mọi dòng khác cũng được đúng 0,45.",
        "sbfl_mu": "Ma trận này cho thấy lý do. Cột đỏ là test fail duy nhất, và nó chạy qua đúng những dòng mà các test pass "
                   f"cũng chạy qua, kể cả dòng lỗi {gt}. Mọi dòng hòa điểm nên phương pháp SBFL chỉ còn đoán. Trên cả 250 chương "
                   f"trình, nó chỉ đúng ngay hạng 1 ở {m('RqOneSbflOchiaiFairAllAccOne')}%.",
        "lien_quan": "Đây là nội dung 1: bộ từ khóa và ba bài tiêu biểu trong các nghiên cứu nhóm đã đọc. Bài trung tâm là "
                     "SemLoc. Từ EffiHolmes, nhóm lấy ý tưởng so lần chạy bình thường với lần chạy có lỗi; từ nghiên cứu công "
                     "nghiệp, nhóm lấy ý tưởng đưa bằng chứng có sẵn vào prompt, chính là phương pháp FailLoc.",
        "semloc_tong_quan": "Phương pháp SemLoc của bài gốc có năm bước: LLM viết ràng buộc, ràng buộc được chèn vào mã, chạy "
                            "bộ test, chấm điểm từng dòng, rồi vá thử để kiểm chứng. Tác giả báo cáo Acc@1 "
                            f"{m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% và cho rằng độ chính xác đến từ bằng chứng "
                            "thực thi. Ba trang sau đi qua từng bước trên dữ liệu thật.",
        "semloc_rang_buoc": f"Trên ví dụ, LLM đoán dòng lỗi là dòng {va['guess_line']}, trong khi nhãn là dòng {gt}. Nó viết "
                            "bốn ràng buộc, ví dụ tổng các phần chia không vượt quá tổng ban đầu. Các dòng in nghiêng là lệnh "
                            "kiểm tra SemLoc chèn vào mã; khi một test chạy qua mà điều kiện sai thì ràng buộc bị vi phạm.",
        "semloc_diem": f"Ở {va['program']}, cả bốn ràng buộc đều không bị vi phạm, nên mọi điểm bằng 0. Để thấy cơ chế chấm "
                       f"điểm, nhóm dùng chương trình thứ hai là {bo['program']}. Mỗi ràng buộc được đếm số test fail và test "
                       "pass vi phạm, tính Ochiai, rồi nhân hệ số theo vị trí. Dòng lỗi được 1,00, dòng 73 chỉ được 0,60.",
        "semloc_thuong": f"Bước cuối là chỗ quan trọng. Mã nguồn cộng thêm {m('ConstPriorWeight')} điểm cho dòng LLM tự đoán, "
                         "lớn hơn mọi điểm phổ, nên dòng 73 vượt lên hạng 1 với 1,80 dù dòng lỗi có điểm phổ cao nhất. Bước "
                         "vá thử còn xác nhận nhầm dòng 73, và trên cả 250 chương trình nó không làm đổi thứ hạng nào.",
        "cau_hoi": "Từ đó nhóm đặt ba câu hỏi nghiên cứu, là nội dung 2. RQ1 tái hiện và kiểm tra cách đánh giá của bài gốc. "
                   "RQ2 hỏi LLM thật sự cần gì, so phương pháp FailLoc với phương pháp SemLoc. RQ3 kiểm tra độ bền, nhóm sẽ "
                   "trình bày ở lần 2.",
        "overclaim": f"Kết quả RQ1 đầu tiên: trong {n_pairs} lần chạy có dòng đoán, hạng 1 của SemLoc là dòng LLM đoán ở "
                     f"{_p(100 * share, 0)}% số lần. Bỏ điểm thưởng thì Acc@1 giảm {m('RqTwoRepairedAllSemlocNoPriorDAccOne').lstrip('−-')} "
                     "điểm. Điểm thưởng tự nó chỉ là lựa chọn thiết kế; chỗ overclaim là bài báo quy độ chính xác cho bằng "
                     "chứng thực thi mà không nói gì về điểm thưởng.",
        "nhan_sai": f"Kết quả thứ hai: chính nhãn của bộ dữ liệu có vấn đề. {m('GtBlankN')} nhãn nằm trên dòng trống, và ở "
                    f"{m('GtNotExecutedN')} chương trình không test fail nào chạy tới dòng được gán nhãn. Con số 42,8% của bài gốc "
                    "được chấm trên chính bộ nhãn này.",
        "chuan_hoa": "Nhóm chuẩn hóa nhãn bằng thực thi. Nếu sửa nhỏ ngay tại nhãn làm mọi test pass thì nhãn được xác nhận; "
                     "nếu không test fail nào chạy tới nhãn, nhóm thử các dòng lân cận. LLM chỉ đề xuất bản sửa, test quyết "
                     f"định. Kết quả là bộ nhãn đã chuẩn hóa gồm {m('GtRepairedN')} chương trình.",
        "failloc_y_tuong": "Cải tiến của nhóm là phương pháp FailLoc. Thay vì năm bước, FailLoc hỏi LLM một lần, đưa kèm mã "
                           "nguồn đánh số dòng cùng tên và thông báo lỗi của các test fail, giống cách lập trình viên vẫn hỏi "
                           f"trợ lý AI. Nó tốn khoảng {m('CostLlmTestsTokensK')} nghìn token mỗi chương trình, so với "
                           f"{m('CostSemlocTokensK')} nghìn của SemLoc.",
        "failloc_vd": f"Đây là prompt thật FailLoc gửi cho ví dụ {va['program']}. LLM trả về năm dòng, dòng {va['failloc_top5'][0]} "
                      f"đứng đầu, đúng dòng lỗi. Trên cùng chương trình, SemLoc xếp dòng {va['guess_line']} ở hạng 1 vì điểm "
                      "thưởng. Đây chỉ là một ví dụ, kết quả trên 200 chương trình ở phần sau.",
        "phuong_phap": "Nhóm so năm phương pháp. SBFL không dùng LLM; LLM-Direct là chế độ hỏi thẳng của chính SemLoc, chỉ có "
                       "mã nguồn; SemLoc và SemLoc bỏ điểm thưởng; và FailLoc. Mọi phương pháp có LLM dùng cùng một mô hình.",
        "thiet_ke_tn": "Để so sánh công bằng, mọi phương pháp chạy trên cùng 200 chương trình của tập test với Gemini 3.8 Flash. "
                    "Mỗi cấu hình chạy 3 lần, kết quả báo trên cả nhãn gốc và nhãn đã chuẩn hóa, kèm khoảng tin cậy 95% tính "
                    "bằng bootstrap.",
        "ket_qua": f"Đây là kết quả chính. FailLoc đứng đầu ở Acc@1 trên cả hai bộ nhãn. Trên nhãn đã chuẩn hóa, FailLoc đạt "
                   f"{a1('repaired', 'llm_tests')}%, SemLoc {a1('repaired', 'semloc')}%, hơn {d1} điểm và khoảng tin cậy không "
                   "chạm 0.",
        "cai_tien": f"Gói lại những gì nhóm làm tốt hơn phương pháp SemLoc trên cùng điều kiện. FailLoc hơn {d1} điểm Acc@1 và "
                    f"{m('RqTwoRepairedAllLlmTestsDAccThree')} điểm Acc@3 trên nhãn đã chuẩn hóa, vẫn hơn trên nhãn gốc, và dùng "
                    f"ít token hơn khoảng {_p(ratio, 0)} lần. Về cách đánh giá, nhóm chấm trên nhãn đã chuẩn hóa, chạy ba lần "
                    "và báo khoảng tin cậy.",
        "tien_do": "Về tiến độ, nội dung 1 và nội dung 2 đã xong. Rà soát nhãn, độ bền, ablation, đóng góp và triết lý khoa học "
                   "đang hoàn thiện, trình bày ở lần 2 ngày 25 đến 26/11. Phân tích thất bại để dành cho buổi bảo vệ, còn "
                   "bài báo arXiv bản cuối làm từ 26/11 đến 10/12.",
        "slide_30": "Nhóm xin cảm ơn thầy và các bạn đã lắng nghe, và rất mong nhận được câu hỏi và góp ý.",
    }

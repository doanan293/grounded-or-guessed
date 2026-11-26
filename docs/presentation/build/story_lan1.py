"""Báo cáo lần 1 (15 trang): the first week, studying the problem and reproducing SemLoc.

Cơ sở lý thuyết (problem, SBFL, related work, SemLoc step by step), the four research questions, the first RQ1 results
(the bonus decides rank 1; the labels have problems), then the progress table. Many pages built here are reused by
lần 2 and the defence (chuan_hoa, failloc_*, phuong_phap, thiet_ke_tn, ket_qua, cai_tien): a page's deck is set by
the LAN*/BAOVE lists, not by the module that builds it. votes_apportion (example 1) runs through SBFL and FailLoc;
blend_orders (example 2) runs through SemLoc's steps (on votes_apportion no constraint is violated, every score is 0).
"""
import json

import viz
from story_common import (MAIN, ROOT, _bonus_rows, _card, _csv, _guess_rank1_share, _note, _title, _unbold, band,
                          examples, name, progress_rows)
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

LAN1 = [("slide_01.svg", 1), ("muc_luc.svg", 22),
        ("bai_toan.svg", 22), ("vi_du.svg", 22), ("sbfl_cong_thuc.svg", 22), ("sbfl_mu.svg", 22), ("lien_quan.svg", 22),
        ("semloc_tong_quan.svg", 22), ("semloc_rang_buoc.svg", 22), ("semloc_diem.svg", 22),
        ("cau_hoi.svg", 20), ("nhan_sai.svg", 22), ("overclaim.svg", 22),
        ("tien_do.svg", 22), ("slide_30.svg", 30)]
KEYWORDS = ["định vị lỗi (fault localization)", "định vị lỗi dựa trên phổ (SBFL)", "lỗi ngữ nghĩa (semantic fault)",
            "ràng buộc ngữ nghĩa (semantic constraint)", "phổ vi phạm (violation spectrum)",
            "kiểm chứng phản thực tế (counterfactual)"]


def _code(ex: dict) -> dict:
    return {c["no"]: c["text"] for c in ex["code_lines"]}


def _ind(t: str) -> int:
    return len(t) - len(t.lstrip())


def _block_end(code: dict, head: int) -> int:
    """Last non-blank line of the block opened at `head` (by indentation)."""
    end = head
    for n in sorted(k for k in code if k > head):
        t = code[n]
        if t.strip() and _ind(t) <= _ind(code[head]):
            break
        if t.strip():
            end = n
    return end


def _loop(code: dict):
    return next((n for n, t in sorted(code.items()) if t.strip().startswith(("for ", "while "))), None)


def scored_line(ex: dict, c: dict) -> str:
    """The line(s) SemLoc credits a constraint's score to (spectrum.find_anchor_lines): a line constraint its line, an
    after-branch check the if line, a loop-tail check the loop body's last statement (an if/elif/else counts as one),
    a return check every return line."""
    code, r = _code(ex), c["region"]
    if r in ("LINE", "AFTER_BRANCH"):
        return str(c["anchor_line"])
    if r == "LOOP_TAIL":
        loop = _loop(code)
        body = [n for n in sorted(code) if loop < n <= _block_end(code, loop) and code[n].strip()]
        top = min(_ind(code[n]) for n in body)
        return str([n for n in body if _ind(code[n]) == top
                    and not code[n].strip().startswith(("elif", "else", "except", "finally"))][-1])
    return ", ".join(str(n) for n, t in sorted(code.items()) if t.strip().startswith("return"))


def inserted_checks(ex: dict) -> dict:
    """Where each constraint is checked in the code window: a line constraint after its line, an after-branch check at the end of the branch, a loop-tail check at the end of
    the loop body, a check on the value about to be returned before the first return, a check on every return at it."""
    code = _code(ex)
    ret = next(n for n, t in sorted(code.items()) if t.strip().startswith("return"))
    loop = _loop(code)
    checks: dict = {}
    for c in ex["constraints"]:
        r = c["region"]
        at = (c["anchor_line"] if r == "LINE" else _block_end(code, c["anchor_line"]) if r == "AFTER_BRANCH"
              else _block_end(code, loop) if r == "LOOP_TAIL" else ret - 1 if r == "BEFORE_USE" else ret)
        if at in code:
            expr = c["expr"].replace("__1", "").replace("__cbfl_result", "ret")
            checks.setdefault(at, {}).setdefault(expr, []).append(c["id"])
    return {at: "; ".join(f"# kiểm tra {', '.join(ids)}: {e}" for e, ids in d.items()) for at, d in checks.items()}


def _cut(t: str, n: int) -> str:
    """Shorten code at a word boundary with an ellipsis, never in the middle of a name."""
    if len(t) <= n:
        return t
    cut = t[:n].rsplit(" ", 1)[0] if " " in t[:n] else t[:n]
    return cut.rstrip() + " …"


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
    items = [("1", "Cơ sở lý thuyết", "Bài toán, phương pháp SBFL, nghiên cứu liên quan, phương pháp SemLoc"),
             ("2", "Phương pháp giải quyết", "Bốn câu hỏi nghiên cứu; tái hiện SemLoc"),
             ("5", "Kết quả", "Điểm thưởng quyết định hạng 1; nhãn của bộ dữ liệu có vấn đề"),
             ("", "Tiến độ", "Việc đã xong và việc của lần 2, lần 3")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 112 + i * 62
        body.append(_r(60, y, 840, 52, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else LAVENDER, rx=10, sw=1.2))
        body.append(_t(92, y + 34, k or "•", size=24, fill=NAVY, weight="bold", anchor="middle"))
        body.append(_t(130, y + 33, head, size=19, fill=NAVY, weight="bold"))
        body.append(_t(370, y + 33, desc, size=14))
    bd.A("muc_luc.svg", viz._g("muc-luc", 60, 112, 840, 362, body))

    # 3. the problem
    _title(bd, "bai_toan.svg", "Định vị lỗi: từ một test fail ra danh sách dòng đáng nghi")
    band(bd, "bai_toan.svg", 1)
    bd.A("bai_toan.svg", viz.pipeline("bai-toan-luong", 40, 112, ["Đầu vào\nmã nguồn + bộ test\n(có test fail)",
                                                                   "Phương pháp\nđịnh vị lỗi", "Đầu ra\ncác dòng xếp hạng\ntừ nghi ngờ nhất"],
                                      accent=1, box_w=250, gap=45, box_h=86))
    rank_body = [_r(640, 214, 240, 150, "#FFFFFF", stroke=LAVENDER, rx=8)]
    for i, (ln, ok) in enumerate(((29, True), (25, False), (26, False))):
        rank_body.append(_t(656, 244 + 34 * i, f"Hạng {i + 1}: dòng {ln}", size=16, weight="bold" if ok else "normal",
                            fill=ORANGE if ok else INK))
    rank_body.append(_t(656, 350, "Ví dụ: dòng lỗi 29 ở hạng 1", size=13, fill=MUTED))
    bd.A("bai_toan.svg", viz._g("vi-du-xep-hang", 640, 214, 240, 150, rank_body))
    bd.A("bai_toan.svg", P("acc-k", 40, 214, 570, [
        ("Đo bằng Acc@k", "Acc@1: tỉ lệ chương trình có dòng lỗi ở hạng 1. Acc@3: dòng lỗi nằm trong 3 dòng đầu."),
    ], size=16, h=150))

    # 4. the running example
    _title(bd, "vi_du.svg", f"Ví dụ 1: hàm {va['program']} và một test fail")
    band(bd, "vi_du.svg", 1)
    short = lambda t: t if len(t) <= 46 else t[:44].rstrip() + " …"
    bd.A("vi_du.svg", viz.code_block("ma-vi-du", 40, 108, [short(vcode[n]) for n in win], first_no=win[0], fs=15, width=540,
                                     highlight={gt}, mark={gt: "dòng lỗi theo nhãn"}))
    bd.A("vi_du.svg", P("test-ket-qua", 40, 330, 540, [
        (f"{va['n_pass']} test pass, {va['n_fail']} test fail", "Test fail đòi tổng các phần chia bằng tổng ban đầu; int(v) ở "
                              "dòng 29 cắt mất phần lẻ.")], size=15,
                       head_color=RED, h=120))
    bd.A("vi_du.svg", P("loi-ngu-nghia", 600, 108, 320, [
        ("Lỗi ngữ nghĩa", "Mã chạy bình thường nhưng tính ra giá trị sai."),
        ("SemFault-250 (Yang 2026)", "250 chương trình Python của bài gốc SemLoc, mỗi chương trình một lỗi, khoảng mười test."),
    ], size=15, h=342))

    # 5. SBFL: the formula, computed by hand on line 29
    _title(bd, "sbfl_cong_thuc.svg", "Phương pháp SBFL nghi những dòng mà test fail hay chạy qua")
    band(bd, "sbfl_cong_thuc.svg", 1)
    bd.A("sbfl_cong_thuc.svg", viz.formula("ochiai", 40, 110, 540, [
        "Ochiai(dòng) = ef / √( F × (ef + ep) )",
        "ef: số test fail chạy qua dòng đó",
        "ep: số test pass chạy qua dòng đó",
        "F: tổng số test fail của chương trình"], size=18))
    n_all = va["n_fail"] + va["n_pass"]
    bd.A("sbfl_cong_thuc.svg", P("tinh-tay", 40, 260, 540, [
        (f"Tính tay cho dòng {gt} của ví dụ 1", f"Cả {n_all} test đều chạy qua dòng {gt}: ef = {va['n_fail']}, ep = {va['n_pass']}, "
                                             f"F = {va['n_fail']}. Ochiai = 1 / √(1 × 5) = 0,45."),
        ("", f"Các dòng khác trong hàm cũng được cả {n_all} test chạy qua nên cũng được 0,45, và không dòng nào nổi lên."),
    ], size=15))
    bd.A("sbfl_cong_thuc.svg", P("sbfl-la-gi", 600, 110, 320, [
        ("Phương pháp SBFL", "Định vị lỗi dựa trên phổ độ phủ (spectrum-based fault localization): chạy bộ test, ghi lại test "
                             "nào chạy qua dòng nào, rồi chấm điểm từng dòng. Dòng gây lỗi thường nằm trên đường chạy của "
                             "test fail và ít nằm trên đường chạy của test pass."),
        ("", "Với lỗi ngữ nghĩa, test fail và test pass thường đi qua đúng cùng các dòng, và cách chấm này hết tác dụng."),
    ], size=14))

    # 6. SBFL on the example: everything ties
    rows = [n for n in win[:-1] if vcode[n].strip()]
    tests = json.loads((ROOT / "data" / "fig_example.json").read_text())["tests"]
    cols = [f"t{j + 1}" for j in range(len(tests))]
    cells = {(i, j) for i, n in enumerate(rows) for j, t in enumerate(tests) if n in t["lines"]}
    fail_cols = {j: RED for j, t in enumerate(tests) if not t["passed"]}
    _title(bd, "sbfl_mu.svg", "Phương pháp SBFL (Abreu 2009) trên ví dụ 1: mọi dòng hòa điểm")
    band(bd, "sbfl_mu.svg", 1)
    bd.A("sbfl_mu.svg", viz.matrix("ma-tran-phu", 30, 104, [f"{n}  {_cut(vcode[n].strip(), 20)}" for n in rows], cols, cells,
                                   row_mark={rows.index(gt): RED}, label_w=280, cell_w=46, row_h=34,
                                   col_colors={**{j: NAVY for j in range(len(cols))}, **fail_cols},
                                   col_sub=["fail" if j in fail_cols else "pass" for j in range(len(cols))]))
    bd.A("sbfl_mu.svg", P("sbfl-doc", 580, 104, 340, [
        ("", f"Chấm tròn: test chạy qua dòng. Cột đỏ: test fail. Hàng tô màu: dòng lỗi {gt}."),
        ("", "Mọi test chạy qua mọi dòng nên dòng nào cũng cùng điểm: phương pháp SBFL chỉ còn đoán."),
    ], size=15, h=252))
    bd.A("sbfl_mu.svg", viz.big_number("sbfl-acc", 580, 380, f"{m('RqOneSbflOchiaiFairAllAccOne')}%",
                                       "Acc@1 của phương pháp SBFL\ntrên cả 250 chương trình", color=RED, size=44, w=340))

    # 7. related work: keywords + three representative studies [content 1]
    _title(bd, "lien_quan.svg", "Nghiên cứu liên quan: từ khóa tìm kiếm và ba bài tiêu biểu")
    band(bd, "lien_quan.svg", 1, content=1)
    chips, cx = [], 40
    for k in KEYWORDS[:3]:
        w = viz.text_w(k, 12) + 24
        chips += [_r(cx, 100, w, 26, viz.LIGHT, rx=13), _t(cx + w / 2, 118, k, size=12, anchor="middle")]
        cx += w + 8
    bd.A("lien_quan.svg", viz._g("tu-khoa", 40, 100, cx - 40, 26, chips))
    cards = [("SemLoc (2026)", [("Cách làm", "LLM viết ràng buộc, chạy test lấy phổ vi phạm."),
                                 ("Kết quả", f"Acc@1 {m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% trên SemFault-250."),
                                 ("Nhóm áp dụng", "chạy lại và kiểm tra từng con số (RQ1).")]),
             ("EffiHolmes (2026)", [("Cách làm", "so lần chạy nhanh với lần chạy chậm để tìm hàm gây chậm."),
                                     ("Kết quả", "140 lỗi hiệu năng thật."),
                                     ("Nhóm áp dụng", "so test pass với test fail.")]),
             ("Sự cố + LLM (2026)", [("Cách làm", "đưa stack trace của sự cố vào prompt."),
                                      ("Kết quả", "38 lỗi thật, đúng chỗ lỗi ở 71%."),
                                      ("Nhóm áp dụng", "đưa lỗi của test fail vào prompt: phương pháp FailLoc.")])]
    for k, (head, blocks) in enumerate(cards):
        bd.A("lien_quan.svg", _t(40 + k * 300, 152, head, size=18, fill=ORANGE, weight="bold"))
        bd.A("lien_quan.svg", P(f"bai-{k}", 40 + k * 300, 162, 284, [(a, b[0].upper() + b[1:]) for a, b in blocks], size=14,
                                h=300))

    # 8. SemLoc overview
    _title(bd, "semloc_tong_quan.svg", "Phương pháp SemLoc: LLM viết ràng buộc, chạy test để kiểm chứng")
    band(bd, "semloc_tong_quan.svg", 1)
    steps = ["1. LLM viết\nràng buộc", "2. Chèn\nvào mã", "3. Chạy\nbộ test", "4. Chấm điểm\ntừng dòng", "5. LLM vá thử,\nchạy lại test"]
    bd.A("semloc_tong_quan.svg", viz.pipeline("quy-trinh-semloc", 40, 108, steps, box_w=158, gap=22, box_h=72))
    expl = ["Điều kiện phải đúng\nnếu mã chạy đúng", "Mỗi ràng buộc thành\nmột lệnh kiểm tra", "Ghi ràng buộc nào bị\nvi phạm trong test nào",
            "Ràng buộc vi phạm ở\ntest fail thì dòng\ncủa nó đáng nghi", "Vá dòng nghi; test\npass lại thì xác nhận"]
    body = []
    for k, e in enumerate(expl):
        for r_, line in enumerate(e.split("\n")):
            body.append(_t(40 + k * 180 + 79, 204 + 18 * r_, line, size=13, fill=MUTED, anchor="middle"))
    bd.A("semloc_tong_quan.svg", viz._g("giai-thich-buoc", 40, 190, 880, 70, body))
    bd.A("semloc_tong_quan.svg", viz.big_number("acc-cong-bo", 48, 290, f"{m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}%",
                                                "Acc@1 phương pháp SemLoc\ncông bố trên SemFault-250\n(Claude Sonnet 4.6)",
                                                size=56, w=300))
    bd.A("semloc_tong_quan.svg", P("loi-hua", 370, 285, 550, [
        ("Bài báo SemLoc (Yang 2026) viết", "LLM chỉ đề xuất, kết quả chạy test quyết định thứ hạng."),
    ], size=16, h=170))

    # 9. SemLoc steps 1-2 on blend_orders (example 2): the function, the bug, the constraints and where they are checked
    bcode = {c["no"]: c["text"] for c in bo["code_lines"]}
    bl = bo["label_lines"][0]
    bwin = list(range(55, 77))
    _title(bd, "semloc_rang_buoc.svg", f"Bước 1 và 2 trên ví dụ 2: LLM đoán dòng {bo['guess_line']}, viết bốn ràng buộc")
    band(bd, "semloc_rang_buoc.svg", 1)
    blines = [_cut(bcode[n][4:], 72) for n in bwin]  # drop the function body's indent; only the log line is long
    bd.A("semloc_rang_buoc.svg", viz.code_block("ma-co-kiem-tra", 30, 100, blines, first_no=bwin[0], fs=10.5, width=640,
                                                highlight={bl, bl + 1}, inserted=inserted_checks(bo)))
    bd.A("semloc_rang_buoc.svg", P("rang-buoc-la-gi", 685, 100, 245, [
        (f"Ví dụ 2: {bo['program']}", f"Gộp hai danh sách đã sắp xếp. Lỗi ở dòng {bl}–{bl + 1}: [1, 5] và [3, 5] ra "
                                      "[1, 3, 5]."),
        ("Ràng buộc", "Điều kiện phải đúng nếu mã chạy đúng. Dòng in nghiêng là lệnh kiểm tra SemLoc chèn vào."),
        ("", f"LLM đoán dòng lỗi là {bo['guess_line']}; nhãn ghi dòng {bl}."),
    ], size=13, h=400))

    # 10. SemLoc steps 3-4 on blend_orders: violations, Ochiai, region weight, line score
    _title(bd, "semloc_diem.svg", "Bước 3 và 4 trên ví dụ 2: đếm vi phạm rồi chấm điểm từng dòng")
    band(bd, "semloc_diem.svg", 1)
    kind = {"LINE": "một dòng", "AFTER_BRANCH": "cuối if", "LOOP_TAIL": "cuối vòng lặp", "ANY_RETURN": "mọi return"}
    where = lambda c: f"{kind.get(c['region'], c['region'])} → {scored_line(bo, c)}"
    rows_ct = [{"id": c["id"], "where": where(c), "expr": _cut(c["expr"].replace("__1", "").replace("__cbfl_result", "ret"), 30), "fail": c["ef"], "pass": c["ep"],
                "ochiai": c["ochiai"], "weight": c["weight"], "score": c["ochiai"] * c["weight"]} for c in bo["constraints"]]
    bd.A("semloc_diem.svg", viz.constraint_table("bang-rang-buoc", 30, 104, 900, rows_ct))
    bd.A("semloc_diem.svg", viz.formula("he-so", 30, 300, 430, [
        "Điểm dòng = Ochiai × hệ số vùng",
        "cuối nhánh if: 1,0 · cuối vòng lặp: 0,9",
        "một dòng: 0,6 · mọi return: 0,3"], size=16))
    bl = bo["label_lines"][0]
    bd.A("semloc_diem.svg", P("doc-bang", 480, 300, 450, [
        ("Đọc bảng", "Mỗi hàng là một ràng buộc; vi phạm = số test làm điều kiện sai."),
        ("", f"C1 và C2 cùng Ochiai 1,00, chỉ khác hệ số: C2 ở câu if dòng {bl} được 1,0, C1 ở dòng đoán "
             f"{bo['guess_line']} chỉ được 0,6."),
    ], size=14, h=175))

    # 12. research questions [content 2]
    bd.E("cau_hoi.svg", [
        ("Popular programming languages", "Bốn câu hỏi nghiên cứu: bằng chứng hay phỏng đoán?"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Kết quả công bố của SemLoc có", "tái hiện được không, và còn giữ", "khi chấm trên nhãn chuẩn hóa?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["Một prompt có test fail (FailLoc)", "có định vị đúng ít nhất bằng",
                                                     "SemLoc không, rẻ hơn bao nhiêu?"]),
        ("Earth", "RQ3"), ("Earth is the third", ["FailLoc thắng nhờ thông tin gì,", "và thêm phức tạp có giúp không?"]),
        ("Saturn", "RQ4"), ("Saturn is a gas giant", ["Kết luận có còn đúng trên lỗi thật,", "mã đổi tên và mô hình khác?"]),
    ])
    _unbold(bd, "cau_hoi.svg", "Một prompt có test fail")
    band(bd, "cau_hoi.svg", 2, content=2)

    # 13. the bonus decides rank 1, and the paper does not say so (overclaim)
    share, n_pairs = _guess_rank1_share()
    _title(bd, "overclaim.svg", f"Điểm thưởng {m('ConstPriorWeight')} đưa dòng LLM đoán lên hạng 1; bài báo không nói")
    band(bd, "overclaim.svg", 5, rq="RQ1")
    rs = sorted(bo["line_scores"], key=lambda r: r["rank"])[:5]
    ser = []
    for r in sorted(rs, key=lambda r: r["line"]):
        isg, isl = r["line"] == bo["guess_line"], r["line"] in bo["label_lines"]
        lab = f"dòng {r['line']}" + (" (nhãn)" if isl else "") + (" (đoán)" if isg else "")
        ser.append((lab, r["spectrum"] + r["bonus"], ORANGE if isg else NAVY if isl else GREY, r["spectrum"] if isg else 0))
    bd.A("overclaim.svg", viz.bars("diem-cuoi", 30, 100, 520, 200, ser, vmax=2.0, unit="", label_w=170, nd=2))
    bd.A("overclaim.svg", _note(30, 322, [f"Chương trình {bo['program']}, lượt chạy 1, Gemini 3.8 Flash.",
                                          "Xám: điểm phổ; cam: điểm thưởng."], size=12, gid="nguon-thuong", w=520))
    bd.A("overclaim.svg", viz.big_number("ty-le", 30, 362, f"{_p(100 * share, 0)}%",
                                         f"trong {n_pairs} lượt (chương trình × lần chạy),\nhạng 1 của SemLoc là dòng LLM đoán",
                                         color=ORANGE, size=44, w=520))
    g0 = "original" if bd.EARLY() else "repaired"  # lần 1: the labels are not normalized yet
    sem = _p(100 * float(rq2[(g0, "semloc")]["acc1_mean"]))
    nob = _p(100 * float(rq2[(g0, "semloc_no_prior")]["acc1_mean"]))
    bd.A("overclaim.svg", P("thuong-overclaim", 580, 100, 350, [
        ("Điểm thưởng", f"Mã nguồn cộng {m('ConstPriorWeight')} cho dòng LLM đoán, trong khi điểm phổ tối đa là 1: dòng "
                        "đoán luôn đứng hạng 1."),
        ("", f"SemLoc−Bonus (không cộng thưởng): Acc@1 giảm từ {sem}% xuống {nob}%"
             + (" (nhãn gốc)." if bd.EARLY() else ".")),
        ("Overclaim", "Bài báo quy độ chính xác cho bằng chứng thực thi và không nhắc điểm thưởng."),
    ], size=14, h=400))

    # 14. the labels have problems
    _title(bd, "nhan_sai.svg", "Chính nhãn của bộ dữ liệu cũng có vấn đề")
    band(bd, "nhan_sai.svg", 2)
    bd.A("nhan_sai.svg", viz.big_number("nhan-trong", 40, 110, m("GtBlankN"), "nhãn gốc nằm trên dòng trống,\nnơi không thể có lỗi",
                                        color=RED, size=56, w=300))
    bd.A("nhan_sai.svg", viz.big_number("nhan-khong-chay", 350, 110, m("GtNotExecutedN"),
                                        "chương trình: không test fail nào\nchạy tới dòng được gán nhãn", color=RED, size=56, w=300))
    bd.A("nhan_sai.svg", P("nhan-la-gi", 660, 104, 270, [
        ("Nhãn", "Dòng lỗi bộ dữ liệu ghi cho mỗi chương trình, dùng để chấm mọi phương pháp."),
        ("", "Nhãn sai thì chỉ đúng dòng lỗi vẫn bị chấm sai."),
    ], size=15, h=290))
    # one real case under each number: (program, first line, last line, original label, verified label, explanation)
    progs = ROOT / "third_party" / "semloc" / "benchmark" / "programs"
    cases = [("download_rate", 73, 75, 74, 75, []),
             ("estimate_temperature", 68, 70, 69, 68, ["Điều kiện dòng 68 bị đảo. Test fail gọi",
                                                        "clamp=True nên bỏ qua dòng 69, dòng",
                                                        "được gán nhãn."])]
    for k, (prog, lo, hi, orig, fixed, why) in enumerate(cases):
        src = (progs / f"{prog}.py").read_text().split("\n")
        x0 = 40 + 310 * k
        bd.A("nhan_sai.svg", _t(x0, 252, f"Ví dụ: {prog}", size=13, fill=NAVY, weight="bold"))
        bd.A("nhan_sai.svg", viz.code_block(f"vd-nhan-{k}", x0, 260, [_cut(src[n - 1][4:], 28) for n in range(lo, hi + 1)], first_no=lo,
                                            fs=10, width=300, highlight={fixed}, mark={orig: "nhãn gốc", fixed: "lỗi thật"}))
        if why:
            bd.A("nhan_sai.svg", _note(x0, 334, why, size=11, gid=f"vd-nhan-chu-{k}", w=300))
    bd.A("nhan_sai.svg", P("nhan-hau-qua", 40, 410, 600, [
        ("", "Việc tiếp theo (lần 2): chuẩn hóa lại nhãn bằng cách chạy test." if bd.EARLY()
         else "Vì vậy trước khi so sánh, nhóm chuẩn hóa lại nhãn bằng cách chạy test.")], size=15, h=66))

    # 15. label normalization by execution
    _title(bd, "chuan_hoa.svg", "Chuẩn hóa nhãn: dòng nào sửa xong làm test pass là dòng lỗi")
    band(bd, "chuan_hoa.svg", 2)
    # a flowchart read top-down: each question on the left, "có" goes right to its outcome, "không" goes down
    qs = ["Sửa nhỏ ngay tại nhãn có làm mọi test pass?", "Có test fail nào chạy tới dòng nhãn gốc?",
          "Sửa nhỏ ở dòng lân cận có làm mọi test pass?"]
    leaves = [(m("GtConfirmedN"), "Xác nhận nhãn gốc", ORANGE), (m("GtUnverifiedN"), "Chưa kiểm chứng, giữ nhãn gốc", GREY),
              (m("GtCorrectedN"), "Dời nhãn sang dòng lân cận", ORANGE), (m("GtUnverifiableN"), "Không kiểm chứng được, loại", GREY)]
    QX, QW, LX, LW, BH, STEP, Y0 = 40, 370, 560, 370, 44, 70, 104
    body = []
    for i, q_ in enumerate(qs):
        y = Y0 + STEP * i
        body += [_r(QX, y, QW, BH, "#FFFFFF", stroke=NAVY, rx=8, sw=1.6), _t(QX + 16, y + 28, q_, size=15)]
        body += [viz._arrow(QX + QW, y + BH / 2, LX - 2, y + BH / 2), _t((QX + QW + LX) / 2, y + BH / 2 - 8, "có", size=13,
                                                                        fill=MUTED, weight="bold", anchor="middle")]
        if i < len(qs) - 1:
            body += [viz._arrow(QX + 40, y + BH, QX + 40, y + STEP - 2), _t(QX + 52, y + BH + 17, "không", size=12, fill=MUTED,
                                                                            weight="bold")]
    y_last = Y0 + STEP * 3
    body += [f'<line x1="{QX + 40}" y1="{Y0 + STEP * 2 + BH}" x2="{QX + 40}" y2="{y_last + BH / 2}" stroke="{MUTED}" stroke-width="2"/>',
             viz._arrow(QX + 40, y_last + BH / 2, LX - 2, y_last + BH / 2),
             _t(QX + 52, Y0 + STEP * 2 + BH + 17, "không", size=12, fill=MUTED, weight="bold")]
    for i, (n, lab, c) in enumerate(leaves):
        y = Y0 + STEP * i
        body += [_r(LX, y, LW, BH, viz.CREAM if c == ORANGE else viz.LIGHT, stroke=c, rx=8, sw=1.6),
                 _t(LX + 16, y + 29, f"{n} nhãn", size=18, weight="bold", fill=NAVY), _t(LX + 120, y + 28, lab, size=15)]
    bd.A("chuan_hoa.svg", viz._g("cay-chuan-hoa", QX, Y0, LX + LW - QX, STEP * 3 + BH, body))
    bd.A("chuan_hoa.svg", P("ket-qua-chuan-hoa", 40, 382, 890, [
        (f"Bộ nhãn đã chuẩn hóa còn {m('GtRepairedN')} chương trình", "LLM chỉ đề xuất bản sửa nhỏ; test quyết định "
                                                                     "dòng lỗi.")],
                                     size=15))

    # 16. FailLoc: the idea
    _title(bd, "failloc_y_tuong.svg", "Phương pháp FailLoc hỏi LLM đúng một lần, kèm thông tin test fail")
    band(bd, "failloc_y_tuong.svg", 3)
    bd.A("failloc_y_tuong.svg", _t(40, 124, "Phương pháp SemLoc: năm bước", size=17, fill=NAVY, weight="bold"))
    bd.A("failloc_y_tuong.svg", viz.pipeline("semloc-5", 40, 136, ["Viết\nràng buộc", "Chèn\nvào mã", "Chạy\nbộ test",
                                                                    "Chấm\nđiểm", "Vá thử"],
                                             box_w=100, gap=18, box_h=58))
    bd.A("failloc_y_tuong.svg", _note(40, 220, [f"Khoảng {m('CostSemlocTokensK')} nghìn token, {m('CostSemlocCalls')} lượt gọi LLM "
                                                "mỗi chương trình"], size=14, gid="chi-phi-semloc", w=580))
    bd.A("failloc_y_tuong.svg", _t(40, 272, "Phương pháp FailLoc: một bước", size=17, fill=ORANGE, weight="bold"))
    bd.A("failloc_y_tuong.svg", viz.pipeline("failloc-1", 40, 284, ["Mã nguồn có số dòng\n+ lỗi của test fail",
                                                                     "Một lượt\ngọi LLM", "Năm dòng\nnghi nhất"],
                                             accent=1, box_w=184, gap=18, box_h=64))
    bd.A("failloc_y_tuong.svg", _note(40, 370, [f"Khoảng {m('CostLlmTestsTokensK')} nghìn token, {m('CostLlmTestsCalls')} lượt gọi "
                                                "LLM mỗi chương trình"], size=14, gid="chi-phi-failloc", w=580))
    bd.A("failloc_y_tuong.svg", P("vi-sao", 650, 104, 280, [
        ("", "Giống lập trình viên dán mã và thông báo lỗi cho trợ lý AI rồi hỏi dòng nào sai."),
        ("", "Câu hỏi: năm bước của SemLoc có tốt hơn cách hỏi thẳng này không?"),
    ], size=15, h=290))

    # 17. FailLoc on the running example
    _title(bd, "failloc_vd.svg", f"Trên ví dụ 1, phương pháp FailLoc xếp dòng lỗi {gt} ở hạng 1")
    band(bd, "failloc_vd.svg", 3)
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
        ("LLM trả về", f"[{ans}]: dòng {va['failloc_top5'][0]} đứng hạng 1, đúng dòng lỗi."),
        ("", f"SemLoc xếp dòng {va['guess_line']} (dòng LLM đoán) ở hạng 1, sai."),
    ], size=15, h=380))

    # 18. the five compared methods
    _title(bd, "phuong_phap.svg", "Năm phương pháp được so sánh trên cùng điều kiện")
    band(bd, "phuong_phap.svg", 4)
    bd.A("phuong_phap.svg", bd.table("bang-phuong-phap", 30, 108, [160, 310, 150, 150, 130], [
        ["Phương pháp", "Đầu vào cho LLM", "Lượt gọi LLM", "Có chạy test?", "Nguồn"],
        ["SBFL (Ochiai)", "không dùng LLM; chỉ độ phủ của test", "0", "có", "Abreu 2009"],
        ["LLM-Direct", "chỉ mã nguồn (chế độ hỏi thẳng\ncủa chính SemLoc)", m("CostLlmDirectCalls"), "không", "Yang 2026"],
        ["SemLoc", "mã nguồn; ràng buộc được chèn\nvà chạy cùng test", m("CostSemlocCalls"), "có", "Yang 2026"],
        ["SemLoc−Bonus", "như SemLoc, bỏ điểm thưởng\ncho dòng LLM đoán", m("CostSemlocCalls"), "có", "nhóm"],
        ["FailLoc", "mã nguồn + tên và lỗi của\ntừng test fail", m("CostLlmTestsCalls"), "có (lấy kết quả)", "nhóm đề xuất"],
    ], highlight_col=None, head_h=40, row_h=52, fs=15,
        note="Lượt gọi LLM: trung bình mỗi chương trình trên tập test với Gemini 3.8 Flash."))

    # 19. design
    _title(bd, "thiet_ke_tn.svg", "Thiết kế thực nghiệm: cùng chương trình, cùng mô hình, ba bộ nhãn")
    band(bd, "thiet_ke_tn.svg", 4)
    cols = [("Dữ liệu", ["SemFault-250", "dev: 50 chương trình", "test: 200 chương trình"], GREY),
            ("Phương pháp", [name(mm) for mm in MAIN], NAVY),
            ("Bộ nhãn", ["Nhãn gốc", "Nhãn đã chuẩn hóa", "Nhãn đã rà soát"], ORANGE),
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
        ("", "Mọi phương pháp có LLM dùng Gemini 3.8 Flash; tập dev chỉ để chọn tham số, kết quả báo trên tập test."),
        ("", "Khoảng tin cậy 95% tính bằng bootstrap trên các chương trình."),
    ], size=15))

    # 20. main results
    _title(bd, "ket_qua.svg", "Phương pháp FailLoc dẫn đầu Acc@1 và Acc@3 trên cả hai bộ nhãn")
    band(bd, "ket_qua.svg", 5)
    widths, row_h, head_h = [180, 100, 100, 115, 115], 50, 56
    grid = [["Phương pháp", "Gốc\nAcc@1", "Gốc\nAcc@3", "Chuẩn hóa\nAcc@1", "Chuẩn hóa\nAcc@3"]]
    grid += [[name(mm)] + [f"{(a1 if k == 1 else a3)(g, mm)}%" for g in ("original", "repaired") for k in (1, 3)] for mm in MAIN]
    bd.A("ket_qua.svg", bd.table("bang-ket-qua", 20, 104, widths, grid, row_h=row_h, head_h=head_h, fs=15))
    fy = 104 + head_h + row_h * MAIN.index("llm_tests")
    bd.A("ket_qua.svg", viz._g("khung-failloc", 20, fy, sum(widths), row_h,
                               [_r(20, fy, sum(widths), row_h, "none", stroke=ORANGE, rx=0, sw=3.5)]))
    bd.A("ket_qua.svg", P("doc-ket-qua", 640, 104, 290, [
        ("", "Acc@1: dòng lỗi ở hạng 1; Acc@3: dòng lỗi trong 3 dòng đầu (tập test, Gemini 3.8 Flash, trung bình 3 lần "
             "chạy)."),
        ("", f"Trên nhãn đã chuẩn hóa, FailLoc hơn SemLoc {d1} điểm Acc@1, khoảng tin cậy từ "
             f"{m('RqTwoRepairedAllLlmTestsDAccOneLo')} đến {m('RqTwoRepairedAllLlmTestsDAccOneHi')}, và "
             f"{m('RqTwoRepairedAllLlmTestsDAccThree')} điểm Acc@3."),
        ("", "Acc@1 của phương pháp SBFL gần như bằng 0, giống ví dụ ở phần 1."),
    ], size=13, h=356))

    # 21. improvement over SemLoc
    ratio = float(m("CostSemlocTokensK").replace(",", ".")) / float(m("CostLlmTestsTokensK").replace(",", "."))
    _title(bd, "cai_tien.svg", "Phương pháp FailLoc so với SemLoc trên cùng điều kiện")
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
    _title(bd, "tien_do.svg", "Tiến độ")
    bd.A("tien_do.svg", viz.progress_table("bang-tien-do", 40, 104, 880, progress_rows(1), row_h=46))
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
    g0 = "original" if bd.EARLY() else "repaired"
    return {
        **({"slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 1 của đề tài: bằng chứng hay phỏng "
                        "đoán, tái hiện và đánh giá việc định vị lỗi ngữ nghĩa trong mã nguồn bằng mô hình ngôn ngữ lớn."}
           if bd.DECK == "lan1" else {}),
        "muc_luc": "Tuần đầu nhóm tìm hiểu bài toán và tái hiện bài gốc. Đầu tiên là cơ sở lý thuyết: bài toán, phương pháp "
                   "SBFL, các nghiên cứu liên quan và phương pháp SemLoc. Sau đó là bốn câu hỏi nghiên cứu, hai kết quả đầu "
                   "tiên khi tái hiện SemLoc, và tiến độ.",
        "bai_toan": "Bài toán định vị lỗi bắt đầu khi chạy test và thấy có test fail. Đầu vào là mã nguồn và bộ test; đầu ra "
                    "là danh sách các dòng mã xếp từ đáng nghi nhất. Nhóm đo bằng Acc@1, tức phần trăm chương trình có dòng "
                    "lỗi thật đứng hạng 1, và Acc@3 cho 3 dòng đầu. Dòng lỗi thật lấy từ nhãn của bộ dữ liệu.",
        "vi_du": f"Đây là ví dụ 1: hàm {va['program']} trong bộ SemFault-250. Nhóm dùng nó cho phương pháp SBFL và phương pháp FailLoc. Chạy test thì {va['n_pass']} test "
                 f"pass, {va['n_fail']} test fail. Test fail đòi tổng các phần chia bằng tổng ban đầu, nhưng int(v) ở dòng {gt} cắt "
                 "mất phần lẻ. Mã vẫn chạy bình thường nên các công cụ kiểm tra cú pháp hay kiểu không báo gì; đó là lỗi "
                 "ngữ nghĩa.",
        "sbfl_cong_thuc": "Phương pháp kinh điển là SBFL, định vị lỗi dựa trên phổ độ phủ. Với mỗi dòng, ta đếm số test fail và "
                          "số test pass chạy qua nó rồi tính điểm Ochiai theo công thức trên màn hình. Tính tay cho dòng 29 của "
                          "ví dụ 1 được 0,45. Vấn đề là mọi dòng khác cũng được đúng 0,45.",
        "sbfl_mu": "Ma trận này cho thấy lý do. Cột đỏ là test fail duy nhất, và nó chạy qua đúng những dòng mà các test pass "
                   f"cũng chạy qua, kể cả dòng lỗi {gt}. Mọi dòng hòa điểm nên phương pháp SBFL chỉ còn đoán. Trên cả 250 chương "
                   f"trình, nó chỉ đúng ngay hạng 1 ở {m('RqOneSbflOchiaiFairAllAccOne')}%.",
        "lien_quan": "Đây là nội dung 1: bộ từ khóa và ba bài tiêu biểu trong các nghiên cứu nhóm đã đọc. Bài trung tâm là "
                     "SemLoc. Từ EffiHolmes, nhóm lấy ý tưởng so lần chạy bình thường với lần chạy có lỗi; từ nghiên cứu công "
                     "nghiệp, nhóm lấy ý tưởng đưa bằng chứng có sẵn vào prompt, chính là phương pháp FailLoc.",
        "semloc_tong_quan": "Phương pháp SemLoc của bài gốc có năm bước: LLM viết ràng buộc, ràng buộc được chèn vào mã, chạy "
                            "bộ test, chấm điểm từng dòng, rồi vá thử để kiểm chứng. Tác giả báo cáo Acc@1 "
                            f"{m('RqOneSemlocClaudeTZeroEightAuthorAllAccOne')}% và cho rằng độ chính xác đến từ bằng chứng "
                            "thực thi. Tiếp theo nhóm đi qua từng bước trên dữ liệu thật.",
        "semloc_rang_buoc": f"Từ đây nhóm dùng ví dụ 2, hàm {bo['program']}, vì ở ví dụ 1 ràng buộc không bị vi phạm lần "
                            "nào nên không có gì để chấm. Hàm này gộp hai danh sách đã sắp xếp thành một, phải giữ đủ mọi phần "
                            f"tử. Lỗi ở dòng {bo['label_lines'][0]} và 73: khi hai danh sách có cùng phần tử cuối, hàm bỏ mất "
                            f"một phần tử, và cả {bo['n_fail']} test fail đều rơi vào trường hợp đó. Bước 1, LLM đọc mã và test "
                            f"fail, đoán dòng lỗi là {bo['guess_line']} và viết bốn ràng buộc, chủ yếu là số phần tử kết quả phải "
                            "bằng tổng hai bên. Bước 2, SemLoc chèn chúng vào mã thành các dòng in nghiêng.",
        "semloc_diem": f"Chạy bộ test trên mã đã chèn kiểm tra. Với mỗi ràng buộc, đếm số test fail "
                       "và số test pass làm điều kiện sai, rồi tính Ochiai. Điểm đó nhân với hệ số theo chỗ đặt ràng buộc: "
                       "chỗ đặt càng hẹp thì hệ số càng cao, return chỉ được 0,3. C1 và C2 giống hệt nhau về điều kiện và số "
                       f"vi phạm; C2 gắn vào câu if nên dòng lỗi {bo['label_lines'][0]} được 1,00, còn C1 là ràng buộc SemLoc "
                       f"bắt LLM đặt ở dòng nó đoán nên dòng {bo['guess_line']} chỉ được 0,60. Bảng hệ số do tác giả tự đặt.",
        "cau_hoi": "Câu hỏi lớn của đề tài là thứ hạng của SemLoc đến từ bằng chứng thực thi hay từ LLM tự đoán. Nhóm tách "
                   "nó thành bốn câu hỏi nghiên cứu, là nội dung 2. RQ1: kết quả công bố của SemLoc có tái hiện được không, "
                   "và còn giữ khi chấm trên nhãn đã chuẩn hóa? RQ2: một prompt có test fail, phương pháp FailLoc, có định vị "
                   "đúng ít nhất bằng SemLoc không, và rẻ hơn bao nhiêu? RQ3: FailLoc thắng nhờ thông tin gì, và thêm phức "
                   "tạp có giúp không? RQ4: kết luận có còn đúng trên lỗi thật, mã đổi tên và các họ mô hình khác?",
        "overclaim": f"Đây là kết quả RQ1 đầu tiên. Bước cuối, có trong mã nguồn nhưng bài báo không mô tả, cộng thêm "
                     f"{m('ConstPriorWeight')} điểm cho dòng LLM đoán. Ở chương trình {bo['program']}, dòng 73 vượt lên hạng 1 với 1,80 dù dòng 72 "
                     f"có điểm phổ cao nhất. Trên tập test, trong {n_pairs} lượt, hạng 1 của SemLoc là dòng LLM đoán ở "
                     f"{_p(100 * share, 0)}% số lượt; bỏ điểm thưởng thì Acc@1 giảm từ "
                     f"{a1(g0, 'semloc')}% xuống {a1(g0, 'semloc_no_prior')}%. Điểm thưởng tự nó chỉ là lựa chọn thiết "
                     "kế; chỗ overclaim là bài báo quy độ chính xác cho bằng chứng thực thi. Bước vá thử cũng không đổi thứ "
                     "hạng nào.",
        "nhan_sai": f"Khi tái hiện, nhóm thấy chính nhãn của bộ dữ liệu có vấn đề. {m('GtBlankN')} nhãn nằm trên dòng trống, và ở "
                    f"{m('GtNotExecutedN')} chương trình không test fail nào chạy tới dòng được gán nhãn. Kết quả công bố của bài gốc "
                    "được chấm trên chính bộ nhãn này." + (" Tuần tới nhóm sẽ chuẩn hóa lại nhãn bằng cách chạy test."
                                                            if bd.EARLY() else ""),
        "chuan_hoa": "Nhóm chuẩn hóa nhãn bằng thực thi. Nếu sửa nhỏ ngay tại nhãn làm mọi test pass thì nhãn được xác nhận; "
                     "nếu không test fail nào chạy tới nhãn, nhóm thử các dòng lân cận. LLM chỉ đề xuất bản sửa, test quyết "
                     f"định. Kết quả là bộ nhãn đã chuẩn hóa gồm {m('GtRepairedN')} chương trình.",
        "failloc_y_tuong": "Cải tiến của nhóm là phương pháp FailLoc. Thay vì năm bước, FailLoc hỏi LLM một lần, đưa kèm mã "
                           "nguồn đánh số dòng cùng tên và thông báo lỗi của các test fail, giống cách lập trình viên vẫn hỏi "
                           f"trợ lý AI. Nó tốn khoảng {m('CostLlmTestsTokensK')} nghìn token mỗi chương trình, so với "
                           f"{m('CostSemlocTokensK')} nghìn của SemLoc.",
        "failloc_vd": f"Đây là prompt thật FailLoc gửi cho ví dụ {va['program']}. LLM trả về năm dòng, dòng {va['failloc_top5'][0]} "
                      f"đứng đầu, đúng dòng lỗi. Trên cùng chương trình, SemLoc xếp dòng {va['guess_line']} ở hạng 1 vì điểm "
                      "thưởng. Đây chỉ là một ví dụ, kết quả trên cả tập test ở phần sau.",
        "phuong_phap": "Nhóm so năm phương pháp. SBFL không dùng LLM; LLM-Direct là chế độ hỏi thẳng của chính SemLoc, chỉ có "
                       "mã nguồn; SemLoc và SemLoc bỏ điểm thưởng; và FailLoc. Mọi phương pháp có LLM dùng cùng một mô hình.",
        "thiet_ke_tn": "Để so sánh công bằng, mọi phương pháp chạy trên cùng các chương trình của tập test với Gemini 3.8 Flash. "
                    "Mỗi cấu hình chạy 3 lần, kết quả báo trên ba bộ nhãn, kèm khoảng tin cậy 95% tính bằng bootstrap.",
        "ket_qua": f"Đây là kết quả chính. FailLoc đứng đầu ở cả Acc@1 lẫn Acc@3 trên cả hai bộ nhãn. Trên nhãn đã chuẩn hóa, FailLoc đạt "
                   f"{a1('repaired', 'llm_tests')}%, SemLoc {a1('repaired', 'semloc')}%, hơn {d1} điểm và khoảng tin cậy không "
                   "chạm 0.",
        "cai_tien": f"Gói lại những gì nhóm làm tốt hơn phương pháp SemLoc trên cùng điều kiện. FailLoc hơn {d1} điểm Acc@1 và "
                    f"{m('RqTwoRepairedAllLlmTestsDAccThree')} điểm Acc@3 trên nhãn đã chuẩn hóa, vẫn hơn trên nhãn gốc, và dùng "
                    f"ít token hơn khoảng {_p(ratio, 0)} lần. Về cách đánh giá, nhóm chấm trên nhãn đã chuẩn hóa, chạy ba lần "
                    "và báo khoảng tin cậy.",
        "tien_do": "Về tiến độ, nội dung 1 và nội dung 2 đã xong, cùng với việc tái hiện SemLoc. Lần 2 nhóm trình bày chuẩn "
                   "hóa nhãn, phương pháp FailLoc và so sánh chính; lần 3 là độ bền, ablation, các hướng bổ sung và đóng góp. "
                   "Bài báo arXiv và phân tích thất bại để dành cho buổi bảo vệ.",
        "slide_30": "Nhóm xin cảm ơn thầy và các bạn đã lắng nghe, và rất mong nhận được câu hỏi và góp ý.",
    }

"""Báo cáo lần 3 (≤ 18 trang): the third week, robustness and contributions. A recap of lần 2 (FailLoc beats SemLoc),
what ablation is, the additions (CovGate, FailLoc+Vote, static tools), the RQ4 design and results (BugsInPy, renaming,
model families), the ablation and additions results, cost, the contributions (content 3) and the progress table.
Most pages are built in story_lan2; this module builds only the pages lần 3 has on its own."""
import viz
from story_common import MAIN, ROOT, _csv, _note, _title, cite, progress_rows
from viz import ORANGE, _p, _r

LAN3 = [("slide_01.svg", 1), ("muc_luc_3.svg", 22), ("nhac_lai_3.svg", 22),
        ("ablation_la_gi.svg", 22), ("shapley.svg", 22),
        ("ba_prompt.svg", 22), ("luong_cov.svg", 22), ("bo_sung.svg", 22),
        ("rq3_thiet_ke.svg", 22), ("bugsinpy.svg", 22), ("doi_ten.svg", 22), ("ho_mo_hinh.svg", 22),
        ("ablation_kq.svg", 22), ("phan_ra.svg", 22), ("bo_sung_kq.svg", 22), ("cai_tien_2.svg", 22),
        ("dong_gop_2.svg", 22), ("tien_do_3.svg", 22), ("slide_30.svg", 30)]


def _acc():
    rq2 = {(r["gt"], r["method"]): r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r.get("subset", "all") == "all"}
    return lambda g, mm, k=1: 100 * float(rq2[(g, mm)][f"acc{k}_mean"])


def pages(bd) -> None:
    P = viz.panel
    acc = _acc()

    # agenda
    _title(bd, "muc_luc_3.svg", "Nội dung trình bày lần 3")
    items = [("", "Nhắc lại lần 2", "FailLoc hơn SemLoc trên nhãn đã chuẩn hóa"),
             ("1", "Cơ sở lý thuyết bổ sung", "Ablation; phân rã Shapley (có ví dụ tính)"),
             ("3", "Cải tiến", "FailLoc+Cov, CovGate, FailLoc+Vote; luồng chạy trên ví dụ"),
             ("4", "Thực nghiệm", "Ba cách thử độ bền (RQ4)"),
             ("5", "Kết quả", "Độ bền, vì sao FailLoc thắng, SemLoc dựa vào đâu, chi phí"),
             ("", "Đóng góp và tiến độ", "Bốn đóng góp trả lời bốn RQ; tiến độ")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 106 + i * 58
        body.append(_r(60, y, 840, 48, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else viz.LAVENDER, rx=10, sw=1.2))
        body.append(viz._t(92, y + 32, k or "•", size=24, fill=viz.NAVY, weight="bold", anchor="middle"))
        body.append(viz._t(130, y + 31, head, size=18, fill=viz.NAVY, weight="bold"))
        body.append(viz._t(470, y + 31, desc, size=14))
    bd.A("muc_luc_3.svg", viz._g("muc-luc", 60, 106, 840, 58 * (len(items) - 1) + 48, body))

    # recap of report 2: FailLoc beats SemLoc on the normalized labels
    _title(bd, "nhac_lai_3.svg", "Nhắc lại lần 2: phương pháp FailLoc hơn phương pháp SemLoc")
    grid = [["Phương pháp", "Acc@1", "Acc@3"]] + [[cite(mm)] + [f"{_p(acc('repaired', mm, k))}%" for k in (1, 3)] for mm in MAIN]
    bd.A("nhac_lai_3.svg", bd.table("lan2", 40, 104, [250, 95, 95], grid, row_h=40, head_h=40, fs=14))
    fy = 104 + 40 + 40 * MAIN.index("llm_tests")
    bd.A("nhac_lai_3.svg", viz._g("khung-failloc-lan2", 40, fy, 440, 40, [_r(40, fy, 440, 40, "none", stroke=ORANGE, rx=0, sw=3.5)]))
    bd.A("nhac_lai_3.svg", _note(40, 374, ["Nhãn đã chuẩn hóa, tập test, Gemini 3.8 Flash,", "trung bình 3 lần chạy."],
                                 size=13, gid="nguon-lan2", w=440))
    bd.A("nhac_lai_3.svg", P("lan2-tom-tat", 500, 104, 430, [
        ("Còn hai câu hỏi", "1. FailLoc thắng nhờ đâu, và thêm phức tạp có giúp không? (RQ3)"),
        ("", "2. Kết quả có giữ trên lỗi thật, mã đổi tên, mô hình khác? (RQ4)"),
    ], size=15, h=232))

    # progress
    _title(bd, "tien_do_3.svg", "Tiến độ")
    bd.A("tien_do_3.svg", viz.progress_table("bang-tien-do-3", 40, 104, 880, progress_rows(3), row_h=46))
    bd.A("tien_do_3.svg", _note(40, 480, ["Có bản nháp: bài báo đã viết xong bản đầu, nhóm hoàn thiện cho buổi bảo vệ."],
                                size=13, gid="chu-thich-tien-do-3", w=880))


def notes(bd) -> dict:
    acc = _acc()
    return {
        **({"slide_01": "Chào thầy và các bạn, nhóm M9 xin trình bày báo cáo tiến độ lần 3 của đề tài bằng chứng hay phỏng "
                        "đoán."} if bd.DECK == "lan3" else {}),
        "muc_luc_3": "Tuần vừa rồi nhóm kiểm chứng độ bền và tổng kết đóng góp. Sau phần nhắc lại, nhóm giải thích ablation, "
                     "các hướng bổ sung và luồng của FailLoc+Cov, rồi ba cách thử độ bền, kết quả, chi phí, đóng góp và tiến độ.",
        "nhac_lai_3": f"Nhắc lại lần 2: phương pháp FailLoc, một lượt gọi LLM kèm test fail, đạt Acc@1 "
                      f"{_p(acc('repaired', 'llm_tests'))}%, so với {_p(acc('repaired', 'semloc'))}% của SemLoc, trên nhãn đã "
                      "chuẩn hóa. Còn hai câu hỏi: vì sao FailLoc thắng, và kết quả có bền không.",
        "tien_do_3": "Về tiến độ, ba nội dung đầu đã xong; bài báo arXiv đã có bản nháp. Bài báo bản cuối, phân tích thất bại và "
                     "kiểm chứng bằng bản sửa để dành cho buổi bảo vệ.",
    }

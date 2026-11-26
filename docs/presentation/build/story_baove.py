"""Bảo vệ (~25 phút, 28 trang, no progress part): the whole story. build_deck builds every story module's pages for
every deck (E/A calls are no-ops for pages a deck lacks), so the defence reuses the pages of lần 1–3; this module builds
the three pages only the defence has: the agenda, FailLoc+Verify and why tests are too weak to be the arbiter, and the
failure analysis. The contributions page also carries future
research (more datasets); a separate conclusion page was dropped (25/11) because it repeated the contributions."""
import story_lan2
import viz
from story_common import _csv, _note, _title, band, examples, ROOT  # noqa: F401
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

import make_figures as mf  # noqa: E402

BAOVE = [("slide_01.svg", 1), ("muc_luc_bv.svg", 22),
         # 1. cơ sở lý thuyết
         ("bai_toan.svg", 22), ("vi_du.svg", 22), ("sbfl_mu.svg", 22), ("lien_quan.svg", 22),
         ("semloc_tong_quan.svg", 22),
         # 2. phương pháp giải quyết
         ("cau_hoi.svg", 20), ("nhan_sai.svg", 22), ("chuan_hoa.svg", 22),
         # 3. cải tiến
         ("luong_failloc.svg", 22), ("luong_semloc_bonus.svg", 22), ("bo_sung.svg", 22), ("luong_cov.svg", 22),
         # 4. thực nghiệm
         ("thiet_ke_tn.svg", 22),
         # 5. kết quả
         ("overclaim.svg", 22), ("nhan_di_dau.svg", 22), ("ba_bo_nhan.svg", 22), ("bugsinpy.svg", 22),
         ("doi_ten.svg", 22), ("ho_mo_hinh.svg", 22), ("ablation_kq.svg", 22), ("bo_sung_kq.svg", 22),
         ("verify_bv.svg", 22), ("that_bai_bv.svg", 22), ("cai_tien_2.svg", 22),
         # đóng góp và kết luận
         ("dong_gop_2.svg", 22),
         ("slide_30.svg", 30)]


def pages(bd) -> None:
    m = bd._m
    P = viz.panel
    bo = examples()["blend_orders"]

    # agenda, no progress part
    _title(bd, "muc_luc_bv.svg", "Nội dung trình bày")
    items = [("1", "Cơ sở lý thuyết", "Bài toán, SBFL, nghiên cứu liên quan, SemLoc"),
             ("2", "Phương pháp giải quyết", "Bốn câu hỏi nghiên cứu; chuẩn hóa nhãn bằng thực thi"),
             ("3", "Cải tiến", "Phương pháp FailLoc; các hướng bổ sung"),
             ("4", "Thực nghiệm", "Năm phương pháp, thiết kế thực nghiệm"),
             ("5", "Kết quả", "Overclaim, ba bộ nhãn, độ bền, vì sao FailLoc thắng"),
             ("", "Đóng góp", "Bốn đóng góp trả lời bốn RQ; hướng phát triển")]
    body = []
    for i, (k, head, desc) in enumerate(items):
        y = 112 + i * 62
        body.append(_r(60, y, 840, 52, viz.CREAM if k else viz.LIGHT, stroke=ORANGE if k else LAVENDER, rx=10, sw=1.2))
        body.append(_t(92, y + 34, k or "•", size=24, fill=NAVY, weight="bold", anchor="middle"))
        body.append(_t(130, y + 33, head, size=19, fill=NAVY, weight="bold"))
        body.append(_t(420, y + 33, desc, size=15))
    bd.A("muc_luc_bv.svg", viz._g("muc-luc", 60, 112, 840, 362, body))

    # FailLoc+Verify and why tests are too weak to be the arbiter
    _title(bd, "verify_bv.svg", "Để test làm trọng tài (FailLoc+Verify) cũng không giúp")
    band(bd, "verify_bv.svg", 5, rq="RQ3")
    bd.A("verify_bv.svg", viz.pipeline("verify", 30, 104, ["FailLoc đề xuất\n5 dòng nghi", "LLM viết bản\nsửa nhỏ mỗi dòng",
                                                            "Chạy bộ test\ntrên bản đã vá", "Dòng có bản sửa\npass lên trước"],
                                       accent=0, box_w=200, gap=30, box_h=74))
    bd.A("verify_bv.svg", viz.big_number("sai-cung-pass", 30, 204,
                                         f"{m('PavmechReviewedOtherLineFixable')}% · {m('PavmechtestReviewedOtherLineFixable')}%",
                                         "lần thử ở dòng không có lỗi mà bản\nsửa nhỏ vẫn làm mọi test pass",
                                         color=RED, size=32, w=300))
    bd.A("verify_bv.svg", viz.big_number("dung-pass", 345, 204,
                                         f"{m('PavmechReviewedFaultLineFixable')}% · {m('PavmechtestReviewedFaultLineFixable')}%",
                                         "lần thử ở dòng lỗi thật\nlàm mọi test pass", color=NAVY, size=32, w=275))
    bd.A("verify_bv.svg", P("verify-giai-thich", 630, 200, 300, [
        ("", "Chỉ khoảng mười test: sửa ở dòng khác thường đủ bù cho phép tính sai."),
        ("", "Test đủ để gợi ý lỗi ở đâu nhưng quá yếu để chứng minh lỗi ở đâu."),
    ], size=15, h=140))
    bd.A("verify_bv.svg", _note(30, 340, ["Nhãn đã rà soát; số trước: tập dev, số sau: tập test."], size=12, gid="ghi-chu-verify", w=580))
    pav = {r["config"]: r for r in _csv(ROOT / "data" / "pav_test.csv") if r["gt"] == "reviewed"}
    pv = lambda c, k: 100 * float(pav[c][k])
    rows = [("FailLoc", pv("chosen", "single_acc1"), GREY), ("FailLoc+MinFix", pv("chosen", "pav_acc1"), ORANGE),
            ("FailLoc+AnyFix", pv("worst", "pav_acc1"), RED)]
    bd.A("verify_bv.svg", viz._g("kq-verify-nhan", 30, 360, 580, 22, [
        _t(30, 376, f"Kết quả trên tập test ({pav['chosen']['n']} chương trình, nhãn đã rà soát, 3 lần chạy): Acc@1",
           size=14, fill=NAVY, weight="bold")]))
    bd.A("verify_bv.svg", viz.bars("kq-verify", 30, 384, 580, 84, rows, vmax=100, unit="%", label_w=270, nd=1))
    w = pav["worst"]
    bd.A("verify_bv.svg", _note(44, 488, [
        "MinFix: kiểm 2 dòng đầu, chỉ nhận bản sửa 1 token; bằng FailLoc.",
        f"AnyFix: kiểm 3 dòng đầu, nhận bản sửa bất kỳ; giảm {_p(abs(100 * float(w['d_acc1'])))} điểm."],
        size=12, gid="kq-verify-chu", w=566))

    # failure analysis
    rows = mf.failure_data()
    _title(bd, "that_bai_bv.svg", "Phương pháp SemLoc sai ở đâu và vì sao")
    band(bd, "that_bai_bv.svg", 5)
    short = {"guess_right": "Dòng LLM đoán đúng", "rescued_by_spectrum": "Đoán sai, phổ cứu vào top 3",
             "prior_hurts": "Phổ đúng, thưởng làm sai", "coverage_only_wins": "Chỉ FailLoc+Cov vào top 3",
             "gt_suspect": "Nhãn đáng ngờ", "all_miss": "Mọi phương pháp sai top 3"}
    ser = [(short[c], float(n), ORANGE if c == "prior_hurts" else NAVY if c == "rescued_by_spectrum" else GREY) for c, n in rows]
    bd.A("that_bai_bv.svg", viz.bars("sau-nhom", 20, 104, 560, 300, ser, vmax=max(n for _, n in rows) * 1.15, unit="",
                                     label_w=280, nd=0))
    bd.A("that_bai_bv.svg", P("nam-mau", 600, 104, 330, [
        ("", "Số chương trình của tập test theo từng nhóm. Thanh cam: phổ vi phạm đã đúng nhưng điểm thưởng làm sai."),
        ("Nguyên nhân sai", "Nhầm điều kiện với câu lệnh nó bảo vệ; lỗi trải nhiều dòng; nhãn đáng ngờ."),
    ], size=15, h=300))

    # the closing page (conclusion per RQ, contributions, future work) is built in story_lan2


def _pav_worst() -> dict:
    return next(r for r in _csv(ROOT / "data" / "pav_test.csv") if r["config"] == "worst" and r["gt"] == "reviewed")


def notes(bd) -> dict:
    """Notes of the defence-only pages, plus the defence's own wording of shared pages (applied last, defence only)."""
    if bd.DECK != "baove":
        return {}
    m = bd._m
    n2 = story_lan2.notes(bd)
    out = {}
    out["slide_01"] = ("Chào thầy và các bạn, nhóm M9 xin trình bày đề tài bằng chứng hay phỏng đoán: tái hiện và đánh giá "
                       "việc định vị lỗi ngữ nghĩa trong mã nguồn bằng mô hình ngôn ngữ lớn.")
    out["muc_luc_bv"] = ("Bài trình bày đi theo năm phần thầy yêu cầu: cơ sở lý thuyết, phương pháp của bài gốc SemLoc, phần "
                         "nhóm kiểm tra lại bài gốc, cải tiến là phương pháp FailLoc, thực nghiệm và kết quả. Cuối cùng là đóng "
                         "góp và kết luận.")
    out["verify_bv"] = (f"Nhóm thử để test làm trọng tài: FailLoc đề xuất dòng, LLM viết bản sửa nhỏ, chạy test, dòng nào có "
                        f"bản sửa pass thì lên trước. Cách này không giúp, vì ở dòng không có lỗi bản sửa nhỏ vẫn làm mọi test "
                        f"pass ở {m('PavmechReviewedOtherLineFixable')}% lần thử trên tập dev và {m('PavmechtestReviewedOtherLineFixable')}% trên tập test. Trên tập test, FailLoc+MinFix, chỉ nhận bản sửa một token, không "
                        f"đổi dòng đứng đầu nào nên kết quả bằng đúng FailLoc, còn FailLoc+AnyFix, nhận bản sửa bất kỳ, làm Acc@1 giảm "
                        f"{_p(abs(100 * float(_pav_worst()['d_acc1'])))} điểm. Test đủ để gợi ý lỗi ở đâu nhưng quá yếu để "
                        "chứng minh lỗi ở đâu.")
    out["that_bai_bv"] = ("Nhóm xếp từng chương trình vào một nhóm kết quả. Nhóm lớn nhất là chương trình mà dòng LLM đoán đã "
                          "đúng; thanh cam là chương trình mà phổ vi phạm đúng nhưng điểm thưởng làm sai. Đọc từng ca, nhóm "
                          "tìm ra năm nguyên nhân sai, liệt kê bên phải.")
    out["dong_gop_2"] = n2["dong_gop_2"] + (" Hướng phát triển là tìm thêm nhiều bộ dữ liệu, nhất là lỗi thật từ nhiều dự án, "
                                             "để chạy các phương pháp trên quy mô lớn hơn.")
    return out

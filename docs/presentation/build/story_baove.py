"""Bảo vệ (~25 phút, 32 trang, no progress part): the whole story. Pages of lần 1 and lần 2 are reused by building
both page sets (their E/A calls are no-ops for pages this deck lacks); four pages are new: the agenda, FailLoc+Verify
and why tests are too weak to be the arbiter, the failure analysis, limitations and conclusion."""
import story_lan1
import story_lan2
import viz
from story_common import _csv, _title, band, examples, ROOT  # noqa: F401
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t

import make_figures as mf  # noqa: E402

BAOVE = [("slide_01.svg", 1), ("muc_luc_bv.svg", 22),
         # 1. cơ sở lý thuyết
         ("bai_toan.svg", 22), ("vi_du.svg", 22), ("sbfl_mu.svg", 22), ("lien_quan.svg", 22),
         ("semloc_tong_quan.svg", 22), ("semloc_rang_buoc.svg", 22), ("semloc_diem.svg", 22),
         # 2. phương pháp giải quyết
         ("cau_hoi.svg", 20), ("nhan_sai.svg", 22), ("chuan_hoa.svg", 22),
         # 3. cải tiến
         ("failloc_y_tuong.svg", 22), ("failloc_vd.svg", 22), ("bo_sung.svg", 22),
         # 4. thực nghiệm
         ("phuong_phap.svg", 22), ("thiet_ke_tn.svg", 22), ("ba_prompt.svg", 22),
         # 5. kết quả
         ("overclaim.svg", 22), ("nhan_di_dau.svg", 22), ("ba_bo_nhan.svg", 22), ("bugsinpy.svg", 22),
         ("doi_ten.svg", 22), ("ho_mo_hinh.svg", 22), ("ablation_kq.svg", 22), ("bo_sung_kq.svg", 22),
         ("verify_bv.svg", 22), ("that_bai_bv.svg", 22), ("cai_tien_2.svg", 22),
         # đóng góp và kết luận
         ("dong_gop_2.svg", 22), ("ket_luan_bv.svg", 22),
         ("slide_30.svg", 30)]


def pages(bd) -> None:
    story_lan1.pages(bd)
    story_lan2.pages(bd)
    m = bd._m
    P = viz.panel
    bo = examples()["blend_orders"]

    # agenda, no progress part
    _title(bd, "muc_luc_bv.svg", "Nội dung trình bày")
    items = [("1", "Cơ sở lý thuyết", "Bài toán, SBFL, nghiên cứu liên quan, SemLoc"),
             ("2", "Phương pháp giải quyết", "Ba câu hỏi nghiên cứu; chuẩn hóa nhãn bằng thực thi"),
             ("3", "Cải tiến", "Phương pháp FailLoc; các hướng bổ sung"),
             ("4", "Thực nghiệm", "Năm phương pháp, thiết kế thực nghiệm, ba mức prompt"),
             ("5", "Kết quả", "Overclaim, ba bộ nhãn, độ bền, vì sao FailLoc thắng"),
             ("", "Đóng góp và kết luận", "Đóng góp, triết lý khoa học, hạn chế")]
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
    band(bd, "verify_bv.svg", 5)
    bd.A("verify_bv.svg", viz.pipeline("verify", 30, 104, ["FailLoc đề xuất\n5 dòng nghi", "LLM viết bản\nsửa nhỏ mỗi dòng",
                                                            "Chạy bộ test\ntrên bản đã vá", "Dòng có bản sửa\npass lên trước"],
                                       accent=0, box_w=200, gap=30, box_h=74))
    bd.A("verify_bv.svg", viz.big_number("sai-cung-pass", 30, 210, f"{m('PavmechReviewedOtherLineFixable')}%",
                                         "lần thử ở dòng không có lỗi mà\nbản sửa nhỏ vẫn làm mọi test pass", color=RED, size=48, w=300))
    bd.A("verify_bv.svg", viz.big_number("dung-pass", 345, 210, f"{m('PavmechReviewedFaultLineFixable')}%",
                                         "lần thử ở dòng lỗi thật\nlàm mọi test pass", color=NAVY, size=48, w=265))
    cf = bo["cf_results"][0] if bo["cf_results"] else None
    bd.A("verify_bv.svg", P("verify-giai-thich", 630, 200, 300, [
        ("", "Mỗi chương trình chỉ có khoảng mười test. Đổi một hằng số ở dòng khác thường đủ bù cho phép tính sai, nên test "
             "pass dù dòng đó không có lỗi."),
        ("", f"SemLoc gặp đúng chuyện này: ở {bo['program']}, bản vá ở dòng 73 (dòng sai) cũng làm mọi test pass."
         if cf and cf["patch"] == "pass" else "Bước vá thử của SemLoc cũng không đổi thứ hạng nào."),
        ("", "Với bộ test cỡ này, test đủ để gợi ý lỗi ở đâu nhưng quá yếu để chứng minh lỗi ở đâu."),
    ], size=14, h=280))
    bd.A("verify_bv.svg", viz._g("ghi-chu-verify", 30, 360, 580, 40, [
        _t(30, 372, "Tập dev, nhãn đã rà soát. Cấu hình tốt nhất của FailLoc+Verify", size=13, fill=MUTED),
        _t(30, 390, "trên tập dev vẫn không hơn FailLoc.", size=13, fill=MUTED)]))

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
        ("", "Mỗi chương trình của tập test được xếp vào một nhóm (nhãn đã chuẩn hóa, lấy đa số ba lần chạy). Thanh cam là "
             "những chương trình mà phổ vi phạm đã đúng nhưng điểm thưởng đẩy dòng đoán sai lên trên."),
        ("Năm nguyên nhân sai", "Nhầm dòng điều kiện với câu lệnh nó bảo vệ; lỗi trải nhiều dòng; bộ phán định chấp nhận "
                                "bản sửa bù trừ; nguyên nhân và triệu chứng nằm trên cùng luồng dữ liệu; nhãn đáng ngờ."),
    ], size=14, h=300))

    # limitations and conclusion
    _title(bd, "ket_luan_bv.svg", "Hạn chế và kết luận")
    band(bd, "ket_luan_bv.svg", 6)
    bd.A("ket_luan_bv.svg", P("han-che", 30, 104, 430, [
        ("Hạn chế", "Bộ phán định chấp nhận bản sửa bù trừ, nên nhãn đã chuẩn hóa còn nhiễu."),
        ("", "Nhãn đã rà soát bắt đầu từ gợi ý của LLM; duyệt mù giảm nhưng không xóa hết rủi ro này."),
        ("", "Tên test của SemFault-250 gần như nói thẳng ý định của hàm."),
        ("", "Lỗi thật chỉ lấy từ một dự án, và phần lớn thí nghiệm dùng một mô hình chính."),
    ], size=14, h=300))
    bd.A("ket_luan_bv.svg", P("ket-luan", 480, 104, 450, [
        ("Kết luận", "Hạng 1 của SemLoc là dòng LLM đoán, trong khi bài báo quy công cho bằng chứng thực thi (overclaim)."),
        ("", "Một prompt có test fail (FailLoc) chính xác hơn và rẻ hơn trên cả ba bộ nhãn; trên lỗi thật cùng chiều ở Acc@3 nhưng mẫu nhỏ."),
        ("", "Test đủ để gợi ý lỗi nhưng quá yếu để làm trọng tài, nên thêm bước kiểm chứng không giúp."),
        ("Hướng tiếp", "Bộ dữ liệu có nhãn kiểm chứng tốt hơn và test mạnh hơn; lỗi thật từ nhiều dự án; giấu tên test để đo "
                       "phần LLM dựa vào tên."),
    ], size=14, h=300))


def notes(bd) -> dict:
    m = bd._m
    n1, n2 = story_lan1.notes(bd), story_lan2.notes(bd)
    out = {**n2, **n1}
    out["cau_hoi"] = ("Từ đó nhóm đặt ba câu hỏi nghiên cứu, là nội dung 2. RQ1: kết quả công bố của SemLoc có tái hiện được "
                      "không, và còn giữ khi chấm công bằng trên nhãn đã chuẩn hóa? RQ2: chỉ với mã nguồn và test fail, "
                      "phương pháp FailLoc có định vị đúng hơn phương pháp SemLoc không, rẻ hơn bao nhiêu, và các cách bổ sung "
                      "có thêm được gì? RQ3: kết luận có còn đúng trên lỗi thật, trên mã đã đổi tên và với năm họ mô hình?")
    out["thiet_ke_tn"] = ("Để so sánh công bằng, mọi phương pháp chạy trên cùng các chương trình của tập test với Gemini 3.8 "
                          "Flash. Mỗi cấu hình chạy 3 lần, kết quả báo trên ba bộ nhãn, kèm khoảng tin cậy 95% tính bằng "
                          "bootstrap.")
    out["slide_01"] = ("Chào thầy và các bạn, nhóm M9 xin trình bày đề tài bằng chứng hay phỏng đoán: tái hiện và đánh giá "
                       "việc định vị lỗi ngữ nghĩa trong mã nguồn bằng mô hình ngôn ngữ lớn.")
    out["muc_luc_bv"] = ("Bài trình bày đi theo năm phần thầy yêu cầu: cơ sở lý thuyết, phương pháp của bài gốc SemLoc, phần "
                         "nhóm kiểm tra lại bài gốc, cải tiến là phương pháp FailLoc, thực nghiệm và kết quả. Cuối cùng là đóng "
                         "góp và kết luận.")
    out["verify_bv"] = (f"Nhóm thử để test làm trọng tài: FailLoc đề xuất dòng, LLM viết bản sửa nhỏ, chạy test, dòng nào có "
                        f"bản sửa pass thì lên trước. Cách này không giúp, vì ở dòng không có lỗi bản sửa nhỏ vẫn làm mọi test "
                        f"pass ở {m('PavmechReviewedOtherLineFixable')}% lần thử. Test đủ để gợi ý lỗi ở đâu nhưng quá yếu để "
                        "chứng minh lỗi ở đâu.")
    out["that_bai_bv"] = ("Nhóm xếp từng chương trình vào một nhóm kết quả. Nhóm lớn nhất là chương trình mà dòng LLM đoán đã "
                          "đúng; thanh cam là chương trình mà phổ vi phạm đúng nhưng điểm thưởng làm sai. Đọc từng ca, nhóm "
                          "tìm ra năm nguyên nhân sai, liệt kê bên phải.")
    out["ket_luan_bv"] = ("Tóm lại, hạng 1 của SemLoc là dòng LLM đoán và bài báo overclaim về nguồn gốc độ chính xác. FailLoc "
                          "chính xác hơn và rẻ hơn trên cả ba bộ nhãn, và cùng chiều trên lỗi thật. Hạn chế lớn nhất là chất lượng nhãn và test của "
                          "bộ dữ liệu, cũng là hướng tiếp theo.")
    out["dong_gop_2"] = ("Nhóm có năm đóng góp, từ việc chỉ ra hạng 1 của SemLoc là dòng đoán đến bảng kiểm tra và gói tái "
                         "hiện. Triết lý khoa học: bằng chứng thực thi là trọng tài, nhưng phải đo nó đóng góp bao nhiêu, luôn "
                         "so với cách làm đơn giản và đặt điều kiện bác bỏ trước.")
    return out

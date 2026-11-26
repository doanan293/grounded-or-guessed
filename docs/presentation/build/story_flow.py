"""Flow pages: one page per method the group proposes, each step drawn with the real content of a running example.

luong_chuan_hoa (lần 2): label normalization on estimate_temperature: the original label 69 is never reached by a
    failing test, a one-token fix the LLM proposes at line 68 makes every test pass, so the normalized label is 68.
luong_failloc (lần 2, bảo vệ): FailLoc on example 1, votes_apportion (fault line 29).
luong_semloc_bonus (lần 2, bảo vệ): SemLoc without the bonus on example 1: no constraint is violated, so without the
    bonus SemLoc ranks no line at all; the rank-1 line of SemLoc there comes from the LLM's guess alone.
luong_cov (lần 3, bảo vệ): FailLoc+Cov on example 2, combine_responses (fault line 72), the program where coverage
    lifts the fault line from rank 2 to rank 1 in all three runs; the page also gives the whole-set effect, which is
    negative, so the example is not read as the general case.
On every page the orange box is the one step where the method differs from its neighbour.
"""
import json

import viz
from story_common import ROOT, _csv, _note, _title, band, cov_example, examples
from viz import NAVY, ORANGE, RED, _p

PAGES = ("luong_chuan_hoa.svg", "luong_failloc.svg", "luong_semloc_bonus.svg", "luong_cov.svg")
LABEL_EXAMPLE = "estimate_temperature"  # the nhan_sai page's second case, worked through the normalization steps
Y, H = 104, 150  # the flow strip


def _acc(g: str, mm: str, k: int = 1) -> str:
    r = next(r for r in _csv(ROOT / "data" / "rq2_ours.csv") if r["gt"] == g and r["method"] == mm
             and r.get("subset", "all") == "all")
    return _p(100 * float(r[f"acc{k}_mean"]))


def _diff(bd, page: str, text: str) -> None:
    bd.A(page, _note(30, Y + H + 32, [text], size=15, fill=ORANGE, weight="bold", gid="khac-mot-cho", w=900))


def _ranks(top: list[int]) -> str:
    return ", ".join(str(n) for n in top)


def _label_example() -> dict:
    """The verified record, test counts and source lines of the label-normalization example."""
    rec = next(v for v in json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
               if v["program"] == LABEL_EXAMPLE)
    lab = next(r for r in _csv(ROOT / "data" / "semfault_labels.csv") if r["program"] == LABEL_EXAMPLE)
    src = (ROOT / "third_party" / "semloc" / "benchmark" / "programs" / f"{LABEL_EXAMPLE}.py").read_text().splitlines()
    return {**rec, "n_fail": int(lab["n_fail"]), "n_pass": int(lab["n_pass"]),
            "reached": lab["fault_hit_by_fail"] == "True", "src": src}


def pages(bd) -> None:
    P = viz.panel
    m = bd._m

    # label normalization on a real example
    pg = "luong_chuan_hoa.svg"
    le = _label_example()
    o, n = le["original"][0], le["lines"][0]
    line = lambda k: f"{k}: {le['src'][k - 1].strip()}"
    _title(bd, pg, f"Luồng chuẩn hóa nhãn trên một ví dụ: nhãn dời từ dòng {o} sang {n}")
    band(bd, pg, 2)
    bd.A(pg, viz.flow("luong", 30, Y, [
        (f"Nhãn gốc: dòng {o}", [line(k) for k in (n, o, o + 1)]),
        (f"Test fail tới dòng {o}?", ["Không: cả " + str(le["n_fail"]) + " test fail", "gọi clamp=True nên",
                                     "bỏ qua khối if"] if not le["reached"] else ["Có"]),
        ("Đề xuất sửa nhỏ", [line(n), f"→ {n}: {le['code'].strip()}", f"(sửa {le['edit_size']} token)"]),
        ("Chạy lại test", [f"{le['n_fail']} test fail và", f"{le['n_pass']} test pass cũ:", "mọi test pass ✓"]),
        ("Nhãn đã chuẩn hóa", [f"dòng {n}", f"(dời từ dòng {o})"]),
    ], box_w=[196, 176, 166, 130, 160], box_h=H, gap=18, accent=3, mono={0, 2}))
    _diff(bd, pg, "LLM chỉ đề xuất bản sửa; chạy test mới quyết định dòng nào là dòng lỗi (hộp cam).")
    bd.A(pg, P("doc-chuan-hoa", 30, 300, 900, [
        ("Đọc sơ đồ", f"Điều kiện dòng {n} bị đảo. Không test fail nào chạy tới dòng {o} được gán nhãn, nên nhóm thử sửa nhỏ "
                      f"các dòng lân cận. Đổi dòng {n} thì mọi test pass, nên dòng {n} là dòng lỗi."),
        ("Trên cả bộ dữ liệu", f"{m('GtConfirmedN')} nhãn được xác nhận, {m('GtCorrectedN')} nhãn dời sang dòng lân cận như "
                               f"ví dụ này, {m('GtUnverifiableN')} nhãn không kiểm chứng được và bị loại."),
    ], size=15, h=170))
    va = examples()["votes_apportion"]
    code = {c["no"]: c["text"].strip() for c in va["code_lines"]}
    gt = va["label_lines"][0]

    # FailLoc on example 1
    pg = "luong_failloc.svg"
    _title(bd, pg, f"Luồng phương pháp FailLoc trên ví dụ 1: dòng lỗi {gt} lên hạng 1")
    band(bd, pg, 3)
    pl = va["failloc_prompt"].split("\n")
    fails = [l.lstrip("- ").rstrip(": ") for l in pl[pl.index("Failing tests:") + 1:] if l.startswith("- ")]
    top = va["failloc_top5"]
    bd.A(pg, viz.flow("luong", 30, Y, [
        ("Mã nguồn đánh số dòng", [f"{n}: {code[n]}" for n in (25, 26, 28, gt)]),
        ("+ Test fail", fails + [f"{va['n_fail']} test fail, {va['n_pass']} test pass"]),
        ("Một lượt gọi LLM", ["Prompt cố định:", "“chương trình có đúng", "một dòng lỗi, trả về", "5 dòng đáng nghi nhất”"]),
        ("Kết quả", ["Năm dòng trả về:", _ranks(top), f"dòng lỗi {gt}: hạng {top.index(gt) + 1} ✓"]),
    ], box_w=[250, 210, 180, 180], box_h=H, accent=1, mono={0}))
    _diff(bd, pg, "Khác LLM-Direct ở đúng một chỗ: prompt có thêm tên và thông báo lỗi của test fail (hộp cam).")
    bd.A(pg, P("doc-failloc", 30, 300, 900, [
        ("Đọc sơ đồ", f"Mỗi hộp là một bước, chữ trong hộp là nội dung thật của ví dụ 1 ({va['program']}, lượt chạy 1, "
                      "Gemini 3.8 Flash). Không chèn ràng buộc, không chạy lại test: FailLoc chỉ dùng kết quả test đã có."),
        ("Trên cả tập test", f"Acc@1 của FailLoc là {_acc('repaired', 'llm_tests')}%, của LLM-Direct là "
                             f"{_acc('repaired', 'llm_direct')}% (nhãn đã chuẩn hóa, trung bình 3 lần chạy)."),
    ], size=15, h=170))

    # SemLoc−Bonus on example 1
    pg = "luong_semloc_bonus.svg"
    guess = va["guess_line"]
    bonus = next(r["bonus"] for r in va["line_scores"] if r["line"] == guess)
    cons = va["constraints"]
    _title(bd, pg, f"Bỏ điểm thưởng, SemLoc không còn xếp được dòng nào ở ví dụ 1")
    band(bd, pg, 3)
    n_viol = sum(c["ef"] > 0 for c in cons)
    bd.A(pg, viz.flow("luong", 30, Y, [
        ("1. LLM viết ràng buộc", [f"{c['id']}: {c['expr'].replace('__cbfl_result', 'ret').replace('__1', '')}"
                                   for c in cons] + [f"đoán dòng lỗi: {guess}"]),
        ("2. Chèn, chạy test", [f"{va['n_fail']} test fail,", f"{va['n_pass']} test pass;", f"{n_viol} ràng buộc bị",
                                "test fail vi phạm"]),
        ("3. Phổ vi phạm", ["Ochiai = 0", "ở mọi dòng"]),
        ("4. Cộng thưởng", [f"+{_p(bonus, 1)} cho dòng {guess}", "(dòng LLM đoán)"]),
        ("Kết quả", ["SemLoc:", f"dòng {guess} hạng 1 ✗", "SemLoc−Bonus: không", "xếp được dòng nào"]),
    ], box_w=[236, 150, 116, 140, 170], box_h=H, gap=22, accent=3, struck={3}, mono={0}))
    _diff(bd, pg, "Khác SemLoc ở đúng một chỗ: bỏ bước cộng thưởng cho dòng LLM đoán (hộp gạch chéo).")
    g = "original" if bd.EARLY() else "repaired"
    bd.A(pg, P("doc-semloc-bonus", 30, 300, 900, [
        ("Đọc sơ đồ", f"Dòng lỗi là {gt}. Không ràng buộc nào bị vi phạm nên điểm phổ bằng 0 ở mọi dòng; hạng 1 của SemLoc "
                      f"ở ví dụ này đến hoàn toàn từ dòng LLM đoán ({va['program']}, lượt chạy 1, Gemini 3.8 Flash)."),
        ("Trên cả tập test", f"bỏ điểm thưởng thì Acc@1 giảm từ {_acc(g, 'semloc')}% (SemLoc) xuống "
                             f"{_acc(g, 'semloc_no_prior')}% (SemLoc−Bonus), "
                             + ("nhãn gốc." if g == "original" else "nhãn đã chuẩn hóa.")),
    ], size=15, h=170))

    # FailLoc+Cov on example 2
    pg = "luong_cov.svg"
    cr = cov_example()
    ccode = {c["no"]: c["text"].strip() for c in cr["code_lines"]}
    cgt = cr["label_lines"][0]
    fp = lambda n: "[f={}/p={}]".format(*cr["fp"][str(n)])
    cfails = [l.lstrip("- ").rstrip(": ") for l in cr["cov_prompt"].split("\n") if l.startswith("- test_")]
    fl, cv = cr["failloc_top5"][0], cr["cov_top5"][0]
    rv = cr["reviewed_lines"]
    other = [n for n in rv if n != cgt]
    _title(bd, pg, f"Luồng FailLoc+Cov trên ví dụ 3: độ phủ đưa dòng {cgt} lên hạng 1")
    band(bd, pg, 3)
    bd.A(pg, viz.flow("luong", 30, Y, [
        ("Mã nguồn + độ phủ [f/p]", [f"{fp(n)} {n}: {ccode[n]}" for n in (68, 71, cgt)]),
        ("+ Test fail", cfails[:3] + [f"({cr['n_fail']} fail, {cr['n_pass']} pass)"]),
        ("Một lượt gọi LLM", ["Prompt như FailLoc,", "thêm câu giải thích", "[f/p] ở đầu"]),
        ("Kết quả", ["FailLoc:", f"{_ranks(fl[:4])} → hạng {fl.index(cgt) + 1}",
                     "FailLoc+Cov:", f"{_ranks(cv[:4])} → hạng {cv.index(cgt) + 1} ✓"]),
    ], box_w=[280, 190, 150, 200], box_h=H, accent=0, mono={0, 1}))
    _diff(bd, pg, "Khác FailLoc ở đúng một chỗ: mỗi dòng mã có thêm [f/p] (hộp cam).")
    bd.A(pg, P("doc-cov", 30, 300, 900, [
        ("Đọc sơ đồ", f"[f/p] là số test fail và số test pass chạy qua dòng đó. Dòng {cgt} là {fp(cgt)}: chỉ test fail chạy "
                      f"tới nó, và FailLoc+Cov xếp nó hạng 1 ở cả 3 lần chạy ({cr['program']}, Gemini 3.8 Flash)."),
        ("Phụ thuộc bộ nhãn", f"Theo nhãn đã chuẩn hóa (dòng {cgt}), độ phủ đẩy dòng lỗi từ hạng {fl.index(cgt) + 1} lên "
                              f"hạng 1. Nhãn đã rà soát tính cả dòng {', '.join(map(str, other))} (câu if) là lỗi, và FailLoc "
                              "đã xếp dòng đó hạng 1: ở bộ nhãn này độ phủ không thêm gì."),
        ("Trên cả tập test", f"thêm độ phủ đổi Acc@1 của FailLoc {m('AblRepairedAllCoverageEffectDAccOne')} điểm (nhãn đã "
                             "chuẩn hóa)."),
    ], size=14, h=196))


def notes(bd) -> dict:
    m = bd._m
    va = examples()["votes_apportion"]
    cr = cov_example()
    gt, cgt = va["label_lines"][0], cr["label_lines"][0]
    g = "original" if bd.EARLY() else "repaired"
    le = _label_example()
    o, n = le["original"][0], le["lines"][0]
    return {
        "luong_chuan_hoa": f"Đây là một nhãn được chuẩn hóa từ đầu đến cuối. Chương trình {LABEL_EXAMPLE} có nhãn gốc ở dòng {o}. "
                           f"Cả {le['n_fail']} test fail đều gọi clamp bằng True nên bỏ qua khối if, không test fail nào chạy tới "
                           f"dòng {o}. Nhóm nhờ LLM đề xuất bản sửa nhỏ cho các dòng lân cận; ở dòng {n}, bỏ chữ not, chỉ một "
                           f"token. Chạy lại cả bộ test thì mọi test pass, nên nhãn dời sang dòng {n}. LLM chỉ đề xuất, test "
                           "mới quyết định.",
        "luong_failloc": f"Đây là luồng của phương pháp FailLoc trên ví dụ 1. Đầu vào là mã nguồn đánh số dòng, cộng thêm tên "
                         "test fail, đó là hộp cam, chỗ duy nhất khác LLM-Direct. Prompt cố định nói chương trình có đúng một "
                         "dòng lỗi và yêu cầu năm dòng đáng nghi nhất. Một lượt gọi LLM trả về "
                         f"{', '.join(map(str, va['failloc_top5']))}: dòng lỗi {gt} đứng hạng 1. Trên cả tập test, FailLoc đạt "
                         f"{_acc('repaired', 'llm_tests')}% Acc@1, LLM-Direct {_acc('repaired', 'llm_direct')}%.",
        "luong_semloc_bonus": "SemLoc−Bonus là SemLoc bỏ bước cộng thưởng. Trên ví dụ 1, LLM viết bốn ràng buộc và đoán dòng "
                              f"{va['guess_line']}. Chạy test thì không ràng buộc nào bị vi phạm, nên điểm phổ bằng 0 ở mọi dòng. "
                              f"SemLoc vẫn xếp dòng {va['guess_line']} hạng 1, chỉ nhờ điểm thưởng 1,2, và sai vì dòng lỗi là "
                              f"{gt}. Gạch bước thưởng đi thì không còn dòng nào được xếp. Trên cả tập test, bỏ thưởng làm Acc@1 "
                              f"giảm từ {_acc(g, 'semloc')}% xuống {_acc(g, 'semloc_no_prior')}%.",
        "luong_cov": f"FailLoc+Cov giống FailLoc, chỉ thêm độ phủ: mỗi dòng có thêm hai số f và p, là số test fail và số test pass chạy qua nó. "
                     f"Nhóm chọn ví dụ 3, {cr['program']}, vì ở ví dụ 1 dòng nào cũng như nhau. Ở đây dòng {cgt} chỉ được test "
                     f"fail chạy qua, và FailLoc+Cov xếp nó hạng 1 ở cả ba lần chạy, còn FailLoc xếp hạng 2. Nhưng mức lợi "
                     f"này phụ thuộc bộ nhãn: nhãn đã rà soát tính cả câu if ngay trên là lỗi, và FailLoc đã xếp câu if hạng "
                     f"1. Trên cả tập test, thêm độ phủ làm Acc@1 đổi {m('AblRepairedAllCoverageEffectDAccOne')} điểm, nên "
                     "thông tin của test fail mới là thứ tạo ra khác biệt.",
    }

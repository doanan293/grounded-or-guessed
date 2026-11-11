"""Build the Vietnamese decks from template-vi.pptx pages: báo cáo lần 1, 2, 3 and bảo vệ.

Re-runnable: every page is rebuilt from the pristine imported SVG kept in orig/.
    python3 docs/presentation/build/build_deck.py lan1|lan2|lan3|baove   (workspace: see README.md)
Every number is read from data/ (repaired ground truth unless stated).
"""
import json
import shutil
import textwrap
import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).parent))
from slidekit import append, drop_group, edit  # noqa: E402

WS = Path(__file__).resolve().parents[3] / "runs" / "slides" / "bao-cao-lan-1_20261108"
SVG = WS / "authoring-svg-flat"
ORIG = WS / "orig"
ROOT = Path(__file__).resolve().parents[3]

BODY = '&quot;Be Vietnam Pro&quot;, sans-serif'
MONO = '&quot;IBM Plex Mono&quot;, sans-serif'
ORANGE, LAVENDER, INK, NAVY, CREAM = "#EB9109", "#BFBEF7", "#1D1D1D", "#0C0A9E", "#FDF1DE"

# svg page name -> source slide of template-vi.pptx
SOURCE = {
    "slide_01.svg": 1, "slide_03.svg": 3, "slide_04.svg": 4, "slide_05.svg": 5, "slide_08.svg": 8, "slide_25.svg": 25,
    "slide_09.svg": 9, "slide_22.svg": 22, "slide_11.svg": 11, "chuong02.svg": 4, "slide_20.svg": 20,
    "slide_19.svg": 19, "thiet_ke.svg": 11, "chuong03.svg": 4, "slide_14.svg": 14, "ket_qua_thu.svg": 22,
    "ket_qua_rq3.svg": 22, "pareto.svg": 22, "slide_21.svg": 21, "slide_30.svg": 30,
    "chuong04.svg": 4, "that_bai.svg": 22, "mo_ho.svg": 14, "mau_loi.svg": 11, "dong_gop.svg": 11,
    "triet_ly.svg": 19, "de_doa.svg": 9, "ket_luan.svg": 5,
    "chuong_nhom.svg": 4, "nhom.svg": 22, "phan_cong.svg": 22, "cong_cu_ai.svg": 22, "hien_trang.svg": 22,
}
INTRO = ["slide_04.svg", "slide_05.svg", "slide_08.svg", "slide_25.svg", "slide_09.svg", "slide_22.svg", "slide_11.svg"]
METHOD = ["chuong02.svg", "slide_20.svg", "slide_19.svg", "thiet_ke.svg"]
RESULTS = ["slide_14.svg", "ket_qua_thu.svg", "ket_qua_rq3.svg", "pareto.svg"]
ANALYSIS = ["chuong04.svg", "that_bai.svg", "mo_ho.svg", "mau_loi.svg", "dong_gop.svg", "triet_ly.svg", "de_doa.svg"]
GROUP = ["chuong_nhom.svg", "nhom.svg", "phan_cong.svg", "cong_cu_ai.svg", "hien_trang.svg"]
DECKS = {
    # report 1 (11/11): the group, its work split, AI tools, status after week 1; background, RQs, design, RQ1 only
    # 15 pages: no table of contents, no section dividers
    "lan1": ["slide_01.svg", "nhom.svg", "phan_cong.svg", "cong_cu_ai.svg", "hien_trang.svg", "slide_05.svg",
             "slide_08.svg", "slide_25.svg", "slide_09.svg", "slide_20.svg", "slide_19.svg", "thiet_ke.svg", "slide_14.svg",
             "slide_21.svg", "slide_30.svg"],
    # report 2 (18–19/11): + repaired labels and the main comparison; no RQ3 / cross-model cost yet
    "lan2": ["slide_01.svg", "slide_03.svg", *INTRO, *METHOD, "chuong03.svg", "slide_14.svg", "ket_qua_thu.svg",
             "slide_21.svg", "slide_30.svg"],
    # report 3 (25–26/11): + RQ3, cost, contributions; failure analysis waits for the final submission
    "lan3": ["slide_01.svg", "slide_03.svg", "slide_20.svg", *RESULTS, "chuong04.svg", "dong_gop.svg", "triet_ly.svg",
             "de_doa.svg", "slide_21.svg", "slide_30.svg"],
    "baove": ["slide_01.svg", "slide_03.svg", *INTRO, *METHOD, "chuong03.svg", *RESULTS, *ANALYSIS, "ket_luan.svg",
              "slide_30.svg"],
}
OCCASION = {"lan1": "Báo cáo lần 1 · 11/11/2026", "lan2": "Báo cáo lần 2 · 18/11/2026", "lan3": "Báo cáo lần 3 · 25/11/2026",
            "baove": "Bảo vệ tiểu luận · 12/2026"}
OUT_NAME = {"lan1": "bao-cao-lan-1.pptx", "lan2": "bao-cao-lan-2.pptx", "lan3": "bao-cao-lan-3.pptx", "baove": "bao-ve.pptx"}
DECK = "lan1"
PAGES: list = []


def EARLY() -> bool:
    """Reports 1 and 2: original + repaired labels only, no ablation / additions / RQ3 yet."""
    return DECK in ("lan1", "lan2")


def fresh() -> None:
    if not ORIG.exists():
        ORIG.mkdir()
        for f in SVG.glob("slide_*.svg"):
            shutil.copy(f, ORIG / f.name)
    for f in ORIG.glob("slide_*.svg"):  # every template page back to pristine
        shutil.copy(f, SVG / f.name)
    for f in SVG.glob("*.svg"):  # named pages of a previously built deck must not leak into this one
        if not f.name.startswith("slide_") and not has(f.name):
            f.unlink()
    for src, name in PAGES:
        shutil.copy(ORIG / f"slide_{src:02d}.svg", SVG / name)


def has(name: str) -> bool:
    return any(n == name for _, n in PAGES)


def E(name, mapping):  # edit text on a page of this deck (no-op for pages the deck does not use)
    if has(name):
        edit(SVG / name, mapping)


def A(name, fragment):
    if has(name):
        append(SVG / name, fragment)


def D(name, gid):
    if has(name):
        drop_group(SVG / name, gid)


def table(gid: str, x: float, y: float, widths: list, rows: list, highlight_col=None,
          row_h=52.0, head_h=40.0, fs=15.0, note=None) -> str:
    """Canonical editable grid: header row in mono bold on lavender, body rows in Be Vietnam Pro."""
    w = sum(widths)
    note_lines = note.split("\n") if note else []
    h = head_h + row_h * (len(rows) - 1) + 20 * len(note_lines) + (10 if note else 0)
    out = [f'<g id="{gid}" data-pptx-bounds="{x} {y} {w} {h}">']
    cy = y
    for r, row in enumerate(rows):
        rh = head_h if r == 0 else row_h
        cx = x
        for c, cell in enumerate(row):
            fill = LAVENDER if r == 0 else (CREAM if c == highlight_col else "#FFFFFF")
            out.append(f'<rect x="{cx}" y="{cy}" width="{widths[c]}" height="{rh}" fill="{fill}" stroke="{ORANGE}" stroke-width="1.5"/>')
            lines = str(cell).split("\n")
            family, weight = (MONO, "bold") if r == 0 or c == 0 else (BODY, "bold" if c == highlight_col else "normal")
            size = fs + 1 if r == 0 else fs
            lh = size * 1.25
            ty = cy + rh / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
            first, rest = escape(lines[0]), "".join(f'<tspan x="{cx + 8}" dy="{lh}">{escape(l)}</tspan>' for l in lines[1:])
            out.append(f'<text x="{cx + 8}" y="{round(ty, 2)}" font-family="{family}" font-size="{size}" '
                       f'font-weight="{weight}" fill="{INK}">{first}{rest}</text>')
            cx += widths[c]
        cy += rh
    for k, line in enumerate(note_lines):
        out.append(f'<text x="{x}" y="{cy + 22 + 18 * k}" font-family="{BODY}" font-size="13" font-style="italic" fill="#555555">{escape(line)}</text>')
    out.append("</g>")
    return "".join(out)


def _csv(name: str) -> list[dict]:
    import csv
    with open(ROOT / "data" / name) as f:
        return list(csv.DictReader(f))


def _m(name: str) -> str:
    """Value of a macro in the Vietnamese numbers file (same numbers as the report)."""
    import re
    text = (ROOT / "docs" / "report" / "generated" / "numbers-vi.tex").read_text()
    return re.search(r"\\newcommand\{\\" + name + r"\}\{([^}]*)\}", text).group(1)


def _p(v) -> str:
    """percent with a Vietnamese decimal comma, e.g. 0.4930 -> 49,3"""
    return f"{100 * float(v):.1f}".replace(".", ",")


def results_pages() -> None:
    """RQ2 table, RQ3 table and the cost/accuracy figure — all numbers read from data/ (repaired GT)."""
    rq2 = {r["method"]: r for r in _csv("rq2_ours.csv") if r["gt"] == "repaired" and r.get("subset", "all") == "all"}
    cost = _csv("llm_cost.csv")
    tok = lambda prefix: f"{round(sum(float(r['tokens_per_program']) for r in cost if r['run_id'].startswith(prefix)) / max(1, sum(r['run_id'].startswith(prefix) for r in cost)) / 1000, 1)}k".replace(".", ",")
    rev = {r["method"]: r for r in _csv("rq2_ours.csv") if r["gt"] == "reviewed" and r.get("subset", "all") == "all"}
    names = [("sbfl_ochiai", "SBFL Ochiai", "0"), ("llm_direct", "LLM hỏi thẳng", tok("direct_test_gemini_r")),
             ("semloc", "SemLoc (bản gốc)", tok("semloc_test_gemini_r")),
             ("semloc_no_prior", "SemLoc bỏ thưởng ẩn", tok("semloc_test_gemini_r")),
             ("llm_tests", "1 prompt + test fail (nhóm)", tok("direct_tests_test_gemini_r")),
             ("llm_coverage", "  … + độ phủ từng dòng", tok("direct_cov_test_gemini_r"))]
    orig = {r["method"]: r for r in _csv("rq2_ours.csv") if r["gt"] == "original" and r.get("subset", "all") == "all"}
    head = f"Gemini 3.8 Flash, tập test, 3 lần chạy. 1 prompt + test fail vs SemLoc, Acc@1 (đã sửa): " \
           f"{_m('RqTwoRepairedAllLlmTestsDAccOne')} [{_m('RqTwoRepairedAllLlmTestsDAccOneLo')}; {_m('RqTwoRepairedAllLlmTestsDAccOneHi')}].\n"
    if EARLY():  # report 1: original + repaired labels, no ablation / additions yet
        A("ket_qua_thu.svg", table("bang-rq2", 84, 128, [330, 115, 115, 115, 133], [
            ["Phương pháp", "Acc@1\nđã sửa", "Acc@3\nđã sửa", "Acc@1\ngốc", "Token/CT"],
            *[[label, _p(rq2[m]["acc1_mean"]), _p(rq2[m]["acc3_mean"]), _p(orig[m]["acc1_mean"]), t]
              for m, label, t in names if m != "llm_coverage"],
        ], highlight_col=None, head_h=48, row_h=40, fs=16,
            note=head + "Đang làm: thông tin nào trong prompt tạo ra khác biệt, các cách bổ sung, rà soát nhãn."))
    else:
        tail = ("Kiểm chứng bằng bản sửa, biểu quyết (dev), ruff, pyrefly: không giúp." if DECK == "baove"
                else "CovGate, biểu quyết (dev), ruff, pyrefly: không giúp.")
        A("ket_qua_thu.svg", table("bang-rq2", 84, 128, [330, 115, 115, 115, 133], [
            ["Phương pháp", "Acc@1\nđã sửa", "Acc@3\nđã sửa", "Acc@1\nrà soát", "Token/CT"],
            *[[label, _p(rq2[m]["acc1_mean"]), _p(rq2[m]["acc3_mean"]), _p(rev[m]["acc1_mean"]), t] for m, label, t in names],
        ], highlight_col=None, head_h=48, row_h=38, fs=16,
            note=head + f"Thêm độ phủ: Acc@1 {_m('AblRepairedAllCoverageEffectDAccOne')} điểm. " + tail))
    bip = {(r["subset"], r["method"]): r for r in _csv("rq3_bugsinpy.csv")}
    ren = {r["method"]: r for r in _csv("rq3_renamed.csv") if r["gt"] == "repaired"}
    fam = [r for r in _csv("rq3_families.csv") if r["gt"] == "repaired"]
    rng = lambda m: (f"{_p(min(float(r['acc1_mean']) for r in fam if r['method'] == m))}–"
                     f"{_p(max(float(r['acc1_mean']) for r in fam if r['method'] == m))}")
    a = lambda m: bip[("all", m)]
    A("ket_qua_rq3.svg", table("bang-rq3", 84, 128, [250, 140, 140, 140, 138], [
        ["Thí nghiệm", "SemLoc", "Chỉ dòng\nLLM đoán", "Chỉ phổ\nngữ nghĩa", "SBFL"],
        [f"BugsInPy: {a('semloc_prior')['n']} lỗi thật\n(Acc@1)", _p(a("semloc_prior")["acc1_mean"]),
         _p(a("llm_guess")["acc1_mean"]), _p(a("semloc_spectrum")["acc1_mean"]), _p(a("sbfl_ochiai")["acc1_mean"])],
        [f"Đổi tên biến, {ren['semloc']['n']} CT\n(Acc@3: gốc → đổi tên)",
         f"{_p(ren['semloc']['orig_acc3_mean'])} → {_p(ren['semloc']['renamed_acc3_mean'])}",
         f"{_p(ren['llm_guess']['orig_acc3_mean'])} → {_p(ren['llm_guess']['renamed_acc3_mean'])}",
         f"{_p(ren['semloc_no_prior']['orig_acc3_mean'])} → {_p(ren['semloc_no_prior']['renamed_acc3_mean'])}", "—"],
        [f"{len({r['family'] for r in fam})} họ model, {fam[0]['n']} CT\n(Acc@1, khoảng)", rng("semloc"), "—", rng("semloc_no_prior"), "—"],
    ], highlight_col=2, head_h=52, row_h=62, fs=16,
        note="Lỗi thật: mọi lần SemLoc đúng ở hạng 1 đều là dòng LLM tự đoán. Đổi tên: dòng đoán gần như giữ nguyên,\n"
             "phổ ngữ nghĩa giảm mạnh (p<0,001). Họ model: tập con nhỏ, chưa đủ để xếp hạng các model."))
    semloc_runs = [r for r in cost if r["run_id"].startswith("semloc_test_gemini_r")]
    cf_share = round(100 * sum(int(r["calls_t0"]) for r in semloc_runs) / sum(int(r["calls"]) for r in semloc_runs))
    png = WS / "images" / "pareto_rq.png"
    import subprocess
    subprocess.run(["pdftoppm", "-png", "-r", "300", "-singlefile", str(ROOT / "docs" / "report" / "generated" / "vi" / "pareto.pdf"),
                    str(png.with_suffix(""))], check=True)
    A("pareto.svg",
           f'<g id="hinh-pareto" data-pptx-bounds="84 120 480 371"><image x="84" y="120" width="480" height="371" '
           f'href="../images/pareto_rq.png" preserveAspectRatio="xMidYMid meet"/></g>'
           + _para("ket-luan-pareto", 590, 150, 300, 300, [
               (20, NAVY, "bold", ["1 prompt rẻ hơn ở", "mọi mô hình"]),
               (16, INK, "normal", [f"Cùng {_csv('pareto.csv')[0]['n']} chương trình, ở cả 5 họ", "model: 1 prompt có Acc@3",
                                    "cao hơn SemLoc và tốn ít token hơn", "(với lỗi được test fail chạy tới)."]),
               (16, INK, "normal", [f"Bước vá thử (CF) chiếm {cf_share}% lượt", "gọi LLM nhưng không cải thiện có",
                                    "ý nghĩa thống kê."])]))


def _para(gid, x, y, w, h, paras) -> str:
    """One <text> per paragraph: first line direct, later lines as positioned tspans (editable text frame)."""
    out, cy = [f'<g id="{gid}" data-pptx-bounds="{x} {y} {w} {h}" font-family="{BODY}">'], y + 30
    for size, color, weight, lines in paras:
        lh = round(size * 1.3, 1)
        rest = "".join(f'<tspan x="{x}" dy="{lh}">{escape(l)}</tspan>' for l in lines[1:])
        out.append(f'<text x="{x}" y="{cy}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(lines[0])}{rest}</text>')
        cy += lh * len(lines) + size * 0.9
    return "".join(out) + "</g>"


def build() -> None:
    fresh()
    E("slide_01.svg", {
        "Introduction to Coding Workshop": ["Grounded or", "Guessed?"],
        "Here is where your presentation begins": ["Tái hiện và đánh giá định vị lỗi bằng LLM",
                                                   f"Nhóm M9 · {OCCASION[DECK]}"],
    })
    toc = {
        "lan1": [("Nhóm & tiến độ", ["Thành viên, phân công,", "công cụ AI, hiện trạng"]),
                 ("Bối cảnh", ["Vấn đề, nghiên cứu liên quan,", "SemLoc"]),
                 ("Phương pháp", ["3 câu hỏi, đề xuất,", "thiết kế thực nghiệm"]),
                 ("Kết quả RQ1", ["Tái hiện, thưởng ẩn,", "nhãn; kế hoạch"])],
        "lan2": [("Bối cảnh", ["Vấn đề, nghiên cứu liên quan,", "SemLoc"]),
                 ("Phương pháp", ["3 câu hỏi, đề xuất,", "thiết kế thực nghiệm"]),
                 ("Kết quả RQ1–RQ2", ["Tái hiện, nhãn đã sửa,", "so sánh chính"]),
                 ("Kế hoạch", ["Tiến độ và việc đến lần 3"])],
        "lan3": [("Câu hỏi", ["Nhắc lại 3 câu hỏi", "nghiên cứu"]),
                 ("Kết quả RQ1–RQ3", ["Nhãn rà soát, ablation,", "độ bền, chi phí"]),
                 ("Đóng góp", ["Đóng góp, triết lý", "khoa học, mối đe dọa"]),
                 ("Kế hoạch", ["Tiến độ và việc đến", "bài nộp cuối"])],
    }.get(DECK, [("Bối cảnh", ["Vấn đề, nghiên cứu liên quan,", "SemLoc"]),
                 ("Phương pháp", ["3 câu hỏi, CovGate,", "thiết kế thực nghiệm"]),
                 ("Kết quả RQ1–RQ3", ["Tái hiện, CovGate,", "độ bền, chi phí"]),
                 ("Phân tích & đóng góp", ["Thất bại, đóng góp,", "triết lý khoa học"])])
    E("slide_03.svg", [
        ("Table of contents", "Mục lục"),
        ("Theory lesson", toc[0][0]), ("Features of the topic", toc[1][0]),
        ("Tips", toc[2][0]), ("Practical exercise", toc[3][0]),
        *[(("You can describe the topic", 0), entry[1]) for entry in toc],
    ])
    results_sub = {"lan1": "RQ1 tái hiện và kiểm tra cách đánh giá", "lan2": "RQ1 tái hiện · RQ2 so sánh chính"}
    dividers = [("chuong_nhom.svg", "Nhóm & tiến độ", "Thành viên · phân công · công cụ AI · hiện trạng"),
                ("slide_04.svg", "Bối cảnh", "Vấn đề, nghiên cứu liên quan và SemLoc"),
                ("chuong02.svg", "Phương pháp", "Câu hỏi nghiên cứu, đề xuất, thiết kế thực nghiệm"),
                ("chuong03.svg", "Kết quả", results_sub.get(DECK, "RQ1 tái hiện · RQ2 CovGate · RQ3 độ bền")),
                ("chuong04.svg", "Đóng góp" if DECK == "lan3" else "Phân tích",
                 "Đóng góp · triết lý khoa học · mối đe dọa" if DECK == "lan3" else "Thất bại · đóng góp · triết lý khoa học")]
    for k, (name, title, sub) in enumerate([d for d in dividers if has(d[0])], start=1):
        E(name, {"01": f"{k:02d}", "Theory lesson": title, "You can enter a subtitle": sub})
    E("slide_05.svg", {
        "Introduction": "Vấn đề: lỗi ngữ nghĩa",
        "Mercury is the closest planet to the Sun and the smallest": [
            "**Định vị lỗi dựa trên phổ**", "(SBFL) xếp hạng dòng code", "theo việc test fail và test",
            "pass có chạy qua nó không.", "Với **lỗi ngữ nghĩa**, test pass", "và test fail chạy qua cùng",
            "các dòng → SBFL mất tín", f"hiệu: Acc@1 chỉ {_m('RqOneSbflOchiaiFairAllAccOne')}%."],
        "Mercury takes a little more than 58 days": [
            "**LLM** hiểu ý đồ của code", "nhưng trả lời ngẫu nhiên,", "khó kiểm chứng.",
            "**SemLoc** (2026) bắt LLM viết", "ràng buộc chạy được, rồi để", "kết quả chạy test phán xử:",
            "Acc@1 42,8%.", "→ Nhóm tái hiện và mở rộng."],
    })
    E("slide_08.svg", {
        "What is this topic about?": "Nghiên cứu liên quan",
        "Mercury": "SemLoc", "Venus": "EffiHolmes", "Mars": "Sự cố+LLM",
    })
    for gid in ("shape-1668", "shape-1669", "shape-1670"):  # template body boxes indent and wrap later lines
        D("slide_08.svg", gid)
    # each column explains itself: problem, method, result, what the group takes (wrapped by hand, ~36 chars a line)
    for i, (x, parts) in enumerate((
            (85, [("Bài toán:", "code Python sai logic. Test fail nhưng không báo dòng nào sai."),
                  ("Cách làm:", "LLM đoán dòng nghi và viết điều kiện “đúng thì phải thế này” chèn vào code. Chạy test: "
                                "điều kiện nào bị vi phạm khi test fail thì dòng đó bị nghi nhiều."),
                  ("Kết quả:", "chỉ đúng dòng lỗi ngay hạng 1 ở 42,8% chương trình."),
                  ("Nhóm học được:", "chạy lại đúng mã của tác giả, kiểm tra từng con số họ công bố (RQ1).")]),
            (386, [("Bài toán:", "code chạy chậm. Test vẫn pass, không có lỗi nào báo ra để lần theo."),
                   ("Cách làm:", "chạy 2 lần, với dữ liệu nhỏ và dữ liệu lớn. Hàm nào chậm hẳn đi khi dữ liệu lớn thì bị "
                                 "nghi; chỉ đưa các hàm đó cho LLM chỉ chỗ sửa."),
                   ("Kết quả:", "thử trên 140 lỗi chạy chậm thật."),
                   ("Nhóm học được:", "đặt lần chạy bình thường cạnh lần chạy có vấn đề, chỉ nghi chỗ khác nhau. Nhóm so "
                                      "test pass với test fail để xếp lại các dòng SemLoc đưa ra (CovGate). Mượn cách chia 3 RQ.")]),
            (680, [("Bài toán:", "2 app Java lớn bị sập hàng nghìn lần mỗi tuần; mỗi lần có stack trace (các hàm đang chạy "
                                 "lúc sập)."),
                   ("Cách làm:", "gom stack trace, đếm hàm nào hay xuất hiện thành bảng xếp hạng hàm đáng nghi, rồi đưa "
                                 "bảng vào prompt hỏi LLM lỗi ở đâu."),
                   ("Kết quả:", "38 lỗi thật, chỉ đúng chỗ lỗi 71%."),
                   ("Nhóm học được:", "đưa bằng chứng thật vào prompt giúp LLM trúng hơn. Nhóm thử 1 prompt có test fail "
                                      "(+ độ phủ từng dòng) thay cho quy trình nhiều bước của SemLoc.")]))):
        out, y = [], 298
        for label, text in parts:
            lines = textwrap.wrap(f"{label} {text}", 36)
            color = ORANGE if label.startswith("Nhóm") else NAVY
            for k, line in enumerate(lines):
                if k == 0:  # bold coloured label, then the rest of the first line
                    body = (f'<tspan font-weight="bold" fill="{color}">{escape(label)}</tspan>'
                            f'{escape(line[len(label):])}')
                else:
                    body = escape(line)
                out.append(f'<text x="{x}" y="{y}" font-family="{BODY}" font-size="12.5" fill="{INK}">{body}</text>')
                y += 15
            y += 5
        A("slide_08.svg", f'<g id="cot-{i}" data-pptx-bounds="{x} 288 245 {y - 288}">' + "".join(out) + '</g>')
    E("slide_25.svg", [
        ("Step-by-step coding", "SemLoc hoạt động thế nào"),
        ("Earth", "Neo"), ("It’s the only planet known", ["Chọn vị trí", "đặt kiểm tra"]),
        ("Mercury", "Ràng buộc"), ("Mercury is the closest", ["LLM viết", "ràng buộc"]),
        ("Jupiter", "Chấm điểm"), ("Jupiter is the biggest", ["Chạy test,", "tính Ochiai"]),
        ("Saturn", "Vá thử"), ("Saturn was named", ["LLM vá dòng,", "chạy lại test"]),
    ])
    E("slide_09.svg", [
        ("Features of the topic", "Khoảng trống của SemLoc"),
        ("Mars", "Thưởng ẩn"), ("Despite being red", ["+1,2 cho dòng LLM", "đoán; paper không nói"]),
        ("Neptune", "CF vô hiệu"), ("It’s the farthest", ["Vá thử không đổi", "thứ hạng nào (0/250)"]),
        ("Jupiter", "GT sai"), ("Jupiter is the biggest", ["56 dòng trống, 65 dòng", "test fail không tới"]),
        ("Saturn", "Cách chấm"), ("Saturn is a gas giant", ["Hòa điểm, DD, chạy", "1 lần, không kiểm định"]),
    ])
    for name, title in (("slide_22.svg", "Khác biệt so với các nghiên cứu"), ("ket_qua_thu.svg", "RQ2: 200 chương trình × 3 lần"),
                        ("ket_qua_rq3.svg", "RQ3: lỗi thật, đổi tên, họ model"), ("pareto.svg", "Chi phí – độ chính xác")):
        E(name, {"Classification": title})
        D(name, "shape-2194")
    A("slide_22.svg", table("bang-so-sanh", 84, 135, [176, 158, 158, 158, 158], [
        ["Tiêu chí", "SemLoc", "EffiHolmes", "Sự cố + LLM", "Nhóm mình"],
        ["Loại lỗi", "ngữ nghĩa", "chạy chậm", "sập (Java)", "ngữ nghĩa"],
        ["Tín hiệu", "ràng buộc LLM\n+ chạy test", "so 2 lần chạy\ntải nhỏ / lớn", "stack trace\n+ xếp hạng", "test fail đưa\nthẳng cho LLM"],
        ["Lỗi thật", "7 có kết quả\ncấp dòng", "140 issue", "38 (công nghiệp)",
         "đang dựng\n(lần 3)" if EARLY() else "31 lỗi thật\n× 3 lần chạy"],
        ["Kiểm tra\nbenchmark", "không", "—", "—", "kiểm chứng nhãn\nbằng thực thi" if EARLY() else "rà soát cả\n250 nhãn"],
        ["Lặp + kiểm\nđịnh", "1 lần", "—", "—", "3 lần + McNemar\n/ Wilcoxon"],
    ], highlight_col=4))
    E("slide_11.svg", [
        ("Recommendations", "Học được & áp dụng"),
        ("Mars", "SemLoc"), ("Despite being red, Mars", ["Giả thuyết từ LLM, test", "phán xử; dùng mã gốc"]),
        ("Venus", "EffiHolmes"), ("Venus is the second", ["So 2 lần chạy để", "lọc nhiễu → CovGate"]),
        ("Neptune", "Sự cố+LLM"), ("Neptune is the farthest", ["Đưa xếp hạng cho LLM", "giúp định vị tốt hơn"]),
        ("Mercury", "Pearson 2017"), ("Mercury is the closest", ["Cách chấm khi hòa điểm", "và khi lỗi thiếu code"]),
        ("Saturn", "Thuộc bài"), ("Saturn is a gas giant", ["LLM có thể thuộc bài →", "biến thể đổi tên (RQ3)"]),
        ("Jupiter", "FlexFL"), ("Jupiter is the biggest", ["Gợi ý SBFL cho LLM ở", "cấp hàm → ta cấp dòng"]),
    ])
    E("thiet_ke.svg", [
        ("Recommendations", "Thiết kế thực nghiệm"),
        ("Mars", "Benchmark"), ("Despite being red, Mars", ["SemFault-250, nhãn", "gốc + đã sửa"] if EARLY() else ["SemFault-250, 3 bộ", "nhãn; 31 BugsInPy"]),
        ("Venus", "Biến thể"), ("Venus is the second", ["Đổi tên, BugsInPy:", "lần báo cáo 3"] if EARLY() else ["Đổi tên, xóa docstring", "→ chống thuộc bài"]),
        ("Neptune", "So sánh"), ("Neptune is the farthest", ["SBFL, LLM hỏi thẳng,", "SemLoc, 1 prompt"] if EARLY() else ["SBFL, ruff, SemLoc,", "1 prompt + test fail"]),
        ("Mercury", "Mô hình"), ("Mercury is the closest", ["Gemini 3.8 Flash", "+ 4 họ model khác"]),
        ("Saturn", "Chỉ số"), ("Saturn is a gas giant", ["Acc@1/3/5, thứ hạng,", "%Susp, lượt gọi, token"]),
        ("Jupiter", "Thống kê"), ("Jupiter is the biggest", ["Lặp 3 lần, McNemar /", "Wilcoxon, effect size"]),
    ])
    E("slide_20.svg", [
        ("Popular programming languages", "Câu hỏi nghiên cứu"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: kết quả SemLoc còn đúng", "với log công bố và với Gemini?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["LLM thật sự cần gì? 1 prompt có", "test fail so với SemLoc?"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, code đổi tên,", "các họ model khác?"]),
        ("Saturn", "Lõi"), ("Saturn is a gas giant", ["Cách làm đơn giản (test fail", "→ LLM) có đủ tốt không?"]),
    ])
    E("slide_19.svg", [
        ("Main topic and details", "Đề xuất: 1 prompt có test fail"),
        ("Mars", "Đầu vào"), ("Despite being red", ["Mã nguồn,", "tên test fail,", "dòng lỗi đầu"]),
        *([("Neptune", "1 lượt gọi"), ("It’s the farthest", ["Không pipeline,", "không ràng buộc"]),
           ("Jupiter", "So với"), ("Jupiter is the biggest", ["SemLoc, LLM", "hỏi thẳng, SBFL"]),
           ("Saturn", "Tiếp theo"), ("It’s a gas giant", ["Ablation, bổ", "sung (lần 3)"])] if EARLY() else
          [("Neptune", "Ablation"), ("It’s the farthest", ["Có / không", "độ phủ từng dòng"]),
           ("Jupiter", "Bổ sung"), ("Jupiter is the biggest", ["CovGate,", "kiểm chứng,", "biểu quyết"] if DECK == "baove"
                                                             else ["CovGate,", "biểu quyết"]),
           ("Saturn", "Tĩnh"), ("It’s a gas giant", ["So với ruff,", "pyrefly"])]),
    ])
    dec = next(r for r in _csv("rq_decomposition.csv") if r["game"] == "semloc" and r["gt"] == "repaired"
               and r["subset"] == "all" and r["metric"] == "acc1")
    vgt = json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
    n_corr = sum(1 for v in (vgt.values() if isinstance(vgt, dict) else vgt) if v.get("status") == "corrected")
    E("slide_14.svg", {
        "9h 55m 23s": "13/13", "Jupiter’s rotation period": "cấu hình SemLoc tái hiện khớp từng số",
        "333,000": _m("GtBlankN") if EARLY() else f"{_m('LabaudAllMoved')}/{_m('LabaudAllN')}",
        "The Sun’s mass compared": "nhãn gốc nằm trên dòng trống" if EARLY() else "nhãn gốc bị dời khi rà soát",
        **({"386,000 km": f"{_m('RqOneSemlocGeminiTZeroEightFairAllAccOne')}→{_m('RqOneSemlocGeminiTZeroEightNoPriorFairAllAccOne')}",
            "Distance between the Earth": "Acc@1 SemLoc khi bỏ thưởng ẩn (Gemini)"} if DECK == "lan1" else
           {"386,000 km": _m("RqTwoRepairedAllLlmTestsDAccOne"), "Distance between the Earth": "Acc@1: 1 prompt có test fail so với SemLoc"}),
    })
    if DECK == "lan1":  # no "Kết quả" divider in this deck: the numbers need their own title
        A("slide_14.svg", f'<g id="tieu-de-rq1" data-pptx-bounds="560 50 360 40"><text x="560" y="78" font-family="{BODY}" '
          f'font-size="24" font-weight="bold" fill="{NAVY}">Kết quả RQ1: tái hiện</text></g>')
    E("slide_21.svg", [
        ("Sequences", "Tiến độ"),
        ("First", "05/11"), ("Saturn is composed", "Chốt nhóm, đề tài"),
        (("Next", 0), "11/11"), ("Mercury is the closest", ["Lần 1: nhóm,", "tài liệu, RQ1"]),
        (("Next", 0), "18/11"), ("Jupiter was named", ["Lần 2: nhãn,", "so sánh RQ2"]),
        (("Next", 0), "22/11"), ("Despite being red", ["RQ3, ablation,", "bổ sung"]),
        (("Next", 0), "25/11"), ("Earth is the third", ["Lần 3: đóng góp,", "triết lý"]),
        ("Last", "12/12"), ("Venus has extremely", ["Bài báo arXiv,", "bảo vệ"]),
    ])
    if has("slide_21.svg"):
        t = (SVG / "slide_21.svg").read_text()  # one-line first column: align it with the other top captions
        t = t.replace('x="190.65" y="65.9832021"', 'x="190.65" y="99.1032021"', 1)
        (SVG / "slide_21.svg").write_text(t.replace('y="99.1032021"', 'y="122.1032021"'))  # clear of the page title
    E("slide_30.svg", {
        "Thanks!": "Cảm ơn!",
        "Do you have any questions?": ["Câu hỏi?", "Góp ý?"],
        "Please keep this slide for attribution": f"Nhóm M9 · {OCCASION[DECK]}",
    })
    results_pages()
    group_pages()


def group_pages() -> None:
    """Report 1: members, the work split by work package, AI tools, status after week 1 (mirrors frontmatter/nhom.tex)."""
    for name, title in (("nhom.svg", "Nhóm M9: thành viên"), ("phan_cong.svg", "Phân công theo mảng việc"),
                        ("cong_cu_ai.svg", "Công cụ AI nhóm sử dụng"), ("hien_trang.svg", "Hiện trạng sau tuần đầu (11/11)")):
        E(name, {"Classification": title})
        D(name, "shape-2194")
    A("nhom.svg", table("bang-nhom", 84, 120, [50, 215, 135, 400], [
        ["#", "Họ và tên", "MSHV", "Vai trò chính"],
        ["1", "Doãn Văn An", "20252778M", "Nhóm trưởng: điều phối, phương pháp, viết bài"],
        ["2", "Tạ Công Nam", "20252640M", "Bộ nhãn và duyệt nhãn; phân tích kết quả"],
        ["3", "Nguyễn Hoàng Hải", "20252583M", "Tổng quan tài liệu, bộ từ khóa"],
        ["4", "Đỗ Xuân Tráng", "20252774M", "Lỗi thật BugsInPy (RQ3)"],
        ["5", "Hoàng Trung Kiên", "20251333M", "Mã đổi tên, các họ mô hình (RQ3)"],
        ["6", "Mai Văn Tùng", "20252788M", "Slide"],
        ["7", "Nguyễn Đức Tùng", "20252772M", "Công cụ phân tích tĩnh; kiểm tra số liệu"],
    ], head_h=40, row_h=40, fs=15,
        note="Đã chốt 7 thành viên · đề tài 02-KH (phát hiện và định vị lỗi, hướng nghiên cứu khoa học)\n"
             "Nhóm trưởng Doãn Văn An: đầu mối liên hệ với giảng viên, giữ kho mã của nhóm."))
    A("phan_cong.svg", table("bang-phan-cong", 84, 112, [400, 200, 200], [
        ["Mảng việc", "Phụ trách chính", "Cùng thực hiện"],
        ["Tài liệu, từ khóa, 3 bài báo được giao", "Nguyễn Hoàng Hải", "Doãn Văn An"],
        ["Hạ tầng LLM, tái hiện SemLoc, RQ1", "Doãn Văn An", "Tạ Công Nam"],
        ["Bộ nhãn: kiểm chứng, rà soát, duyệt mù", "Tạ Công Nam", "Doãn Văn An;\ncả nhóm duyệt"],
        ["RQ2: prompt đề xuất, ablation,\nbổ sung, phân tích tĩnh", "Doãn Văn An", "Nguyễn Đức Tùng"],
        ["RQ3: BugsInPy, mã đổi tên,\ncác họ mô hình", "Đỗ Xuân Tráng,\nHoàng Trung Kiên", "Doãn Văn An"],
        ["Phân tích thất bại, đóng góp,\ntriết lý khoa học", "Doãn Văn An", "Tạ Công Nam,\nHoàng Trung Kiên"],
        ["Báo cáo, bài báo arXiv, slide,\ngói tái hiện", "Doãn Văn An", "Mai Văn Tùng,\nNguyễn Đức Tùng"],
    ], head_h=38, row_h=48, fs=14,
        note="Chia theo mảng việc của cả tiểu luận; nhóm trưởng gánh phần lớn khối lượng."))
    A("cong_cu_ai.svg", table("bang-cong-cu-ai", 84, 125, [220, 580], [
        ["Công cụ", "Dùng để làm gì"],
        ["Claude Code\n(Anthropic)", "Trợ lý chính: đọc tài liệu, viết mã và kiểm thử,\nchạy thực nghiệm, soạn LaTeX và slide"],
        ["LLM thực nghiệm\n(qua proxy)", "Gemini 3.8 Flash (chính), Claude Sonnet 4.6 (đối chiếu bài gốc);\nRQ3: Gemini 3.5 Flash-Lite, Claude Sonnet 5.5, GPT-6 luna, gpt-oss-120b"],
        ["Kiểm soát", "Nhóm trưởng duyệt mọi thay đổi; số liệu sinh tự động\ntừ dữ liệu; mọi lượt gọi LLM có nhật ký và bộ đệm"],
    ], head_h=40, row_h=66, fs=15))
    A("hien_trang.svg", table("bang-hien-trang", 84, 112, [215, 425, 160], [
        ["Nội dung", "Hiện trạng", "Tự đánh giá"],
        ["1. Tài liệu, từ khóa", "3 bài được giao + tài liệu thêm, bộ từ khóa,\nbảng so sánh", "Đạt"],
        ["2. RQ, thực nghiệm", "3 RQ, thiết kế; hạ tầng LLM; tái hiện SemLoc;\ncó kết quả RQ1. RQ2 đang chạy", "Đang làm,\nđúng tiến độ"],
    ], head_h=40, row_h=56, fs=15,
        note="Khó khăn: chạy lại SemLoc không khớp nhật ký công bố; hạn mức gọi LLM; dựng môi trường BugsInPy.\n"
             "Hướng xử lý: báo cáo cả tính lại và chạy lại; bộ đệm lượt gọi LLM; dựng BugsInPy song song với RQ2."))


def analysis_pages() -> None:
    """Failure analysis, contributions, scientific stance, threats, conclusion — numbers from data/."""
    from collections import Counter
    sig = _csv("failure_signals.csv")
    cat = Counter(r["category"] for r in sig)
    wrong = sum(r["category"] != "guess_right" for r in sig)
    hb = sum(r["category"] != "guess_right" and r["guess_relation"] == "header_body" for r in sig)
    tol = {r["method"]: r for r in _csv("failure_tolerance.csv")}
    off = {(r["method"], r["offset"]): int(r["count"]) for r in _csv("failure_offsets.csv")}
    rq2 = {r["method"]: r for r in _csv("rq2_ours.csv") if r["gt"] == "repaired" and r.get("subset", "all") == "all"}
    dec = next(r for r in _csv("rq_decomposition.csv") if r["game"] == "semloc" and r["gt"] == "repaired"
               and r["subset"] == "all" and r["metric"] == "acc1")
    vgt = json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
    st = Counter(v["status"] for v in vgt)
    for name, title in (("that_bai.svg", f"Phân nhóm {len(sig)} chương trình"),):
        E(name, {"Classification": title})
        D(name, "shape-2194")
    A("that_bai.svg", table("bang-that-bai", 84, 128, [270, 420, 118], [
        ["Nhóm", "Định nghĩa", "Số CT"],
        ["Dòng đoán đúng", "dòng LLM đoán là dòng lỗi chuẩn", str(cat["guess_right"])],
        ["Phổ cứu được", "đoán sai, lỗi vẫn trong top-3", str(cat["rescued_by_spectrum"])],
        ["Thưởng \"gây hại\"", "phổ đúng hạng 1, thưởng đẩy dòng sai lên", str(cat["prior_hurts"])],
        ["Chỉ độ phủ thắng", "SemLoc trượt, LLM + độ phủ trúng top-3", str(cat["coverage_only_wins"])],
        ["GT đáng ngờ", "nhãn chưa kiểm chứng, mọi cách trượt", str(cat["gt_suspect"])],
        ["Mọi cách trượt", "còn lại", str(cat["all_miss"])],
    ], highlight_col=None, head_h=40, row_h=40, fs=16,
        note="Gemini 3.8 Flash, đa số 3 lần chạy, dòng lỗi chuẩn đã sửa. Một nửa số chương trình được giải bằng chính dòng đoán."))
    E("mo_ho.svg", {
        "9h 55m 23s": f"{hb}/{wrong}", "Jupiter’s rotation period": "lần đoán sai là cặp đầu khối – thân khối",
        "333,000": f"{_p(tol['semloc']['acc1_exact'])}→{_p(tol['semloc']['acc1_guard_strict'])}",
        "The Sun’s mass compared": "Acc@1 SemLoc nếu chấp nhận cả hai dòng",
        "386,000 km": f"{off[('llm_guess', '1')]} : {off[('llm_guess', '-1')]}",
        "Distance between the Earth": "lần đoán lệch xuống 1 dòng so với lên 1 dòng",
    })
    E("mau_loi.svg", [
        ("Recommendations", "5 mẫu nguyên nhân thất bại"),
        ("Mars", "Đầu khối"), ("Despite being red, Mars", ["GT ở dòng if, lỗi ở", "câu lệnh nó bảo vệ"]),
        ("Venus", "Khối lỗi"), ("Venus is the second", ["Xóa dòng nào cũng", "sửa được lỗi"]),
        ("Neptune", "Sửa bù trừ"), ("Neptune is the farthest", ["Oracle nhận bản sửa", "đúng test, sai chỗ"]),
        ("Mercury", "Nhân quả"), ("Mercury is the closest", ["Nguyên nhân, triệu", "chứng ở hai dòng"]),
        ("Saturn", "GT đáng ngờ"), ("Saturn is a gas giant", ["Gán cho dòng def", "lồng, bỏ qua [:-1]"]),
        ("Jupiter", "Bài học"), ("Jupiter is the biggest", ["Dùng bằng chứng để", "thu hẹp, đưa cho LLM"]),
    ])
    E("dong_gop.svg", [
        ("Recommendations", "Đóng góp khoa học"),
        ("Mars", "C1 Đoán"), ("Despite being red, Mars", ["Hạng 1 = dòng đoán;", "CF không đổi hạng"]),
        ("Venus", "C2 Nhãn"), ("Venus is the second", [f"{_m('LabaudAllMoved')}/{_m('LabaudAllN')} nhãn bị dời;", "2 bộ nhãn mới"]),
        ("Neptune", "C3 1 prompt"), ("Neptune is the farthest", [f"Acc@1 {_m('RqTwoRepairedAllLlmTestsDAccOne')} điểm,", "rẻ hơn ~7 lần"]),
        ("Mercury", "C4 Âm tính"), ("Mercury is the closest", ["Độ phủ, kiểm chứng", "(dev), ruff: không giúp"] if DECK == "baove"
                                                             else ["Độ phủ, CovGate,", "ruff: không giúp"]),
        ("Saturn", "Cơ chế"), ("Saturn is a gas giant", [f"Sửa lách: {_m('PavmechReviewedOtherLineFixable')}% lần thử", "ở dòng ứng viên sai"]
                                                         if DECK == "baove" else ["Sửa lách kiểm thử", "ở dòng không lỗi"]),
        ("Jupiter", "C5 Tái hiện"), ("Jupiter is the biggest", ["Bảng kiểm 7 mục,", "Docker, số = macro"]),
    ])
    E("triet_ly.svg", [
        ("Main topic and details", "Triết lý khoa học"),
        ("Mars", "Test phán xử"), ("Despite being red", ["…khi test đủ", "chặt; nêu rõ", "ai quyết định"]),
        ("Neptune", "Đo đóng góp"), ("It’s the farthest", ["Phân rã, bỏ", "từng thành phần"]),
        ("Jupiter", "Mốc đơn giản"), ("Jupiter is the biggest", ["Pipeline phải", "thắng 1 prompt"]),
        ("Saturn", "Chịu bác bỏ"), ("It’s a gas giant", ["Lặp 3 lần, CI,", "nêu cả âm tính"]),
    ])
    E("de_doa.svg", [
        ("Features of the topic", "Các mối đe dọa"),
        ("Mars", "Vòng tròn"), ("Despite being red", ["Nhãn rà soát do LLM", "gợi ý; báo cả 3 bộ"]),
        ("Neptune", "Lỗi thật ít"), ("It’s the farthest", ["31 lỗi, 1 dự án;", "CI còn chứa 0"]),
        ("Jupiter", "Mô hình"), ("Jupiter is the biggest", ["Suy luận mặc định,", "mô hình mới hơn"]),
        ("Saturn", "Tên test"), ("Saturn is a gas giant", ["Tên test nói rõ ý", "định; 1 hàm/lần"]),
    ])
    E("ket_luan.svg", {
        "Introduction": "Kết luận",
        "Mercury is the closest planet to the Sun and the smallest": [
            "**Grounded hay guessed?**", "Hạng 1 luôn là dòng LLM", "đoán (theo thiết kế).", f"{_m('LabaudAllMoved')}/{_m('LabaudAllN')} nhãn gốc bị",
            "dời; nhãn lệch có lợi", "cho SemLoc."],
        "Mercury takes a little more than 58 days": [
            "**Đề xuất**", "Đưa test fail cho LLM:", f"Acc@1 {_p(rq2['llm_tests']['acc1_mean'])} so với {_p(rq2['semloc']['acc1_mean'])},",
            "rẻ hơn ~7 lần. Độ phủ,", "kiểm chứng (dev), ruff:", "không giúp. Bảng kiểm 7 mục."],
    })


def main(deck: str) -> None:
    global DECK, PAGES
    DECK = deck
    PAGES = [(SOURCE[n], n) for n in DECKS[deck]]
    build()
    analysis_pages()
    json.dump({"schema": "ppt-master.roundtrip-page-plan.v1",
               "pages": [{"source_slide": s, **({} if n == f"slide_{s:02d}.svg" else {"svg": n})} for s, n in PAGES]},
              open(WS / "page_plan.json", "w"), indent=2)
    print(f"built {deck}: {len(PAGES)} pages → {OUT_NAME[deck]}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "lan1")

"""Build the Vietnamese decks from template-vi.pptx pages: báo cáo lần 1, báo cáo lần 2, bảo vệ.

Re-runnable: every page is rebuilt from the pristine imported SVG kept in orig/.
    python3 docs/presentation/build/build_deck.py lan1|lan2|baove   (workspace: see README.md)
Every number is read from data/ (repaired ground truth unless stated).
"""
import json
import shutil
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
}
INTRO = ["slide_04.svg", "slide_05.svg", "slide_08.svg", "slide_25.svg", "slide_09.svg", "slide_22.svg", "slide_11.svg"]
METHOD = ["chuong02.svg", "slide_20.svg", "slide_19.svg", "thiet_ke.svg"]
RESULTS = ["slide_14.svg", "ket_qua_thu.svg", "ket_qua_rq3.svg", "pareto.svg"]
ANALYSIS = ["chuong04.svg", "that_bai.svg", "mo_ho.svg", "mau_loi.svg", "dong_gop.svg", "triet_ly.svg", "de_doa.svg"]
DECKS = {
    "lan1": ["slide_01.svg", "slide_03.svg", *INTRO, *METHOD, "chuong03.svg", *RESULTS, "slide_21.svg", "slide_30.svg"],
    "lan2": ["slide_01.svg", "slide_03.svg", "slide_20.svg", *RESULTS, *ANALYSIS, "slide_21.svg", "slide_30.svg"],
    "baove": ["slide_01.svg", "slide_03.svg", *INTRO, *METHOD, "chuong03.svg", *RESULTS, *ANALYSIS, "ket_luan.svg",
              "slide_30.svg"],
}
OCCASION = {"lan1": "Báo cáo lần 1 · 18/11/2026", "lan2": "Báo cáo lần 2 · 25/11/2026", "baove": "Bảo vệ tiểu luận · 12/2026"}
OUT_NAME = {"lan1": "bao-cao-lan-1.pptx", "lan2": "bao-cao-lan-2.pptx", "baove": "bao-ve.pptx"}
DECK = "lan1"
PAGES: list = []


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


def _p(v) -> str:
    """percent with a Vietnamese decimal comma, e.g. 0.4930 -> 49,3"""
    return f"{100 * float(v):.1f}".replace(".", ",")


def results_pages() -> None:
    """RQ2 table, RQ3 table and the cost/accuracy figure — all numbers read from data/ (repaired GT)."""
    rq2 = {r["method"]: r for r in _csv("rq2_ours.csv") if r["gt"] == "repaired" and r.get("subset", "all") == "all"}
    cost = _csv("llm_cost.csv")
    tok = lambda prefix: f"{round(sum(float(r['tokens_per_program']) for r in cost if r['run_id'].startswith(prefix)) / max(1, sum(r['run_id'].startswith(prefix) for r in cost)) / 1000, 1)}k".replace(".", ",")
    names = [("sbfl_ochiai", "SBFL Ochiai", "0"), ("llm_direct", "LLM hỏi thẳng (1 prompt)", tok("direct_test_gemini_r")),
             ("semloc", "SemLoc (bản gốc)", tok("semloc_test_gemini_r")),
             ("semloc_no_prior", "SemLoc bỏ thưởng ẩn", tok("semloc_test_gemini_r")),
             ("covgate", "CovGate (nhóm)", tok("semloc_test_gemini_r")),
             ("llm_coverage", "LLM + độ phủ (1 prompt, nhóm)", tok("direct_cov_test_gemini_r"))]
    n = rq2["semloc"]["n"]
    A("ket_qua_thu.svg", table("bang-rq2", 84, 128, [330, 115, 115, 115, 133], [
        ["Phương pháp", "Acc@1", "Acc@3", "Acc@5", "Token/CT"],
        *[[label, _p(rq2[m]["acc1_mean"]), _p(rq2[m]["acc3_mean"]), _p(rq2[m]["acc5_mean"]), t] for m, label, t in names],
    ], highlight_col=None, head_h=40, row_h=40, fs=16,
        note=f"Gemini 3.8 Flash, {n} chương trình test, ground truth đã sửa bằng thực thi, trung bình 3 lần chạy.\n"
             f"LLM + độ phủ vs SemLoc: Acc@3 p<0,001 (McNemar). Bỏ thưởng ẩn: −{_p(float(rq2['semloc']['acc1_mean']) - float(rq2['semloc_no_prior']['acc1_mean']))} điểm Acc@1."))
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
             "phổ ngữ nghĩa giảm mạnh (p<0,001). Họ model: model càng yếu càng phụ thuộc vào điểm thưởng cho dòng đoán."))
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
               (20, NAVY, "bold", ["Một prompt có độ phủ", "thắng pipeline ở top-3"]),
               (16, INK, "normal", [f"Cùng {_csv('pareto.csv')[0]['n']} chương trình, ở cả 5 họ", "model: LLM + độ phủ có Acc@3",
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
        "Here is where your presentation begins": ["Kiểm chứng bằng thực thi: định vị lỗi bằng LLM",
                                                   f"Nhóm M9 · {OCCASION[DECK]}"],
    })
    last = ("Kế hoạch", ["Tiến độ và việc đến lần 2"]) if DECK == "lan1" else ("Phân tích & đóng góp", ["Thất bại, đóng góp,", "triết lý khoa học"])
    E("slide_03.svg", [
        ("Table of contents", "Mục lục"),
        ("Theory lesson", "Bối cảnh"), ("Features of the topic", "Phương pháp"),
        ("Tips", "Kết quả RQ1–RQ3"), ("Practical exercise", last[0]),
        (("You can describe the topic", 0), ["Vấn đề, nghiên cứu liên quan,", "SemLoc"]),
        (("You can describe the topic", 0), ["3 câu hỏi, CovGate,", "thiết kế thực nghiệm"]),
        (("You can describe the topic", 0), ["Tái hiện, CovGate,", "độ bền, chi phí"]),
        (("You can describe the topic", 0), last[1]),
    ])
    for name, num, title, sub in (("slide_04.svg", "01", "Bối cảnh", "Vấn đề, nghiên cứu liên quan và SemLoc"),
                                  ("chuong02.svg", "02", "Phương pháp", "Câu hỏi nghiên cứu, CovGate, thiết kế thực nghiệm"),
                                  ("chuong03.svg", "03", "Kết quả", "RQ1 tái hiện · RQ2 CovGate · RQ3 độ bền"),
                                  ("chuong04.svg", "04", "Phân tích", "Thất bại · đóng góp · triết lý khoa học")):
        E(name, {"01": num, "Theory lesson": title, "You can enter a subtitle": sub})
    E("slide_05.svg", {
        "Introduction": "Vấn đề: lỗi ngữ nghĩa",
        "Mercury is the closest planet to the Sun and the smallest": [
            "**Định vị lỗi dựa trên phổ**", "(SBFL) xếp hạng dòng code", "theo việc test fail và test",
            "pass có chạy qua nó không.", "Với **lỗi ngữ nghĩa**, test pass", "và test fail chạy qua cùng",
            "các dòng → SBFL mất tín", "hiệu: Acc@1 chỉ 6,4%."],
        "Mercury takes a little more than 58 days": [
            "**LLM** hiểu ý đồ của code", "nhưng trả lời ngẫu nhiên,", "khó kiểm chứng.",
            "**SemLoc** (2026) bắt LLM viết", "ràng buộc chạy được, rồi để", "kết quả chạy test phán xử:",
            "Acc@1 42,8%.", "→ Nhóm tái hiện và mở rộng."],
    })
    E("slide_08.svg", {
        "What is this topic about?": "Nghiên cứu liên quan",
        "Mercury": "SemLoc", "Venus": "EffiHolmes", "Mars": "Crash+LLM",
        "closest planet to the Sun and the smallest": ["Lỗi ngữ nghĩa.", "LLM + chạy test.", "Acc@1 42,8%."],
        "Venus has a beautiful name": ["Lỗi hiệu năng.", "Profiling 2 tải.", "140 issue thật."],
        "Despite being red, Mars": ["Crash Java,", "38 lỗi thật.", "Định vị 71%."],
    })
    A("slide_08.svg",
           f'<g id="tai-lieu-them" data-pptx-bounds="85 470 790 44"><text x="85" y="488" font-family="{BODY}" font-size="15" fill="{INK}">'
           f'<tspan font-weight="bold">+ 23 tài liệu nhóm tìm thêm: </tspan>SBFL kinh điển (Tarantula, Ochiai, DStar) · định vị lỗi bằng LLM</text>'
           f'<text x="85" y="508" font-family="{BODY}" font-size="15" fill="{INK}">(AutoFL, AgentFL, FlexFL) · benchmark (Defects4J, BugsInPy, QuixBugs) · nhiễm dữ liệu LLM</text></g>')
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
        ["Tiêu chí", "SemLoc", "EffiHolmes", "Crash+LLM", "Nhóm mình"],
        ["Loại lỗi", "ngữ nghĩa", "hiệu năng", "crash (Java)", "ngữ nghĩa"],
        ["Tín hiệu", "ràng buộc LLM\n+ chạy test", "profiling\n2 mức tải", "stack trace\n+ xếp hạng", "độ phủ + ràng\nbuộc + Shapley"],
        ["Lỗi thật", "7 có kết quả\ncấp dòng", "140 issue", "38 (công nghiệp)", "31 lỗi thật\n× 3 lần chạy"],
        ["Kiểm tra\nbenchmark", "không", "—", "—", "sửa 46 GT\nbằng thực thi"],
        ["Lặp + kiểm\nđịnh", "1 lần", "—", "—", "3 lần + McNemar\n/ Wilcoxon"],
    ], highlight_col=4))
    E("slide_11.svg", [
        ("Recommendations", "Học được & áp dụng"),
        ("Mars", "SemLoc"), ("Despite being red, Mars", ["Giả thuyết từ LLM, test", "phán xử; dùng mã gốc"]),
        ("Venus", "EffiHolmes"), ("Venus is the second", ["So 2 lần chạy để", "lọc nhiễu → CovGate"]),
        ("Neptune", "Crash+LLM"), ("Neptune is the farthest", ["Đưa xếp hạng cho LLM", "giúp định vị tốt hơn"]),
        ("Mercury", "Pearson 2017"), ("Mercury is the closest", ["Cách chấm khi hòa điểm", "và khi lỗi thiếu code"]),
        ("Saturn", "Thuộc bài"), ("Saturn is a gas giant", ["LLM có thể thuộc bài →", "biến thể đổi tên (RQ3)"]),
        ("Jupiter", "FlexFL"), ("Jupiter is the biggest", ["Gợi ý SBFL cho LLM ở", "cấp hàm → ta cấp dòng"]),
    ])
    E("thiet_ke.svg", [
        ("Recommendations", "Thiết kế thực nghiệm"),
        ("Mars", "Benchmark"), ("Despite being red, Mars", ["SemFault-250 + kiểm", "chứng; 31 BugsInPy"]),
        ("Venus", "Biến thể"), ("Venus is the second", ["Đổi tên, xóa docstring", "→ chống thuộc bài"]),
        ("Neptune", "So sánh"), ("Neptune is the farthest", ["SBFL, LLM hỏi thẳng,", "SemLoc, CovGate"]),
        ("Mercury", "Mô hình"), ("Mercury is the closest", ["Gemini 3.8 Flash", "+ 4 họ model khác"]),
        ("Saturn", "Chỉ số"), ("Saturn is a gas giant", ["Acc@1/3/5, thứ hạng,", "%Susp, lượt gọi, token"]),
        ("Jupiter", "Thống kê"), ("Jupiter is the biggest", ["Lặp 3 lần, McNemar /", "Wilcoxon, effect size"]),
    ])
    E("slide_20.svg", [
        ("Popular programming languages", "Câu hỏi nghiên cứu"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: kết quả SemLoc còn đúng", "với log công bố và với Gemini?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["Cải tiến: CovGate có chính xác", "hơn và rẻ hơn SemLoc gốc?"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, code đổi tên,", "các họ model khác?"]),
        ("Saturn", "Lõi"), ("Saturn is a gas giant", ["LLM đưa giả thuyết, bằng chứng", "thực thi mới là người phán xử."]),
    ])
    E("slide_19.svg", [
        ("Main topic and details", "CovGate: thêm độ phủ vào SemLoc"),
        ("Mars", "Cổng độ phủ"), ("Despite being red", ["Bỏ dòng mà", "test fail", "không đi qua"]),
        ("Neptune", "λ·Ochiai"), ("It’s the farthest", ["Cộng điểm SBFL,", "λ chọn trên dev"]),
        ("Jupiter", "CF xếp lại"), ("Jupiter is the biggest", ["Dùng kết quả", "vá thử để xếp"]),
        ("Saturn", "Thưởng có cứ"), ("It’s a gas giant", ["Chỉ thưởng khi", "có bằng chứng"]),
    ])
    dec = next(r for r in _csv("rq_decomposition.csv") if r["game"] == "semloc" and r["gt"] == "repaired"
               and r["subset"] == "all" and r["metric"] == "acc1")
    vgt = json.loads((ROOT / "data" / "semfault_verified_gt.json").read_text())
    n_corr = sum(1 for v in (vgt.values() if isinstance(vgt, dict) else vgt) if v.get("status") == "corrected")
    E("slide_14.svg", {
        "9h 55m 23s": "13/13", "Jupiter’s rotation period": "cấu hình SemLoc tái hiện khớp từng số",
        "333,000": f"{round(100 * float(dec['phi_guess']) / float(dec['full']))}%",
        "The Sun’s mass compared": "Acc@1 của SemLoc đến từ dòng LLM tự đoán",
        "386,000 km": str(n_corr), "Distance between the Earth": "ground truth sai được sửa bằng thực thi",
    })
    E("slide_21.svg", [
        ("Sequences", "Tiến độ"),
        ("First", "08/11"), ("Saturn is composed", "Tài liệu, hạ tầng"),
        (("Next", 0), "09/11"), ("Mercury is the closest", ["RQ1–RQ3 xong,", "review độc lập"]),
        (("Next", 0), "18/11"), ("Jupiter was named", ["Báo cáo lần 1:", "nội dung 1–2"]),
        (("Next", 0), "22/11"), ("Despite being red", ["Phân tích lỗi,", "đóng góp"]),
        (("Next", 0), "25/11"), ("Earth is the third", ["Báo cáo lần 2:", "nội dung 1–3"]),
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
        ("Mars", "Đoán/phổ"), ("Despite being red, Mars", [f"Acc@1 {_p(dec['full'])}: đoán", f"{_p(dec['phi_guess'])} + phổ {_p(dec['phi_spectrum'])}"]),
        ("Venus", "1 prompt"), ("Venus is the second", [f"Acc@3 {_p(rq2['llm_coverage']['acc3_mean'])} so với", f"{_p(rq2['semloc']['acc3_mean'])} (lỗi chạy tới)"]),
        ("Neptune", "Cách chấm"), ("Neptune is the farthest", ["Thưởng ẩn, CF không", "đổi hạng, DD, SBFL"]),
        ("Mercury", "GT mới"), ("Mercury is the closest", [f"{st['confirmed']} xác nhận,", f"{st['corrected']} sửa vị trí"]),
        ("Saturn", "Mơ hồ"), ("Saturn is a gas giant", [f"Acc@1 {_p(tol['semloc']['acc1_exact'])}→{_p(tol['semloc']['acc1_guard_strict'])}", "theo quy ước nhãn"]),
        ("Jupiter", "Tái hiện"), ("Jupiter is the biggest", ["Docker offline, cache", "LLM, số = macro"]),
    ])
    E("triet_ly.svg", [
        ("Main topic and details", "Triết lý khoa học"),
        ("Mars", "Test phán xử"), ("Despite being red", ["LLM đề xuất,", "kiểm thử", "quyết định"]),
        ("Neptune", "Đo đóng góp"), ("It’s the farthest", ["Phân rã, bỏ", "từng thành phần"]),
        ("Jupiter", "Baseline"), ("Jupiter is the biggest", ["Pipeline phải", "thắng 1 prompt"]),
        ("Saturn", "Chịu bác bỏ"), ("It’s a gas giant", ["Lặp 3 lần, CI,", "nêu cả âm tính"]),
    ])
    E("de_doa.svg", [
        ("Features of the topic", "Các mối đe dọa"),
        ("Mars", "Oracle nhiễu"), ("Despite being red", ["Nhận sửa bù trừ;", "báo cả GT gốc"]),
        ("Neptune", "Lỗi thật ít"), ("It’s the farthest", ["31 lỗi, 1 dự án;", "CI còn chứa 0"]),
        ("Jupiter", "Mô hình"), ("Jupiter is the biggest", ["Suy luận mặc định,", "mô hình mới hơn"]),
        ("Saturn", "Prompt nhóm"), ("Saturn is a gas giant", ["Viết trước khi xem", "test, không chỉnh"]),
    ])
    E("ket_luan.svg", {
        "Introduction": "Kết luận",
        "Mercury is the closest planet to the Sun and the smallest": [
            "**Grounded hay guessed?**", "Hạng 1 chủ yếu là dòng", f"LLM đoán ({_p(dec['phi_guess'])}/{_p(dec['full'])} điểm",
            "Acc@1); top-3 chủ yếu là", "bằng chứng thực thi.", "Lỗi thật: mọi lần đúng", "hạng 1 là dòng đoán."],
        "Mercury takes a little more than 58 days": [
            "**Đề xuất**", "Đưa thẳng độ phủ cho", f"LLM: Acc@3 {_p(rq2['llm_coverage']['acc3_mean'])} so với",
            f"{_p(rq2['semloc']['acc3_mean'])} với lỗi được", "chạy tới, rẻ ~5 lần.", "Bảng kiểm 7 mục cho", "mọi đánh giá."],
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

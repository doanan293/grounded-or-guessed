"""Build the Vietnamese progress-report deck (báo cáo lần 1) from template-vi.pptx pages.

Re-runnable: every page is rebuilt from the pristine imported SVG kept in orig/.
    python3 docs/presentation/build/build_bao_cao_lan_1.py  (workspace: see README.md)
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

# output page -> (source slide, svg file)
PAGES = [
    (1, "slide_01.svg"), (3, "slide_03.svg"), (4, "slide_04.svg"), (5, "slide_05.svg"),
    (8, "slide_08.svg"), (25, "slide_25.svg"), (9, "slide_09.svg"), (22, "slide_22.svg"),
    (11, "slide_11.svg"), (4, "chuong02.svg"), (20, "slide_20.svg"), (19, "slide_19.svg"),
    (11, "thiet_ke.svg"), (4, "chuong03.svg"), (14, "slide_14.svg"), (22, "ket_qua_thu.svg"),
    (21, "slide_21.svg"), (30, "slide_30.svg"),
]


def fresh() -> None:
    if not ORIG.exists():
        ORIG.mkdir()
        for f in SVG.glob("slide_*.svg"):
            shutil.copy(f, ORIG / f.name)
    for src, name in PAGES:
        shutil.copy(ORIG / f"slide_{src:02d}.svg", SVG / name)


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


def build() -> None:
    fresh()
    edit(SVG / "slide_01.svg", {
        "Introduction to Coding Workshop": ["Tái hiện &", "mở rộng SemLoc"],
        "Here is where your presentation begins": ["Định vị lỗi ngữ nghĩa với ràng buộc từ LLM",
                                                   "Đề tài 2KH · IT5440 · Báo cáo tiến độ lần 1"],
    })
    edit(SVG / "slide_03.svg", [
        ("Table of contents", "Mục lục"),
        ("Theory lesson", "Bối cảnh"), ("Features of the topic", "Phương pháp"),
        ("Tips", "Kết quả bước đầu"), ("Practical exercise", "Kế hoạch"),
        (("You can describe the topic", 0), ["Vấn đề, nghiên cứu liên quan,", "SemLoc"]),
        (("You can describe the topic", 0), ["3 câu hỏi, CovGate,", "thiết kế thực nghiệm"]),
        (("You can describe the topic", 0), ["Tái hiện, kiểm tra benchmark,", "chạy thử, BugsInPy"]),
        (("You can describe the topic", 0), ["Tiến độ và việc đến lần 2"]),
    ])
    for name, num, title, sub in (("slide_04.svg", "01", "Bối cảnh", "Vấn đề, nghiên cứu liên quan và SemLoc"),
                                  ("chuong02.svg", "02", "Phương pháp", "Câu hỏi nghiên cứu, CovGate, thiết kế thực nghiệm"),
                                  ("chuong03.svg", "03", "Kết quả", "Tái hiện, kiểm tra benchmark, chạy thử, BugsInPy")):
        edit(SVG / name, {"01": num, "Theory lesson": title, "You can enter a subtitle": sub})
    edit(SVG / "slide_05.svg", {
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
    edit(SVG / "slide_08.svg", {
        "What is this topic about?": "Nghiên cứu liên quan",
        "Mercury": "SemLoc", "Venus": "EffiHolmes", "Mars": "Crash+LLM",
        "closest planet to the Sun and the smallest": ["Lỗi ngữ nghĩa.", "LLM + chạy test.", "Acc@1 42,8%."],
        "Venus has a beautiful name": ["Lỗi hiệu năng.", "Profiling 2 tải.", "140 issue thật."],
        "Despite being red, Mars": ["Crash Java,", "38 lỗi thật.", "Định vị 71%."],
    })
    append(SVG / "slide_08.svg",
           f'<g id="tai-lieu-them" data-pptx-bounds="85 470 790 44"><text x="85" y="488" font-family="{BODY}" font-size="15" fill="{INK}">'
           f'<tspan font-weight="bold">+ 23 tài liệu nhóm tìm thêm: </tspan>SBFL kinh điển (Tarantula, Ochiai, DStar) · định vị lỗi bằng LLM</text>'
           f'<text x="85" y="508" font-family="{BODY}" font-size="15" fill="{INK}">(AutoFL, AgentFL, FlexFL) · benchmark (Defects4J, BugsInPy, QuixBugs) · nhiễm dữ liệu LLM</text></g>')
    edit(SVG / "slide_25.svg", [
        ("Step-by-step coding", "SemLoc hoạt động thế nào"),
        ("Earth", "Neo"), ("It’s the only planet known", ["Chọn vị trí", "đặt kiểm tra"]),
        ("Mercury", "Ràng buộc"), ("Mercury is the closest", ["LLM viết", "ràng buộc"]),
        ("Jupiter", "Chấm điểm"), ("Jupiter is the biggest", ["Chạy test,", "tính Ochiai"]),
        ("Saturn", "Vá thử"), ("Saturn was named", ["LLM vá dòng,", "chạy lại test"]),
    ])
    edit(SVG / "slide_09.svg", [
        ("Features of the topic", "Khoảng trống của SemLoc"),
        ("Mars", "Lỗi thật ít"), ("Despite being red", ["Chỉ 7 lỗi BugsInPy", "có kết quả cấp dòng"]),
        ("Neptune", "Bỏ độ phủ"), ("It’s the farthest", ["Không dùng tín hiệu", "SBFL nào"]),
        ("Jupiter", "Chạy 1 lần"), ("Jupiter is the biggest", ["Không lặp, không", "kiểm định thống kê"]),
        ("Saturn", "Cách chấm"), ("Saturn is a gas giant", ["Hòa điểm, DD, bỏ", "chương trình lỗi"]),
    ])
    for name, title in (("slide_22.svg", "Khác biệt so với các nghiên cứu"), ("ket_qua_thu.svg", "Chạy thử: 50 chương trình dev")):
        edit(SVG / name, {"Classification": title})
        drop_group(SVG / name, "shape-2194")
    append(SVG / "slide_22.svg", table("bang-so-sanh", 84, 135, [176, 158, 158, 158, 158], [
        ["Tiêu chí", "SemLoc", "EffiHolmes", "Crash+LLM", "Nhóm mình"],
        ["Loại lỗi", "ngữ nghĩa", "hiệu năng", "crash (Java)", "ngữ nghĩa"],
        ["Tín hiệu", "ràng buộc LLM\n+ chạy test", "profiling\n2 mức tải", "stack trace\n+ xếp hạng", "độ phủ\n+ ràng buộc"],
        ["Lỗi thật", "7 có kết quả\ncấp dòng", "140 issue", "38 (công nghiệp)", "31 dựng được\n(youtube-dl)"],
        ["Kiểm tra\nbenchmark", "không", "—", "—", "có: 22% GT\nlà dòng trống"],
        ["Lặp + kiểm\nđịnh", "1 lần", "—", "—", "3 lần +\nkiểm định"],
    ], highlight_col=4))
    edit(SVG / "slide_11.svg", [
        ("Recommendations", "Học được & áp dụng"),
        ("Mars", "SemLoc"), ("Despite being red, Mars", ["Giả thuyết từ LLM, test", "phán xử; dùng mã gốc"]),
        ("Venus", "EffiHolmes"), ("Venus is the second", ["So 2 lần chạy để", "lọc nhiễu → CovGate"]),
        ("Neptune", "Crash+LLM"), ("Neptune is the farthest", ["Đưa xếp hạng cho LLM", "giúp định vị tốt hơn"]),
        ("Mercury", "Pearson 2017"), ("Mercury is the closest", ["Cách chấm khi hòa điểm", "và khi lỗi thiếu code"]),
        ("Saturn", "Thuộc bài"), ("Saturn is a gas giant", ["LLM có thể thuộc bài →", "biến thể đổi tên (RQ3)"]),
        ("Jupiter", "FlexFL"), ("Jupiter is the biggest", ["Gợi ý SBFL cho LLM ở", "cấp hàm → ta cấp dòng"]),
    ])
    edit(SVG / "thiet_ke.svg", [
        ("Recommendations", "Thiết kế thực nghiệm"),
        ("Mars", "Benchmark"), ("Despite being red, Mars", ["SemFault-250 (dev 50,", "test 200) + 31 BugsInPy"]),
        ("Venus", "Biến thể"), ("Venus is the second", ["Đổi tên, xóa docstring", "→ chống thuộc bài"]),
        ("Neptune", "So sánh"), ("Neptune is the farthest", ["SBFL, LLM hỏi thẳng,", "SemLoc, CovGate"]),
        ("Mercury", "Mô hình"), ("Mercury is the closest", ["Gemini 3.8 Flash; phụ:", "Claude, GPT-6, gpt-oss"]),
        ("Saturn", "Chỉ số"), ("Saturn is a gas giant", ["Acc@1/3/5, thứ hạng,", "%Susp, lượt gọi, token"]),
        ("Jupiter", "Thống kê"), ("Jupiter is the biggest", ["Lặp 3 lần, McNemar /", "Wilcoxon, effect size"]),
    ])
    edit(SVG / "slide_20.svg", [
        ("Popular programming languages", "Câu hỏi nghiên cứu"),
        ("Neptune", "RQ1"), ("Mercury is the closest", ["Tái hiện: kết quả SemLoc còn đúng", "với log công bố và với Gemini?"]),
        ("Venus", "RQ2"), ("Venus has a beautiful", ["Cải tiến: CovGate có chính xác", "hơn và rẻ hơn SemLoc gốc?"]),
        ("Earth", "RQ3"), ("Earth is the third", ["Độ bền: lỗi thật, code đổi tên,", "các họ model khác?"]),
        ("Saturn", "Lõi"), ("Saturn is a gas giant", ["LLM đưa giả thuyết, bằng chứng", "thực thi mới là người phán xử."]),
    ])
    edit(SVG / "slide_19.svg", [
        ("Main topic and details", "CovGate: thêm độ phủ vào SemLoc"),
        ("Mars", "Cổng độ phủ"), ("Despite being red", ["Bỏ dòng mà", "test fail", "không đi qua"]),
        ("Neptune", "Kết hợp điểm"), ("It’s the farthest", ["Điểm ràng buộc", "+ điểm SBFL"]),
        ("Jupiter", "Vá thử gọn"), ("Jupiter is the biggest", ["Chỉ kiểm chứng", "top-K qua cổng"]),
        ("Saturn", "Mục tiêu"), ("It’s a gas giant", ["Đúng hơn và", "ít gọi LLM hơn"]),
    ])
    edit(SVG / "slide_14.svg", {
        "9h 55m 23s": "13/13", "Jupiter’s rotation period": "cấu hình SemLoc tái hiện khớp từng số",
        "333,000": "22%", "The Sun’s mass compared": "ground truth SemFault-250 trỏ vào dòng trống",
        "386,000 km": "31 lỗi", "Distance between the Earth": "BugsInPy thật dựng được (youtube-dl)",
    })
    edit(SVG / "slide_21.svg", [
        ("Sequences", "Tiến độ"),
        ("First", "08/11"), ("Saturn is composed", "Tài liệu, hạ tầng"),
        (("Next", 0), "12/11"), ("Mercury is the closest", ["Tái hiện, gắn", "nhãn, chạy thử"]),
        (("Next", 0), "18/11"), ("Jupiter was named", ["Báo cáo lần 1:", "xong nội dung 1–2"]),
        (("Next", 0), "19/11"), ("Despite being red", ["CovGate, chạy đủ", "thí nghiệm"]),
        (("Next", 0), "23/11"), ("Earth is the third", ["Thống kê, đóng", "góp, báo cáo lần 2"]),
        ("Last", "26/11"), ("Venus has extremely", ["Bài báo, báo cáo,", "bảo vệ (≤12/12)"]),
    ])
    t = (SVG / "slide_21.svg").read_text()  # one-line first column: align it with the other top captions
    t = t.replace('x="190.65" y="65.9832021"', 'x="190.65" y="99.1032021"', 1)
    (SVG / "slide_21.svg").write_text(t.replace('y="99.1032021"', 'y="122.1032021"'))  # clear of the page title
    edit(SVG / "slide_30.svg", {
        "Thanks!": "Cảm ơn!",
        "Do you have any questions?": ["Câu hỏi?", "Góp ý?"],
        "Please keep this slide for attribution": "Báo cáo tiến độ lần 1 · 18/11/2026",
    })
    pilot = ROOT / "data" / "pilot_dev_gemini_default.csv"
    if pilot.exists():
        import csv
        rows = {(r["source"], r["subset"]): r for r in csv.DictReader(open(pilot))}
        pct = lambda v: f"{round(100 * float(v))}%"
        def row(label, src):
            a, s = rows[(src, "all")], rows[(src, "semantic")]
            return [label, pct(a["acc1"]), pct(a["acc3"]), pct(a["acc5"]), pct(s["acc1"])]
        cost = rows[("cost (ours)", "all")]
        append(SVG / "ket_qua_thu.svg", table("bang-chay-thu", 84, 140, [300, 125, 125, 125, 125], [
            ["Phương pháp", "Acc@1", "Acc@3", "Acc@5", "Ngữ nghĩa\nAcc@1"],
            row("SBFL Ochiai (log)", "published: SBFL Ochiai"),
            row("SemLoc + Gemini 2.5 Pro\n(log tác giả)", "published: SemLoc gemini-2.5-pro T0.8"),
            row("SemLoc + Claude 4.6\n(log tác giả)", "published: SemLoc claude-sonnet-4-6 T0.8"),
            row("SemLoc + Gemini 3.8 Flash\n(nhóm chạy lại)", next(k[0] for k in rows if k[0].startswith("ours"))),
        ], highlight_col=None, head_h=52, row_h=56, fs=16,
            note=f"Cùng 50 chương trình dev, mức suy luận mặc định; nhóm: {cost['n_ran'].replace('calls=', '').split()[0]} lượt gọi LLM.\n"
                 "“Ngữ nghĩa” = 33 chương trình có dòng lỗi được cả test pass lẫn fail chạy qua."))
    json.dump({"schema": "ppt-master.roundtrip-page-plan.v1",
               "pages": [{"source_slide": s, **({} if n == f"slide_{s:02d}.svg" else {"svg": n})} for s, n in PAGES]},
              open(WS / "page_plan.json", "w"), indent=2)
    print("built", len(PAGES), "pages")


if __name__ == "__main__":
    build()

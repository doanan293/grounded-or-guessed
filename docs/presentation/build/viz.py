"""Native SVG pictures for the storytelling slides (960 x 540 canvas). Each function returns one
<g id=… data-pptx-bounds="x y w h"> group of plain rect/text/circle/polygon atoms, so the exported shapes stay
editable in PowerPoint. Colours and fonts are the template's (see build_deck.py)."""
from datetime import date
from xml.sax.saxutils import escape

BODY = '&quot;Be Vietnam Pro&quot;, sans-serif'
MONO = '&quot;IBM Plex Mono&quot;, sans-serif'
ORANGE, LAVENDER, INK, NAVY, CREAM = "#EB9109", "#BFBEF7", "#1D1D1D", "#0C0A9E", "#FDF1DE"
RED, GREY, LIGHT, MUTED = "#D9541E", "#A3A3A0", "#F2F2EE", "#5F5F5A"
HILITE = "#FBD9C9"


def _p(v: float, nd: int = 1) -> str:
    return f"{v:.{nd}f}".replace(".", ",")


def _frame(x, y, size, w, anchor="start", lines=1, lh=None) -> str:
    """A fixed text frame (data-pptx-frame) around a label: exported as a box that does not auto-grow, so LibreOffice
    and PowerPoint both keep the text exactly where the SVG puts it (an auto-growing box drifts sideways)."""
    w = max(w, size)
    fx = x if anchor == "start" else x - w / 2 if anchor == "middle" else x - w
    h = size * 0.35 + (lh or size * 1.2) * (lines - 1) + size * 1.25
    return f' data-pptx-frame="{round(fx, 1)} {round(y - size * 1.1, 1)} {round(w, 1)} {round(h, 1)}"'


def text_w(s: str, size: float, family: str = BODY, bold: bool = False) -> float:
    """Rendered width of one line in px, from the real font when it is installed (fallback: 0.56 em per character)."""
    font = _font(size, family, bold)
    if font is None:
        return len(s) * size * (0.6 if family == MONO else 0.56)
    return font.getlength(s)


_FONTS: dict = {}


def _font(size, family, bold):
    key = (round(size * 4), family, bold)
    if key not in _FONTS:
        try:
            from PIL import ImageFont
            from pathlib import Path
            d = Path.home() / ".local/share/fonts/QA-VN"
            name = ("IBMPlexMono" if family == MONO else "BeVietnamPro") + ("-Bold" if bold else "-Regular") + ".ttf"
            _FONTS[key] = ImageFont.truetype(str(d / name), size=max(1, round(size * 4))) if (d / name).exists() else None
        except Exception:
            _FONTS[key] = None
    f = _FONTS[key]
    return None if f is None else _Scaled(f)


class _Scaled:
    def __init__(self, f):
        self.f = f

    def getlength(self, s):
        return self.f.getlength(s) / 4


def _t(x, y, s, size=16, fill=INK, weight="normal", anchor="start", family=BODY, style="normal") -> str:
    w = text_w(str(s), size, family, weight == "bold") * 1.2 + 12
    return (f'<text x="{round(x, 1)}" y="{round(y, 1)}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}"{_frame(x, y, size, w, anchor)}>{escape(str(s))}</text>')


def _r(x, y, w, h, fill, stroke="none", rx=0, sw=1.5) -> str:
    return (f'<rect x="{round(x, 1)}" y="{round(y, 1)}" width="{round(w, 1)}" height="{round(h, 1)}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def _arrow(x1, y1, x2, y2, color=MUTED) -> str:
    """Straight horizontal or vertical arrow: a line plus a triangle head (no markers)."""
    out = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2"/>'
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        pts = f"{x2},{y2} {x2 - 9 * d},{y2 - 5} {x2 - 9 * d},{y2 + 5}"
    else:
        d = 1 if y2 > y1 else -1
        pts = f"{x2},{y2} {x2 - 5},{y2 - 9 * d} {x2 + 5},{y2 - 9 * d}"
    return out + f'<polygon points="{pts}" fill="{color}"/>'


def _g(gid, x, y, w, h, body: list[str]) -> str:
    return f'<g id="{gid}" data-pptx-bounds="{round(x, 1)} {round(y, 1)} {round(w, 1)} {round(h, 1)}">' + "".join(body) + "</g>"


def code_block(gid, x, y, lines: list[str], highlight: set = frozenset(), first_no: int = 1, fs: float = 15,
               width: float = 620, mark: dict | None = None, inserted: dict | None = None) -> str:
    """Line-numbered code; lines in `highlight` (by printed number) get a warm band; `mark` puts a note at a line's end;
    `inserted` {line: text or [texts]} adds italic check line(s) (what an instrumenting tool inserts) right after that line."""
    lh = fs * 1.45
    inserted = {k: [v] if isinstance(v, str) else list(v) for k, v in (inserted or {}).items()}
    extra = sum(len(v) for v in inserted.values())
    h = lh * (len(lines) + extra) + 16
    body = [_r(x, y, width, h, "#FFFFFF", stroke=LAVENDER, rx=8)]
    k = 0
    for i, line in enumerate(lines):
        no, cy = first_no + i, y + 8 + lh * k
        k += 1
        if no in highlight:
            body.append(_r(x + 2, cy, width - 4, lh, HILITE))
        body.append(_t(x + 34, cy + lh * 0.72, no, size=fs - 3, fill=GREY, anchor="end", family=MONO))
        body.append(_t(x + 44, cy + lh * 0.72, line.replace(" ", " ") or " ", size=fs, family=MONO))
        if mark and no in mark:
            body.append(_t(x + width - 10, cy + lh * 0.72, mark[no], size=fs - 2, fill=RED, weight="bold", anchor="end"))
        for text in inserted.get(no, []):
            cy2 = y + 8 + lh * k
            k += 1
            body.append(_r(x + 2, cy2, width - 4, lh, "#EEEDFC"))
            body.append(_t(x + 44, cy2 + lh * 0.72, text, size=fs - 2, fill=NAVY, style="italic", family=MONO))
    return _g(gid, x, y, width, h, body)


def bars(gid, x, y, w, h, series: list[tuple], vmax: float, unit: str = "%", label_w: float = 170, nd: int = 1) -> str:
    """Horizontal bars: (label, value, colour[, base]); value printed at the bar end; `base` draws a grey first part."""
    n = len(series)
    step = h / n
    bh = min(34, step * 0.66)
    span = w - label_w - 70
    body = []
    for i, s in enumerate(series):
        label, v, c = s[0], s[1], s[2]
        cy = y + step * i + (step - bh) / 2
        body.append(_t(x + label_w - 10, cy + bh * 0.68, label, size=17, weight="bold" if c != GREY else "normal", anchor="end"))
        bw = max(2, span * v / vmax)
        body.append(_r(x + label_w, cy, bw, bh, c, rx=4))
        if len(s) > 3 and s[3]:  # stacked: the first s[3] of the bar is a grey base (e.g. spectrum under a bonus)
            body.append(_r(x + label_w, cy, span * s[3] / vmax, bh, GREY, rx=4))
        body.append(_t(x + label_w + bw + 8, cy + bh * 0.68, f"{_p(v, nd)}{unit}", size=17, fill=INK, weight="bold"))
    return _g(gid, x, y, w, h, body)


def pipeline(gid, x, y, steps: list[str], accent: int | None = None, box_w: float = 150, box_h: float = 70,
             gap: float = 34, color: str = NAVY, dashed: set = frozenset()) -> str:
    """Boxes left to right joined by arrows; step `accent` is filled orange; text lines split on '\\n'."""
    body = []
    for i, s in enumerate(steps):
        bx = x + i * (box_w + gap)
        fill = CREAM if i == accent else "#FFFFFF"
        stroke = ORANGE if i == accent else color
        body.append(_r(bx, y, box_w, box_h, fill, stroke=stroke, rx=10, sw=2))
        lines = s.split("\n")
        for k, line in enumerate(lines):
            ty = y + box_h / 2 + (k - (len(lines) - 1) / 2) * 20 + 6
            body.append(_t(bx + box_w / 2, ty, line, size=16, anchor="middle", weight="bold" if k == 0 else "normal"))
        if i:
            body.append(_arrow(bx - gap + 3, y + box_h / 2, bx - 3, y + box_h / 2))
    w = len(steps) * box_w + (len(steps) - 1) * gap
    return _g(gid, x, y, w, box_h, body)


def big_number(gid, x, y, value: str, caption: str, color: str = NAVY, size: float = 64, w: float = 260) -> str:
    lines = caption.split("\n")
    body = [_t(x, y + size * 0.85, value, size=size, fill=color, weight="bold")]
    body += [_t(x, y + size + 26 + 22 * k, line, size=17, fill=MUTED) for k, line in enumerate(lines)]
    return _g(gid, x, y, w, size + 30 + 22 * len(lines), body)


def _d(s: str, year: int = 2026) -> date:
    d, m = (int(v) for v in s.split("/"))
    return date(year, m, d)


def gantt(gid, x, y, w, rows: list[tuple], today: str | None = None, label_w: float = 260, row_h: float = 40) -> str:
    """rows: (task, 'dd/mm' start, 'dd/mm' end, done?). Done bars are navy, upcoming bars lavender."""
    start = min(_d(r[1]) for r in rows)
    end = max(_d(r[2]) for r in rows)
    days = (end - start).days + 1
    span = w - label_w - 95  # room for the date label after the last bar
    px = lambda s: x + label_w + span * (_d(s) - start).days / days
    body = []
    for i, (task, a, b, done) in enumerate(rows):
        cy = y + i * row_h
        body.append(_t(x + label_w - 12, cy + row_h * 0.62, task, size=16, anchor="end"))
        bx, bw = px(a), max(10, px(b) - px(a) + span / days)
        body.append(_r(bx, cy + 8, bw, row_h - 16, NAVY if done else LAVENDER, rx=5))
        body.append(_t(bx + bw + 6, cy + row_h * 0.62, f"{a}–{b}" if a != b else a, size=13, fill=MUTED))
    if today:
        tx = px(today)
        h = len(rows) * row_h
        body.append(f'<line x1="{round(tx, 1)}" y1="{y - 6}" x2="{round(tx, 1)}" y2="{y + h}" stroke="{RED}" stroke-width="2" stroke-dasharray="5 4"/>')
        body.append(_t(tx, y - 12, f"hôm nay {today}", size=13, fill=RED, anchor="middle", weight="bold"))
    return _g(gid, x, y - 28, w, len(rows) * row_h + 28, body)


def matrix(gid, x, y, rows: list[str], cols: list[str], cells: set, row_mark: dict | None = None, cell_w: float = 56,
           row_h: float = 30, label_w: float = 120, col_colors: dict | None = None, col_sub: list | None = None) -> str:
    """Dot matrix: rows × cols, a dot in each (row, col) of `cells`; row_mark {row: colour} paints a band."""
    body = []
    w = label_w + cell_w * len(cols)
    for j, c in enumerate(cols):
        body.append(_t(x + label_w + cell_w * (j + 0.5), y + 18, c, size=15, anchor="middle", weight="bold",
                       fill=(col_colors or {}).get(j, INK)))
        if col_sub:  # a small second header line, e.g. pass / fail
            body.append(_t(x + label_w + cell_w * (j + 0.5), y + 34, col_sub[j], size=12, anchor="middle",
                           fill=(col_colors or {}).get(j, INK)))
    for i, r in enumerate(rows):
        cy = y + (44 if col_sub else 30) + i * row_h
        if row_mark and i in row_mark:
            body.append(_r(x, cy, w, row_h, HILITE))
        no, _, code = r.partition("  ")
        if no.isdigit():  # "NN  code": right-aligned line number, then the code left-aligned like an editor
            body.append(_t(x + 30, cy + row_h * 0.68, no, size=13, anchor="end", family=MONO, fill=GREY))
            body.append(_t(x + 40, cy + row_h * 0.68, code, size=15, family=MONO))
        else:
            body.append(_t(x + label_w - 10, cy + row_h * 0.68, r, size=15, anchor="end", family=MONO))
        for j in range(len(cols)):
            if (i, j) in cells:
                body.append(f'<circle cx="{round(x + label_w + cell_w * (j + 0.5), 1)}" cy="{round(cy + row_h / 2, 1)}" r="7" '
                            f'fill="{(col_colors or {}).get(j, NAVY)}"/>')
    return _g(gid, x, y, w, (44 if col_sub else 30) + row_h * len(rows), body)


def wrap(text: str, width: float, size: float, family: str = BODY, bold: bool = False) -> list[str]:
    """Greedy word wrap measured with the real font, so a line fills the box instead of a character-count guess."""
    lines, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if cur and text_w(cand, size, family, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def panel(gid, x, y, w, blocks: list[tuple], size: float = 14, head_color: str = NAVY, fill: str = "#FFFFFF",
          h: float | None = None, rule: str | None = None) -> str:
    """Explanation text beside a picture: a white sheet with a thin coloured rule on the left, blocks of (heading, text)
    set as ONE editable text frame. A heading is optional (None/"" = plain paragraph); `h` stretches the sheet so its
    bottom lines up with the picture next to it."""
    pad = 16
    inner = w - 2 * pad - 4
    lh = round(size * 1.42, 1)
    rows = []  # (dy, markup)
    for head, text in blocks:
        gap = round(size * 0.75, 1) if rows else 0
        if head:
            rows.append((lh + gap, f'<tspan font-weight="bold" fill="{head_color}">{escape(head)}</tspan>'))
            gap = 0
        for line in wrap(text, inner * 0.93, size):  # head-room: the quality checker measures wider than the font
            rows.append((lh + gap, escape(line)))
            gap = 0
    x0, y0 = x + pad + 4, y + pad + size
    first = rows[0][1]
    rest = "".join(f'<tspan x="{x0}" dy="{dy}">{mk}</tspan>' for dy, mk in rows[1:])
    text_h = size * 1.3 + sum(dy for dy, _ in rows[1:])
    need = round(pad * 2 + text_h, 1)
    h = max(need, h or 0)
    frame = f' data-pptx-frame="{x0} {round(y + pad - 4, 1)} {round(x + w - 2 - x0, 1)} {round(text_h + 8, 1)}"'
    text = (f'<text x="{x0}" y="{round(y0, 1)}" font-family="{BODY}" font-size="{size}" fill="{INK}"{frame}>'
            f'<tspan x="{x0}" dy="0">{first}</tspan>{rest}</text>')
    return _g(gid, x, y, w, h, [_r(x, y, w, h, fill, stroke="#E4E3F6", rx=6, sw=1),
                                _r(x, y, 4, h, rule or head_color, rx=0), text])


def before_after(gid, x, y, w, rows: list[tuple], head=("Tiêu chí", "Phương pháp SemLoc", "Phương pháp FailLoc", "Chênh lệch"),
                 row_h: float = 50) -> str:
    """Before → after table: criterion | before (grey) → after (orange) | gain badge."""
    cw = [w * 0.27, w * 0.24, w * 0.24, w * 0.25]
    xs = [x, x + cw[0], x + cw[0] + cw[1], x + cw[0] + cw[1] + cw[2]]
    body = []
    for k, hd in enumerate(head):
        body.append(_t(xs[k] + (12 if k == 0 else cw[k] / 2), y + 22, hd, size=15, fill=MUTED, weight="bold",
                       anchor="start" if k == 0 else "middle"))
    for i, (crit, before, after, delta) in enumerate(rows):
        cy = y + 36 + i * row_h
        body.append(_r(x, cy, w, row_h - 8, "#FFFFFF" if i % 2 else LIGHT, rx=8))
        body.append(_t(xs[0] + 12, cy + row_h * 0.52, crit, size=16, weight="bold"))
        body.append(_t(xs[1] + cw[1] / 2, cy + row_h * 0.52, before, size=17, fill=MUTED, anchor="middle"))
        body.append(_arrow(xs[2] - 16, cy + (row_h - 8) / 2, xs[2] + 8, cy + (row_h - 8) / 2, color=ORANGE))
        body.append(_t(xs[2] + cw[2] / 2, cy + row_h * 0.52, after, size=17, fill=ORANGE, weight="bold", anchor="middle"))
        body.append(_r(xs[3] + 14, cy + 7, cw[3] - 28, row_h - 22, CREAM, stroke=ORANGE, rx=13, sw=1.2))
        body.append(_t(xs[3] + cw[3] / 2, cy + row_h * 0.5, delta, size=14, fill=INK, weight="bold", anchor="middle"))
    return _g(gid, x, y, w, 36 + row_h * len(rows), body)


def claim_vs_evidence(gid, x, y, w, rows: list[tuple], head=("Bài báo nói", "Nhóm kiểm tra thấy"), size: float = 14,
                      row_h: float = 74) -> str:
    """Two columns, one row per claim: what the paper states (grey) → what the group's check found (orange edge)."""
    import textwrap
    cw = (w - 40) / 2
    per = max(10, int((cw - 24) / (size * 0.55)))
    body = [_t(x + 12, y + 20, head[0], size=15, fill=MUTED, weight="bold"),
            _t(x + cw + 52, y + 20, head[1], size=15, fill=ORANGE, weight="bold")]
    for i, (claim, found) in enumerate(rows):
        cy = y + 32 + i * row_h
        for k, (txt, stroke, fill) in enumerate(((claim, LAVENDER, LIGHT), (found, ORANGE, "#FFFFFF"))):
            cx = x + k * (cw + 40)
            body.append(_r(cx, cy, cw, row_h - 10, fill, stroke=stroke, rx=8, sw=1.5))
            lines = textwrap.wrap(txt, per)
            lh = size * 1.35
            ty = cy + (row_h - 10) / 2 - (len(lines) - 1) * lh / 2 + size * 0.35
            rest = "".join(f'<tspan x="{round(cx + 12, 1)}" dy="{round(lh, 1)}">{escape(l)}</tspan>' for l in lines[1:])
            body.append(f'<text x="{round(cx + 12, 1)}" y="{round(ty, 1)}" font-family="{BODY}" font-size="{size}" '
                        f'fill="{INK}"><tspan x="{round(cx + 12, 1)}" dy="0">{escape(lines[0])}</tspan>{rest}</text>')
        body.append(_arrow(x + cw + 6, cy + (row_h - 10) / 2, x + cw + 34, cy + (row_h - 10) / 2, color=ORANGE))
    return _g(gid, x, y, w, 32 + row_h * len(rows), body)


def section_band(gid, idx: int, label: str, x: float = 600, y: float = 14, w: float = 340, content: int | None = None) -> str:
    """Small band at the top right naming the part of the talk (the teacher's five parts) and, where a page answers one
    of the teacher's four required contents, that content's number."""
    s = f"Phần {idx} · {label}" + (f" · Nội dung {content}" if content else "")
    w = max(w, text_w(s, 13, bold=True) + 40)
    x = min(x, 940 - w)
    body = [_r(x, y, w, 26, CREAM, stroke=ORANGE, rx=13, sw=1.2),
            _t(x + w / 2, y + 18, s, size=13, fill=INK, weight="bold", anchor="middle")]
    return _g(gid, x, y, w, 26, body)


def formula(gid, x, y, w, lines: list[str], size: float = 16) -> str:
    """A boxed formula: first line bold (the formula), next lines the meaning of each symbol."""
    lh = size * 1.5
    h = lh * len(lines) + 18
    body = [_r(x, y, w, h, "#FFFFFF", stroke=NAVY, rx=10, sw=1.8)]
    for i, line in enumerate(lines):
        body.append(_t(x + 16, y + 12 + lh * (i + 0.75), line, size=size if i == 0 else size - 2,
                       weight="bold" if i == 0 else "normal", fill=NAVY if i == 0 else INK))
    return _g(gid, x, y, w, h, body)


def constraint_table(gid, x, y, w, rows: list[dict], row_h: float = 34) -> str:
    """Constraint | where it is checked | expression | failing tests violating | passing tests violating | Ochiai |
    region weight | score given to the line."""
    cols = [("Ràng buộc", 0.09), ("Chỗ đặt → dòng", 0.17), ("Điều kiện", 0.32), ("Test fail vi phạm", 0.1),
            ("Test pass vi phạm", 0.1), ("Ochiai", 0.07), ("Hệ số", 0.06), ("Điểm dòng", 0.09)]
    xs, cx = [], x
    for _, f in cols:
        xs.append(cx)
        cx += w * f
    body = [_r(x, y, w, 40, LAVENDER, rx=6)]
    for (head, f), x0 in zip(cols, xs):
        for k, part in enumerate(head.split(" vi ")):
            body.append(_t(x0 + 6, y + 17 + 15 * k, part if k == 0 else "vi " + part, size=12, weight="bold"))
    for i, r in enumerate(rows):
        cy = y + 40 + i * row_h
        if i % 2:
            body.append(_r(x, cy, w, row_h, LIGHT))
        vals = [r["id"], r["where"], r["expr"], str(r["fail"]), str(r["pass"]), _p(r["ochiai"], 2), _p(r["weight"], 1),
                _p(r["score"], 2)]
        for k, (v, x0) in enumerate(zip(vals, xs)):
            body.append(_t(x0 + 6, cy + row_h * 0.64, v, size=12, family=MONO if k == 2 else BODY,
                           weight="bold" if k == 7 else "normal"))
    return _g(gid, x, y, w, 40 + row_h * len(rows), body)


STATUS_FILL = {"Đã xong": "#DDEBDA", "Đang hoàn thiện": CREAM, "Chưa làm": "#F4DCD3", "Có bản nháp": CREAM}


def progress_table(gid, x, y, w, rows: list[tuple], row_h: float = 44) -> str:
    """Work item | status (coloured cell) | when it is presented or done."""
    cw = [w * 0.55, w * 0.2, w * 0.25]
    body = [_r(x, y, w, 36, LAVENDER, rx=6)]
    for k, (head, x0) in enumerate(zip(("Việc", "Trạng thái", "Trình bày / thời gian"), (x, x + cw[0], x + cw[0] + cw[1]))):
        body.append(_t(x0 + 10, y + 24, head, size=15, weight="bold"))
    for i, (task, status, when) in enumerate(rows):
        cy = y + 36 + i * row_h
        body.append(_r(x, cy, w, row_h, "#FFFFFF", stroke=LAVENDER, sw=1))
        body.append(_r(x + cw[0] + 4, cy + 6, cw[1] - 8, row_h - 12, STATUS_FILL.get(status, LIGHT), rx=10))
        body.append(_t(x + 10, cy + row_h * 0.62, task, size=14))
        body.append(_t(x + cw[0] + cw[1] / 2, cy + row_h * 0.62, status, size=13, weight="bold", anchor="middle"))
        body.append(_t(x + cw[0] + cw[1] + 10, cy + row_h * 0.62, when, size=14))
    return _g(gid, x, y, w, 36 + row_h * len(rows), body)

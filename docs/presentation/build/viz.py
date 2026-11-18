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


def _t(x, y, s, size=16, fill=INK, weight="normal", anchor="start", family=BODY, style="normal") -> str:
    return (f'<text x="{round(x, 1)}" y="{round(y, 1)}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'font-style="{style}" fill="{fill}" text-anchor="{anchor}">{escape(str(s))}</text>')


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
               width: float = 620, mark: dict | None = None) -> str:
    """Line-numbered code; lines in `highlight` (by printed number) get a warm band; `mark` puts a note at a line's end."""
    lh = fs * 1.45
    h = lh * len(lines) + 16
    body = [_r(x, y, width, h, "#FFFFFF", stroke=LAVENDER, rx=8)]
    for i, line in enumerate(lines):
        no, cy = first_no + i, y + 8 + lh * i
        if no in highlight:
            body.append(_r(x + 2, cy, width - 4, lh, HILITE))
        body.append(_t(x + 34, cy + lh * 0.72, no, size=fs - 3, fill=GREY, anchor="end", family=MONO))
        body.append(_t(x + 44, cy + lh * 0.72, line.replace(" ", " ") or " ", size=fs, family=MONO))
        if mark and no in mark:
            body.append(_t(x + width - 10, cy + lh * 0.72, mark[no], size=fs - 2, fill=RED, weight="bold", anchor="end"))
    return _g(gid, x, y, width, h, body)


def bars(gid, x, y, w, h, series: list[tuple], vmax: float, unit: str = "%", label_w: float = 170, nd: int = 1) -> str:
    """Horizontal bars: (label, value, colour[, faded]); value printed at the bar end."""
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
    span = w - label_w
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
           row_h: float = 30, label_w: float = 120, col_colors: dict | None = None) -> str:
    """Dot matrix: rows × cols, a dot in each (row, col) of `cells`; row_mark {row: colour} paints a band."""
    body = []
    w = label_w + cell_w * len(cols)
    for j, c in enumerate(cols):
        body.append(_t(x + label_w + cell_w * (j + 0.5), y + 18, c, size=15, anchor="middle", weight="bold",
                       fill=(col_colors or {}).get(j, INK)))
    for i, r in enumerate(rows):
        cy = y + 30 + i * row_h
        if row_mark and i in row_mark:
            body.append(_r(x, cy, w, row_h, HILITE))
        body.append(_t(x + label_w - 10, cy + row_h * 0.68, r, size=15, anchor="end", family=MONO))
        for j in range(len(cols)):
            if (i, j) in cells:
                body.append(f'<circle cx="{round(x + label_w + cell_w * (j + 0.5), 1)}" cy="{round(cy + row_h / 2, 1)}" r="7" '
                            f'fill="{(col_colors or {}).get(j, NAVY)}"/>')
    return _g(gid, x, y, w, 30 + row_h * len(rows), body)

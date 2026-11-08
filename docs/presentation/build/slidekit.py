"""Text replacement inside round-trip SVG pages, keeping each <text> element's own attributes.

edit(path, {old_snippet: new}) — `new` is a string (one line) or a list of lines. The <text>
whose concatenated content contains `old_snippet` keeps its opening tag; its children are replaced
by the canonical lines model (first line direct, later lines as data-paragraph-line-break tspans).
A run of the form **bold** inside a line becomes a bold tspan.
"""
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

TEXT_RE = re.compile(r"<text\b[^>]*>.*?</text>", re.S)


def _plain(el: str) -> str:
    return re.sub(r"<[^>]+>", "", el).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


def _runs(line: str) -> str:
    parts = re.split(r"(\*\*.+?\*\*)", line)
    out = []
    for p in parts:
        if p.startswith("**") and p.endswith("**"):
            out.append(f'<tspan font-weight="bold">{escape(p[2:-2])}</tspan>')
        elif p:
            out.append(escape(p))
    return "".join(out)


def _render(open_tag: str, lines: list[str]) -> str:
    fs = float(re.search(r'font-size="([\d.]+)"', open_tag).group(1))
    tag = re.sub(r'\s(data-pptx-text-model|data-paragraph-line-height)="[^"]*"', "", open_tag)
    if len(lines) > 1:
        tag = tag[:-1] + f' data-pptx-text-model="lines" data-paragraph-line-height="{round(fs * 1.2, 2)}">'
    # the importer's lines model keeps the first row inside a <tspan>; a bare first row is dropped on export
    body = "<tspan>" + _runs(lines[0]) + "</tspan>" if (len(lines) > 1 or "**" in lines[0]) else _runs(lines[0])
    body += "".join(f'<tspan data-paragraph-line-break="1">{_runs(l)}</tspan>' for l in lines[1:])
    return tag + body + "</text>"


def edit(path, mapping: dict) -> None:
    p = Path(path)
    s = p.read_text()
    for key, new in (mapping.items() if isinstance(mapping, dict) else mapping):
        old, nth = key if isinstance(key, tuple) else (key, None)  # (snippet, n) picks the n-th match
        lines = [new] if isinstance(new, str) else list(new)
        hits = [m for m in TEXT_RE.finditer(s) if old in _plain(m.group(0))]
        exact = [m for m in hits if _plain(m.group(0)).strip() == old]
        if nth is None and len(hits) > 1 and len(exact) == 1:
            hits = exact  # a heading equal to the snippet wins over body text that merely contains it
        if nth is None and len(hits) != 1:
            sys.exit(f"{p.name}: {len(hits)} <text> elements match {old!r}")
        m = hits[nth or 0]
        el = m.group(0)
        open_tag = re.match(r"<text\b[^>]*>", el).group(0)
        s = s[:m.start()] + _render(open_tag, lines) + s[m.end():]
    p.write_text(s)


def texts(path) -> list[str]:
    return [_plain(m.group(0)) for m in TEXT_RE.finditer(Path(path).read_text()) if _plain(m.group(0)).strip()]


def drop_group(path, gid: str) -> None:
    """Delete one top-level <g id=gid>...</g> (balanced) from the page."""
    p = Path(path); s = p.read_text()
    start = s.index(f'<g id="{gid}"'); depth, i = 0, start
    for m in re.finditer(r"<g\b[^>]*?(/?)>|</g>", s[start:]):
        if m.group(0) == "</g>": depth -= 1
        elif not m.group(1): depth += 1
        if depth == 0:
            end = start + m.end(); break
    p.write_text(s[:start] + s[end:])


def append(path, fragment: str) -> None:
    """Insert authored SVG before </svg>."""
    p = Path(path); s = p.read_text(); i = s.rindex("</svg>")
    p.write_text(s[:i] + fragment + s[i:])

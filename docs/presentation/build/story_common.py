"""Helpers and data shared by the storytelling decks (lần 1, lần 2, bảo vệ).

Every number on a slide comes from data/ or from the report's macros (bd._m), the same sources as the report.
"""
import csv
import json
import sys
from pathlib import Path

import viz
from viz import GREY, INK, LAVENDER, MUTED, NAVY, ORANGE, RED, _p, _r, _t  # noqa: F401

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from method_names import name  # noqa: E402,F401

MAIN = ["sbfl_ochiai", "llm_direct", "semloc", "semloc_no_prior", "llm_tests"]
PARTS = {1: "Cơ sở lý thuyết", 2: "Phương pháp giải quyết", 3: "Cải tiến", 4: "Thực nghiệm", 5: "Kết quả",
         6: "Đóng góp và kết luận"}  # 1-5: the teacher's five parts; 6 is unnumbered


def examples() -> dict:
    """The two running examples (scripts/figure_data.py): votes_apportion and blend_orders."""
    return json.loads((ROOT / "data" / "fig_semloc_examples.json").read_text())


def band(bd, page: str, part: int, content: int | None = None) -> None:
    bd.A(page, viz.section_band(f"phan-{part}", part if part <= 5 else None, PARTS[part], content=content))


def _csv(path: Path) -> list[dict]:
    with open(path) as f:
        return list(csv.DictReader(f))


def _title(bd, page: str, title: str) -> None:
    bd.E(page, {"Classification": title})
    bd.D(page, "shape-2194")


def _note(x, y, lines, size=16, fill=MUTED, weight="normal", gid="ghi-chu", w=380) -> str:
    body = [_t(x, y + 22 * k, line, size=size, fill=fill, weight=weight) for k, line in enumerate(lines)]
    return viz._g(gid, x, y - size, w, 22 * len(lines) + 6, body)


def _card(gid, x, y, w, h, head, lines, color=NAVY) -> str:
    body = [_r(x, y, w, h, "#FFFFFF", stroke=color, rx=12, sw=2), _t(x + 18, y + 34, head, size=19, fill=color, weight="bold")]
    body += [_t(x + 18, y + 66 + 24 * k, line, size=16) for k, line in enumerate(lines)]
    return viz._g(gid, x, y, w, h, body)


def _unbold(bd, page: str, starts: str) -> None:
    """Drop a template's bold on the <text> whose first line starts with `starts`."""
    if not bd.has(page):
        return
    import re
    p = bd.SVG / page
    s = p.read_text()
    m = re.search(r'<text\b[^>]*>(?:<tspan>)?' + re.escape(starts), s)
    if not m:
        raise SystemExit(f"{page}: no text starting with {starts!r}")
    tag_end = s.index(">", m.start())
    s = s[:m.start()] + s[m.start():tag_end].replace(' font-weight="bold"', "") + s[tag_end:]
    p.write_text(s)


def cover(bd, deck: str, occasion: str) -> None:
    """Vietnamese title large; underneath, the English paper title small and italic, then topic, group, advisor, date."""
    bd.E("slide_01.svg", {
        "Introduction to Coding Workshop": ["Bằng chứng hay phỏng đoán:", "Tái hiện và đánh giá việc định vị",
                                            "lỗi ngữ nghĩa trong mã nguồn bằng", "mô hình ngôn ngữ lớn"],
    })
    if not bd.has("slide_01.svg"):
        return
    bd.D("slide_01.svg", "shape-1430")  # template subtitle box: hanging indent; replaced by our own frame
    p = bd.SVG / "slide_01.svg"
    s = p.read_text()
    s = s.replace('y="217.42351706" text-anchor="start" xml:space="preserve" font-size="60"',
                  'y="150" text-anchor="start" xml:space="preserve" font-size="36"', 1)
    s = s.replace('font-size="36" fill="#0C0A9E" data-pptx-text-baseline="metrics-v1" data-pptx-text-model="lines" '
                  'data-paragraph-line-height="72.0"', 'font-size="36" fill="#0C0A9E" data-pptx-text-baseline="metrics-v1" '
                  'data-pptx-text-model="lines" data-paragraph-line-height="46"', 1)
    p.write_text(s)
    x = 124.75
    rows = [("Grounded or Guessed: A Reproducibility Study", "italic", MUTED, 0),
            ("of LLM-Based Semantic Fault Localization", "italic", MUTED, 22),
            ("Đề tài 02-KH · Nhóm M9", "normal", INK, 34),
            ("GVHD: PGS. TS. Huỳnh Quyết Thắng", "normal", INK, 22),
            (occasion, "normal", INK, 22)]
    body = "".join(f'<tspan x="{x}" dy="{dy}" font-style="{st}" fill="{c}">{t}</tspan>' for t, st, c, dy in rows)
    bd.A("slide_01.svg", f'<g id="phu-de-bia" data-pptx-bounds="{x} 360 520 150"><text x="{x}" y="380" '
                         f'font-family="{viz.BODY}" font-size="16">{body}</text></g>')


def _bonus_rows() -> list[dict]:
    from make_figures import bonus_example
    return bonus_example()[1]


def _guess_rank1_share() -> tuple[float, int]:
    rows = _csv(ROOT / "data" / "semloc_line_scores.csv")
    guesses = [r for r in rows if r["is_guess"] == "1"]
    return sum(r["rank"] == "1" for r in guesses) / len(guesses), len(guesses)



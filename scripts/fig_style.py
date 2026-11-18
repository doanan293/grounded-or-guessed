"""Shared look of the report figures: Times New Roman 13 pt at print size (guide III.1.2), decimal comma in Vietnamese,
one accent colour per role. FailLoc (the group's method) is always orange, SemLoc always blue, everything else grey;
the two accents pass the dataviz palette validator (CVD ΔE 26, contrast ≥ 3:1)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

WIDTH_IN = 16 / 2.54  # \linewidth of the Vietnamese report (A4, 2.5 cm margins)
FAILLOC, SEMLOC, GREY, INK, MUTED, GRID = "#d9541e", "#2a78d6", "#9a9a94", "#1d1d1b", "#5f5f5a", "#e4e4df"
COLOR = {"llm_tests": FAILLOC, "semloc": SEMLOC}


def color(method: str) -> str:
    return COLOR.get(method, GREY)


def apply(lang: str = "vi") -> None:
    for d in (Path.home() / ".local/share/fonts", Path("/usr/share/fonts")):
        for f in d.glob("**/times*.ttf"):
            font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({
        "font.family": "serif", "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
        "font.size": 13, "axes.labelsize": 13, "xtick.labelsize": 13, "ytick.labelsize": 13, "legend.fontsize": 13,
        "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
        "pdf.fonttype": 42, "savefig.dpi": 300,
    })


def fmt(v: float, nd: int = 1, lang: str = "vi") -> str:
    s = f"{v:.{nd}f}"
    return s.replace(".", ",") if lang == "vi" else s

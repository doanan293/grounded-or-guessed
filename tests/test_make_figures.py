import csv
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("make_figures", ROOT / "scripts" / "make_figures.py")
mf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mf)
VI = ROOT / "docs" / "report" / "generated" / "vi"


def _rq2(gt, m):
    return next(r for r in csv.DictReader(open(ROOT / "data" / "rq2_ours.csv"))
                if r["gt"] == gt and r["method"] == m and r.get("subset", "all") == "all")


def test_c1_matches_table():
    rows = mf.rq2_main_data(("original", "repaired"))
    assert {r["method"] for r in rows} == {"sbfl_ochiai", "llm_direct", "semloc", "semloc_no_prior", "llm_tests"}
    r = next(r for r in rows if r["gt"] == "repaired" and r["method"] == "llm_tests")
    assert abs(r["acc1"] - 100 * float(_rq2("repaired", "llm_tests")["acc1_mean"])) < 1e-9
    assert abs(r["acc3_sd"] - 100 * float(_rq2("repaired", "llm_tests")["acc3_sd"])) < 1e-9


def test_cost_points():
    pts = {p["method"]: p for p in mf.cost_acc_data()}
    assert set(pts) == {"llm_direct", "semloc", "llm_tests"}
    assert pts["llm_tests"]["ktokens"] < pts["semloc"]["ktokens"]


def test_vi_decimal_comma():
    assert mf.fmt(52.25, 1) == "52,2" or mf.fmt(52.25, 1) == "52,3"
    assert mf.fmt(4.0, 1) == "4,0"


def test_pdf_width_16cm():
    mf.main()
    for name in ("fig_rq2_main", "fig_cost_acc", "fig_semloc_bonus"):
        info = subprocess.run(["pdfinfo", str(VI / f"{name}.pdf")], capture_output=True, text=True).stdout
        w_pt = float(next(l for l in info.splitlines() if l.startswith("Page size")).split()[2])
        assert abs(w_pt / 72 * 2.54 - 16.0) < 0.1, name

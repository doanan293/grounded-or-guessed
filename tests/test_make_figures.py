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
    for name in ("fig_rq2_main", "fig_cost_acc", "fig_semloc_bonus", "fig_label_flow", "fig_ablation", "fig_addons",
                 "fig_rq3", "fig_decomposition", "fig_improvement", "fig_failures"):
        info = subprocess.run(["pdfinfo", str(VI / f"{name}.pdf")], capture_output=True, text=True).stdout
        w_pt = float(next(l for l in info.splitlines() if l.startswith("Page size")).split()[2])
        assert abs(w_pt / 72 * 2.54 - 16.0) < 0.1, name


def test_sbfl_matrix_tex():
    import json
    ex = json.loads((ROOT / "data" / "fig_example.json").read_text())
    tex = mf.sbfl_matrix_tex(ex)
    assert tex.startswith("\\begin{tikzpicture}") and tex.rstrip().endswith("\\end{tikzpicture}")
    assert tex.count("\\covdot") == sum(len(t["lines"]) for t in ex["tests"])
    assert tex.count("\\testhead") == len(ex["tests"])
    assert "\\gtrow" in tex  # the labelled fault line is highlighted
    # every Ochiai value printed equals ef/sqrt((ef+nf)(ef+ep)) of its line
    assert "0,45" in tex


def _examples():
    import json
    return json.loads((ROOT / "data" / "fig_semloc_examples.json").read_text())


def test_semloc_example_tex_lists_constraints_and_scores():
    bo = _examples()["blend_orders"]
    tex = mf.semloc_example_tex(bo)
    for c in bo["constraints"]:
        assert c["id"] in tex and mf.fmt(c["ochiai"], 2) in tex
    assert "0,60 + 1,2" in tex and "kiểm tra C1" in tex and "Hệ số vùng" in tex
    assert "1,00 & 0,6 & 0,60" in tex  # C1: Ochiai × region weight = score given to line 73
    assert "\\begin{tabular}" in tex


def test_failloc_example_tex_shows_prompt_and_answer():
    va = _examples()["votes_apportion"]
    tex = mf.failloc_example_tex(va)
    assert "test\\_truncation\\_sum\\_equals\\_total\\_fail" in tex and "exactly one faulty line" in tex
    assert "[29, 25, 26, 28, 30]" in tex


def test_label_flow_sums_to_n():
    d = mf.label_flow_data()
    assert sum(v for _, v in d["parts"]) == d["n"] == 250


def test_ablation_rows_match_csv():
    rows = mf.ablation_data()
    r = next(x for x in rows if x["gt"] == "repaired" and x["contrast"] == "tests_effect")
    assert abs(r["d_acc1"] - 5.44) < 1e-6 and abs(r["lo1"] - 1.68) < 1e-6
    assert {x["gt"] for x in rows} == {"original", "repaired", "reviewed"}


def test_addons_include_covgate_cov_and_vote():
    names = [r["name"] for r in mf.addons_data()]
    assert any("CovGate" in n for n in names) and any("FailLoc+Cov" in n for n in names) and any("FailLoc+Vote" in n for n in names)


def test_rq3_panels():
    d = mf.rq3_data()
    assert abs(d["bugsinpy"]["llm_tests"] - 50.54) < 1e-6
    assert len(d["families"]) == 5
    assert abs(d["renamed"]["semloc_no_prior"][1] - 55.91) < 1e-6  # Acc@3 after renaming, normalized labels


def test_decomposition_and_improvement():
    d = mf.decomposition_data()
    r = next(x for x in d if x["gt"] == "repaired" and x["metric"] == "acc1")
    assert abs(r["guess"] - 32.28) < 1e-6 and abs(r["spectrum"] - 21.58) < 1e-6
    imp = {r["setting"]: r for r in mf.improvement_data()}
    assert abs(imp["Nhãn đã chuẩn hóa"]["failloc1"] - 64.2) < 0.05 and "BugsInPy (lỗi thật)" in imp


def test_failure_categories_count_programs():
    d = dict(mf.failure_data())
    assert sum(d.values()) > 0 and "prior_hurts" in d


def test_english_figures_for_the_paper():
    mf.main_en()
    out = ROOT / "docs" / "report" / "generated"
    for name in ("fig_rq2_main", "fig_ablation", "fig_improvement"):
        info = subprocess.run(["pdfinfo", str(out / f"{name}.pdf")], capture_output=True, text=True).stdout
        w_pt = float(next(l for l in info.splitlines() if l.startswith("Page size")).split()[2])
        assert abs(w_pt / 72 * 2.54 - 18.2) < 0.1, name
        text = subprocess.run(["pdftotext", str(out / f"{name}.pdf"), "-"], capture_output=True, text=True).stdout
        assert "nhãn" not in text.lower() and "," not in text.replace(", ", ""), name  # English labels, decimal points

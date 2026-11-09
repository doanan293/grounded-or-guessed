import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("make_tables", ROOT / "scripts" / "make_tables.py")
mt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mt)


def test_to_vi_translates_labels_and_uses_decimal_commas():
    en = (r"SemLoc (as released) & 52.3{\scriptsize$\pm$0.8} & +16.6{\scriptsize\,[10.5, 22.8]} \\" + "\n"
          r"\multicolumn{7}{l}{\emph{Execution-repaired ground truth, $n=179$, 3 repeats}} \\" + "\n"
          r"\cmidrule(lr){2-4} Method & Acc@1 & $\Delta$Acc@1 [95\% CI] \\")
    vi = mt.to_vi(en)
    assert "SemLoc (bản phát hành)" in vi and "52,3{\\scriptsize$\\pm$0,8}" in vi and "+16,6{\\scriptsize\\,[10,5; 22,8]}" in vi
    assert "Ground truth đã sửa bằng thực thi, $n=179$, 3 lần lặp" in vi
    assert r"\cmidrule(lr){2-4}" in vi and "Phương pháp" in vi and "[CI 95\\%]" in vi


def test_to_vi_leaves_no_known_english_label():
    for name in ("rq1_table", "rq2_table", "rq3_bugsinpy_table", "rq3_renamed_table", "rq3_families_table",
                 "rq2_by_label_table", "decomposition_ours_table", "decomposition_table"):
        vi = mt.to_vi(getattr(mt, name)())
        for word in ("ground truth,", "repeats", "Method", "Original", "Renamed", "w/o", "only", "alone", "All bugs"):
            assert word not in vi, (name, word)


def test_pct_and_escape():
    assert mt.pct(0.428) == "42.8"
    assert mt.pct(None) == "--"
    assert mt.tex("semloc_claude_T0.8") == r"semloc\_claude\_T0.8"


def test_rq1_table_has_author_and_fair_columns():
    tex = mt.rq1_table()
    assert r"\begin{tabular}" in tex and "Author" in tex and "Fair" in tex
    assert "42.8" in tex  # SemLoc Claude T=0.8, author scoring, all 250

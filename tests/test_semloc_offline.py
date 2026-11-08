import json

from flx._semloc import SEMLOC_ROOT, ensure_on_path


def test_published_summary_matches_paper():
    s = json.loads((SEMLOC_ROOT / "results/RQ1/semloc_claude_T0.8/results/summary.json").read_text())
    assert s["n_programs"] == 250
    assert s["rq1"]["top1_accuracy"] == 0.428
    assert s["rq1"]["top3_accuracy"] == 0.68


def test_semloc_modules_importable():
    ensure_on_path()
    import baselines  # noqa: F401
    import constraint_inference  # noqa: F401
    import spectrum  # noqa: F401

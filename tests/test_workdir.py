import json

from flx._semloc import SEMLOC_ROOT
from flx.workdir import make_workdir

BENCH = SEMLOC_ROOT / "benchmark"


def test_make_workdir_subset(tmp_path):
    make_workdir(BENCH, ["ad_mix", "adjust_queue"], tmp_path / "w")
    assert sorted(p.name for p in (tmp_path / "w/programs").iterdir()) == ["ad_mix.py", "adjust_queue.py"]
    assert sorted(p.name for p in (tmp_path / "w/testcases").iterdir()) == ["test_ad_mix.py", "test_adjust_queue.py"]
    assert (tmp_path / "w/programs/ad_mix.py").read_text() == (BENCH / "programs/ad_mix.py").read_text()
    gt = json.loads((tmp_path / "w/ground_truth.json").read_text())
    assert [p["function"] for p in gt["programs"]] == ["ad_mix", "adjust_queue"]


def test_make_workdir_idempotent(tmp_path):
    make_workdir(BENCH, ["ad_mix"], tmp_path / "w")
    make_workdir(BENCH, ["ad_mix"], tmp_path / "w")
    assert len(list((tmp_path / "w/programs").iterdir())) == 1


def test_program_source_falls_back_to_the_benchmark(tmp_path):
    """Archived runs carry no programs/ symlinks: analysis must find the source the run used (renamed or original)."""
    from flx.workdir import program_source
    root = tmp_path
    (root / "third_party" / "semloc" / "benchmark" / "programs").mkdir(parents=True)
    (root / "data" / "semfault_renamed" / "programs").mkdir(parents=True)
    (root / "third_party" / "semloc" / "benchmark" / "programs" / "p.py").write_text("orig")
    (root / "data" / "semfault_renamed" / "programs" / "p.py").write_text("renamed")
    run = root / "runs" / "semloc_test_gemini_r1"
    (run / "programs").mkdir(parents=True)
    assert program_source(run, "p", root).read_text() == "orig"
    assert program_source(root / "runs" / "semloc_renamed_gemini_r1", "p", root).read_text() == "renamed"
    (run / "programs" / "p.py").write_text("own")
    assert program_source(run, "p", root).read_text() == "own"

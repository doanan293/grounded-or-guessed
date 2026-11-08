from pathlib import Path

import pytest

from flx._semloc import SEMLOC_ROOT
from flx.rename import keep_names, rename_program, test_outcomes

FX = Path(__file__).parent / "fixtures"
BENCH = SEMLOC_ROOT / "benchmark"
CASES = [(FX / "mini/programs/prog.py", FX / "mini/testcases/test_prog.py")] + [
    (BENCH / "programs" / f"{p}.py", BENCH / "testcases" / f"test_{p}.py")
    for p in ("ad_mix", "calibrate_latency", "api_rate_guard")]


@pytest.mark.parametrize("prog,test", CASES, ids=lambda p: Path(p).stem)
def test_renamed_preserves_lines_and_outcomes(prog, test):
    src = prog.read_text()
    out = rename_program(src, keep_names(test.read_text()))
    assert out.count("\n") == src.count("\n")
    assert test_outcomes(out, prog, test) == test_outcomes(src, prog, test)
    assert out != src


def test_rename_hides_identifiers_and_docstrings():
    src = (BENCH / "programs/calibrate_latency.py").read_text()
    out = rename_program(src, keep_names((BENCH / "testcases/test_calibrate_latency.py").read_text()))
    assert "def calibrate_latency(" in out          # the function the tests import keeps its name
    assert "_compute_parameter" not in out           # private helper renamed
    assert "Interpolated latency value" not in out   # docstring text removed
    assert "#" not in "".join(l for l in out.splitlines() if l.strip().startswith("#"))


def test_rename_is_deterministic():
    src = (BENCH / "programs/ad_mix.py").read_text()
    keep = keep_names((BENCH / "testcases/test_ad_mix.py").read_text())
    assert rename_program(src, keep) == rename_program(src, keep)

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("method_names", ROOT / "scripts" / "method_names.py")
mn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mn)


def test_names_fixed():
    assert mn.name("llm_tests") == "FailLoc"
    assert mn.name("llm_direct") == "LLM-Direct"
    assert mn.name("llm_coverage") == "FailLoc+Cov"
    assert mn.name("semloc") == "SemLoc"
    assert mn.name("semloc_no_prior") == "SemLoc−Bonus"
    assert mn.name("sbfl_ochiai") == "SBFL (Ochiai)"
    assert mn.name("covgate") == "CovGate"
    assert mn.OURS == "llm_tests"
    with pytest.raises(KeyError):
        mn.name("nope")

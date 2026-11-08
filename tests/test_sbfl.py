import json
import math

from flx._semloc import SEMLOC_ROOT
from flx.coverage import load
from flx.sbfl import sbfl_scores


def test_ochiai_matches_published():
    cov = load("data/coverage/semfault/ad_mix.json")
    ours = sbfl_scores(cov, "ochiai")
    pub = json.loads((SEMLOC_ROOT / "results/RQ1/sbfl_ochiai/ad_mix.json").read_text())["sbfl"]["line_scores"]
    assert set(ours) == {int(k) for k in pub}
    assert all(math.isclose(ours[int(k)], v, abs_tol=1e-9) for k, v in pub.items())


def test_dstar_formula():
    cov = {"program": "x", "tests": [
        {"id": "f1", "passed": False, "lines": [5]}, {"id": "f2", "passed": False, "lines": [5]},
        {"id": "p1", "passed": True, "lines": [5, 6]}]}
    s = sbfl_scores(cov, "dstar")
    assert s[5] == 4.0 and 6 not in s  # ef=2, ep=1, nf=0 → 2²/(1+0); line 6 never run by a failing test

import json
from pathlib import Path

from flx.coverage import collect, load, save

MINI = Path(__file__).parent / "fixtures" / "mini"


def test_collect_mini(tmp_path):
    cov = collect("prog", MINI / "programs" / "prog.py", MINI / "testcases" / "test_prog.py")
    assert cov["program"] == "prog"
    by_name = {t["id"].split("::")[-1]: t for t in cov["tests"]}
    assert [by_name[n]["passed"] for n in ("test_a", "test_b", "test_c", "test_d")] == [True, True, False, False]
    assert 7 in by_name["test_c"]["lines"] and 4 in by_name["test_d"]["lines"]
    assert 4 not in by_name["test_a"]["lines"]
    p = tmp_path / "prog.json"
    save(cov, p)
    assert load(p) == cov and json.loads(p.read_text())["program"] == "prog"

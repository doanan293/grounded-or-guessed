from flx.labels import Label
from flx.split import make_split


def _labels(n=250, n_sem=150):
    return [Label(f"p{i:03d}", 3, 1, True, i < n_sem, "semantic" if i < n_sem else "coverage_revealed")
            for i in range(n)]


def test_split_sizes_and_determinism():
    s1, s2 = make_split(_labels()), make_split(_labels())
    assert s1 == s2 and len(s1["dev"]) == 50 and len(s1["test"]) == 200
    assert not set(s1["dev"]) & set(s1["test"])
    assert s1["seed"] == 20261108 and s1["dev"] == sorted(s1["dev"])


def test_split_stratified():
    labs = _labels()
    s = make_split(labs)
    sem = {l.program for l in labs if l.category == "semantic"}
    share_dev = sum(p in sem for p in s["dev"]) / 50
    assert abs(share_dev - len(sem) / len(labs)) <= 0.05

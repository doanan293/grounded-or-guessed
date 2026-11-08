from flx.decompose import shapley


def test_shapley_additive_game():
    w = {"a": 0.1, "b": 0.3, "c": 0.05}
    phi = shapley(lambda S: sum(w[p] for p in S), list(w))
    assert all(abs(phi[p] - w[p]) < 1e-12 for p in w)


def test_shapley_sums_to_grand_coalition():
    v = lambda S: 0.4 if {"a", "b"} <= S else (0.1 if S else 0.0)
    phi = shapley(v, ["a", "b", "c"])
    assert abs(sum(phi.values()) - v(frozenset("abc"))) < 1e-12


def test_component_scores_compose_signals():
    from flx.decompose import component_scores
    cov = {"program": "p", "tests": [{"id": "f", "passed": False, "lines": [3, 5]},
                                     {"id": "p", "passed": True, "lines": [3]}]}
    sem = {"line_scores": {"3": 0.5, "5": 1.2 + 0.2}, "fault_line_pred": 5, "constraint_scores": {}}
    assert component_scores(sem, cov, frozenset()) == {}
    assert component_scores(sem, cov, frozenset({"guess"})) == {5: 1.2}
    s = component_scores(sem, cov, frozenset({"spectrum"}))
    assert abs(s[3] - 0.5) < 1e-9 and abs(s[5] - 0.2) < 1e-9
    c = component_scores(sem, cov, frozenset({"coverage"}))
    assert c[5] > c[3] > 0


def test_per_program_shapley_averages_to_the_aggregate():
    """Acc@k is a mean of per-program hits, so the aggregate Shapley value is the mean of per-program ones
    (what makes a per-program / cluster bootstrap of the decomposition valid)."""
    from flx.decompose import per_program_shapley, shapley
    progs = ["a", "b", "c"]
    hit = {"a": lambda s: float("g" in s), "b": lambda s: float({"g", "s"} <= s), "c": lambda s: float(bool(s))}
    per = per_program_shapley(lambda s: {p: hit[p](s) for p in progs}, ["g", "s"], progs)
    agg = shapley(lambda s: sum(hit[p](s) for p in progs) / 3, ["g", "s"])
    for pl in ("g", "s"):
        assert abs(sum(per[p][pl] for p in progs) / 3 - agg[pl]) < 1e-12
    assert per["b"] == {"g": 0.5, "s": 0.5}

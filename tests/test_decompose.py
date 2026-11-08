from flx.decompose import shapley


def test_shapley_additive_game():
    w = {"a": 0.1, "b": 0.3, "c": 0.05}
    phi = shapley(lambda S: sum(w[p] for p in S), list(w))
    assert all(abs(phi[p] - w[p]) < 1e-12 for p in w)


def test_shapley_sums_to_grand_coalition():
    v = lambda S: 0.4 if {"a", "b"} <= S else (0.1 if S else 0.0)
    phi = shapley(v, ["a", "b", "c"])
    assert abs(sum(phi.values()) - v(frozenset("abc"))) < 1e-12

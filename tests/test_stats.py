import math

from flx.stats import mcnemar


def test_mcnemar_exact_small():
    # discordant pairs b=8 (only a correct), c=2 (only b correct): exact two-sided binomial p = 0.109375
    a = [True] * 8 + [False] * 2 + [True] * 5
    b = [False] * 8 + [True] * 2 + [True] * 5
    stat, p = mcnemar(a, b)
    assert math.isclose(p, 0.109375, rel_tol=1e-6)


def test_mcnemar_identical_is_one():
    assert mcnemar([True, False], [True, False])[1] == 1.0


def test_wilcoxon_paired_detects_shift():
    from flx.stats import wilcoxon_paired
    x = [1, 2, 1, 3, 2, 1, 2, 1, 1, 2]
    y = [3, 4, 3, 5, 4, 3, 4, 3, 3, 4]
    assert wilcoxon_paired(x, y)[1] < 0.01
    assert wilcoxon_paired(x, x)[1] == 1.0


def test_cliffs_delta_bounds():
    from flx.stats import cliffs_delta
    assert cliffs_delta([5, 6, 7], [1, 2, 3]) == 1.0
    assert cliffs_delta([1, 2, 3], [5, 6, 7]) == -1.0
    assert cliffs_delta([1, 2], [1, 2]) == 0.0


def test_cluster_bootstrap_wider_than_plain():
    from flx.stats import cluster_bootstrap_ci
    vals = {f"p{i}": float(i < 10) for i in range(20)}        # 10 ones, 10 zeros
    one_cluster_each = {p: i for i, p in enumerate(vals)}
    two_clusters = {p: int(v) for p, v in vals.items()}       # ones in one cluster, zeros in the other
    lo1, hi1 = cluster_bootstrap_ci(vals, one_cluster_each, n=2000)
    lo2, hi2 = cluster_bootstrap_ci(vals, two_clusters, n=2000)
    assert hi2 - lo2 > hi1 - lo1


def test_paired_rank_biserial():
    """Matched-pairs rank-biserial: (sum of ranks of positive diffs − negative) / total rank sum, zeros dropped."""
    from flx.stats import paired_rank_biserial
    assert paired_rank_biserial([1, 1, 1], [0, 0, 0]) == 1.0
    assert paired_rank_biserial([0, 0], [1, 1]) == -1.0
    # diffs +1, +2, −3 → ranks 1, 2, 3 → (1 + 2 − 3) / 6 = 0
    assert paired_rank_biserial([1, 2, 0], [0, 0, 3]) == 0.0
    # zero differences are dropped: one +0.5, rest ties → +1
    assert paired_rank_biserial([0.5, 1, 1], [0, 1, 1]) == 1.0
    assert paired_rank_biserial([1, 1], [1, 1]) == 0.0


def test_paired_diff_ci_resamples_programs_not_repeats():
    from flx.stats import paired_diff_ci
    progs = [f"p{i}" for i in range(10)]
    hit, miss = {p: True for p in progs}, {p: False for p in progs}
    assert paired_diff_ci([hit] * 3, [miss] * 3, progs, None, k_boot=500) == (1.0, 1.0, 1.0)
    a = {p: i % 2 == 0 for i, p in enumerate(progs)}
    b = {p: i % 3 == 0 for i, p in enumerate(progs)}
    one = paired_diff_ci([a], [b], progs, None, k_boot=2000)
    three = paired_diff_ci([a, a, a], [b, b, b], progs, None, k_boot=2000)
    assert one == three  # copying a repeat adds no information, so the interval must not shrink


def test_paired_diff_ci_cluster_widens():
    from flx.stats import paired_diff_ci
    progs = [f"p{i}" for i in range(20)]
    a = {p: i < 10 for i, p in enumerate(progs)}
    b = {p: False for p in progs}
    clusters = {p: i // 10 for i, p in enumerate(progs)}  # two clusters: all-hit and all-miss
    d0, lo0, hi0 = paired_diff_ci([a], [b], progs, None, k_boot=2000)
    d1, lo1, hi1 = paired_diff_ci([a], [b], progs, clusters, k_boot=2000)
    assert d0 == d1 == 0.5 and (hi1 - lo1) > (hi0 - lo0)

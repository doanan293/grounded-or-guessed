"""Paired tests for per-program outcomes."""
from math import comb


def mcnemar(a: list[bool], b: list[bool]) -> tuple[float, float]:
    """McNemar test on paired correct/incorrect outcomes. Exact two-sided binomial when b+c < 25,
    otherwise the continuity-corrected chi-square approximation. Returns (statistic, p)."""
    assert len(a) == len(b)
    n01 = sum(1 for x, y in zip(a, b) if x and not y)
    n10 = sum(1 for x, y in zip(a, b) if y and not x)
    n = n01 + n10
    if n == 0:
        return 0.0, 1.0
    if n < 25:
        k = min(n01, n10)
        p = min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)
        return float(k), p
    stat = (abs(n01 - n10) - 1) ** 2 / n
    from math import erfc, sqrt
    return stat, erfc(sqrt(stat / 2))  # chi-square(1) survival


def wilcoxon_paired(x: list[float], y: list[float]) -> tuple[float, float]:
    """Two-sided Wilcoxon signed-rank test on paired values (zero differences dropped)."""
    from scipy.stats import wilcoxon
    if all(a == b for a, b in zip(x, y)):
        return 0.0, 1.0
    r = wilcoxon(x, y, zero_method="wilcox", alternative="two-sided")
    return float(r.statistic), float(r.pvalue)


def cliffs_delta(x: list[float], y: list[float]) -> float:
    """P(X > Y) − P(X < Y) over all pairs; in [−1, 1]."""
    gt = sum(1 for a in x for b in y if a > b)
    lt = sum(1 for a in x for b in y if a < b)
    return (gt - lt) / (len(x) * len(y))


def cluster_bootstrap_ci(per_program: dict[str, float], clusters: dict[str, int], n: int = 10000,
                         seed: int = 20261108, alpha: float = 0.05) -> tuple[float, float]:
    """Percentile CI of the mean, resampling whole clusters (structurally similar programs together).
    Each draw picks as many clusters as there are, with replacement; the statistic is the mean over the
    programs of the drawn clusters (vectorized: per-cluster sums and sizes)."""
    import numpy as np
    groups: dict = {}
    for p, v in per_program.items():
        g = groups.setdefault(clusters.get(p, ("solo", p)), [0.0, 0])
        g[0] += v
        g[1] += 1
    sums = np.array([g[0] for g in groups.values()])
    sizes = np.array([g[1] for g in groups.values()])
    idx = np.random.default_rng(seed).integers(0, len(sums), size=(n, len(sums)))
    stats = np.sort(sums[idx].sum(axis=1) / sizes[idx].sum(axis=1))
    return float(stats[int(alpha / 2 * n)]), float(stats[int((1 - alpha / 2) * n) - 1])


def paired_rank_biserial(x: list[float], y: list[float]) -> float:
    """Matched-pairs rank-biserial correlation (the effect size of the Wilcoxon signed-rank test), in [−1, 1]:
    (R+ − R−) / (R+ + R−) over |x − y| ranks (average ranks for ties), zero differences dropped."""
    from scipy.stats import rankdata
    d = [a - b for a, b in zip(x, y) if a != b]
    if not d:
        return 0.0
    ranks = rankdata([abs(v) for v in d])
    pos = sum(r for r, v in zip(ranks, d) if v > 0)
    neg = sum(r for r, v in zip(ranks, d) if v < 0)
    return float((pos - neg) / (pos + neg))


def paired_diff_ci(a: list[dict], b: list[dict], programs: list[str], clusters: dict | None,
                   k_boot: int = 10000, seed: int = 20261108) -> tuple[float, float, float]:
    """(Δ, lo, hi): Acc(a) − Acc(b) with a 95% bootstrap CI. `a` and `b` are repeats, each {program: hit}
    (absent = miss). Each program's hits are averaged over repeats *before* resampling, so the unit of
    resampling is the program (or its template cluster), never a repeat."""
    def avg(reps, p):
        return sum(bool(r.get(p, False)) for r in reps) / len(reps)
    diff = {p: avg(a, p) - avg(b, p) for p in programs}
    delta = sum(diff.values()) / len(diff)
    lo, hi = cluster_bootstrap_ci(diff, clusters if clusters is not None else {p: i for i, p in enumerate(programs)},
                                  n=k_boot, seed=seed)
    return round(delta, 4), round(lo, 4), round(hi, 4)

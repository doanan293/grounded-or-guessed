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
    """Percentile CI of the mean, resampling whole clusters (structurally similar programs together)."""
    import random
    rng = random.Random(seed)
    groups: dict[int, list[float]] = {}
    for p, v in per_program.items():
        groups.setdefault(clusters.get(p, hash(p)), []).append(v)
    keys = list(groups)
    stats = []
    for _ in range(n):
        vals = [v for k in (rng.choice(keys) for _ in keys) for v in groups[k]]
        stats.append(sum(vals) / len(vals))
    stats.sort()
    return stats[int(alpha / 2 * n)], stats[int((1 - alpha / 2) * n) - 1]


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

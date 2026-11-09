from flx.failures import CATEGORIES, category, select

BASE = {"guess_hit": False, "semloc_top1": False, "semloc_top3": False, "spectrum_rank": None,
        "llmcov_top3": False, "gt_status": "confirmed"}


def test_category_rules():
    assert category({**BASE, "guess_hit": True, "semloc_top1": True, "semloc_top3": True}) == "guess_right"
    assert category({**BASE, "semloc_top3": True, "spectrum_rank": 2.0}) == "rescued_by_spectrum"
    assert category({**BASE, "spectrum_rank": 1.0, "semloc_top3": True}) == "prior_hurts"
    assert category({**BASE, "llmcov_top3": True}) == "coverage_only_wins"
    assert category(BASE) == "all_miss"
    assert category({**BASE, "gt_status": "unverified"}) == "gt_suspect"      # checked before all_miss
    assert category({**BASE, "gt_status": "unverifiable"}) == "gt_suspect"
    assert set(CATEGORIES) == {"guess_right", "rescued_by_spectrum", "prior_hurts", "coverage_only_wins",
                               "all_miss", "gt_suspect"}


def test_select_spreads_clusters():
    cases = [{"program": f"p{i}", "category": "all_miss", "cluster": i % 3} for i in range(6)]
    picked = select(cases, per_category=3, seed=20261108)
    assert len(picked) == 3 and len({c["cluster"] for c in picked}) == 3
    assert picked == select(cases, per_category=3, seed=20261108)
    assert len(select(cases, per_category=10, seed=1)) == 6


SRC = '''def f(xs, cap):
    total = 0
    for x in xs:
        if x > cap:
            total += cap - 1
        else:
            total += x

    return total
'''


def test_line_relation():
    from flx.failures import line_relation
    assert line_relation(SRC, 4, 5) == "header_body"      # `if x > cap:` vs its first body line
    assert line_relation(SRC, 5, 4) == "header_body"      # symmetric
    assert line_relation(SRC, 3, 4) == "header_body"      # `for` header vs nested `if` (first body statement)
    assert line_relation(SRC, 8, 9) == "blank_gt"         # ground truth on a blank line
    assert line_relation(SRC, 2, 9) == "other"
    assert line_relation(SRC, 5, 5) == "same"


NESTED = '''def g(v, cap):
    if cap is not None:
        if v > cap:
            v = cap - 1
    for i in range(3):
        a = i
        b = a + 1
        c = b + 1
        d = c + 1
    return v
'''


def test_line_relation_nested_guard():
    from flx.failures import line_relation
    assert line_relation(NESTED, 2, 4) == "header_body"   # outer guard vs the statement its nested guard protects
    assert line_relation(NESTED, 5, 8) == "other"         # third statement of a loop body is not the guarded one

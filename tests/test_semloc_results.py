import sys

import pytest

from flx._semloc import SEMLOC_ROOT
from flx.semloc_results import (acc_at_k, best_ranks_from_csv, dd_best_ranks, direct_fl_best_ranks,
                                find_localization_csv, median_rank, rq1a_table, sbfl_best_ranks)

RQ1 = SEMLOC_ROOT / "results" / "RQ1"
GT = SEMLOC_ROOT / "benchmark" / "ground_truth.json"


def test_acc_at_k_counts_none_as_miss():
    assert acc_at_k({"a": 1, "b": 4, "c": None}, 3) == 1 / 3


def test_median_rank_ignores_misses_like_upstream():
    assert median_rank({"a": 1, "b": 6, "c": 2, "d": None}) == 2


def test_semloc_claude_t08_matches_summary():
    ranks = best_ranks_from_csv(find_localization_csv(RQ1 / "semloc_claude_T0.8"))
    assert len(ranks) == 250
    assert round(acc_at_k(ranks, 1), 3) == 0.428 and round(acc_at_k(ranks, 3), 3) == 0.68


def test_sbfl_ochiai_matches_paper():
    ranks = sbfl_best_ranks(RQ1 / "sbfl_ochiai", GT)
    assert round(acc_at_k(ranks, 1), 3) == 0.064 and round(acc_at_k(ranks, 3), 3) == 0.132


def test_dd_counts_any_hit_as_rank_one_like_upstream():
    ranks = dd_best_ranks(RQ1 / "dd", GT)
    assert set(ranks.values()) <= {1, None}
    assert round(acc_at_k(ranks, 1), 3) == 0.38


def test_direct_fl_matches_upstream():
    ranks = direct_fl_best_ranks(RQ1 / "semantic_indexing_disabled_claude")
    assert round(acc_at_k(ranks, 1), 3) == 0.352 and round(acc_at_k(ranks, 3), 3) == 0.412


def test_table_matches_upstream_print_results_for_every_config():
    sys.path.insert(0, str(SEMLOC_ROOT))
    import print_results as up
    gt = up.load_ground_truth()
    rows = {r["config"]: r for r in rq1a_table(RQ1, GT)}
    assert len(rows) == 13
    for cfg, r in rows.items():
        d = str(RQ1 / cfg)
        if cfg.startswith("sbfl_"):
            ref = up._acc_from_sbfl(d, cfg.split("_", 1)[1], gt)
        elif cfg == "dd":
            ref = up._acc_from_sbfl(d, "dd", gt)
        elif cfg.startswith("semantic_indexing_disabled"):
            ref = up._acc_from_direct_fl(d)
        else:
            top = RQ1 / cfg / "rq1_localization.csv"
            ref = up._acc_from_semloc_dir(d) or (up._acc_from_csv(str(top)) if top.exists() else {})
        if not ref or ref.get("acc1") is None:
            assert r["n"] == 0, cfg
            continue
        for k in ("acc1", "acc3", "acc5"):
            assert r[k] == pytest.approx(ref[k]), (cfg, k)
        assert r["n"] == ref["n"], cfg

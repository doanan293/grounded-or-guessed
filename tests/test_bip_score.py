from flx.bip_score import METHODS, artifact_rank, bug_ranks

COV = {"program": "b", "n_empty_coverage": 0, "tests": [
    {"id": "f1", "passed": False, "lines": [10, 11, 12]},
    {"id": "p1", "passed": True, "lines": [10, 13]},
]}
RES = {"line_scores": [{"line": 13, "score": 1.0}, {"line": 11, "score": 0.5}, {"line": 12, "score": 0.5}],
       "fault_line": 12, "best_rank": 3}


def test_bug_ranks_scores_true_fault_not_llm_guess():
    r = bug_ranks(RES, COV, [11], covgate={"gate": False, "lam": 0.5, "no_prior": False})
    assert set(r) == set(METHODS)
    assert r["semloc_spectrum"] == 2.5          # 11 ties with 12 behind 13 → average rank
    assert r["semloc_prior"] == 3.0             # +1.2 lifts 12 to 1.7 > 13 (1.0) > 11 (0.5)
    assert r["covgate"] == 2.5                  # + 0.5·Ochiai: 12 = 2.2, 13 = 1.0 + 0, 11 = 0.5 + 0.5 → tie
    assert r["llm_guess"] is None               # guessed 12, fault is 11
    assert r["sbfl_ochiai"] == 1.5              # 11, 12 executed only by the failing test → tie at 1–2
    assert r["sbfl_dstar"] == 1.5


def test_prior_and_guess_when_llm_is_right():
    r = bug_ranks(RES, COV, [12], covgate={"gate": False, "lam": 0.5, "no_prior": False})
    assert r["semloc_prior"] == 1.0
    assert r["llm_guess"] == 1.0
    assert r["covgate"] == 1.0


def test_error_result_misses_every_llm_method_but_not_sbfl():
    r = bug_ranks({"error": "Constraint inference failed"}, COV, [11],
                  covgate={"gate": False, "lam": 0.5, "no_prior": False})
    assert r["semloc_spectrum"] is None and r["semloc_prior"] is None and r["llm_guess"] is None
    assert r["covgate"] is None
    assert r["sbfl_ochiai"] == 1.5


def test_artifact_rank_is_rank_of_the_llm_guess():
    assert artifact_rank(RES) == 3
    assert artifact_rank({"error": "x"}) is None

from flx.pav import Check, rank, verify_candidates


def test_rank_puts_verified_first_in_llm_order():
    checks = {7: [Check(False, None)], 4: [Check(True, 2)], 9: [Check(True, 1)]}
    assert rank([7, 4, 9, 3], checks, k=3, attempts=1, order="llm") == [4, 9, 7, 3]


def test_rank_by_edit_size_breaks_ties_by_llm_order():
    checks = {7: [Check(True, 3)], 4: [Check(True, 1)], 9: [Check(True, 1)]}
    assert rank([7, 4, 9], checks, k=3, attempts=1, order="size") == [4, 9, 7]


def test_rank_respects_k_and_attempts():
    # line 9 is only verified on the 2nd attempt and line 3 lies beyond k=3
    checks = {7: [Check(False, None), Check(False, None)], 4: [Check(False, None), Check(False, None)],
              9: [Check(False, None), Check(True, 1)], 3: [Check(True, 1)]}
    assert rank([7, 4, 9, 3], checks, k=3, attempts=1, order="llm") == [7, 4, 9, 3]
    assert rank([7, 4, 9, 3], checks, k=3, attempts=2, order="llm") == [9, 7, 4, 3]


def test_rank_without_any_verified_keeps_llm_ranking():
    assert rank([5, 6], {}, k=3, attempts=2, order="llm") == [5, 6]


def test_verify_candidates_records_every_attempt():
    src = "def f(x):\n    return x + 2\n"
    proposals = {2: [{"kind": "replace", "code": "return x + 1"}, {"kind": "replace", "code": "return x * 100"}]}
    passes = {"return x + 1"}

    def propose(numbered, line, failing):
        return proposals.get(line, [])

    def runs(src_, line, kind, code):
        return code in passes

    out = verify_candidates(src, [2, 1], k=2, propose=propose, passes=runs)
    assert [(c.passed, c.size) for c in out[2]] == [(True, 1), (False, None)]
    assert out[1] == []


def test_rank_max_size_ignores_large_fixes():
    checks = {67: [Check(False, None)], 65: [Check(True, 10)], 64: [Check(True, 2)]}
    assert rank([67, 65, 64], checks, k=3, attempts=1, order="llm", max_size=2) == [64, 67, 65]
    assert rank([67, 65, 64], checks, k=3, attempts=1, order="llm") == [65, 64, 67]


def test_strict_proposer_raises_on_llm_errors(monkeypatch):
    """A failed LLM call (e.g. quota exhausted) must not look like "no passing fix" in propose-and-verify."""
    import pytest
    import flx.llm_gateway as gw
    from flx.verify_gt import llm_propose

    def boom(*a, **k):
        raise RuntimeError("429 quota")
    monkeypatch.setattr(gw, "chat", boom)
    assert llm_propose("m", attempts=1)("1: x = 1", 1, "") == []          # the label oracle keeps its old behaviour
    with pytest.raises(RuntimeError):
        llm_propose("m", attempts=1, strict=True)("1: x = 1", 1, "")

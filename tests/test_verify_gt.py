from pathlib import Path

from flx.verify_gt import candidates, try_patch, verify

FX = Path(__file__).parent / "fixtures"
ONE = (FX / "onebug/programs/add.py", FX / "onebug/testcases/test_add.py")
OMI = (FX / "omission/programs/norm.py", FX / "omission/testcases/test_norm.py")
BLANK = (FX / "blankgt/programs/mean.py", FX / "blankgt/testcases/test_mean.py")


def test_try_patch_fixes_onebug():
    src = ONE[0].read_text()
    assert try_patch(src, 3, "replace", "return a + b + c", *ONE) is True
    assert try_patch(src, 2, "replace", "c = 0", *ONE) is False


def test_candidates_stay_inside_function_and_include_blank():
    src = OMI[0].read_text()
    assert candidates(src, "norm", 3, radius=4) == [2, 3, 4]


def test_insert_after_blank_line():
    # ground truth points at the blank line 3 (omission fault); filling it is a verified fix
    propose = lambda src, line, failing: [{"kind": "replace", "code": "if t == 0: return xs"}] if line == 3 else []
    r = verify("norm", OMI[0], OMI[1], "norm", [3], propose, executable=False)
    assert r["status"] == "confirmed" and r["lines"] == [3]


def test_verify_corrects_neighbouring_line():
    propose = lambda src, line, failing: [{"kind": "replace", "code": "return a + b + c"}] if line == 3 else [{"kind": "replace", "code": "pass"}]
    r = verify("add", ONE[0], ONE[1], "add", [2], propose, executable=False)
    assert r["status"] == "corrected" and r["lines"] == [3]


def test_verify_never_trusts_llm_without_tests():
    propose = lambda src, line, failing: [{"kind": "replace", "code": "return 42"}]
    r = verify("add", ONE[0], ONE[1], "add", [3], propose, executable=True)
    assert r["status"] == "unverified"


def test_edit_size_counts_tokens():
    from flx.verify_gt import edit_size
    assert edit_size("    return a - b + c", "return a + b + c") == 1
    assert edit_size("    if not clamp:", "if clamp:") == 1
    assert edit_size("    c = 0", "c = 2 * b") == 3  # 0→2, +*, +b


def test_blank_label_prefers_fixing_a_code_line():
    # ground truth on blank line 4; filling it with "m = t / len(xs)" overrides line 3 and passes, but the fault is the
    # statement on line 3 → a fix there wins over a compensating insert on the blank line
    def propose(src, line, failing):
        return [{"kind": "replace", "code": "m = t / len(xs)"}] if line in (3, 4) else []
    r = verify("mean", BLANK[0], BLANK[1], "mean", [4], propose, executable=False)
    assert r["status"] == "corrected" and r["lines"] == [3]


def test_insert_after_a_statement_does_not_confirm_it():
    # inserting "return a + b + c" after line 2 overrides the real fault on line 3 and passes every test, but says
    # nothing about line 2: an executed label with no passing replacement stays unverified
    propose = lambda src, line, failing: [{"kind": "insert_after", "code": "return a + b + c"}]
    r = verify("add", ONE[0], ONE[1], "add", [2], propose, executable=True)
    assert r["status"] == "unverified" and r["lines"] == [2]


def test_blank_label_still_confirmed_for_an_omission():
    # no statement nearby can be fixed: the fault is a missing line, and filling the blank line confirms it
    propose = lambda src, line, failing: [{"kind": "replace", "code": "if t == 0: return xs"}] if line == 3 else []
    r = verify("norm", OMI[0], OMI[1], "norm", [3], propose, executable=False)
    assert r["status"] == "confirmed" and r["lines"] == [3]


def test_minimal_allows_an_expression_swap():
    # SemFault injects swaps such as len(tail) → window: 4 token edits on a short line
    from flx.verify_gt import is_minimal
    assert is_minimal("    avg = total / window", "avg = total / len(tail)")
    assert not is_minimal("    avg = total / window", "avg = sum(xs) / max(len(xs), 1)")


def test_rejects_compensating_rewrite():
    # line 2 "c = 2 * b" also makes every test pass (3 token edits); the real fault (3) wins on the smaller edit
    def propose(src, line, failing):
        return {2: [{"kind": "replace", "code": "c = 2 * b"}], 3: [{"kind": "replace", "code": "return a + b + c"}]}.get(line, [])
    r = verify("add", ONE[0], ONE[1], "add", [1], propose, executable=False)
    assert r["status"] == "corrected" and r["lines"] == [3] and r["edit_size"] == 1

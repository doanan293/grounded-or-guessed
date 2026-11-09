import importlib.util
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("blind_review", ROOT / "scripts" / "blind_review.py")
br = importlib.util.module_from_spec(spec)
spec.loader.exec_module(br)

SRC = ["def f(x):", '    """doc"""', "", "    y = x + 1", "    if y > 3:", "        y = 3", "", "    z = y * 2",
       "    _log.debug('z')", "    return z"]


def test_candidates_include_every_relevant_line_and_pad_with_code_lines():
    c = br.candidates(SRC, {5, 6}, minimum=4)
    assert {5, 6} <= set(c) and len(c) >= 4
    assert all(SRC[ln - 1].strip() for ln in c if ln not in {5, 6})   # padding never uses blank lines
    assert 3 not in c and 7 not in c


def test_candidates_keep_a_blank_relevant_line():
    assert 3 in br.candidates(SRC, {3}, minimum=3)                     # an original label on a blank line stays visible


def test_assignment_two_distinct_eligible_reviewers_and_balanced():
    members = ["a", "b", "c", "d", "e", "f"]
    cases = [{"program": f"p{i}", "seen_by": members[i % 6] if i < 30 else None} for i in range(60)]
    out = br.assign(cases, members, per_case=2, rng=random.Random(1))
    load = Counter(m for ms in out.values() for m in ms)
    assert set(load.values()) == {20}
    for c in cases:
        ms = out[c["program"]]
        assert len(set(ms)) == 2 and c["seen_by"] not in ms


def test_answer_lines_letters_and_numbers():
    letters = {"A": 5, "B": 6, "C": 8}
    assert br.answer_lines("B", letters) == {6}
    assert br.answer_lines("a + c", letters) == {5, 8}
    assert br.answer_lines("12", letters) == {12}
    assert br.answer_lines("?", letters) is None

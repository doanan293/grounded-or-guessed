import math

from flx.ranking import metrics, rank_of


def test_rank_average_ties():
    s = {10: 0.5, 11: 0.5, 12: 0.1}
    assert rank_of(s, [11], "first") == 2
    assert rank_of(s, [11], "average") == 1.5
    assert rank_of(s, [11], "worst") == 2
    assert rank_of(s, [10], "worst") == 2 and rank_of(s, [10], "first") == 1


def test_best_of_several_faulty_lines():
    assert rank_of({1: 0.9, 2: 0.5, 3: 0.1}, [3, 2], "average") == 2


def test_unranked_fault_is_none():
    assert rank_of({1: 0.9}, [7], "average") is None
    assert rank_of({}, [7], "average") is None


def test_missing_program_counts_as_miss():
    m = metrics({"a": 1.0}, ["a", "b"])
    assert m["n"] == 2 and m["acc1"] == 0.5 and m["acc5"] == 0.5


def test_average_rank_counts_against_k():
    m = metrics({"a": 1.5, "b": 3.0, "c": None}, ["a", "b", "c"])
    assert m["acc1"] == 0.0 and math.isclose(m["acc3"], 2 / 3)
    assert m["median_rank"] == 3.0

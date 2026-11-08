from flx.covgate import covgate_explain, covgate_scores

COV = {"program": "p", "tests": [
    {"id": "f1", "passed": False, "lines": [3, 4, 5]},
    {"id": "p1", "passed": True, "lines": [3, 4, 6]}]}
SEM = {"line_scores": {"3": 0.5, "5": 0.5, "6": 0.9, "8": 1.2}, "fault_line_pred": 8, "constraint_scores": {}}


def test_gate_drops_lines_not_hit_by_failing():
    s = covgate_scores(SEM, COV, gate=True, lam=0.0, no_prior=False)
    assert set(s) == {3, 5}


def test_gate_drops_unexecuted_fault_is_reported():
    e = covgate_explain(SEM, COV, faulty=[6], gate=True, lam=0.0, no_prior=False)
    assert e["rank"] is None and e["fault_gated"] is True
    e2 = covgate_explain(SEM, COV, faulty=[5], gate=True, lam=0.0, no_prior=False)
    assert e2["fault_gated"] is False and e2["rank"] is not None


def test_no_prior_subtracts_bonus():
    s = covgate_scores(SEM, COV, gate=False, lam=0.0, no_prior=True)
    assert 8 not in s  # 1.2 was only the prior → removed
    sem = {**SEM, "line_scores": {**SEM["line_scores"], "8": 2.0}}
    assert abs(covgate_scores(sem, COV, gate=False, lam=0.0, no_prior=True)[8] - 0.8) < 1e-9


def test_lambda_breaks_ties_only_small():
    # lines 3 and 5 tie at 0.5; ochiai(5) = 1/sqrt(1*1)=1 > ochiai(3) = 1/sqrt(1*2)
    s = covgate_scores(SEM, COV, gate=True, lam=0.01, no_prior=False)
    assert s[5] > s[3] and s[5] - s[3] < 0.01


def test_cf_rerank_puts_primary_lines_first():
    sem = {"line_scores": {"3": 0.9, "5": 0.4}, "fault_line_pred": None,
           "constraint_scores": {"C1": {"ochiai": 0.9}, "C2": {"ochiai": 0.4}}}
    cf = [{"cid": "C1", "status": "OverApproximate", "pruned": False},
          {"cid": "C2", "status": "Primary", "pruned": False}]
    attribute = lambda scores: {5: scores["C2"]["ochiai"]} if "C2" in scores else {}
    s = covgate_scores(sem, COV, gate=False, lam=0.0, no_prior=False, cf=cf, attribute=attribute)
    assert max(s, key=s.get) == 5


def test_semloc_attribute_reproduces_published_line_scores():
    import json
    from flx._semloc import SEMLOC_ROOT
    from flx.covgate import PRIOR, semloc_attribute
    R = SEMLOC_ROOT / "results/RQ1/semloc_claude_T0.8"
    for prog in ("ad_mix", "adjust_queue", "batchnorm_running_mean"):
        sem = json.loads((R / "scores" / f"{prog}.json").read_text())
        attr = semloc_attribute(R / "constraints" / f"{prog}.json", SEMLOC_ROOT / "benchmark/programs" / f"{prog}.py")
        got = attr(sem["constraint_scores"])
        want = {int(k): v for k, v in sem["line_scores"].items()}
        fp = sem.get("fault_line_pred")
        if isinstance(fp, int) and fp in want:
            want[fp] -= PRIOR
            if want[fp] <= 1e-12:
                del want[fp]
        assert set(got) == set(want), prog
        assert all(abs(got[k] - want[k]) < 1e-9 for k in want), prog

"""RQ3a scoring on BugsInPy: rank the developer-fixed lines (not the LLM's own guess) under each method.

The SemLoc artifact's BugsInPy runner reports `best_rank` = rank of the LLM's own `fault_line` in its
line scores (artifact_rank), which measures self-consistency, not localization. We score the true
faulty lines (developer diff, buggy side, inside the target function) with fair average-rank ties:
  semloc_spectrum  the runner's line scores as produced (it applies no fault-line prior)
  semloc_prior     + SemLoc's +1.2 fault-line prior, as its SemFault pipeline applies
  llm_guess        the LLM's fault_line alone (rank 1 or miss)
  covgate          semloc_prior scores with CovGate (parameters chosen on SemFault dev)
  sbfl_ochiai / sbfl_dstar  from the per-test coverage matrix
A runner error is a miss for every LLM method.
"""
from typing import Optional

from flx.covgate import PRIOR, covgate_scores
from flx.ranking import rank_of
from flx.sbfl import sbfl_scores

METHODS = ("semloc_spectrum", "semloc_prior", "llm_guess", "covgate", "sbfl_ochiai", "sbfl_dstar")


def _semloc(result: dict) -> tuple[dict[int, float], Optional[int]]:
    scores = {int(e["line"]): float(e["score"]) for e in result.get("line_scores", [])}
    fl = result.get("fault_line")
    return scores, (int(fl) if isinstance(fl, (int, float)) else None)


def bug_ranks(result: dict, cov: dict, faulty: list[int], covgate: dict) -> dict[str, Optional[float]]:
    out = {"sbfl_ochiai": rank_of(sbfl_scores(cov, "ochiai"), faulty),
           "sbfl_dstar": rank_of(sbfl_scores(cov, "dstar"), faulty)}
    if "error" in result:
        return {**{m: None for m in METHODS}, **out}
    spec, fl = _semloc(result)
    prior = dict(spec)
    if fl is not None:
        prior[fl] = prior.get(fl, 0.0) + PRIOR
    out["semloc_spectrum"] = rank_of(spec, faulty)
    out["semloc_prior"] = rank_of(prior, faulty)
    out["llm_guess"] = rank_of({fl: 1.0}, faulty) if fl is not None else None
    out["covgate"] = rank_of(covgate_scores({"line_scores": prior, "fault_line_pred": fl}, cov, **covgate), faulty)
    return {m: out[m] for m in METHODS}


def artifact_rank(result: dict) -> Optional[int]:
    """The artifact's own metric: rank of the LLM's guess in its line scores."""
    return None if "error" in result else result.get("best_rank")

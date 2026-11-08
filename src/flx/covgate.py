"""CovGate: SemLoc's semantic line scores, gated and tie-broken by coverage, optionally re-ranked by CF.

Inputs are SemLoc's own artifacts (scores/<p>.json, refined_base_cf/<p>.json) and a CoverageMatrix.
- no_prior: remove the +1.2 SemLoc adds to the LLM's own fault_line guess (apply_fault_line_prior).
- cf:       re-score with only CF-kept constraints (Primary/Secondary, not pruned) and put those lines
            first — the step the SemLoc artifact computes but never uses for ranking.
- gate:     drop lines that no failing test executes.
- lam:      add lam × Ochiai(line) (small lam = tie-break only).
- grounded_prior: keep the +1.2 on the LLM's guess only if a failing test executes that line AND a
            constraint violated in failing tests (ef > 0) is attributed to it; otherwise drop it.
"""
from typing import Callable, Optional

from flx.ranking import rank_of
from flx.sbfl import sbfl_scores

PRIOR = 1.2  # spectrum.apply_fault_line_prior default prior_weight
CF_KEEP = ("Primary", "Secondary")
CF_OFFSET = 1000.0


def covgate_scores(semloc: dict, cov: dict, *, gate: bool, lam: float, no_prior: bool,
                   cf: Optional[list] = None, attribute: Optional[Callable[[dict], dict]] = None,
                   grounded_prior: bool = False) -> dict[int, float]:
    scores = {int(k): float(v) for k, v in semloc.get("line_scores", {}).items()}
    fp = semloc.get("fault_line_pred")
    if grounded_prior and not no_prior and isinstance(fp, int):
        no_prior = not _guess_is_grounded(semloc, cov, fp, attribute)
    if no_prior and isinstance(fp, int) and fp in scores:
        scores[fp] -= PRIOR
        if scores[fp] <= 1e-12:
            del scores[fp]
    if cf and attribute is not None:
        kept = {r["cid"] for r in cf if r.get("status") in CF_KEEP and not r.get("pruned")}
        if kept:
            cs = semloc.get("constraint_scores", {})
            for ln, v in attribute({c: cs[c] for c in kept if c in cs}).items():
                scores[ln] = scores.get(ln, 0.0) + CF_OFFSET + v
    if gate:
        failing = set().union(*(set(t["lines"]) for t in cov["tests"] if not t["passed"]))
        scores = {ln: v for ln, v in scores.items() if ln in failing}
    if lam:
        och = sbfl_scores(cov, "ochiai")
        scores = {ln: v + lam * och.get(ln, 0.0) for ln, v in scores.items()}
    return scores


def _guess_is_grounded(semloc: dict, cov: dict, line: int, attribute: Optional[Callable[[dict], dict]]) -> bool:
    run_by_failing = any(line in t["lines"] for t in cov["tests"] if not t["passed"])
    if not run_by_failing or attribute is None:
        return False
    violated = {c: s for c, s in semloc.get("constraint_scores", {}).items() if s.get("ef", 0) > 0}
    return line in attribute(violated) if violated else False


def covgate_explain(semloc: dict, cov: dict, faulty: list[int], ties: str = "average", **opts) -> dict:
    gated = covgate_scores(semloc, cov, **opts)
    ungated = covgate_scores(semloc, cov, **{**opts, "gate": False}) if opts.get("gate") else gated
    fault_gated = any(ln in ungated and ln not in gated for ln in faulty) or (
        opts.get("gate") and not any(ln in gated for ln in faulty) and any(ln in ungated for ln in faulty))
    return {"rank": rank_of(gated, faulty, ties), "fault_gated": bool(fault_gated)}


def semloc_attribute(constraints_path, src_path) -> Callable[[dict], dict]:
    """SemLoc's own constraint → line attribution for one program (spectrum.attribute_to_statements)."""
    from pathlib import Path

    from flx._semloc import ensure_on_path
    ensure_on_path()
    from instrumentation import parse_constraints
    from spectrum import attribute_to_statements
    _, constraints = parse_constraints(Path(constraints_path).read_text())
    src = Path(src_path).read_text()
    return lambda scores: attribute_to_statements(scores, constraints, src)

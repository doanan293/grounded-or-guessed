"""Display names of the compared methods (same in Vietnamese and English); ids in data/ stay unchanged."""
OURS = "llm_tests"
NAMES = {
    "llm_tests": "FailLoc",            # one LLM call with the program and the failing tests (the group's method)
    "llm_direct": "LLM-Direct",        # SemLoc's own direct-prediction mode: program only
    "llm_coverage": "FailLoc+Cov",     # FailLoc prompt + per-line coverage
    "semloc": "SemLoc",
    "semloc_no_prior": "SemLoc−Bonus",  # SemLoc without the +1.2 bonus on the LLM-guessed line
    "sbfl_ochiai": "SBFL (Ochiai)",
    "sbfl_dstar": "SBFL (DStar)",
    "covgate": "CovGate",
    "covgate_cf": "CovGate+CF",
    "cf_rerank": "SemLoc+CF",
    "gate_only": "SemLoc+Gate",
    "lam_only": "SemLoc+λOchiai",
    "grounded_prior_only": "SemLoc+GroundedBonus",
    "llm_guess": "LLM-Guess",
    "pav": "FailLoc+Verify",
    "vote": "FailLoc+Vote",
}


def name(method_id: str) -> str:
    return NAMES[method_id]

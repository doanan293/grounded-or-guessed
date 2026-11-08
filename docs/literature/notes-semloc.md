# SemLoc — Structured Grounding of Free-Form LLM Reasoning for Fault Localization

Yang, Zhu, Zhang, Gupta, Kundu (UC Riverside, Cisco Research). arXiv:2603.29109, 2026.
Artifact: https://github.com/jerry729/SemLoc (Apache-2.0), vendored at `third_party/semloc` @ c1db564.

## Problem
Spectrum-based fault localization (SBFL) ranks statements by how often failing vs passing tests
execute them. For *semantic* faults, failing and passing tests run the same statements, so the
spectra collapse. Free-form LLM localization reasons about intent but is stochastic, unverifiable,
and cannot separate root causes from downstream symptoms.

## Method (4 stages)
1. **Structural anchors:** parse the program (tree-sitter, SSA view) to find typed locations where a
   property can be checked: entries, def-use sites, loop boundaries, returns (8 region types).
2. **Structured semantic grounding:** zero-shot LLM call returns constraints in a closed IR
   (`cbfl-ir`): ⟨id, category κ (9 categories), region ρ, anchor α, predicate φ, intent ι⟩, validated
   against a schema; ungroundable constraints are dropped.
3. **Semantic spectrum:** instrument the program with `__cbfl.check(cid, lambda: φ)`, run pytest,
   build the constraint × test violation matrix, score each constraint with Ochiai, and propagate the
   score to the statement that establishes the property (max over constraints).
4. **Counterfactual verification:** constraints violated on any passing test are dropped as
   over-approximate; for each remaining constraint an LLM writes a one-line patch at the attributed
   line (T = 0), tests are re-run, and the outcome marks the constraint primary / secondary / etc.

## Evaluation
- **SemFault-250:** 250 single-function, single-fault Python programs "extracted from real-world
  repositories and prior benchmarks" (Deep Stability, Apache Fineract, Bedework, Redis), filtered for
  semantic errors; 8–12 tests each (mean 10.0, mean 3.5 failing).
- **Baselines:** SBFL Ochiai/Tarantula, delta debugging (DD), LLM direct prediction (SemLoc†),
  SemLoc without counterfactuals (SemLoc+), AutoFL (function level, not comparable).
- **Models:** Claude Sonnet 4.6 and Gemini 2.5 Pro at T = 0 / 0.3 / 0.8.
- **Results (Table 3):** SemLoc Claude T = 0.8: Acc@1 42.8%, Acc@3 68.0%, Acc@5 76.8%, %Susp 7.6%;
  SBFL Ochiai 6.4 / 13.2 / 30.4 (%Susp 43.6); DD reported as 0.0 / 0.0 / 0.0.
  Counterfactual verification adds ~12 pp Acc@1. Direct LLM (SemLoc†) plateaus at ~44% Acc@3.
- **Real bugs (RQ3):** BugsInPy, AutoFL picks the function, SemLoc ranks lines inside it, Claude
  Sonnet 4.6 T = 0.8. Runs end to end on only 68 of 463 bugs; line-level table reported for **7
  youtube-dl bugs** (57.1 / 85.7 / 100). Authors call it a *feasibility* result.

## Limitations we found (inputs for our RQs)
- Real-bug evidence is n = 7; failures are blamed on execution infrastructure (installs with
  `--no-deps` into one interpreter) → our RQ3(a) rebuilds per-project environments.
- SemFault-250 programs read like LLM-written code (uniform docstrings, `_EPSILON`-style constants),
  so memorization/contamination is untested → our RQ3(b) renamed variants.
- Discards coverage entirely → our CovGate (RQ2).
- Evaluation code (`print_results.py`) is optimistic: SBFL ties broken by line order; DD counts any hit
  as rank 1 (published logs give DD Acc@1 = 38.0%, paper Table 3 says 0.0%); programs that fail to
  run are dropped from the denominator (Gemini T = 0.8 n = 249; CF-disabled Gemini n = 214).
  No published results for Claude T = 0.0. `semloc report --rq1` prints nothing (flag bug).
- Single run per configuration; no significance tests.

## Relevance
Base method for the whole study: RQ1 (reproduction), RQ2 (CovGate on top of its spectrum),
RQ3 (robustness on real bugs, renamed code, other model families).

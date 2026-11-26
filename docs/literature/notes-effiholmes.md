# EffiHolmes — Differential Profiling-Guided Repository Level Time Inefficiency Fix Localization

Yang, Peng, Ding (HKUST-GZ, CUHK). arXiv:2608.03558, 2026.

## Problem
Time-inefficiency issues make code slow without failing tests or crashing, so there is no binary
oracle and no stack trace: classic fault localization and LLM-based localization do not apply.
Single-run profiling cannot separate real hotspots from noise, and profilers drown the relevant
execution path in background execution.

## Method
1. **Differential profiling:** profile under a default and a scaled workload; functions whose cost
   grows with scale are inefficiency hotspots.
2. **Execution path extraction:** build compact call paths from the entry point to the hotspot and
   to the function named in the issue.
3. **Guided LLM reasoning** with domain heuristics to move from hotspot to the code that must change.

## Evaluation
- **RepoEffi-Bench:** 140 time-inefficiency issues from 5 data-science repositories in SWE-bench's
  set (1,594 issue–PR pairs → 692 LLM-flagged → 444 manually confirmed → 140 reproducible slowdowns
  with verified speedup). Issue texts sanitized to remove fix-location hints.
- **Metrics:** file- and function-level Acc@1/3/5.
- **Results:** beats retrieval-, agent-, procedure- and profiling-based baselines, e.g. +4.29 pp
  file-level Acc@3 with GPT-5.1 and +15.00 pp function-level Acc@5 with qwen3-4b; robust across model
  sizes. RQs: effectiveness, ablation, robustness to smaller models, failure analysis.

## Relevance to our study
- Same core idea as SemLoc and our CovGate: **contrast two executions** (default vs scaled workload;
  passing vs failing tests) to filter noise before asking the LLM.
- Its RQ structure (effectiveness / ablation / robustness across model scale / failure analysis) is a
  template for ours.
- Not used experimentally: performance faults are out of scope (spec §9). Cited as future work.

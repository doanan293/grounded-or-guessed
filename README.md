# Grounded or Guessed

**Replication package for _"Grounded or Guessed: An Execution-Verified Reproducibility Study of LLM-Based Semantic Fault Localization"_** (work in progress, Hanoi University of Science and Technology, course IT5440, 2026).

LLM-based fault localization tools claim that grounding LLM reasoning in execution evidence is what makes them accurate. We re-examine that claim on the most recent such tool, SemLoc (Yang et al., arXiv:2603.29109), using only execution evidence as the arbiter:

- **Reproduction and evaluation audit (RQ1).** We recompute every published configuration from the authors' own logs, score it both the authors' way and a fair way (average-rank ties, fixed denominators), and ablate implementation details that the paper does not describe.
- **CovGate (RQ2).** We gate and tie-break semantic scores with per-test coverage, let counterfactual verification actually re-rank, and only credit the LLM's own guess when execution evidence supports it.
- **Robustness (RQ3).** We test on real bugs (BugsInPy), on identifier-renamed programs (memorization check), and across model families (Gemini, Claude, GPT, an open-weight model) at each provider's default reasoning level.
- **SemFault-250-verified.** We re-derive the benchmark's ground truth by execution: a line is faulty only if a one-line patch there makes every test pass.

## Findings so far (2026-11-08, milestone 2)

Numbers are Acc@k (%) on SemFault-250's 200-program test split, 3 repeats, Gemini 3.8 Flash at provider-default reasoning, scored with average-rank ties and a fixed denominator, on the execution-repaired ground truth unless noted.

| Finding | Evidence (in this repo) |
|---|---|
| All 13 published configurations reproduce exactly from the released logs; the released counterfactual step never changes a ranking (0/250 programs, 5 configurations) | `data/rq1a_table.csv`, `data/rq1_cf_identity.json` |
| An undocumented +1.2 bonus on the LLM's own fault-line guess carries most of the top-1 accuracy: Shapley split of SemLoc's Acc@1 49.3 = guess 28.9 + semantic spectrum 20.3; Acc@3 71.2 = guess 26.8 + spectrum 44.4 | `data/rq_decomposition.csv` |
| 56/250 ground-truth lines are blank and 65/250 are executed by no failing test; re-deriving the ground truth by execution (82 confirmed, 46 corrected) raises every LLM method by 11–19 pp | `data/semfault_verified_gt.json`, `data/rq_gt_sensitivity.csv` |
| One prompt with per-line coverage counts beats the whole pipeline: Acc@3 86.7 vs 71.2 (p < .001), at about a fifth of the tokens | `data/rq2_ours.csv`, `data/llm_cost.csv`, `docs/report/generated/pareto.pdf` |
| CovGate (dev-tuned λ·Ochiai tie-break) adds 3.5 pp Acc@3 (McNemar p = .039); counterfactual re-ranking does not help, yet costs 42 % of SemLoc's LLM calls | `data/rq2_ours.csv`, `data/llm_cost.csv` |
| On 31 real youtube-dl bugs (BugsInPy), every SemLoc top-1 hit is the LLM's own guess (46.2 = 46.2); the semantic spectrum alone reaches 7.5. The artifact's BugsInPy metric ranks the LLM's guess, not the fixed lines | `data/rq3_bugsinpy.csv` |
| Renaming identifiers (behaviour-preserving) leaves the guess intact but cuts the constraint-based ranking: spectrum-only Acc@3 66.7 → 51.9 (p < .001) | `data/rq3_renamed.csv` |
| Across five model families the weaker the model, the more it leans on the guess bonus (Flash-Lite −20 pp Acc@1 without it, Gemini 3.8 ±1) | `data/rq3_families.csv` |
| The released BugsInPy runner leaves stale bytecode after its counterfactual patch (same size, same second), which can hide the bug in the next run; fixed in our driver | `src/flx/bip_run.py` |

`scripts/regenerate_all.sh` rebuilds every table and figure from the runs; `data/runs.csv` lists every run and its health.

## Layout

```
src/flx/            our code: LLM gateway, coverage matrices, SBFL, CovGate, ranking, statistics, BugsInPy probe
scripts/            experiment drivers (run_semloc.sh, run_matrix.sh, rq1_audit.py, covgate_eval.py, …)
tests/              pytest suite (TDD; run with .venv/bin/pytest)
data/               derived data: labels, dev/test split, coverage matrices, result tables
third_party/semloc/ SemLoc artifact @ c1db564 (Apache-2.0), with one patch routing LLM calls through our gateway
infra/proxy/        Docker compose for the OpenAI-compatible LLM proxy; MODELS.md documents models and reasoning levels
docs/               spec and plans (docs/superpowers), literature notes, LaTeX report and paper, slides
.agents/, .claude/  agent skills used by the authors (third-party; see their own licences)
```

## Reproducing

Requirements: Linux, Python ≥ 3.10, [uv](https://github.com/astral-sh/uv), Docker (for the LLM proxy), TeX Live (report/paper).

```bash
uv venv && uv pip install -e ".[dev]" -e third_party/semloc
.venv/bin/pytest -q                                   # unit tests

# Offline (no LLM): RQ1 audit and CovGate on the published SemLoc logs
.venv/bin/python scripts/rq1_audit.py
.venv/bin/python scripts/covgate_eval.py

# LLM runs: configure .env from .env.example, start the proxy, then e.g.
docker compose -f infra/proxy/compose.yaml up -d
scripts/run_matrix.sh semloc_test_gemini gemini-3.8-flash-high test 3
```

Each repeat is one run id and one working directory; `python -m flx.run_health` must report a healthy run before its numbers are used. LLM calls are cached and logged per run id.

## Credits and licences

- Project code (`src/`, `scripts/`, `tests/`, `infra/`, `docs/`): MIT, see `LICENSE`.
- `third_party/semloc/`: SemLoc by Zhaorui Yang, Haichao Zhu, Qian Zhang, Rajiv Gupta, Ashish Kundu — Apache-2.0 (`third_party/semloc/LICENSE.txt`), including the SemFault-250 benchmark and published results. We thank the authors for releasing their complete artifact; this study would not be possible otherwise.
- `.agents/skills/`: third-party agent skills (humanizer, ppt-master, research-paper-writing, latex-document-skill) under their own licences.
- Slides use a Slidesgo template (credits slide kept).

# Grounded or Guessed

**Replication package for _"Grounded or Guessed: An Execution-Verified Reproducibility Study of LLM-Based Semantic Fault Localization"_** (work in progress, Hanoi University of Science and Technology, course IT5440, 2026).

LLM-based fault localization tools claim that grounding LLM reasoning in execution evidence is what makes them accurate. We re-examine that claim on the most recent such tool, SemLoc (Yang et al., arXiv:2603.29109), using only execution evidence as the arbiter:

- **Reproduction and evaluation audit (RQ1).** We recompute every published configuration from the authors' own logs, score it both the authors' way and a fair way (average-rank ties, fixed denominators), and ablate implementation details that the paper does not describe.
- **CovGate (RQ2).** We gate and tie-break semantic scores with per-test coverage, let counterfactual verification actually re-rank, and only credit the LLM's own guess when execution evidence supports it.
- **Robustness (RQ3).** We test on real bugs (BugsInPy), on identifier-renamed programs (memorization check), and across model families (Gemini, Claude, GPT, an open-weight model) at each provider's default reasoning level.
- **SemFault-250-verified.** We re-derive the benchmark's ground truth by execution: a line is faulty only if a one-line patch there makes every test pass.

## Findings (2026-11-09, after Phase 3)

Acc@k (%) on SemFault-250's test split, 3 repeats, Gemini 3.8 Flash at provider-default reasoning, average-rank ties and a fixed denominator, on the execution-repaired ground truth (179 test programs) unless noted. Δ are percentage points with 95% template-cluster bootstrap CIs. Every number here is a macro in `docs/report/generated/numbers.tex`.

| Finding | Evidence |
|---|---|
| All 13 published configurations reproduce exactly from the released logs; the released counterfactual step never changes a ranking (0/250 programs, 5 configurations) | `data/rq1a_table.csv`, `data/rq1_cf_identity.json` |
| Top-1 is mostly *guessed*: Shapley split of SemLoc's Acc@1 52.3 = LLM's own fault-line guess (an undocumented +1.2 bonus) 30.7 + semantic spectrum 21.6; top-3 is mostly *grounded*: Acc@3 75.4 = 28.5 + 46.9 | `data/rq_decomposition.csv` |
| One prompt with per-line coverage counts beats the whole pipeline: Acc@3 92.0 vs 75.4 (Δ +16.6 [+10.5, +22.8]), Acc@1 Δ +4.8 [+1.5, +8.7], at about a fifth of the tokens; it is also rename-robust (Acc@3 Δ −0.9 [−3.5, +1.3]) | `data/rq2_ours.csv`, `data/rq3_renamed.csv`, `data/llm_cost.csv` |
| On 31 real youtube-dl bugs (BugsInPy) every SemLoc top-1 hit is the LLM's own guess (46.2 = 46.2); the semantic spectrum alone reaches 7.5. LLM + coverage points the same way (Acc@3 69.9 vs 53.8) but n = 31 leaves the CI across 0 | `data/rq3_bugsinpy.csv` |
| Renaming identifiers cuts the constraint-based ranking (spectrum-only Acc@3 70.6 → 55.1) but not the guess | `data/rq3_renamed.csv` |
| 56/250 ground-truth lines are blank and 65/250 are executed by no failing test; SemFault-250-verified re-derives them by execution (226 programs kept). Our minimal-fix oracle can still accept compensating fixes — see the failure analysis | `data/semfault_verified_gt.json`, `docs/analysis/failure-analysis.md` |
| Line-level Acc@1 is ambiguous for faults spanning a guard and the statement it guards: accepting either raises SemLoc's Acc@1 from 52.3 to 73.9–76.2; method ordering is unchanged | `data/failure_tolerance.csv` |
| CovGate (dev-tuned) adds +3.9 pp Acc@3; counterfactual re-ranking does not help yet costs 42% of SemLoc's LLM calls | `data/rq2_ours.csv`, `data/llm_cost.csv` |
| The released BugsInPy runner ranks the LLM's guess instead of the fixed lines, and leaves stale bytecode after its counterfactual patch | `src/flx/bip_score.py`, `src/flx/bip_run.py` |

Contributions, scientific stance and threats to validity: `docs/analysis/contributions.md`.

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

Full instructions, four reproduction levels and a result-to-script map: **[REPRODUCE.md](REPRODUCE.md)**. Run outputs, the LLM call log and the replayable LLM response cache are released as an archive (`scripts/export_artifact.py`); `docker build -t grounded-or-guessed .` gives an offline environment in which `scripts/regenerate_all.sh` rebuilds every CSV and table byte-identically.

### Quick start

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

## Citing

See `CITATION.cff`.

## Credits and licences

- Project code (`src/`, `scripts/`, `tests/`, `infra/`, `docs/`): MIT, see `LICENSE`.
- `third_party/semloc/`: SemLoc by Zhaorui Yang, Haichao Zhu, Qian Zhang, Rajiv Gupta, Ashish Kundu — Apache-2.0 (`third_party/semloc/LICENSE.txt`), including the SemFault-250 benchmark and published results. We thank the authors for releasing their complete artifact; this study would not be possible otherwise.
- `.agents/skills/`: third-party agent skills (humanizer, ppt-master, research-paper-writing, latex-document-skill) under their own licences.
- Slides use a Slidesgo template (credits slide kept).

# Grounded or Guessed

**Replication package for _"Grounded or Guessed: A Reproducibility Study of LLM-Based Semantic Fault Localization"_** (work in progress, Hanoi University of Science and Technology, course IT5440, 2026).

When tests fail, developers increasingly hand the failure to an LLM and ask where the bug is. Research tools propose far more elaborate pipelines that claim to ground the model's reasoning in execution. We test that claim on SemLoc (Yang et al., arXiv:2603.29109) and compare it with the everyday practice:

- **Reproduction and evaluation audit (RQ1).** We recompute every published configuration from the authors' logs, score it the authors' way and a fair way, ablate undocumented details, and check the benchmark's labels (by execution, then by an LLM pre-review and a team review).
- **What does the LLM need? (RQ2).** One prompt with the failing tests vs. the pipeline; an ablation separating failing tests from per-line coverage; more elaborate additions (CovGate on SemLoc, propose-and-verify with test-passing patches, voting); static analysis (ruff, pyrefly).
- **Robustness (RQ3).** Real bugs (BugsInPy), identifier-renamed programs, five model families, and three label sets (original, execution-repaired, reviewed).

## Findings (2026-11-09, Phase 5)

Acc@k (%) on SemFault-250's test split, 3 repeats, Gemini 3.8 Flash at provider-default reasoning, average-rank ties and a fixed denominator, on the execution-repaired labels (179 test programs) unless noted. Δ are percentage points with 95% template-cluster bootstrap CIs. Every number is a macro in `docs/report/generated/numbers.tex`.

| Finding | Evidence |
|---|---|
| All 13 published configurations reproduce exactly from the released logs. SemLoc's top-1 is *guessed* by construction: an undocumented +1.2 bonus always ranks the LLM's own guess first (SemLoc Acc@1 52.3 = the guess's; spectrum alone 43.2), and the counterfactual step never changes a ranking yet costs 42% of the LLM calls | `data/rq1_audit.csv`, `data/rq1_cf_identity.json`, `data/rq_decomposition.csv` |
| 112 of 250 original labels move under review (56 on blank lines, 32 one line off); the mislabels favor SemLoc: its Acc@3 lead over LLM direct (60.3 vs 43.0 on original labels) disappears on reviewed labels (90.0 vs 90.8) | `data/label_audit.csv`, `data/semfault_reviewed_gt.json` |
| One prompt with the failing tests beats SemLoc at Acc@1 on all three label sets: +7.7 (original), +10.2 [+5.3, +16.0] (repaired), +12.5 (reviewed); Acc@3 +14.5 [+8.5, +20.8] (repaired); 2.0k vs 14.0k tokens per program | `data/rq2_ours.csv`, `data/llm_cost.csv` |
| Failing tests carry the signal (Acc@3 +27.2 over LLM direct); per-line coverage does not (Acc@3 +2.1 [−0.2, +4.9], Acc@1 −5.4 [−9.4, −2.1]) | `data/ablation_coverage.csv` |
| Nothing more elaborate helps: CovGate (an Ochiai tie-breaker) +3.9 Acc@3 on SemLoc; propose-and-verify and voting do not improve the simple prompt (dev); ruff and pyrefly flag a faulty line in 1 and 0 of 250 programs. Mechanism: a small patch passes every test at 23.3% of non-faulty lines vs 42.5% of faulty ones | `data/pav_dev_grid.csv`, `data/pav_mechanism.csv`, `data/vote_dev.csv`, `data/static_tools.csv` |
| On 31 real youtube-dl bugs SemLoc's top-1 is the guess (46.2 = 46.2); the simple prompt points the same way (Acc@3 71.0 vs 53.8) but n = 31 leaves the CI across 0 | `data/rq3_bugsinpy.csv` |
| Renaming identifiers cuts the constraint-based ranking (spectrum-only Acc@3 70.6 → 55.1) but not the guess | `data/rq3_renamed.csv` |
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

Full instructions, four reproduction levels and a result-to-script map: **[REPRODUCE.md](REPRODUCE.md)**. Run outputs, the LLM call log and the replayable LLM response cache are released as an archive attached to the GitHub release (`scripts/export_artifact.py`); `docker build -t grounded-or-guessed .` gives an offline environment in which `scripts/regenerate_all.sh` rebuilds every CSV and table byte-identically.

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

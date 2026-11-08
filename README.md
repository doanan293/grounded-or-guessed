# Grounded or Guessed

**Replication package for _"Grounded or Guessed: An Execution-Verified Reproducibility Study of LLM-Based Semantic Fault Localization"_** (work in progress, Hanoi University of Science and Technology, course IT5440, 2026).

LLM-based fault localization tools claim that grounding LLM reasoning in execution evidence is what makes them accurate. We re-examine that claim on the most recent such tool, SemLoc (Yang et al., arXiv:2603.29109), using only execution evidence as the arbiter:

- **Reproduction and evaluation audit (RQ1).** We recompute every published configuration from the authors' own logs, score it both the authors' way and a fair way (average-rank ties, fixed denominators), and ablate implementation details that the paper does not describe.
- **CovGate (RQ2).** We gate and tie-break semantic scores with per-test coverage, let counterfactual verification actually re-rank, and only credit the LLM's own guess when execution evidence supports it.
- **Robustness (RQ3).** We test on real bugs (BugsInPy), on identifier-renamed programs (memorization check), and across model families (Gemini, Claude, GPT, an open-weight model) at each provider's default reasoning level.
- **SemFault-250-verified.** We re-derive the benchmark's ground truth by execution: a line is faulty only if a one-line patch there makes every test pass.

## Findings so far (2026-11-08)

| Finding | Evidence (in this repo) |
|---|---|
| All 13 published configurations reproduce exactly from the released logs | `data/rq1a_table.csv` |
| In the released code, counterfactual verification never changes the reported ranking (0 / 250 programs, 5 configurations) | `data/rq1_cf_identity.json` |
| An undocumented +1.2 bonus for the LLM's own fault-line guess accounts for ~13 pp Acc@1 (42.8 % → 30.0 %, Claude T=0.8) | `data/rq1_audit.csv` |
| 56 / 250 ground-truth lines are blank lines; 65 / 250 are not executed by any failing test | `data/semfault_labels.csv`, `docs/literature/benchmark-notes.md` |
| Coverage gating raises Acc@3 by 3–7 pp on programs whose ground truth is executable | `data/rq2_published.csv` |

Everything above is preliminary and will change as the remaining experiments finish.

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

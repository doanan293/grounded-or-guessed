# BugsInPy for RQ3(a) — setup notes

## How SemLoc ran BugsInPy (upstream `src/bip_runner.py`, `scripts/reproduce_rq3.sh`)

- Bug metadata (`python_version`, buggy/fixed commit, test file) is downloaded from
  `https://raw.githubusercontent.com/soarsmu/BugsInPy/master/` per bug.
- `checkout_bug` clones the project repo and checks out the buggy commit under `/tmp/bip_checkouts`.
- `install_project` runs `pip install -e . --no-deps` **into the interpreter running SemLoc** —
  no per-bug virtualenv and no dependencies, regardless of the bug's declared `python_version`.
- Faulty lines come from the buggy→fixed diff; the target function comes from AutoFL's prediction.

## What the published logs show (`results/RQ3/bugsInPy_results/`, 463 bugs + summary)

| Outcome | Bugs |
|---|---|
| SemLoc ran end to end (has ground truth + failing tests) | **68** |
| "No violations report generated" (tests could not run — missing deps / wrong Python) | 352 |
| Constraint inference failed (invalid JSON from the LLM) | 27 |
| Unknown project `tqdm` | 8 |
| Other tracebacks | 5 |

The 68 come from: youtube-dl 33, ansible 10, black 8, thefuck 6, matplotlib 5, luigi 4, cookiecutter 2.
Published files hold summaries only (no constraints/violations, no per-test coverage), so they cannot
score CovGate — environments must be rebuilt.

## Our approach

- One uv virtualenv per (project, Python version, exact bug requirements) under
  `runs/bip/venvs/<project>-py<ver>-<req-hash>`; the checkout is put on `PYTHONPATH` (no `pip -e`);
  Python ≥ 3.8 (uv's oldest). Requirement-install failures are recorded in the status `note`.
- Order by expected yield: youtube-dl → black → thefuck → cookiecutter → luigi → ansible → matplotlib.
- Status per bug in `data/bugsinpy_status.csv`. Time box: 10–12/11; threshold ≥20 bugs with
  `env_ok & tests_reproduce & sbfl_ok`.

## Result (2026-11-08) — threshold provisionally met

Probe: `python -m flx.bip status` over the 68 bugs SemLoc completed upstream (`runs/bip/candidates_68.txt`).

| Project | Probed | probe passed: env builds, failing test fails on buggy commit **and passes on fixed commit**, per-test coverage of the faulty file obtainable | …and failing test reaches a faulty line |
|---|---|---|---|
| youtube-dl | 33 | **31** | 22 |
| ansible / black / cookiecutter / luigi / matplotlib / thefuck | 35 | 0 | 0 |
| **Total** | 68 | **31** (≥ 20, provisional) | 22 |

"Provisional": the spec's threshold is ≥ 20 bugs on which SBFL, SemLoc **and** CovGate run to
completion; SemLoc/CovGate have not been run on these bugs yet (milestone 2). All 31 come from one
project (youtube-dl) — a stated limitation. Upstream's "7" counts bugs with line-level SemLoc results,
a different measure, so the two numbers are not compared directly.

Other projects fail on environment setup: pytest "found no collectors" (20, import errors at
collection), missing `numpy` / `psutil` / `ansible` not covered by the bug's requirements.txt (8),
unparseable `run_test.sh` (3). Upstream SemLoc reported line-level results on only 7 youtube-dl bugs.

Decision: milestone 2 runs SemLoc / SBFL / CovGate on the 31 youtube-dl bugs (22 where the fault is
reached are the primary set); extending other projects is optional work if time allows.

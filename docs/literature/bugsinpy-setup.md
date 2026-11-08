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

- One virtualenv per project under `runs/bip/venvs/<project>` (uv), holding SemLoc's deps plus the
  project installed **with** its dependencies, Python version as close to BugsInPy's as uv offers.
- Order by expected yield: youtube-dl → black → thefuck → cookiecutter → luigi → ansible → matplotlib.
- Status per bug in `data/bugsinpy_status.csv`. Time box: 10–12/11; threshold ≥20 bugs with
  `env_ok & tests_reproduce & sbfl_ok`.

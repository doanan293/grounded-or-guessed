# SemFault-250 — notes from our labeling (data/semfault_labels.csv)

Labels follow spec §3.3, computed with SemLoc's own per-test coverage helper (`flx.labels`).

| Label | Programs | Meaning |
|---|---|---|
| semantic | 164 | a faulty line is executed by ≥1 failing and ≥1 passing test |
| coverage_revealed | 21 | failing tests reach a faulty line, no passing test does |
| not_executed | 65 | no failing test executes any ground-truth faulty line |

## Ground-truth audit (finding for RQ1)

For the 65 `not_executed` programs, the ground-truth line in `benchmark/ground_truth.json` is:
- a **blank line** in 56 programs (22% of the benchmark);
- a code line no failing test reaches in 9 programs
  (e.g. `cached_preference:83`, `config_expiry:78`, `estimate_temperature:69`, `feature_cache:31`,
  `kv_snapshot_reader:69`, `limit_job:73`).

SemLoc (Claude T=0.8) still assigns a rank to 35 of these 65, but never rank 1. Its top-1 line sits
next to the ground-truth line: offset +1 in 39 cases, −1 in 13, ±2–4 in the rest. SBFL ranks none of
them (blank lines are never covered).

Working hypothesis: many are **omission faults** (the fix inserts a line, e.g. a missing
normalization), and the ground truth records the insertion point, which in the buggy file is blank.
Example: `calibrate_latency` GT = 73 (blank); the inverted guard `if not clamp:` is on line 70, which
is SemLoc's top-1 line.

Consequences to handle in milestone 2:
- line-exact Acc@k caps every method below 100% on ~22% of programs and penalizes coverage-based
  methods most (they can never rank a blank line);
- report results on the full set **and** on the 185 programs whose fault line is executable;
- consider the omission-fault convention used by Defects4J-style FL studies (count the adjacent
  statement) as a sensitivity analysis, stated as such.

## Split (data/split.json, seed 20261108, stratified by label)

dev 50 / test 200; label shares are kept within one program of proportional.

#!/usr/bin/env bash
# Rebuild every derived table and figure from runs/ and data/ in dependency order (no LLM calls).
#   scripts/regenerate_all.sh
# Run after any run finishes, so no CSV, table or figure is left stale.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/bin/python
# single-prompt runs that cover their whole split are copied next to the committed rankings
$PY - <<'PY'
import json, shutil
from pathlib import Path
split = json.loads(Path("data/split.json").read_text()); sub50 = json.loads(Path("data/subset50.json").read_text())["programs"]
renamed = json.loads(Path("data/renamed/test_programs.json").read_text()); bugs = list(json.loads(Path("data/bugsinpy_targets.json").read_text()))
for f in sorted(Path("runs").glob("direct*_r[0-9].json")):
    progs = (split["test"] if "_test_" in f.name else renamed if "_renamed_" in f.name else bugs if "_bip_" in f.name
             else sub50)
    if set(progs) <= set(json.loads(f.read_text())):
        shutil.copy(f, Path("data/rankings") / f.name)
PY
$PY scripts/llm_cost.py > /dev/null
$PY scripts/runs_table.py > /dev/null
$PY scripts/build_reviewed_gt.py > /dev/null
$PY scripts/gt_sensitivity.py > /dev/null
$PY scripts/rq2_ours.py > /dev/null
$PY scripts/ablation_coverage.py > /dev/null
$PY scripts/static_tools.py > /dev/null
$PY scripts/rq3_families.py > /dev/null
$PY scripts/rq3_renamed.py > /dev/null
$PY -W ignore scripts/rq3_bugsinpy.py > /dev/null
$PY scripts/decompose.py --published --out data/rq_decomposition_published.csv > /dev/null
$PY scripts/decompose.py --runs semloc_test_gemini_r1 semloc_test_gemini_r2 semloc_test_gemini_r3 --out data/rq_decomposition.csv > /dev/null
$PY scripts/failure_cases.py > /dev/null
$PY scripts/pareto_data.py > /dev/null
$PY scripts/checklist.py > /dev/null
$PY scripts/make_tables.py
$PY scripts/make_numbers.py > /dev/null
$PY scripts/check_claims.py --fix docs/analysis/contributions.md docs/analysis/failure-analysis.md

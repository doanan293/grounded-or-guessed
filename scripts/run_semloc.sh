#!/usr/bin/env bash
# Run the upstream SemLoc pipeline (RQ1 configuration) on one working dir through the flx gateway.
#   scripts/run_semloc.sh <workdir> <model> <temperature> <run_id>
# Same run_id = resume from cache; a new run_id = an independent repeat.
set -euo pipefail
[ $# -eq 4 ] || { echo "usage: $0 <workdir> <model> <temperature> <run_id>" >&2; exit 2; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKDIR="$(realpath "$1")"; MODEL="$2"; TEMP="$3"; RUN_ID="$4"
set -a; [ -f "$ROOT/.env" ] && . "$ROOT/.env"; set +a
export FLX_USE_GATEWAY=1 FLX_RUN_ID="$RUN_ID"
export PATH="$ROOT/.venv/bin:$PATH"  # SemLoc shells out to a bare `pytest`
export FLX_LLM_LOG="${FLX_LLM_LOG:-$ROOT/runs/llm_log.jsonl}" FLX_LLM_CACHE_DIR="${FLX_LLM_CACHE_DIR:-$ROOT/runs/llm_cache}"
cd "$ROOT/third_party/semloc"
"$ROOT/.venv/bin/python" src/run_eval.py \
    --working-dir "$WORKDIR" --model "$MODEL" --temperature "$TEMP" \
    --workers "${WORKERS:-4}" --steps 1,3,4,5,6,8 --cf-on-base
cat "$WORKDIR/results_cf_base/summary.json" | head -8

#!/usr/bin/env bash
# Run the upstream SemLoc pipeline (RQ1 configuration) on one working dir through the flx gateway.
#   scripts/run_semloc.sh <workdir> <model> <temperature> <run_id>
# Same run_id = resume (cache + SemLoc skip-if-exists). An independent repeat needs a new run_id AND
# a new workdir: SemLoc skips steps whose outputs exist, so a workdir is bound to one run_id.
# Exit 1 if the run is unhealthy (LLM failures SemLoc swallowed), 3 if the workdir belongs to another run.
set -euo pipefail
[ $# -eq 4 ] || { echo "usage: $0 <workdir> <model> <temperature> <run_id>" >&2; exit 2; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKDIR="$(realpath "$1")"; MODEL="$2"; TEMP="$3"; RUN_ID="$4"
if [ -f "$WORKDIR/.flx_run_id" ] && [ "$(cat "$WORKDIR/.flx_run_id")" != "$RUN_ID" ]; then
    echo "refusing: $WORKDIR belongs to run_id $(cat "$WORKDIR/.flx_run_id"), not $RUN_ID (use a new workdir per repeat)" >&2
    exit 3
fi
mkdir -p "$WORKDIR" && echo "$RUN_ID" > "$WORKDIR/.flx_run_id"
set -a; [ -f "$ROOT/.env" ] && . "$ROOT/.env"; set +a
export FLX_USE_GATEWAY=1 FLX_RUN_ID="$RUN_ID"
export PATH="$ROOT/.venv/bin:$PATH"  # SemLoc shells out to a bare `pytest`
export FLX_LLM_LOG="${FLX_LLM_LOG:-$ROOT/runs/llm_log.jsonl}" FLX_LLM_CACHE_DIR="${FLX_LLM_CACHE_DIR:-$ROOT/runs/llm_cache}"
cd "$ROOT/third_party/semloc"
"$ROOT/.venv/bin/python" src/run_eval.py \
    --working-dir "$WORKDIR" --model "$MODEL" --temperature "$TEMP" \
    --workers "${WORKERS:-4}" --steps 1,3,4,5,6,8 --cf-on-base
head -8 "$WORKDIR/results_cf_base/summary.json"
cd "$ROOT" && "$ROOT/.venv/bin/python" -m flx.run_health --workdir "$WORKDIR" --run-id "$RUN_ID" --log "$FLX_LLM_LOG"

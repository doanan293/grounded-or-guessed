#!/usr/bin/env bash
# SemLoc's own "LLM direct" baseline (semantic indexing disabled = SemLoc† in the paper) as repeats.
#   scripts/run_direct.sh <config> <model> <dev|test|file.json> <reps>
# Workdir runs/<config>_r<i>, run_id = workdir name; per-program results in <workdir>/direct_fl/.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
CONFIG="$1"; MODEL="$2"; PROGS="$3"; REPS="$4"
set -a; [ -f .env ] && . ./.env; set +a
export FLX_USE_GATEWAY=1 PATH="$ROOT/.venv/bin:$PATH"
for i in $(seq 1 "$REPS"); do
    RUN="${CONFIG}_r${i}"; WD="$ROOT/runs/$RUN"
    "$ROOT/.venv/bin/python" -c "
import json, sys
from pathlib import Path
from flx.workdir import make_workdir
from flx._semloc import SEMLOC_ROOT
p = sys.argv[1]
names = json.loads(Path('data/split.json').read_text())[p] if p in ('dev', 'test') else json.loads(Path(p).read_text())
make_workdir(SEMLOC_ROOT / 'benchmark', names, Path(sys.argv[2]))" "$PROGS" "$WD"
    if [ -f "$WD/.flx_run_id" ] && [ "$(cat "$WD/.flx_run_id")" != "$RUN" ]; then echo "workdir owned by another run" >&2; exit 3; fi
    echo "$RUN" > "$WD/.flx_run_id"
    FLX_RUN_ID="$RUN" "$ROOT/.venv/bin/python" third_party/semloc/src/run_eval.py --working-dir "$WD" --model "$MODEL" \
        --workers "${WORKERS:-4}" --disable-semantic-index > "$ROOT/runs/$RUN.log" 2>&1
    "$ROOT/.venv/bin/python" -m flx.run_health --workdir "$WD" --run-id "$RUN"
done

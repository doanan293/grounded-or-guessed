#!/usr/bin/env bash
# Run one SemLoc configuration as independent repeats: workdir runs/<config>_r<i>, run_id = that name.
#   scripts/run_matrix.sh <config> <model> <programs: dev|test|subset50|path.json> <reps> [first_rep]
# Stops at the first unhealthy repeat (run_semloc.sh exits non-zero).
set -euo pipefail
[ $# -ge 4 ] || { echo "usage: $0 <config> <model> <dev|test|subset50|file.json> <reps> [first_rep]" >&2; exit 2; }
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$1"; MODEL="$2"; PROGS="$3"; REPS="$4"; FIRST="${5:-1}"
BENCH="${BENCH:-$ROOT/third_party/semloc/benchmark}"
cd "$ROOT"  # program lists are resolved against data/
for i in $(seq "$FIRST" "$REPS"); do
    RUN="${CONFIG}_r${i}"; WD="$ROOT/runs/$RUN"
    "$ROOT/.venv/bin/python" - "$BENCH" "$PROGS" "$WD" <<'PY'
import json, sys
from pathlib import Path
from flx.workdir import make_workdir
bench, progs, wd = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
data = Path("data")
if progs in ("dev", "test"):
    names = json.loads((data / "split.json").read_text())[progs]
elif progs == "subset50":
    names = json.loads((data / "subset50.json").read_text())["programs"]
else:
    names = json.loads(Path(progs).read_text())
make_workdir(bench, names, wd)
print(f"{wd.name}: {len(names)} programs")
PY
    WORKERS="${WORKERS:-8}" "$ROOT/scripts/run_semloc.sh" "$WD" "$MODEL" 0.8 "$RUN" > "$ROOT/runs/$RUN.log" 2>&1
    echo "$RUN healthy"
done

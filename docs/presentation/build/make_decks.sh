#!/usr/bin/env bash
# Build, check and export the decks: make_decks.sh [lan1] [lan2] [baove]  (default: all three)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"; cd "$ROOT"
S=.claude/skills/ppt-master/scripts; W=runs/slides/bao-cao-lan-1_20261108
declare -A OUT=([lan1]=bao-cao-lan-1.pptx [lan2]=bao-cao-lan-2.pptx [baove]=bao-ve.pptx)
for deck in "${@:-lan1 lan2 baove}"; do
  for d in $deck; do
    python3 docs/presentation/build/build_deck.py "$d"
    python3 $S/svg_authoring_view.py $W/authoring-svg-flat --refresh-summary > /dev/null
    python3 $S/svg_quality_checker.py $W --roundtrip --json > "$W/validation/qc_$d.txt" 2>&1 || true
    if grep -q "\[ERROR\] With errors: [1-9]" "$W/validation/qc_$d.txt"; then
      grep "\[ERROR\]" "$W/validation/qc_$d.txt" | head -20; echo "quality gate failed for $d"; exit 1; fi
    out=$(python3 $S/svg_to_pptx.py $W --roundtrip 2>&1 | grep -o "runs/slides/[^ ]*\.pptx" | tail -1)
    cp "$out" "docs/presentation/${OUT[$d]}"
    echo "$d -> docs/presentation/${OUT[$d]}"
  done
done

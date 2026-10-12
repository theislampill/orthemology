#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-"$ROOT/controls-replay"}
mkdir -p "$OUT"
"$ROOT/lean.sh" -j1 "$ROOT/RootCosts.lean" > "$OUT/RootCosts.log" 2>&1
for name in Regression FamilyDeletionControls; do
  "$ROOT/lean.sh" -j1 "$ROOT/tests/$name.lean" > "$OUT/$name.log" 2>&1
done
for file in "$ROOT"/mutation-controls/*.lean; do
  name=$(basename "$file" .lean)
  if "$ROOT/lean.sh" -j1 "$file" > "$OUT/$name.log" 2>&1; then
    echo "UNEXPECTEDLY ACCEPTED MUTANT: $name"; exit 1
  fi
  if ! grep -q 'error:' "$OUT/$name.log"; then
    echo "Mutant failed without a Lean error: $name"; exit 1
  fi
  printf 'Correctly rejected mutant: %s\n' "$name"
done
printf 'Positive regression and semantic hypothesis-deletion controls passed.\n'

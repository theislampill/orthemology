#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-"$ROOT/full-replay"}
mkdir -p "$OUT/logs" "$OUT/mutations"
bash "$ROOT/frozen-source/verify.sh" "$OUT"
export ATTRIBUTION_BUILD="$OUT/build"
LEAN="$ROOT/frozen-source/lean.sh"
for name in IndependentChecks DeletionControls AxiomAudit; do
  "$LEAN" -j1 "$ROOT/$name.lean" > "$OUT/logs/$name.log" 2>&1
done
"$LEAN" -j1 "$ROOT/frozen-source/tests/Regression.lean" > "$OUT/logs/Regression.log" 2>&1
"$LEAN" -j1 -o "$OUT/build/RootCosts.olean" "$ROOT/frozen-controls/RootCosts.lean" > "$OUT/logs/RootCosts.log" 2>&1
"$LEAN" -j1 "$ROOT/frozen-controls/tests/FamilyDeletionControls.lean" > "$OUT/logs/FamilyDeletionControls.log" 2>&1
for file in "$ROOT/frozen-controls/mutation-controls/"*.lean; do
  name=$(basename "$file" .lean)
  if "$LEAN" -j1 "$file" > "$OUT/mutations/$name.log" 2>&1; then
    echo "FAILED: invalid mutant unexpectedly accepted: $name"; exit 1
  fi
  grep -q 'error:' "$OUT/mutations/$name.log"
  printf 'Expected rejection: %s\n' "$name"
done
if grep -En 'sorryAx|warning:|error:' "$OUT/logs/"*.log; then exit 1; fi
printf 'PASS: central proofs, all targets, regressions, supplement, independent checks, all-theorem axiom audit, and expected-failure controls.\n'

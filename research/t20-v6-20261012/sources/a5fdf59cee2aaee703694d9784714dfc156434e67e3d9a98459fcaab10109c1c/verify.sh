#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-"$ROOT/.build"}
mkdir -p "$OUT/logs"
OUT=$(cd "$OUT" && pwd)
MATHLIB=${MATHLIB_C44:-private-locator:18d48e051fd31eaf177f}
LEAN=${LEAN_419:-private-locator:cb50f30cfa35bdf3a0cf}
export LEAN_PATH="$OUT:$MATHLIB/.lake/build/lib/lean"
for p in "$MATHLIB"/.lake/packages/*/.lake/build/lib/lean; do export LEAN_PATH="$LEAN_PATH:$p"; done
"$LEAN" --version | tee "$OUT/logs/lean-version.log"
python3 "$ROOT/verify_inputs.py" "$OUT/INPUT_VERIFICATION.json"
for name in RootImage Availability; do
  "$LEAN" -o "$OUT/$name.olean" "$ROOT/dependencies/$name.lean" > "$OUT/logs/dependency-$name.log" 2>&1
 done
for name in CoveringPortfolio LabelTransport OpaqueSearch CanonicalReplies RandomizedFinite RandomizedSearch SourceCorrespondence ExactCap OpaqueActions FullCommandInterface RepairStateBridge; do
  "$LEAN" -o "$OUT/$name.olean" "$ROOT/$name.lean" > "$OUT/logs/$name.log" 2>&1
 done
for name in TargetCovering TargetSearch NegativeControls Check; do
  "$LEAN" -o "$OUT/$name.olean" "$ROOT/tests/$name.lean" > "$OUT/logs/test-$name.log" 2>&1
 done
if grep -R -E 'sorryAx|error:' "$OUT/logs"; then
  echo 'Unexpected proof hole or compiler error' >&2; exit 1
fi
python3 "$ROOT/tests/semantic_controls.py" "$OUT/SEMANTIC_RESULTS.json"
python3 -O "$ROOT/tests/semantic_controls.py" "$OUT/SEMANTIC_RESULTS_OPTIMIZED.json"
cmp "$OUT/SEMANTIC_RESULTS.json" "$OUT/SEMANTIC_RESULTS_OPTIMIZED.json"
python3 "$ROOT/tests/mutation_controls.py" "$OUT" "$LEAN"
python3 "$ROOT/verify_inputs.py" "$OUT/INPUT_VERIFICATION_AFTER.json"
cmp "$OUT/INPUT_VERIFICATION.json" "$OUT/INPUT_VERIFICATION_AFTER.json"
echo 'PASS: generic kernel modules, statement checks, source bindings, semantic controls, six rejected proof mutations.'

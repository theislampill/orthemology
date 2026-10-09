#!/usr/bin/env bash
set -euo pipefail
REVIEW=$(cd -- "$(dirname -- "$0")" && pwd)
INVERSE_REVIEW=$(cd -- "$REVIEW/../formal-identification-review/frozen" && pwd)
BASE=$(cd -- "$REVIEW/../formal-identification" && pwd)
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
export LEAN_PATH="$REVIEW/frozen:$INVERSE_REVIEW:$(lake env printenv LEAN_PATH)"
for module in BernoulliAssignments HistogramGrouping Model GenerativePanels EndpointLaw Verification; do
  lean -DwarningAsError=true --root="$REVIEW/frozen" -o "$REVIEW/frozen/$module.olean" "$REVIEW/frozen/$module.lean"
done
lean --trust=0 -DwarningAsError=true --root="$REVIEW/frozen" "$REVIEW/frozen/Verification.lean"

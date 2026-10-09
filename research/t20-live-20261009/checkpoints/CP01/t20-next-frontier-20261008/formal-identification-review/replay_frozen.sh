#!/usr/bin/env bash
set -euo pipefail
REVIEW=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=$(cd -- "$REVIEW/../formal-identification" && pwd)
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
DEPS=$(lake env printenv LEAN_PATH)
export LEAN_PATH="$REVIEW/frozen:$DEPS"
lean -DwarningAsError=true --root="$REVIEW/frozen" -o "$REVIEW/frozen/Calibration.olean" "$REVIEW/frozen/Calibration.lean"
lean -DwarningAsError=true --root="$REVIEW/frozen" -o "$REVIEW/frozen/HitTransform.olean" "$REVIEW/frozen/HitTransform.lean"
lean -DwarningAsError=true --root="$REVIEW/frozen" -o "$REVIEW/frozen/CalibratedPanels.olean" "$REVIEW/frozen/CalibratedPanels.lean"
lean -DwarningAsError=true --root="$REVIEW/frozen" "$REVIEW/frozen/Verification.lean"

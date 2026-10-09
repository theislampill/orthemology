#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
export PATH="$ROOT/toolchain/lean-4.19.0-linux/bin:$PATH"
export XDG_CACHE_HOME="$ROOT/toolchain/cache"
cd "$ROOT/mathlib"
lake env lean -DwarningAsError=true --root="$ROOT" -o "$ROOT/Calibration.olean" "$ROOT/Calibration.lean"
lake env lean -DwarningAsError=true --root="$ROOT" -o "$ROOT/HitTransform.olean" "$ROOT/HitTransform.lean"
export LEAN_PATH="$ROOT:$(lake env printenv LEAN_PATH)"
lean -DwarningAsError=true --root="$ROOT" -o "$ROOT/CalibratedPanels.olean" "$ROOT/CalibratedPanels.lean"
lean -DwarningAsError=true "$ROOT/Verification.lean"

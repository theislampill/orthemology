#!/usr/bin/env bash
set -euo pipefail
REVIEW=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=[OMITTED_PRIVATE_MACHINE_PATH]
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
DEPS=$(lake env printenv LEAN_PATH)
export LEAN_PATH="$REVIEW:$DEPS"
lean -t0 -DwarningAsError=true --root="$REVIEW" -o "$REVIEW/GraphContinuation.olean" "$REVIEW/GraphContinuation.lean"

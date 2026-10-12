#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=private-locator:33568aac5b6e8da06f38
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
DEPS=$(lake env printenv LEAN_PATH)
export LEAN_PATH="$HERE:$DEPS"
lean -t0 -DwarningAsError=true --root="$HERE" "$@"

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
DEP="$ROOT/../formal-identification"
export PATH="$DEP/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$DEP/mathlib"
export LEAN_PATH="$ROOT:$DEP:$(lake env printenv LEAN_PATH)"
lean -DwarningAsError=true --root="$ROOT" -o "$ROOT/${1%.lean}.olean" "$ROOT/$1"

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
MATHLIB=${MATHLIB_C44:-private-locator:18d48e051fd31eaf177f}
export LEAN_PATH="${COVERING_BUILD_DIR:-$ROOT/.build}:$MATHLIB/.lake/build/lib/lean"
for p in "$MATHLIB"/.lake/packages/*/.lake/build/lib/lean; do export LEAN_PATH="$LEAN_PATH:$p"; done
exec "${LEAN_419:-private-locator:cb50f30cfa35bdf3a0cf}" "$@"

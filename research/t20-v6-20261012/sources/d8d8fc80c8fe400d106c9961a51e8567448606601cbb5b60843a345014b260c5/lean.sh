#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
MATHLIB=private-locator:18d48e051fd31eaf177f
export LEAN_PATH="${INTERLOCK_BUILD:-$ROOT}:$MATHLIB/.lake/build/lib/lean"
for p in "$MATHLIB"/.lake/packages/*/.lake/build/lib/lean; do export LEAN_PATH="$LEAN_PATH:$p"; done
exec private-locator:cb50f30cfa35bdf3a0cf "$@"

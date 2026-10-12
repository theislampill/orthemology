#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(cd -- "$HERE/../.." && pwd)
LEAN=${LEAN_BIN_DIR:-"$ROOT/tranche2/toolchain/lean-4.19.0-linux/bin"}
MATHLIB=${MATHLIB_DIR:-"$ROOT/tranche2/toolchain/mathlib4"}
BUILD=${BUILD_DIR:-"$HERE/build"}
mkdir -p "$BUILD"
export PATH="$LEAN:$PATH"
[[ $(git -C "$MATHLIB" rev-parse HEAD) == c44e0c8ee63ca166450922a373c7409c5d26b00b ]]
"$LEAN/lean" --version | grep -F 'version 4.19.0'
cd "$MATHLIB"
for M in "$@"; do
  lake env bash -c 'export LEAN_PATH="$1:$LEAN_PATH"; exec lean -j1 --root="$2" -o "$1/$3.olean" "$2/$3.lean"' _ "$BUILD" "$HERE/lean" "$M" > "$BUILD/$M.log" 2>&1
  cat "$BUILD/$M.log"
  if grep -E 'error:|sorryAx|PANIC|stack overflow' "$BUILD/$M.log"; then exit 1; fi
  printf '%s PASS\n' "$M"
done

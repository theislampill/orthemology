#!/usr/bin/env bash
set -euo pipefail
D=$(cd -- "$(dirname -- "$0")" && pwd)
T=${TOOLCHAIN_DIR:-"$D/../toolchain"}
BASE=${COMMON_OBSERVATION_SOURCE:-"$D/../common-observation-audit/snapshot"}
BUILD_DIR=${BUILD_DIR:-"$(mktemp -d private-locator:2ea6c493a91ee93546c8)"}
mkdir -p "$BUILD_DIR"
BUILD_DIR=$(cd -- "$BUILD_DIR" && pwd)
export PATH="$T/lean-4.19.0-linux/bin:$PATH"
[[ $(git -C "$T/mathlib4" rev-parse HEAD) == c44e0c8ee63ca166450922a373c7409c5d26b00b ]]
cd "$T/mathlib4"
for M in SelfVerifyingSupport CommonObservationBoundary CommonObservationFiniteActions CompactObservationBoundary CompactBoundaryControls; do
  SRC="$BASE"
  if [[ "$M" == Compact* ]]; then SRC="$D/lean"; fi
  lake env bash -c 'export LEAN_PATH="$1:$LEAN_PATH"; exec lean -j1 --root="$2" -o "$1/$3.olean" "$2/$3.lean"' _ "$BUILD_DIR" "$SRC" "$M" > "$BUILD_DIR/$M.log" 2>&1
  if grep -E 'error:|sorryAx' "$BUILD_DIR/$M.log"; then exit 1; fi
  echo "$M PASS"
done
printf 'Fresh local closure: %s\n' "$BUILD_DIR"

#!/usr/bin/env bash
# Installs only into this package directory, using official Lean/mathlib releases.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
LEAN_VERSION=4.19.0
LEAN_SHA256=6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe
MATHLIB_COMMIT=c44e0c8ee63ca166450922a373c7409c5d26b00b
mkdir -p "$ROOT/toolchain" "$ROOT/results"
if [[ ! -x "$ROOT/toolchain/lean-$LEAN_VERSION-linux/bin/lean" ]]; then
  archive="$ROOT/toolchain/lean-$LEAN_VERSION-linux.tar.zst"
  if [[ ! -f "$archive" ]]; then
    curl --fail --location --retry 2 \
      "https://github.com/leanprover/lean4/releases/download/v$LEAN_VERSION/lean-$LEAN_VERSION-linux.tar.zst" \
      -o "$archive"
  fi
  printf '%s  %s\n' "$LEAN_SHA256" "$archive" | sha256sum --check
  tar --zstd -xf "$archive" -C "$ROOT/toolchain"
fi
export PATH="$ROOT/toolchain/lean-$LEAN_VERSION-linux/bin:$PATH"
export XDG_CACHE_HOME="$ROOT/toolchain/cache"
lean --version
if [[ ! -d "$ROOT/mathlib" ]]; then
  git clone --depth 1 --branch "v$LEAN_VERSION" \
    https://github.com/leanprover-community/mathlib4.git "$ROOT/mathlib"
fi
actual=$(git -C "$ROOT/mathlib" rev-parse HEAD)
if [[ "$actual" != "$MATHLIB_COMMIT" ]]; then
  echo "Mathlib checkout mismatch: expected $MATHLIB_COMMIT, got $actual" >&2
  exit 1
fi
cd "$ROOT/mathlib"
lake exe cache get \
  Mathlib/NumberTheory/Padics/PadicVal/Basic.lean \
  Mathlib/Tactic/NormNum.lean Mathlib/Tactic/Ring.lean \
  Mathlib/Data/Fintype/Powerset.lean Mathlib/Data/Finset/BooleanAlgebra.lean \
  Mathlib/Algebra/BigOperators/Group/Finset/Basic.lean

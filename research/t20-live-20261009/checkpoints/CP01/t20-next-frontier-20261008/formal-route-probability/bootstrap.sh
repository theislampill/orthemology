#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
DEP="$ROOT/../formal-identification"
(cd "$DEP"; sha256sum --check SOURCE_MANIFEST.sha256; ./bootstrap.sh)
export PATH="$DEP/toolchain/lean-4.19.0-linux/bin:$PATH"
export XDG_CACHE_HOME="$DEP/toolchain/cache"
cd "$DEP/mathlib"
lake exe cache get Mathlib/Algebra/BigOperators/Ring/Finset.lean Mathlib/Algebra/Order/Field/Rat.lean

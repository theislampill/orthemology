#!/usr/bin/env bash
set -euo pipefail
cd private-locator:8f24556a330b05a11a95
export LEAN_PATH="$PWD/hase-internal-graph-20261010:$PWD/hase-full-per-extension-20261010/validation:$PWD/hase-imported-compiler-transport-20261010/validation/replay-bxNUv6:$(find "$PWD/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd :)"
exec .toolchains/lean-4.19.0-linux/bin/lean --trust=0 "$@"

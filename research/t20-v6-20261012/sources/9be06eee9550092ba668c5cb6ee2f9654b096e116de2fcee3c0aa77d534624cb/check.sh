#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
export LEAN_PATH="$ROOT/validation:$W/homogeneous-per-model-20261010/operational:$W/homogeneous-per-closure-20261010/validation:$W/hase-imported-compiler-transport-20261010/validation/replay-bxNUv6:$(find "$W/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd :)"
for MODULE in SourceTransport HenkinSoundness DependencyAudit; do
  "$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/$MODULE.olean" "$ROOT/$MODULE.lean"
done

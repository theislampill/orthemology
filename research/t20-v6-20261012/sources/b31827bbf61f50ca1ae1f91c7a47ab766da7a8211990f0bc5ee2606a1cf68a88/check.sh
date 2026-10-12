#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export LEAN_PATH="$PWD/hase-raw-context-uniformity-20261010/validation:$PWD/hase-church-structural-20261010/validation:$PWD/hase-closed-church-identity-20261010/validation:$PWD/hase-closed-scalar-instances-20261010/validation/fresh-ie5j3ep9:$PWD/hase-full-per-review-20261010/fresh-lib:$(find "$PWD/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd:)"
.toolchains/lean-4.19.0-linux/bin/lean --trust=0 -o hase-raw-context-uniformity-20261010/validation/RawContextUniformity.olean hase-raw-context-uniformity-20261010/RawContextUniformity.lean
export LEAN_PATH="$PWD/hase-effective-instance-assessment-20261010/validation:$LEAN_PATH"
.toolchains/lean-4.19.0-linux/bin/lean --trust=0 -o hase-raw-context-uniformity-20261010/validation/RawContextControls.olean hase-raw-context-uniformity-20261010/RawContextControls.lean

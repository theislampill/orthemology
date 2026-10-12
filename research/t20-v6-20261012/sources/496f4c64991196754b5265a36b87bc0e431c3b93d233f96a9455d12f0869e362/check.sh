#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
R="$PWD/hase-structured-context-uniformity-20261010"
export LEAN_PATH="$R/validation:$PWD/hase-raw-context-uniformity-20261010/validation:$PWD/hase-church-structural-20261010/validation:$PWD/hase-closed-church-identity-20261010/validation:$PWD/hase-closed-scalar-instances-20261010/validation/fresh-ie5j3ep9:$PWD/hase-effective-instance-assessment-20261010/validation:$PWD/hase-full-per-review-20261010/fresh-lib:$(find "$PWD/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd:)"
for M in "$@"; do
  .toolchains/lean-4.19.0-linux/bin/lean --trust=0 -o "$R/validation/$M.olean" "$R/$M.lean"
done

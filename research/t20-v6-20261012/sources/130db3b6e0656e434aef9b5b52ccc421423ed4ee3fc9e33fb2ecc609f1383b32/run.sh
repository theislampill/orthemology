#!/bin/bash
set -euo pipefail
cd private-locator:8f24556a330b05a11a95
export LEAN_PATH="$(pwd)/hase-church-structural-20261010/validation:$(pwd)/hase-closed-scalar-instances-20261010/validation/fresh-ie5j3ep9:$(pwd)/hase-full-per-review-20261010/fresh-lib"
for d in separating-projection-lean-20261009/.lake/packages/*/.lake/build/lib/lean; do export LEAN_PATH="$LEAN_PATH:$(pwd)/$d"; done
.toolchains/lean-4.19.0-linux/bin/lean --trust=0 -o hase-church-structural-20261010/validation/$1.olean hase-church-structural-20261010/$1.lean

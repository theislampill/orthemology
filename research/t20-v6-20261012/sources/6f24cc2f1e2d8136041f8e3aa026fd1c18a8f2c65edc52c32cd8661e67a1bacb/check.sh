#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
export LEAN_PATH="$ROOT/validation:$W/hase-full-e-dependent-induction-20261010/validation:$W/hase-rigidity-initiality-20261010/validation:$W/hase-type-parameter-substitution-20261010/validation:$W/hase-dependent-substitution-20261010/validation:$W/hase-church-structural-20261010/validation:$(cat "$W/hase-generic-rigidity-review-20261010/lean_path.txt")"
export LEAN_PATH="$LEAN_PATH:$W/hase-closed-church-completeness-review-20261010/fresh-lib:$W/hase-complete-development-review-20261010/fresh-lib:$W/hase-effective-instance-assessment-20261010/validation"
for module in InductionRigidityConverse; do
  "$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/$module.olean" "$ROOT/$module.lean"
done

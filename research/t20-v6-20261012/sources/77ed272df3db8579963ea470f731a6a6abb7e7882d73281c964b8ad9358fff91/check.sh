#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
export LEAN_PATH="$W/hase-church-structural-20261010/validation:$ROOT/validation:$W/hase-rigidity-initiality-20261010/validation:$(cat "$W/hase-generic-rigidity-review-20261010/lean_path.txt")"
"$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/UnitTransfer.olean" "$ROOT/UnitTransfer.lean"
"$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/FoldNaturality.olean" "$ROOT/FoldNaturality.lean"

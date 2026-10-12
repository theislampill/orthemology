#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
export LEAN_PATH="$ROOT/validation:$W/hase-complete-development-review-20261010/fresh-lib:$(cat "$W/hase-generic-rigidity-review-20261010/lean_path.txt")"
for file in TaggedPER Boundary; do
  "$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/$file.olean" "$ROOT/$file.lean"
done

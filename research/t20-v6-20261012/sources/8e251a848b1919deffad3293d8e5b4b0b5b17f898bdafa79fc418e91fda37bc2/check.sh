#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
export LEAN_PATH="$ROOT/validation:$W/hase-sigma-tag-boundary-20261010/validation:$W/hase-complete-development-review-20261010/fresh-lib:$(cat "$W/hase-generic-rigidity-review-20261010/lean_path.txt")"
"$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/CompletionSeparation.olean" "$ROOT/CompletionSeparation.lean"
"$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$ROOT/validation/Controls.olean" "$ROOT/Controls.lean"

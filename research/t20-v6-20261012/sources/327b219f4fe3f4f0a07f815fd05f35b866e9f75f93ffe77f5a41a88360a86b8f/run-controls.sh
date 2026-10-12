#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$HERE")
export LEAN_PATH=$(cat "$HERE/LEAN_PATH.txt")
"$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$HERE/fresh-lib/IndependentControls.olean" "$HERE/IndependentControls.lean" > "$HERE/IndependentControls.log" 2>&1

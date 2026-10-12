#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$HERE")
source "$HERE/env.sh"
OUT=$(mktemp -d "$HERE/validation/fresh-XXXXXX")
export LEAN_PATH="$OUT:$LEAN_PATH"
for m in SeededSourceLookup SeededSourceHistories SeededSourceControls SeededSourceAudit; do
  "$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$OUT/$m.olean" "$HERE/$m.lean"
done
printf 'Fresh output: %s\n' "$OUT"

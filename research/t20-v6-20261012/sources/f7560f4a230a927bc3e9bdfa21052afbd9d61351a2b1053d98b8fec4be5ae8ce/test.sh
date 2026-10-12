#!/bin/bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$ROOT")
source <(sed '/^for module/,$d' "$ROOT/replay.sh")
printf "%s\n" "$LEAN_PATH" > "$ROOT/lean_path.txt"
LEAN="$W/.toolchains/lean-4.19.0-linux/bin/lean"
"$LEAN" --version > "$ROOT/logs/toolchain.log"
"$LEAN" --trust=0 "$ROOT/sources/IndependentPositive.lean" > "$ROOT/logs/positive.log" 2>&1
for n in RejectOriginalScope RejectRawAsTyped; do
  if "$LEAN" --trust=0 "$ROOT/sources/$n.lean" > "$ROOT/logs/$n.log" 2>&1; then
    echo "Unexpected success $n"; exit 1
  fi
  grep -Eq 'type mismatch|Application type mismatch' "$ROOT/logs/$n.log"
done
printf 'PASS: positive and two expected rejection tests\n'

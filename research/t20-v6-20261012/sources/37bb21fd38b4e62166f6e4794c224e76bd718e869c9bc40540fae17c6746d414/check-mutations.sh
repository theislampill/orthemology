#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
for name in DropValidity DropNullary SubsetSupport; do
  if "$HERE/run-lean.sh" "$HERE/mutations/$name.lean" > "$HERE/mutations/$name.log" 2>&1; then
    echo "ERROR mutation accepted: $name"; exit 1
  fi
  if grep -Eq 'unknown module|unknown identifier|file not found|maximum recursion|maximum number of heartbeats|failed to synthesize' "$HERE/mutations/$name.log"; then
    echo "ERROR mutation did not reach intended proof obligation: $name"; exit 1
  fi
  grep -Eq 'unsolved goals|type mismatch|tactic.*failed' "$HERE/mutations/$name.log"
  echo "PASS rejected semantic mutation: $name"
done

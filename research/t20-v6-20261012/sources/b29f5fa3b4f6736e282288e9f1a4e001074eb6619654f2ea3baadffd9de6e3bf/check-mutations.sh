#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
for name in UnsupportedSeed KeyOnlyStops DropGuard; do
  if "$HERE/run-lean.sh" "$HERE/mutations/$name.lean" > "$HERE/mutations/$name.log" 2>&1; then
    echo "UNEXPECTED ACCEPTANCE: $name"
    exit 1
  fi
  if grep -qE "unknown module|file not found|unexpected token" "$HERE/mutations/$name.log"; then
    echo "Invalid rejection mechanism: $name"
    exit 1
  fi
  printf 'Rejected as expected: %s\n' "$name"
done

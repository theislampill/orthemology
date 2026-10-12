#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
for name in DropGuard DropNullary DropChildCosts; do
  if "$HERE/run-lean.sh" "$HERE/mutations/$name.lean" > "$HERE/mutations/$name.log" 2>&1; then
    echo "FAIL: mutation $name was accepted"; exit 1
  fi
  if ! grep -q 'unsolved goals' "$HERE/mutations/$name.log"; then
    echo "FAIL: mutation $name did not fail at its correspondence proof"; cat "$HERE/mutations/$name.log"; exit 1
  fi
  if grep -qE 'unknown module|file .* not found|maximum recursion|maximum number of heartbeats' "$HERE/mutations/$name.log"; then
    echo "FAIL: unrelated failure for mutation $name"; exit 1
  fi
  echo "EXPECTED REJECTION: $name"
done

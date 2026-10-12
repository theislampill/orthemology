#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
for name in OverpricedCertificate IgnoreRootJudgement; do
  if "$HERE/fresh/run-lean.sh" "$HERE/fresh/mutations/$name.lean" > "$HERE/logs/$name.log" 2>&1; then
    echo "FAIL semantic mutation unexpectedly accepted: $name"; exit 1
  fi
  if grep -Eq 'unknown module|unknown identifier|file not found|maximum recursion|maximum number of heartbeats|failed to synthesize' "$HERE/logs/$name.log"; then
    echo "FAIL unrelated compilation error for: $name"; exit 1
  fi
  grep -q 'unsolved goals' "$HERE/logs/$name.log"
  grep -q 'Valid G t' "$HERE/logs/$name.log"
  echo "PASS independent exact-verifier mutation rejected: $name"
done

#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
"$HERE/run-lean.sh" --version
for module in LocalFintypeProd GuardedTree Bound Catalogue Attainment; do
  "$HERE/run-lean.sh" -o "$HERE/frozen/$module.olean" "$HERE/frozen/$module.lean"
  printf 'Checked frozen source: %s\n' "$module"
done
for module in Candidates Saturation Stability Controls; do
  "$HERE/run-lean.sh" -o "$HERE/$module.olean" "$HERE/$module.lean"
  printf 'Checked: %s\n' "$module"
done
printf 'Replay passed: five frozen sources and four new modules.\n'

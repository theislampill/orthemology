#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
"$HERE/run-lean.sh" --version
for module in LocalFintypeProd GuardedTree Bound Catalogue Attainment Candidates Saturation Stability; do
  "$HERE/run-lean.sh" -o "$HERE/frozen/$module.olean" "$HERE/frozen/$module.lean"
  printf 'Checked frozen source: %s\n' "$module"
done
for module in Executable FiniteTable Controls Main; do
  "$HERE/run-lean.sh" -o "$HERE/$module.olean" "$HERE/$module.lean"
  printf 'Checked new source: %s\n' "$module"
done
"$HERE/run-lean.sh" --run "$HERE/Main.lean"
printf 'Replay passed: eight frozen and four new modules, runtime checks invoked twice.\n'

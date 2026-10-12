#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
FRESH="$HERE/fresh"
find "$FRESH" -name '*.olean' -delete
BASE=[OMITTED_PRIVATE_MACHINE_PATH]
{
  date -u +'%Y-%m-%dT%H:%M:%SZ'
  printf 'Independent source root: %s\n' "$FRESH"
  printf 'Initial local olean count: '
  find "$FRESH" -name '*.olean' | wc -l
  printf 'Pinned Lean executable digest: '
  sha256sum "$BASE/toolchain/lean-4.19.0-linux/bin/lean"
  export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
  cd "$BASE/mathlib"
  printf 'External library path: '
  lake env printenv LEAN_PATH
} > "$HERE/logs/environment.log"
"$FRESH/replay.sh" > "$HERE/logs/final-replay.log" 2>&1
"$FRESH/check-mutations.sh" > "$HERE/logs/submitter-mutations.log" 2>&1
"$FRESH/run-lean.sh" --run "$FRESH/AdverseChecks.lean" > "$HERE/logs/adverse.log" 2>&1
printf 'Fresh replay, submitter semantic mutations, and independent adverse checks passed.\n'

#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=private-locator:33568aac5b6e8da06f38
cmp "$HERE/LocalFintypeProd.lean" "$BASE/mathlib/Mathlib/Data/Fintype/Prod.lean"
"$HERE/run-lean.sh" --version
for MODULE in LocalFintypeProd GuardedTree Bound Controls; do
  "$HERE/run-lean.sh" -o "$HERE/$MODULE.olean" "$HERE/$MODULE.lean"
  printf 'Checked: %s\n' "$MODULE"
done
for NAME in SupportShrink PremiseReversal NegativePricePruning; do
  LOG="$HERE/mutations/$NAME.log"
  if "$HERE/run-lean.sh" "$HERE/mutations/$NAME.lean" > "$LOG" 2>&1; then
    echo "ERROR: false mutation $NAME unexpectedly compiled" >&2
    exit 1
  fi
  if [[ "$NAME" == NegativePricePruning ]]; then
    grep -q 'unsolved goals' "$LOG"
    grep -q '⊢ False' "$LOG"
  else
    grep -q "tactic 'decide' proved that the proposition" "$LOG"
    grep -q '^is false$' "$LOG"
  fi
  printf 'Expected rejection: %s\n' "$NAME"
done
if grep -En '\b(sorry|admit|axiom|native_decide)\b' \
    "$HERE/GuardedTree.lean" "$HERE/Bound.lean" "$HERE/Controls.lean"; then
  echo 'ERROR: prohibited proof escape in production source' >&2
  exit 1
fi
printf 'Replay passed: 4 modules and 3 expected-failure mutations.\n'

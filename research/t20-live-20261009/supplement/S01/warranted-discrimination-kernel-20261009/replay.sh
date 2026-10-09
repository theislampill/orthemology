#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=[OMITTED_PRIVATE_MACHINE_PATH]
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
DEPS=$(lake env printenv LEAN_PATH)
export LEAN_PATH="$HERE:$DEPS"
lean --version
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/CertificateFrontier.olean" "$HERE/CertificateFrontier.lean"
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/Controls.olean" "$HERE/Controls.lean"
for NAME in CostBlind CurrentCost InfinitePrice; do
  LOG="$HERE/mutations/$NAME.log"
  if lean -t0 -DwarningAsError=true --root="$HERE" "$HERE/mutations/$NAME.lean" > "$LOG" 2>&1; then
    echo "ERROR: false mutation $NAME unexpectedly compiled" >&2
    exit 1
  fi
  grep -q "tactic 'decide' proved that the proposition" "$LOG"
  grep -q '^is false$' "$LOG"
  echo "Expected rejection: $NAME (decide proved the proposition false)"
done

#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=[OMITTED_PRIVATE_MACHINE_PATH]/t20-next-frontier-20261008/formal-identification
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$BASE/mathlib"
DEPS=$(lake env printenv LEAN_PATH)
export LEAN_PATH="$HERE:$DEPS"
lean --version
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/CertificateFrontier.olean" "$HERE/CertificateFrontier.lean"
lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/ScopeChecks.olean" "$HERE/ScopeChecks.lean"
if [[ -f "$HERE/Controls.lean" ]]; then
  lean -t0 -DwarningAsError=true --root="$HERE" -o "$HERE/Controls.olean" "$HERE/Controls.lean"
fi

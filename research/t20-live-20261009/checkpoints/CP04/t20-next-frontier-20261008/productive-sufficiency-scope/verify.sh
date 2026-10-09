#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
DEP="$ROOT/../formal-identification"
PROB="$ROOT/../formal-route-probability"
export PATH="$DEP/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$DEP/mathlib"
export LEAN_PATH="$ROOT:$ROOT/inherited:$PROB:$DEP:$(lake env printenv LEAN_PATH)"
for n in SourceIdentityDerived OriginalBearerBridge BridgeControls; do
 lean -DwarningAsError=true --root="$ROOT/inherited" -o "$ROOT/inherited/$n.olean" "$ROOT/inherited/$n.lean"
done
lean -DwarningAsError=true --trust=0 --root="$ROOT" -o "$ROOT/ScopeTest.olean" "$ROOT/ScopeTest.lean"

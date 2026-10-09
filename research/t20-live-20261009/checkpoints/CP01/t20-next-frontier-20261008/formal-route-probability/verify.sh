#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
DEP="$ROOT/../formal-identification"
(cd "$DEP"; sha256sum --check SOURCE_MANIFEST.sha256; ./verify.sh)
for module in BernoulliAssignments HistogramGrouping Model GenerativePanels EndpointLaw Verification; do
  "$ROOT/compile.sh" "$module.lean"
done
export PATH="$DEP/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$DEP/mathlib"
export LEAN_PATH="$ROOT:$DEP:$(lake env printenv LEAN_PATH)"
lean --trust=0 -DwarningAsError=true "$ROOT/Verification.lean"

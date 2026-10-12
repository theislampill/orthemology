#!/bin/bash
set -euo pipefail
JRU_CHECK_ROOT=$(cd "$(dirname "$0")" && pwd)
source "$JRU_CHECK_ROOT/env.sh"
for module in JointRecursorCongruence JointRecursorUniqueness JointCanonicalRecursor JointRecursorControls JointRecursorAudit; do
  echo "Checking $module"
  "$JRU_WORK/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$JRU_CHECK_ROOT/validation/$module.olean" "$JRU_CHECK_ROOT/$module.lean"
done

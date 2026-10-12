#!/bin/bash
set -euo pipefail
JIC_CHECK_ROOT=$(cd "$(dirname "$0")" && pwd)
source "$JIC_CHECK_ROOT/env.sh"
for module in JointInductionSupport JointInductionInitiality JointInductionSectionCorollaries JointInductionUniformSection JointInductionComputationLaws JointInductionSectionApplication JointInductionLaws JointInductionControls JointInductionRawBoundary JointInductionAudit; do
  echo "Checking $module"
  "$JIC_WORK/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$JIC_CHECK_ROOT/validation/$module.olean" "$JIC_CHECK_ROOT/$module.lean"
done

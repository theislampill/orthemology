#!/bin/bash
set -euo pipefail
JIC_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
JIC_WORK=$(dirname "$JIC_ROOT")
source "$JIC_WORK/hase-joint-extraction-fidelity-20261010/env.sh"
export LEAN_PATH="$JIC_ROOT/validation:$JIC_WORK/hase-joint-mixed-structure-20261010/validation:$JIC_WORK/hase-induction-positive-consequences-20261010/validation:$JIC_WORK/hase-full-rule-independence-20261010/validation:$JIC_WORK/hase-tagged-full-induction-20261010/validation:$JIC_WORK/hase-induction-rigidity-converse-20261010/validation:$JIC_WORK/hase-completion-principle-separation-20261010/validation:$LEAN_PATH"

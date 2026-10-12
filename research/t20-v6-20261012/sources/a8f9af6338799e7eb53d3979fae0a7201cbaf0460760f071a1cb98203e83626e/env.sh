#!/bin/bash
set -euo pipefail
JRU_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
JRU_WORK=$(dirname "$JRU_ROOT")
source "$JRU_WORK/hase-joint-induction-computation-20261010/env.sh"
export LEAN_PATH="$JRU_ROOT/validation:$LEAN_PATH"

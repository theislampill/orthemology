#!/bin/bash
set -euo pipefail
W=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source "$W/hase-joint-certificate-codec-20261010/env.sh"
export LEAN_PATH="$W/hase-source-family-computability-20261010/validation:$W/hase-fullper-effective-boundary-20261010/validation:$W/hase-bounded-halting-pr-20261010/validation:$LEAN_PATH"

#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
W=$(dirname "$HERE")
source "$W/hase-finite-sidecar-realisation-20261011/env.sh"
export LEAN_PATH="$W/hase-finite-sidecar-independent-review-20261011/fresh-lib:$LEAN_PATH"

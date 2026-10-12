#!/bin/bash
set -euo pipefail
FSC_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FSC_WORK=$(dirname "$FSC_ROOT")
source "$FSC_WORK/hase-joint-recursor-uniqueness-20261010/env.sh"
export LEAN_PATH="$FSC_WORK/hase-joint-proof-uniqueness-20261010/validation:$LEAN_PATH"

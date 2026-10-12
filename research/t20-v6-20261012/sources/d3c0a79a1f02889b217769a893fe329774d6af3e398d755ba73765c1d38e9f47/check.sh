#!/bin/bash
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
W=$(dirname "$HERE")
source "$W/hase-joint-recursor-uniqueness-20261010/env.sh"
OUT=$(mktemp -d "$HERE/validation/fresh-XXXXXX")
export LEAN_PATH="$OUT:$LEAN_PATH"
for m in JointProofUniqueness OriginalProofUniqueness ProofUniquenessControls ProofUniquenessAudit; do
  "$W/.toolchains/lean-4.19.0-linux/bin/lean" --trust=0 -o "$OUT/$m.olean" "$HERE/$m.lean"
done
printf 'Fresh output: %s\n' "$OUT"

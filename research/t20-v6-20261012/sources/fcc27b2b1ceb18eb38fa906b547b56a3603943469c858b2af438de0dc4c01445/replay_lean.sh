#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
REVIEW="$ROOT/tranche20/research-resumption/continuation-independent-review"
AUTHOR="$ROOT/tranche20/research-resumption/testimony-continuation"
TOOLCHAIN="$ROOT/tranche20/hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux"
DEPS="$ROOT/tranche20/hase-positive-research/toolchain-preparation/dependencies"
BUILD="$REVIEW/lean-build"
mkdir -p "$BUILD"
cmp "$ROOT/tranche20/testimony-continuation/grounded-attestation/lean/GroundedSupport.lean" "$AUTHOR/lean/GroundedSupport.lean"
cp "$ROOT/tranche20/testimony-continuation/grounded-attestation/lean/GroundedSupport.lean" "$BUILD/"
cp "$AUTHOR/lean/"*.lean "$BUILD/"
cp "$REVIEW/reviewer-lean/"*.lean "$BUILD/"
export LEAN_PATH="$BUILD:$(find "$DEPS" -path '*/.lake/build/lib/lean' -type d | paste -sd: -)"
cd "$BUILD"
"$TOOLCHAIN/bin/lean" --version
for module in GroundedSupport ContextualEncoding SupportBridge Readback ReviewerControls ReviewerReadback; do
  echo "Compiling ${module}.lean"
  "$TOOLCHAIN/bin/lean" -o "$module.olean" "$module.lean"
done

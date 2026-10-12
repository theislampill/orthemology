#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-"$ROOT/replay"}
mkdir -p "$OUT/logs" "$OUT/build"
export ATTRIBUTION_BUILD="$OUT/build"
for name in DynamicInterlock CoveringCore UnknownRootAttribution; do
  "$ROOT/lean.sh" -j1 -o "$OUT/build/$name.olean" "$ROOT/legacy/$name.lean" > "$OUT/logs/$name.log" 2>&1
done
for name in RootImage Availability FixedFamilies Correspondence ImageMinima MapTransport; do
  "$ROOT/lean.sh" -j1 -o "$OUT/build/$name.olean" "$ROOT/$name.lean" > "$OUT/logs/$name.log" 2>&1
done
for file in "$ROOT"/tests/Target*.lean; do
  "$ROOT/lean.sh" -j1 "$file" > "$OUT/logs/$(basename "$file" .lean).log" 2>&1
done
if grep -En 'sorryAx|warning:|error:' "$OUT"/logs/*.log; then exit 1; fi
if grep -En '\b(sorry|admit|axiom|unsafe|native_decide)\b' "$ROOT"/*.lean; then exit 1; fi
"$ROOT/lean.sh" --version > "$OUT/logs/toolchain.log"
sha256sum private-locator:cb50f30cfa35bdf3a0cf >> "$OUT/logs/toolchain.log"
printf 'All central sources and target tests compiled; no sorryAx, warnings, or errors.\n'

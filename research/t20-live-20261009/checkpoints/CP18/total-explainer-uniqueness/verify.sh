#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
lean=t20-next-frontier-20261008/formal-identification/toolchain/lean-4.19.0-linux/bin/lean
out=total-explainer-uniqueness
"$lean" --version
if grep -nE '\b(sorry|admit|done)\b|^[[:space:]]*axiom[[:space:]]' "$out"/*.lean; then
  echo 'Unfinished or assumed proof detected.' >&2
  exit 1
fi
"$lean" "$out/Uniqueness.lean" | tee "$out/uniqueness-check.log"
"$lean" "$out/FiniteControl.lean" | tee "$out/control-check.log"
sha256sum --check "$out/source-baseline.sha256"
echo 'Both new Lean files passed; the two prior Lean files are unchanged.'

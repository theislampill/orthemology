#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
lean=t20-next-frontier-20261008/formal-identification/toolchain/lean-4.19.0-linux/bin/lean
out=total-explainer-uniqueness
"$lean" --version
if grep -nE '\b(sorry|admit|done)\b|^[[:space:]]*axiom[[:space:]]' "$out/BooleanControl.lean"; then
  echo 'Unfinished or assumed proof detected.' >&2
  exit 1
fi
"$lean" "$out/BooleanControl.lean" | tee "$out/boolean-check.log"
if grep -q 'sorryAx' "$out/boolean-check.log"; then
  echo 'Unfinished-proof dependency detected.' >&2
  exit 1
fi
sha256sum --check "$out/artifact.sha256"
sha256sum --check "$out/source-baseline.sha256"
echo 'Boolean control passed; earlier recorded artifacts are unchanged.'

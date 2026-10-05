#!/usr/bin/env bash
set -euo pipefail
if [[ -z "${TOOLCHAIN_ENV:-}" || ! -r "$TOOLCHAIN_ENV" ]]; then
  printf 'Set TOOLCHAIN_ENV to an explicit readable trusted environment script.\n' >&2
  exit 2
fi
ROOT=$(cd "$(dirname "$0")/.." && pwd)
python3 "$ROOT/scripts/verify-inputs.py"
while IFS= read -r module; do
  "$ROOT/scripts/check-module.sh" "$module" reproduction
 done < "$ROOT/dependency-order.txt"
for module in SubstitutionSyntax SubstitutionAdmissibility SubstitutionControls AdmissibilityContract SubstitutionReadback; do
  "$ROOT/scripts/check-module.sh" "$module" reproduction
 done
SOURCE_DIR="$ROOT/review/sources" "$ROOT/scripts/check-module.sh" IndependentControls reproduction
python3 "$ROOT/scripts/verify-inputs.py"

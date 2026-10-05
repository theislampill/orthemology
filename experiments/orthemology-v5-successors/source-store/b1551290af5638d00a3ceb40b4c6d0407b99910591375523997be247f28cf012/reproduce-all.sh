#!/usr/bin/env bash
set -euo pipefail
: "${TOOLCHAIN_ENV:?Set TOOLCHAIN_ENV to the existing verified environment.sh}"
PACKAGE=$(cd "$(dirname "$0")/.." && pwd)
"$PACKAGE/scripts/verify-sources.py"
while IFS= read -r module; do
  [[ -z "$module" ]] && continue
  "$PACKAGE/scripts/reproduce-module.sh" "$module"
done < "$PACKAGE/dependency-order.txt"

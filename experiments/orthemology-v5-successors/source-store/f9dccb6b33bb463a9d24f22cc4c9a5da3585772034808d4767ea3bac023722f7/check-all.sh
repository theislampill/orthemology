#!/usr/bin/env bash
set -euo pipefail
PACKAGE=$(cd "$(dirname "$0")/.." && pwd)
while IFS= read -r module; do
  [[ -n "$module" ]] || continue
  "$PACKAGE/scripts/check-module.sh" "$module"
done < "$PACKAGE/dependency-order.txt"

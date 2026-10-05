#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
MODULE_SOURCE_DIR="$ROOT/sources" REPRO_LOG_DIR="$ROOT/reproduction/logs" \
  "$ROOT/../scripts/check-module.sh" "${1:?module}"

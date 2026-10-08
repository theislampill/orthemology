#!/usr/bin/env bash
set -u
ROOT=$(cd "$(dirname "$0")/.." && pwd)
if [[ -z "${TOOLCHAIN_ENV:-}" || ! -r "$TOOLCHAIN_ENV" ]]; then
  printf 'Set TOOLCHAIN_ENV to an explicit readable trusted environment script.\n' >&2
  exit 2
fi
source "$TOOLCHAIN_ENV"
export LEAN_PATH="$ROOT/sources:$LEAN_PATH"
name="$1"
phase="${2:-development}"
cd "${SOURCE_DIR:-$ROOT/sources}"
LOG_DIR="$ROOT/reproduction-logs"
mkdir -p "$LOG_DIR"
log="$LOG_DIR/${phase}-${name}.log"
start=$(date -u +%FT%TZ)
sha=$(sha256sum "$name.lean" | cut -d' ' -f1)
timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o "$name.olean" "$name.lean" > "$log" 2>&1
code=$?
end=$(date -u +%FT%TZ)
printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$phase" "$name" "$sha" "$start" "$end" "$code" >> "$LOG_DIR/commands.tsv"
cat "$log"
printf '\nEXIT=%s MODULE=%s PHASE=%s\n' "$code" "$name" "$phase"
exit "$code"

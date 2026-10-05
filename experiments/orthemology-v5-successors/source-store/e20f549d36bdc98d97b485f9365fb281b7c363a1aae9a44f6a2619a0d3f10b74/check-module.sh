#!/usr/bin/env bash
set -uo pipefail
PACKAGE=$(cd "$(dirname "$0")/.." && pwd)
if [[ -z "${TOOLCHAIN_ENV:-}" ]]; then
  printf 'TOOLCHAIN_ENV must explicitly name a readable toolchain environment file.\n' >&2
  exit 90
fi
if [[ ! -f "$TOOLCHAIN_ENV" || ! -r "$TOOLCHAIN_ENV" ]]; then
  printf 'TOOLCHAIN_ENV is not a readable regular file.\n' >&2
  exit 91
fi
mode=$(stat -c '%a' -- "$TOOLCHAIN_ENV") || exit 91
if (( (8#$mode & 8#444) == 0 )); then
  printf 'TOOLCHAIN_ENV has no file read permission.\n' >&2
  exit 91
fi
env_sha=$(sha256sum -- "$TOOLCHAIN_ENV" | cut -d' ' -f1)
source "$TOOLCHAIN_ENV" || exit 93
if [[ -z "${LEAN_ROOT:-}" ]]; then
  printf 'The supplied environment must set LEAN_ROOT.\n' >&2
  exit 94
fi
LEAN_BIN="$LEAN_ROOT/bin/lean"
expected=92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
actual=$(sha256sum -- "$LEAN_BIN" | cut -d' ' -f1) || exit 92
if [[ "$actual" != "$expected" ]]; then
  printf 'Lean binary identity does not match the pinned toolchain.\n' >&2
  exit 92
fi
module=${1:?module}
[[ "$module" =~ ^[A-Za-z_][A-Za-z0-9_]*$ ]] || exit 95
SOURCE_DIR=${MODULE_SOURCE_DIR:-"$PACKAGE/sources"}
LOG_DIR=${REPRO_LOG_DIR:-"$PACKAGE/reproduction/logs"}
export LEAN_PATH="$SOURCE_DIR:$PACKAGE/sources:${LEAN_PATH:-}"
mkdir -p "$LOG_DIR"
stamp=$(date -u +%Y%m%dT%H%M%S%N)
log="$LOG_DIR/${stamp}-${module}.log"
cd "$SOURCE_DIR" || exit 96
source_sha=$(sha256sum -- "$module.lean" | cut -d' ' -f1) || exit 97
printf 'UTC %s\nModule %s\nSource SHA256 %s\nEnvironment SHA256 %s\nInvoked Lean SHA256 %s\nCommand: timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o %s.olean %s.lean\n' \
  "$stamp" "$module" "$source_sha" "$env_sha" "$actual" "$module" "$module" > "$log"
timeout 180 "$LEAN_BIN" -j1 -o "$module.olean" "$module.lean" >> "$log" 2>&1
rc=$?
printf '\nEXIT %s\n' "$rc" >> "$log"
cat "$log"
exit "$rc"

#!/usr/bin/env bash
set -euo pipefail
: "${TOOLCHAIN_ENV:?Set TOOLCHAIN_ENV to the existing independently verified toolchain environment}"
[[ -f "$TOOLCHAIN_ENV" && -r "$TOOLCHAIN_ENV" ]] || { printf '%s\n' 'TOOLCHAIN_ENV must be a readable regular file.' >&2; exit 66; }
# Deliberately not in an || or if condition: errexit must remain active while sourcing.
source "$TOOLCHAIN_ENV"
: "${LEAN_ROOT:?The environment must export LEAN_ROOT}"
: "${LEAN_PATH:?The environment must export the pinned dependency LEAN_PATH}"
PACKAGE=$(cd "$(dirname "$0")/../.." && pwd)
expected=92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
[[ -x "$LEAN_ROOT/bin/lean" ]] || exit 68
[[ $(sha256sum "$LEAN_ROOT/bin/lean" | cut -d' ' -f1) = "$expected" ]] || exit 92
module=${1:?module}
case "$module" in ''|*[!A-Za-z0-9_]*) exit 64;; esac
[[ -f "$PACKAGE/sources/$module.lean" && -r "$PACKAGE/sources/$module.lean" ]] || exit 65
export LEAN_PATH="$PACKAGE/sources:$LEAN_PATH"
mkdir -p "$PACKAGE/reproduction-logs"
run=$(mktemp -d "$PACKAGE/reproduction-logs/$(date -u +%Y%m%dT%H%M%S)-${module}-XXXXXX")
log="$run/command.log"
cd "$PACKAGE/sources"
printf 'PORTABLE REPRODUCTION; separate from frozen acceptance evidence\nCommand: timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o %s.olean %s.lean\n' "$module" "$module" > "$log"
sha256sum "$module.lean" >> "$log"
cp "$module.lean" "$run/source.lean"
if timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o "$module.olean" "$module.lean" >> "$log" 2>&1; then rc=0; else rc=$?; fi
printf '\nEXIT=%s\n' "$rc" >> "$log"
cat "$log"
exit "$rc"

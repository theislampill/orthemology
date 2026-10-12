#!/usr/bin/env bash
set -uo pipefail
: "${TOOLCHAIN_ENV:?Set TOOLCHAIN_ENV to the existing verified environment.sh}"
source "$TOOLCHAIN_ENV"
PACKAGE=$(cd "$(dirname "$0")/.." && pwd)
expected=92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
[[ $(sha256sum "$LEAN_ROOT/bin/lean" | cut -d' ' -f1) = "$expected" ]] || exit 92
export LEAN_PATH="$PACKAGE/sources:$LEAN_PATH"
module=${1:?module}; stamp=$(date -u +%Y%m%dT%H%M%S%N)
log="$PACKAGE/logs/${stamp}-${module}.log"
cd "$PACKAGE/sources"
printf 'START %s\nCommand: timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o %s.olean %s.lean\n' "$(date -u --iso-8601=seconds)" "$module" "$module" > "$log"
sha256sum "$module.lean" >> "$log"
source_hash=$(sha256sum "$module.lean" | cut -d' ' -f1)
mkdir -p "$PACKAGE/logs/source-snapshots"
if [[ ! -e "$PACKAGE/logs/source-snapshots/${source_hash}.lean" ]]; then
  cp "$module.lean" "$PACKAGE/logs/source-snapshots/${source_hash}.lean"
fi
timeout 180 "$LEAN_ROOT/bin/lean" -j1 -o "$module.olean" "$module.lean" >> "$log" 2>&1
rc=$?
printf '\nEND %s\nEXIT %s\n' "$(date -u --iso-8601=seconds)" "$rc" >> "$log"
cat "$log"; exit "$rc"

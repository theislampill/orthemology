#!/usr/bin/env bash
# Narrow scope-review protocol, never a primary mutation-suite success.
# Usage: bash run-scope-review.sh TOOLCHAIN_BIN MATHLIB_ROOT NEW_OUTPUT_DIRECTORY
set -euo pipefail
fail() { printf '%s\n' "ERROR: $*" >&2; exit 1; }
[[ $# == 3 ]] || fail 'expected toolchain directory, Mathlib root, and fresh output directory'
SOURCE_ROOT=$(cd -- "$(dirname -- "$0")" && pwd -P)
for ARG in "$@"; do
  [[ "$ARG" == /* && "$ARG" != *:* && "$ARG" != *$'\n'* ]] || fail 'roots must be absolute paths without colon or newline'
done
[[ "$SOURCE_ROOT" != *:* && "$SOURCE_ROOT" != *$'\n'* ]] || fail 'source root cannot contain colon or newline'
TOOLCHAIN_BIN=$(cd -- "$1" && pwd -P)
MATHLIB_ROOT=$(cd -- "$2" && pwd -P)
[[ -f "$TOOLCHAIN_BIN/lean" && -x "$TOOLCHAIN_BIN/lean" && -f "$TOOLCHAIN_BIN/lake" && -x "$TOOLCHAIN_BIN/lake" ]] || fail 'explicit lean and lake executables are required'
[[ ! -e "$3" && ! -L "$3" ]] || fail 'output must not already exist'
OUTPUT_PARENT=$(cd -- "$(dirname -- "$3")" && pwd -P)
OUTPUT_ROOT="$OUTPUT_PARENT/$(basename -- "$3")"
for ROOT in "$SOURCE_ROOT" "$TOOLCHAIN_BIN" "$MATHLIB_ROOT"; do
  [[ "$OUTPUT_ROOT" != "$ROOT" && "$OUTPUT_ROOT" != "$ROOT/"* ]] || fail 'output must be outside source, toolchain, and Mathlib roots'
done
for FILE in CertificateFrontier.lean ScopeChecks.lean; do
  [[ -f "$SOURCE_ROOT/$FILE" && ! -L "$SOURCE_ROOT/$FILE" ]] || fail "missing or non-ordinary source: $FILE"
done
# Optional in this historical protocol only; the received six-source owner
# still requires the stored Controls provider. A malformed present path fails.
if [[ -e "$SOURCE_ROOT/Controls.lean" || -L "$SOURCE_ROOT/Controls.lean" ]]; then
  [[ -f "$SOURCE_ROOT/Controls.lean" && ! -L "$SOURCE_ROOT/Controls.lean" ]] || fail 'non-ordinary optional Controls source'
fi
export PATH="$TOOLCHAIN_BIN:$PATH"
unset LEAN_PATH
cd -- "$MATHLIB_ROOT"
VERSION=$("$TOOLCHAIN_BIN/lean" --version)
case "$VERSION" in
  'Lean (version 4.19.0,'*|'Lean (version 4.19.0)'*) ;;
  *) fail 'this source edition names Lean 4.19.0; exact environment still needs separate qualification' ;;
esac
printf '%s\n' "$VERSION"
DEPS=$("$TOOLCHAIN_BIN/lake" env printenv LEAN_PATH)
[[ -n "$DEPS" && "$DEPS" != *$'\n'* ]] || fail 'explicit Mathlib environment returned no usable dependency path'
mkdir -- "$OUTPUT_ROOT"
export LEAN_PATH="$OUTPUT_ROOT:$DEPS"
"$TOOLCHAIN_BIN/lean" -t0 -DwarningAsError=true --root="$SOURCE_ROOT" -o "$OUTPUT_ROOT/CertificateFrontier.olean" "$SOURCE_ROOT/CertificateFrontier.lean"
[[ -f "$OUTPUT_ROOT/CertificateFrontier.olean" && ! -L "$OUTPUT_ROOT/CertificateFrontier.olean" ]] || fail 'compiler did not produce the fresh CertificateFrontier object'
"$TOOLCHAIN_BIN/lean" -t0 -DwarningAsError=true --root="$SOURCE_ROOT" -o "$OUTPUT_ROOT/ScopeChecks.olean" "$SOURCE_ROOT/ScopeChecks.lean"
[[ -f "$OUTPUT_ROOT/ScopeChecks.olean" && ! -L "$OUTPUT_ROOT/ScopeChecks.olean" ]] || fail 'compiler did not produce the fresh ScopeChecks object'
if [[ -f "$SOURCE_ROOT/Controls.lean" ]]; then
  "$TOOLCHAIN_BIN/lean" -t0 -DwarningAsError=true --root="$SOURCE_ROOT" -o "$OUTPUT_ROOT/Controls.olean" "$SOURCE_ROOT/Controls.lean"
  [[ -f "$OUTPUT_ROOT/Controls.olean" && ! -L "$OUTPUT_ROOT/Controls.olean" ]] || fail 'compiler did not produce the fresh Controls object'
fi

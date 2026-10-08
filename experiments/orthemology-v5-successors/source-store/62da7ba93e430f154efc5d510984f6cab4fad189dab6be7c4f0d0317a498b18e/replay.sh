#!/usr/bin/env bash
set -euo pipefail
HERE="$(dirname "$(realpath -- "$0")")"
if (( $# > 1 )); then
  echo 'Usage: replay.sh [fresh-output-directory]' >&2
  exit 64
fi
REQUESTED_OUT="${1:-$HERE/../modal-union-replay-v2}"
OUT="$(realpath -m -- "$REQUESTED_OUT")"
# Validate both guards before creating directories, logs or temporary builds.
case "$OUT" in
  "$HERE"|"$HERE"/*)
    echo 'Refusing output equal to or inside the sealed input tree' >&2
    exit 64
    ;;
esac
if [[ -e "$REQUESTED_OUT" || -L "$REQUESTED_OUT" || -e "$OUT" || -L "$OUT" ]]; then
  echo 'Refusing an existing output path; select a fresh directory' >&2
  exit 73
fi
if [[ ! -d "$(dirname "$OUT")" ]]; then
  echo 'The fresh output directory must have an existing parent' >&2
  exit 73
fi
LEAN_BIN="$(realpath "$(command -v "${LEAN_BIN:-lean}")")"
# Atomic creation also refuses a destination created after the initial check.
mkdir -- "$OUT"
cd "$HERE"
BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT
export LEAN_PATH="$BUILD"
"$LEAN_BIN" --version | tee "$OUT/toolchain.txt"
grep -q 'version 4.19.0,' "$OUT/toolchain.txt"
"$LEAN_BIN" --trust=0 -o "$BUILD/ModalUnion.olean" "$HERE/ModalUnion.lean" > "$OUT/core.log" 2>&1
"$LEAN_BIN" --trust=0 -o "$BUILD/FiniteControls.olean" "$HERE/FiniteControls.lean" > "$OUT/finite.log" 2>&1
"$LEAN_BIN" --trust=0 -o "$BUILD/AxiomAudit.olean" "$HERE/AxiomAudit.lean" > "$OUT/axioms.log" 2>&1
if grep -Eq 'sorryAx|Lean.ofReduceBool' "$OUT/axioms.log"; then
  echo 'Rejected non-kernel/admission dependency in axiom audit' >&2
  exit 1
fi
if grep -nE '(^|[[:space:]])(sorry|admit)([[:space:]]|$)|^[[:space:]]*axiom[[:space:]]' \
  "$HERE/ModalUnion.lean" "$HERE/FiniteControls.lean" "$HERE/AxiomAudit.lean"; then
  echo 'Rejected admitted goal or declared axiom in authored modules' >&2
  exit 1
fi
set +e
"$LEAN_BIN" --trust=0 "$HERE/negative-controls/RejectedClaims.lean" > "$OUT/rejected.log" 2>&1
NEGATIVE_EXIT=$?
set -e
test "$NEGATIVE_EXIT" -ne 0
test "$(grep -c "tactic 'decide' proved that the proposition" "$OUT/rejected.log")" -eq 3
test "$(grep -c 'error:' "$OUT/rejected.log")" -eq 3
(
  cd "$HERE"
  sha256sum ModalUnion.lean FiniteControls.lean AxiomAudit.lean \
    negative-controls/RejectedClaims.lean replay.sh test_harness.py
) > "$OUT/SHA256SUMS"
printf '%s\n' 'PASS: three green modules; all authored theorem axioms printed; three false finite claims rejected.' | tee "$OUT/RESULT.txt"

#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=$(dirname "$HERE")
FORMAL="$BASE/formal-identification"
export PATH="$FORMAL/toolchain/lean-4.19.0-linux/bin:$PATH"
OUT=${1:-"$HERE/kernel-replay"}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
cp "$HERE/RetainedInterior.lean" "$OUT/RetainedInterior.lean"
cd "$FORMAL/mathlib"
lake env lean -t 0 -DwarningAsError=true --root="$OUT" \
  -o "$OUT/RetainedInterior.olean" "$OUT/RetainedInterior.lean" \
  >"$OUT/TRUST_ZERO.log" 2>&1
if grep -Eq 'sorryAx|error:|warning:' "$OUT/TRUST_ZERO.log"; then
  cat "$OUT/TRUST_ZERO.log"; exit 1
fi
python - "$HERE" "$OUT" <<'PY'
from pathlib import Path
import sys
src=Path(sys.argv[1],'RetainedInterior.lean').read_text();out=Path(sys.argv[2])
assert 'sorry' not in src and '\naxiom ' not in src
# A genuinely false weakened statement: connector hits replace connector misses.
bad=src.replace('¬ Hit GA GB (a i) (b (i + 1))','Hit GA GB (a i) (b (i + 1))')
assert bad != src
(out/'FalseConnectorPremise.lean').write_text(bad)
# A false stronger conclusion: one positive hit need not witness two routes.
bad=src.replace('m ≤ Fintype.card R','m + 1 ≤ Fintype.card R')
assert bad != src
(out/'FalseCountBound.lean').write_text(bad)
PY
for NAME in FalseConnectorPremise FalseCountBound; do
  if lake env lean -t 0 -DwarningAsError=true "$OUT/$NAME.lean" >"$OUT/$NAME.log" 2>&1; then
    echo "ERROR: falsified control $NAME was accepted"; exit 1
  fi
  grep -q 'error:' "$OUT/$NAME.log"
done
lean --version >"$OUT/LEAN_VERSION.txt"
echo "PASS: isolated trust-zero replay, axiom report, and two rejected falsified controls"

#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "$0")" && pwd)
BASE=$(dirname "$HERE")/t20-next-frontier-20261008/formal-identification
export PATH="$BASE/toolchain/lean-4.19.0-linux/bin:$PATH"
OUT=${1:-"$HERE/verified"}
mkdir -p "$OUT"
OUT=$(cd "$OUT" && pwd)
cp "$HERE/GraphContinuation.lean" "$OUT/GraphContinuation.lean"
cd "$BASE/mathlib"
lake env lean -t 0 -DwarningAsError=true --root="$OUT" \
  -o "$OUT/GraphContinuation.olean" "$OUT/GraphContinuation.lean" \
  > "$OUT/KERNEL.log" 2>&1
if grep -Eq 'sorryAx|error:|warning:' "$OUT/KERNEL.log"; then cat "$OUT/KERNEL.log"; exit 1; fi
python - "$HERE" "$OUT" <<'PY'
from pathlib import Path
import re, sys
here, out = map(Path, sys.argv[1:])
s = (here/'GraphContinuation.lean').read_text()
assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', s)
a = s.replace('n + S.card + 1 = 2 * t ∧', 'n + S.card + 1 = t ∧')
b = s.replace('character (if i ∈ S then toggle S j else S) x := by', 'character S x := by')
assert a != s and b != s
(out/'FalseSteinerCost.lean').write_text(a)
(out/'FalsePreservation.lean').write_text(b)
PY
for bad in FalseSteinerCost FalsePreservation; do
  if lake env lean -t 0 -DwarningAsError=true "$OUT/$bad.lean" > "$OUT/$bad.log" 2>&1; then
    echo "FAIL: false claim $bad accepted"; exit 1
  fi
  grep -q 'error:' "$OUT/$bad.log"
done
lean --version > "$OUT/LEAN_VERSION.txt"
python "$HERE/controls.py" > "$OUT/CONTROLS.log"
echo 'PASS: fresh kernel replay, axiom readback, two rejected false claims, exact state-table controls'

#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
export PATH="$ROOT/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$ROOT/mathlib"
python - "$ROOT" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
s = (p / 'Calibration.lean').read_text()
assert s.count('(5 / 6 : ℚ) ^ c') == 1
(p / 'results' / 'CalibrationMutation.lean').write_text(s.replace('(5 / 6 : ℚ) ^ c', '(1 / 6 : ℚ) ^ c'))
s = (p / 'HitTransform.lean').read_text()
old = '∑ T : Finset E, if (T ∩ U).Nonempty then n T else 0'
assert s.count(old) == 1
(p / 'results' / 'HitMutation.lean').write_text(s.replace(old, '∑ T : Finset E, if T.Nonempty then n T else 0'))
PY
for name in Calibration Hit; do
  set +e
  lake env lean "$ROOT/results/${name}Mutation.lean" >"$ROOT/results/${name}-mutation-rejected.log" 2>&1
  code=$?
  set -e
  if [[ $code -eq 0 ]]; then
    echo "ERROR: $name mutation was unexpectedly accepted"
    exit 1
  fi
  grep -q 'error:' "$ROOT/results/${name}-mutation-rejected.log"
  echo "$name mutation rejected by Lean (exit $code)"
done
rm "$ROOT/results/CalibrationMutation.lean" "$ROOT/results/HitMutation.lean"

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ROOT="$PWD"
export PATH="${LEAN_BIN:-$ROOT/../.toolchains/lean-4.19.0-linux/bin}:$PATH"
export XDG_CACHE_HOME="$ROOT/.cache"
mkdir -p logs .lake/build/lib/lean
lean --version | tee logs/toolchain.log
printf 'Fresh verification start: ' | tee logs/verification-time.log
date -u +%FT%TZ | tee -a logs/verification-time.log
if grep -En '\b(sorry|admit|axiom|native_decide|unsafe|partial)\b' \
    MomentRecovery.lean Counterexample.lean Checks.lean; then
  echo 'Forbidden proof escape or added axiom token detected.' >&2
  exit 1
fi
lake build MomentRecovery Counterexample Checks Verify 2>&1 | tee logs/build.log
for module in MomentRecovery Counterexample Checks Verify; do
  # Direct Lean invocation always re-elaborates and kernel-checks this source.
  lake env lean -o ".lake/build/lib/lean/$module.olean" "$module.lean" \
    2>&1 | tee "logs/fresh-$module.log"
done
python3 - <<'PY'
import re
from pathlib import Path
text = Path('logs/fresh-Verify.log').read_text()
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
rows = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)
expected = re.findall(r'^#print axioms (\S+)', Path('Verify.lean').read_text(), re.M)
assert len(rows) == len(expected), 'Missing or repeated foundation audit rows'
assert {name for name, _ in rows} == set(expected), 'Foundation audit names mismatch'
for name, axioms in rows:
    found = {x.strip() for x in axioms.split(',') if x.strip()}
    assert found <= allowed, (name, found - allowed)
assert 'sorryAx' not in text
print(f'Foundation audit passed for all {len(rows)} expected declarations; only standard axioms allowed.')
PY
for control in RejectFalseCubic RejectMissingDistinctness; do
  if lake env lean "controls/$control.lean" > "logs/control-$control.log" 2>&1; then
    echo "Expected rejection unexpectedly accepted: $control" >&2
    exit 1
  fi
  grep -q 'error:' "logs/control-$control.log"
  echo "Expected rejection confirmed: $control"
done
printf 'Fresh verification end: ' | tee -a logs/verification-time.log
date -u +%FT%TZ | tee -a logs/verification-time.log

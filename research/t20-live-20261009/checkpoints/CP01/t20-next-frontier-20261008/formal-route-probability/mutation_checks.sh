#!/usr/bin/env bash
# Original/mutated/restored same-module checks in a disposable copy.
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
DEP="$ROOT/../formal-identification"
CONTROL=$(mktemp -d "$ROOT/results/mutation-workspace.XXXXXX")
trap 'rm -rf "$CONTROL"' EXIT
cp "$ROOT"/*.lean "$CONTROL/"
export PATH="$DEP/toolchain/lean-4.19.0-linux/bin:$PATH"
cd "$DEP/mathlib"
export LEAN_PATH="$CONTROL:$DEP:$(lake env printenv LEAN_PATH)"
compile() { lean -DwarningAsError=true --root="$CONTROL" -o "$CONTROL/$1.olean" "$CONTROL/$1.lean"; }
for name in BernoulliAssignments HistogramGrouping Model GenerativePanels; do
  compile "$name" >"$ROOT/results/mutation-original-$name.log" 2>&1
done
echo 'All original modules accepted (exit 0)'
python - "$CONTROL/Model.lean" <<'PY'
import sys,pathlib
p=pathlib.Path(sys.argv[1]);s=p.read_text()
old='if enabled S (M.kind r) ∧ ω r = true then M.outputs r else ∅'
assert s.count(old)==1
p.write_text(s.replace(old,'if enabled S (M.kind r) ∧ ω r = false then M.outputs r else ∅'))
PY
set +e
compile Model >"$ROOT/results/endpoint-gate-mutation.log" 2>&1
code=$?
set -e
[[ $code -ne 0 ]]
grep -Eq 'error: (unsolved goals|type mismatch|tactic|simp made no progress)' "$ROOT/results/endpoint-gate-mutation.log"
! grep -q 'unknown module\|unknown package\|no such file\|must be contained' "$ROOT/results/endpoint-gate-mutation.log"
echo "Endpoint-success gate reversal rejected (exit $code)"
cp "$ROOT/Model.lean" "$CONTROL/Model.lean"
compile Model >"$ROOT/results/endpoint-gate-restored.log" 2>&1
echo 'Restored endpoint model accepted (exit 0)'
python - "$CONTROL/Model.lean" <<'PY'
import sys,pathlib
p=pathlib.Path(sys.argv[1]);s=p.read_text()
assert s.count('| .c => 5 / 6')==1
p.write_text(s.replace('| .c => 5 / 6','| .c => 2 / 3'))
PY
compile Model >"$ROOT/results/calibration-mutant-model.log" 2>&1
set +e
compile GenerativePanels >"$ROOT/results/calibration-forward-mutation.log" 2>&1
code=$?
set -e
[[ $code -ne 0 ]]
grep -q 'error:' "$ROOT/results/calibration-forward-mutation.log"
! grep -q 'unknown module\|unknown package\|no such file\|must be contained' "$ROOT/results/calibration-forward-mutation.log"
echo "Altered AB-support calibration rejected by forward panel proof (exit $code)"
cp "$ROOT/Model.lean" "$CONTROL/Model.lean"
compile Model >"$ROOT/results/calibration-restored-model.log" 2>&1
compile GenerativePanels >"$ROOT/results/calibration-restored-panels.log" 2>&1
echo 'Restored model and panel derivation accepted (exit 0)'

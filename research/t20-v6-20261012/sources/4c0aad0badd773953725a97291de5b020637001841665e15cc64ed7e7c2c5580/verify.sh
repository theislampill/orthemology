#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")" && pwd)
OUT=${1:-"$ROOT/replay-author"}
mkdir -p "$OUT/build" "$OUT/logs" "$OUT/controls"
OUT=$(cd "$OUT" && pwd)
export INTERLOCK_BUILD="$OUT/build"
python "$ROOT/hash_candidate.py" > "$OUT/logs/candidate-before.json"
"$ROOT/lean.sh" --version > "$OUT/logs/toolchain.log"
grep -F 'version 4.19.0' "$OUT/logs/toolchain.log"
sha256sum private-locator:cb50f30cfa35bdf3a0cf >> "$OUT/logs/toolchain.log"
python "$ROOT/check_binding.py" > "$OUT/logs/source-binding-before.log"
for name in HistoryModel HistoryInvariant HistorySafety HistoryTrace NegativeControls; do
  "$ROOT/lean.sh" -j1 -o "$OUT/build/$name.olean" "$ROOT/$name.lean" > "$OUT/logs/$name.log" 2>&1
done
for name in Targets MultiEpoch; do
  "$ROOT/lean.sh" -j1 "$ROOT/tests/$name.lean" > "$OUT/logs/$name.log" 2>&1
done
if grep -En 'sorryAx|warning:|error:' "$OUT"/logs/History*.log "$OUT/logs/NegativeControls.log" "$OUT/logs/Targets.log" "$OUT/logs/MultiEpoch.log"; then exit 1; fi
if grep -En '\b(sorry|admit|axiom|unsafe|native_decide)\b' "$ROOT"/*.lean "$ROOT"/tests/*.lean; then exit 1; fi
python "$ROOT/check_controls.py" "$OUT/controls" > "$OUT/logs/controls.log"
python "$ROOT/source_replay.py" > "$OUT/logs/source-replay.json"
python "$ROOT/check_binding.py" > "$OUT/logs/source-binding-after.log"
python "$ROOT/hash_candidate.py" > "$OUT/logs/candidate-after.json"
cmp "$OUT/logs/candidate-before.json" "$OUT/logs/candidate-after.json"
printf 'PASS: all five modules plus two target fixtures compiled; seven false-claim controls rejected; seven accepted-source scenarios passed; candidate and frozen inputs unchanged.\n'

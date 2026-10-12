#!/usr/bin/env bash
# NOT EXECUTED HERE. A future authorised, isolated verification attempt only.
set -euo pipefail
if [[ $# != 2 ]]; then
  echo "usage: $0 EXTRACTED_CHECKPOINT ABSENT_SCRATCH_DIRECTORY" >&2; exit 64
fi
ROOT=$(cd "$1" && pwd)
SCRATCH=$2
[[ ! -e "$SCRATCH" ]] || { echo 'Scratch path already exists; refusing reuse' >&2; exit 65; }
command -v elan >/dev/null || { echo 'Elan missing; obtain an authorised toolchain environment first' >&2; exit 66; }
command -v python3 >/dev/null
T='leanprover/lean4:v4.19.0'
PIN='c44e0c8ee63ca166450922a373c7409c5d26b00b'
# Verify proposal bytes before copying them into a new project.
python3 - "$ROOT" <<'PY'
import hashlib,json,pathlib,sys
root=pathlib.Path(sys.argv[1])
for x in json.loads((root/'provenance/PROPOSAL_IDENTITIES.json').read_text())['files']:
    p=root/x['path'];b=p.read_bytes()
    if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:
        raise SystemExit('Proposal identity mismatch: '+x['path'])
print('Proposal byte identities matched; no theorem credit follows.')
PY
mkdir -p "$SCRATCH"
SCRATCH=$(cd "$SCRATCH" && pwd)
SEQ=0
run() {
  SEQ=$((SEQ+1))
  local log="$SCRATCH/command-$(printf '%03d' "$SEQ")"
  mkdir "$log"
  printf '%q ' "$@" > "$log/command.txt"; printf '\n' >> "$log/command.txt"
  pwd > "$log/cwd.txt"; date -u +%FT%TZ > "$log/start.txt"
  set +e
  "$@" > "$log/stdout.bin" 2> "$log/stderr.bin"
  local rc=$?
  set -e
  printf '%s\n' "$rc" > "$log/exit.txt"; date -u +%FT%TZ > "$log/end.txt"
  cat "$log/stdout.bin"; cat "$log/stderr.bin" >&2
  return "$rc"
}
run elan toolchain install "$T"
run elan run "$T" lean --version
run elan run "$T" lake --version
elan run "$T" lean --version | grep -F '4.19.0' >/dev/null
elan run "$T" lean --version | grep -F '6caaee842e94' >/dev/null
elan run "$T" lake --version | grep -F '5.0.0-6caaee8' >/dev/null
LEAN_BIN=$(elan which --toolchain "$T" lean)
LAKE_BIN=$(elan which --toolchain "$T" lake)
run sha256sum "$LEAN_BIN" "$LAKE_BIN"
for trial in a b; do
  PROJECT="$SCRATCH/project-$trial"
  mkdir "$PROJECT"
  cp -R "$ROOT/proposals/lean/." "$PROJECT/"
  cd "$PROJECT"
  [[ $(cat lean-toolchain) == "$T" ]]
  run elan run "$T" lake update
  [[ $(git -C .lake/packages/mathlib rev-parse HEAD) == "$PIN" ]]
  [[ $(cat .lake/packages/mathlib/lean-toolchain) == "$T" ]]
  run git -C .lake/packages/mathlib rev-parse HEAD
  run elan run "$T" lake exe cache get
  # This is a fresh project. Dependency cache is pinned; own target artifacts must not pre-exist.
  [[ ! -e .lake/build/lib/lean/P02.olean ]]
  [[ ! -e .lake/build/lib/lean/P02/MeasureCore.olean ]]
  [[ ! -e .lake/build/lib/lean/P02/T300ThreeBit.olean ]]
  run elan run "$T" lake build P02
  for f in .lake/build/lib/lean/P02.olean .lake/build/lib/lean/P02/MeasureCore.olean .lake/build/lib/lean/P02/T300ThreeBit.olean; do
    [[ -s "$f" ]] || { echo "Missing or empty artifact: $f" >&2; exit 67; }
  done
  mkdir audit
  # Keep both command-record streams and convenient exact copies of the readback output.
  run elan run "$T" lake env lean -o audit/Readbacks.olean Readbacks.lean
  LAST="$SCRATCH/command-$(printf '%03d' "$SEQ")"
  cp "$LAST/stdout.bin" audit/Readbacks.stdout.bin
  cp "$LAST/stderr.bin" audit/Readbacks.stderr.bin
  [[ -s audit/Readbacks.olean && -s audit/Readbacks.stdout.bin ]]
  if grep -E 'sorryAx|error:|unknown constant|declaration uses .sorry.' audit/Readbacks.*.bin; then
    echo 'Forbidden or failed formal readback' >&2; exit 68
  fi
  run sha256sum .lake/build/lib/lean/P02.olean .lake/build/lib/lean/P02/MeasureCore.olean .lake/build/lib/lean/P02/T300ThreeBit.olean audit/Readbacks.olean
  python3 - <<'PY'
import hashlib,json,pathlib
root=pathlib.Path('.')
paths=list(root.glob('*.lean'))+list(root.glob('P02/*.lean'))+[root/'lean-toolchain',root/'lake-manifest.json']
rows=[{'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(paths)]
(root/'audit/INPUT_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n')
PY
  cd "$SCRATCH"
done
run cmp "$SCRATCH/project-a/audit/Readbacks.stdout.bin" "$SCRATCH/project-b/audit/Readbacks.stdout.bin"
printf '%s\n' 'BUILD_OBSERVED_PENDING_TYPE_AXIOM_REVIEW' > "$SCRATCH/STATUS.txt"
printf '%s\n' 'No theorem/obligation PASS: inspect all 11 exact types, axiom ceilings, source maps and anti-spoofing controls before granting scoped credit.'

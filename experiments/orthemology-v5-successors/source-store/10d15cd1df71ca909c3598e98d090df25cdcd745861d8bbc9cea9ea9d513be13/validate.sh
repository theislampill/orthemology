#!/usr/bin/env bash
set -euo pipefail
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$HERE/../../../.." && pwd)
source "$ROOT/toolchain-restored/environment.sh"
export LEAN_PATH="$HERE/src:$LEAN_PATH"
cd "$HERE"
RUN="${1:-validation-$(date -u +%Y%m%dT%H%M%SZ)}"
mkdir -p "logs/$RUN"
TIMEFORMAT='elapsed_seconds=%3R'
printf 'UTC %s\n' "$(date -u +%FT%TZ)" > "logs/$RUN/environment.txt"
lean --version >> "logs/$RUN/environment.txt"
printf 'LEAN_ROOT=%s\nMATHLIB_ROOT=%s\nLEAN_PATH=%s\n' "$LEAN_ROOT" "$MATHLIB_ROOT" "$LEAN_PATH" >> "logs/$RUN/environment.txt"
sha256sum "$ROOT/toolchain-restored/environment.sh" "$LEAN_ROOT/bin/lean" "$MATHLIB_ROOT/Mathlib.lean" "$MATHLIB_ROOT/lean-toolchain" "$MATHLIB_ROOT/lake-manifest.json" >> "logs/$RUN/environment.txt"
for MODULE in IndexedCompletionCore IndexedCompletionCompact IndexedCompletionForgetting IndexedCompletionDiameter; do
  printf 'timeout 180 lean -j1 -o src/%s.olean src/%s.lean\n' "$MODULE" "$MODULE" > "logs/$RUN/$MODULE.log"
  if { time timeout 180 lean -j1 -o "src/$MODULE.olean" "src/$MODULE.lean"; } >> "logs/$RUN/$MODULE.log" 2>&1; then
    echo 'exit=0' >> "logs/$RUN/$MODULE.log"
  else
    STATUS=$?; echo "exit=$STATUS" >> "logs/$RUN/$MODULE.log"; cat "logs/$RUN/$MODULE.log"; exit "$STATUS"
  fi
done
if { time timeout 180 lean -j1 readbacks/IndexedCompletionReadback.lean; } > "logs/$RUN/Readback.log" 2>&1; then
  echo 'exit=0' >> "logs/$RUN/Readback.log"
else
  STATUS=$?; echo "exit=$STATUS" >> "logs/$RUN/Readback.log"; cat "logs/$RUN/Readback.log"; exit "$STATUS"
fi
python3 - "$RUN" <<'PY'
import hashlib,json,pathlib,re,sys
base=pathlib.Path('.')
run=sys.argv[1]
files=sorted((base/'src').glob('*.lean'))+sorted((base/'readbacks').glob('*.lean'))
violations=[]
for p in files:
    text=p.read_text()
    if re.search(r'\b(sorry|admit|axiom)\b',text): violations.append(str(p))
    if re.search(r'set_option\s+(maxHeartbeats|maxRecDepth)',text): violations.append(str(p))
if violations: raise SystemExit('Forbidden declaration/option scan: '+repr(violations))
readback=(base/'logs'/run/'Readback.log').read_text()
found=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",readback,re.S)
allowed={'propext','Classical.choice','Quot.sound'}
for name,axs in found:
    unexpected=set(x.strip() for x in axs.split(',') if x.strip())-allowed
    if unexpected: raise SystemExit(f'{name}: unexpected axioms {unexpected}')
no_axioms=re.findall(r"'([^']+)' does not depend on any axioms",readback)
expected=len(re.findall(r'^#print axioms ',(base/'readbacks'/'IndexedCompletionReadback.lean').read_text(),re.M))
if len(found)+len(no_axioms)!=expected:
    raise SystemExit(f'Incomplete axiom readback {len(found)+len(no_axioms)} != {expected}')
report={'status':'PASS','expected_axiom_readbacks':expected,'readbacks_with_standard_axioms':len(found),'readbacks_without_axioms':len(no_axioms),'allowed_axioms':sorted(allowed),'module_wall_cap_seconds':180,'compiler_threads':1,'heartbeats':'default','files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files]}
(base/'logs'/run/'VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
PY

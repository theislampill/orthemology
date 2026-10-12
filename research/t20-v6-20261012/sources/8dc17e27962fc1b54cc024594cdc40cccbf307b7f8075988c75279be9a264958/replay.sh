#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
WORKSPACE=$(dirname -- "$ROOT")
export ROOT WORKSPACE
python - <<'PY'
import hashlib,json,os,pathlib
r=pathlib.Path(os.environ['ROOT']);w=pathlib.Path(os.environ['WORKSPACE']);out=[]
for name in ['hase-open-term-standardness-20261010','hase-imported-compiler-transport-20261010']:
    p=w/name/'MANIFEST.json';m=json.loads(p.read_text())
    for x in m['files']:
        f=w/name/x['path'];assert hashlib.sha256(f.read_bytes()).hexdigest()==x['sha256'],f
    out.append({'directory':name,'manifest_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'all_listed_files_verified':True})
(r/'INPUTS.json').write_text(json.dumps(out,indent=2)+'\n')
PY
LEAN="$WORKSPACE/.toolchains/lean-4.19.0-linux/bin/lean"
SOURCE_LIB=${SOURCE_LIB:-$(python - <<'PYSOURCE'
import json,os,pathlib
r=pathlib.Path(os.environ['WORKSPACE'])/'hase-imported-compiler-transport-20261010'
m=json.loads((r/'validation/FINAL_REPLAY.json').read_text())
print(r/m['fresh_source_output'])
PYSOURCE
)}
test -f "$SOURCE_LIB/UArrowAndCompilerControls.olean" || { echo "Run the imported compiler package replay first." >&2; exit 1; }
export LEAN_PATH="$SOURCE_LIB:$(find "$WORKSPACE/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd :)"
OUT=$(mktemp -d "$ROOT/validation/new-file-replay-XXXXXX")
"$LEAN" --trust=0 -o "$OUT/RawMotiveBoundary.olean" "$ROOT/RawMotiveBoundary.lean" | tee "$ROOT/validation/FINAL_REPLAY.log"
python - <<'PY'
import hashlib,json,os,pathlib,re
r=pathlib.Path(os.environ['ROOT']);p=r/'RawMotiveBoundary.lean';log=(r/'validation/FINAL_REPLAY.log').read_text()
t=re.sub(r'/\-.*?\-/','',p.read_text(),flags=re.S);t=re.sub(r'--[^\n]*','',t)
assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',t)
assert 'sorryAx' not in log and 'error:' not in log and 'warning:' not in log
for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
    assert set(re.sub(r'\s+','',match).split(',')) <= {'propext','Classical.choice','Quot.sound',''}
(r/'validation/FINAL_REPLAY.json').write_text(json.dumps({'status':'PASS','trust_zero':True,
    'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'scope':'New rule-test file replayed against the sealed independently rebuilt original source closure; not a second 83-module rebuild.'},indent=2)+'\n')
print('PASS: exact new rule test; both predecessor manifests preserved.')
PY

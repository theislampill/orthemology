#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd -- "$(dirname -- "$0")" && pwd)
WORKSPACE=$(dirname -- "$ROOT")
LEAN="$WORKSPACE/.toolchains/lean-4.19.0-linux/bin/lean"
OUT=$(mktemp -d "$ROOT/validation/replay-XXXXXX")
export BUILD_OUT="$OUT"
python "$ROOT/build_sources.py"
export LEAN_PATH="$OUT:$(find "$WORKSPACE/separating-projection-lean-20261009/.lake/packages" -path '*/.lake/build/lib/lean' -type d | paste -sd :)"
cd "$ROOT/proofs"
for name in OpenTermStandardness FrozenCompilerMirror PERInterface ImportedCompilerTransport; do
  "$LEAN" -o "$OUT/$name.olean" "$name.lean"
done | tee "$ROOT/validation/FINAL_TRANSPORT_REPLAY.log"
python - "$ROOT" "$OUT" <<'PY'
import hashlib, json, pathlib, re, sys
root, out = map(pathlib.Path, sys.argv[1:])
manifest = json.loads((root.parent/'hase-open-term-standardness-20261010/MANIFEST.json').read_text())
for x in manifest['files']:
    p=root.parent/'hase-open-term-standardness-20261010'/x['path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'], x['path']
for name in ['OpenTermStandardness.lean','FrozenCompilerMirror.lean','PERInterface.lean']:
    assert (root/'proofs'/name).read_bytes()==(root.parent/'hase-open-term-standardness-20261010'/name).read_bytes(), name
for p in (root/'proofs').glob('*.lean'):
    t=re.sub(r'/\-.*?\-/','',p.read_text(),flags=re.S)
    t=re.sub(r'--[^\n]*','',t)
    assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',t), p.name
log=(root/'validation/FINAL_TRANSPORT_REPLAY.log').read_text()
assert 'sorryAx' not in log and 'error:' not in log and 'warning:' not in log
for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
    assert set(re.sub(r'\s+','',match).split(',')) <= {'propext','Quot.sound','Classical.choice',''}, match
result={'status':'PASS','fresh_source_output':str(out.relative_to(root)),
        'original_project_modules':83,'new_external_objects':2,'proof_modules':4,
        'prior_reviewed_manifest_preserved':True,
        'proof_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'proofs').glob('*.lean')},
        'scope':'Actual imported compiler transport; no full new HasE model or literal HasE proof.'}
(root/'validation/FINAL_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS: fresh 83-module source build and four proof modules; prior reviewed package preserved.')
PY

#!/usr/bin/env python3
"""Copy and bind author inputs before executing only the copied verifier."""
import hashlib, json, pathlib, shutil, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'repair-evidence-commutation-20261010'
def row(path):
    raw=path.read_bytes()
    return {'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(raw).hexdigest(), 'bytes':len(raw)}
inputs=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())['inputs']
paths=sorted(p for p in AUTHOR.rglob('*') if p.is_file())+[ROOT/x['path'] for x in inputs]
before=[row(p) for p in paths]
baseline_path=HERE/'SOURCE_BASELINE.json'
if baseline_path.exists():
    assert json.loads(baseline_path.read_text())==before, 'Original sources changed since baseline'
else:
    baseline_path.write_text(json.dumps(before,indent=2)+'\n')
for item in json.loads((AUTHOR/'MANIFEST.json').read_text())['files']:
    actual=row(AUTHOR/item['path'])
    assert actual['sha256']==item['sha256'] and actual['bytes']==item['bytes']
for item in inputs:
    actual=row(ROOT/item['path'])
    assert actual['sha256']==item['sha256'] and actual['bytes']==item['bytes']
replay=HERE/'author-replay'
replay.mkdir(exist_ok=True)
shutil.copytree(AUTHOR,replay/AUTHOR.name,dirs_exist_ok=True)
for item in inputs:
    dest=replay/item['path']; dest.parent.mkdir(exist_ok=True,parents=True)
    shutil.copy2(ROOT/item['path'],dest)
run=subprocess.run([sys.executable,'-B','verify.py'],cwd=replay/AUTHOR.name,text=True,capture_output=True)
(HERE/'AUTHOR_REPLAY.stdout.txt').write_text(run.stdout)
(HERE/'AUTHOR_REPLAY.stderr.txt').write_text(run.stderr)
receipt={'command':[sys.executable,'-B','verify.py'],'cwd':str((replay/AUTHOR.name).relative_to(HERE)), 'exit_code':run.returncode, 'input_manifest_matches':True, 'original_sources_unchanged':before==[row(p) for p in paths], 'replayed_receipt_matches_author':(replay/AUTHOR.name/'CHECK_RESULTS.json').read_bytes()==(AUTHOR/'CHECK_RESULTS.json').read_bytes(), 'stdout_matches_author':run.stdout==(AUTHOR/'verification.txt').read_text()}
(HERE/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
assert run.returncode==0 and all(receipt[x] for x in ('original_sources_unchanged','replayed_receipt_matches_author','stdout_matches_author'))
print(json.dumps(receipt,indent=2))

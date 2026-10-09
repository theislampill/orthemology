#!/usr/bin/env python3
"""Recheck frozen source identity and isolate the deterministic author replay."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
here=Path(__file__).resolve().parent;root=here.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((here/'SOURCE_BINDINGS.json').read_text());tracked={}
def require(p,h):
    assert sha(p)==h,str(p);tracked[str(p)]=h
for rec in sources['frozen_manifests']:
    base=root/rec['directory'];manifest=base/rec['manifest'];require(manifest,rec['manifest_sha256'])
    actual=json.loads(manifest.read_text())['files']
    assert {x['path']:x['sha256'] for x in actual}=={x['path']:x['sha256'] for x in rec['payloads']}
    for row in rec['payloads']:require(base/row['path'],row['sha256'])
for row in sources['inspected_mathematical_sources']:require(root/row['path'],row['sha256'])
manifest=here/'MANIFEST.json'
if manifest.exists():
    for row in json.loads(manifest.read_text())['files']:require(here/row['path'],row['sha256'])
with tempfile.TemporaryDirectory(prefix='interaction-absence-replay-') as tmp:
    td=Path(tmp);(td/'results').mkdir();shutil.copyfile(here/'exact_controls.py',td/'exact_controls.py')
    proc=subprocess.run([sys.executable,str(td/'exact_controls.py')],capture_output=True,text=True,check=True)
    assert proc.stdout==(here/'results/exact_controls.log').read_text()
    assert (td/'results/exact_controls.json').read_bytes()==(here/'results/exact_controls.json').read_bytes()
for path,digest in tracked.items():assert sha(Path(path))==digest,'Changed during replay: '+path
print(json.dumps({'status':'PASS','bound_artifacts_rechecked':len(tracked),'frozen_predecessor_payloads':sum(len(x['payloads']) for x in sources['frozen_manifests']),'author_replay_byte_identical':True,'before_after_identity':True,'scope':'Byte identity and deterministic replay; no physical certification, integration or T20 closure.'},indent=2))

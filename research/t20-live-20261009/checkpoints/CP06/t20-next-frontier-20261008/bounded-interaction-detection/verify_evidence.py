#!/usr/bin/env python3
"""Verify frozen ancestry, exact imported dependency, and isolated author replay."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
here=Path(__file__).resolve().parent;root=here.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((here/'SOURCE_BINDINGS.json').read_text());tracked={}
def require(p,h):
    assert sha(p)==h,str(p);tracked[str(p)]=h
for rec in sources['frozen_manifests']:
    base=root/rec['directory'];m=base/rec['manifest'];require(m,rec['manifest_sha256'])
    obj=json.loads(m.read_text())
    assert {x['path']:x['sha256'] for x in obj['files']}=={x['path']:x['sha256'] for x in rec['payloads']}
    for row in rec['payloads']:require(base/row['path'],row['sha256'])
for field in ['additional_frozen_artifacts','imported_unary_dependency','inspected_mathematical_sources']:
    for row in sources[field]:require(root/row['path'],row['sha256'])
manifest=here/'MANIFEST.json'
if manifest.exists():
    for row in json.loads(manifest.read_text())['files']:require(here/row['path'],row['sha256'])
with tempfile.TemporaryDirectory(prefix='bounded-interaction-replay-') as tmp:
    td=Path(tmp);(td/'results').mkdir();shutil.copyfile(here/'exact_controls.py',td/'exact_controls.py')
    p=subprocess.run([sys.executable,str(td/'exact_controls.py')],capture_output=True,text=True,check=True)
    assert p.stdout==(here/'results/exact_controls.log').read_text()
    assert (td/'results/exact_controls.json').read_bytes()==(here/'results/exact_controls.json').read_bytes()
for path,digest in tracked.items():assert sha(Path(path))==digest,'Changed during replay: '+path
print(json.dumps({'status':'PASS','bound_artifacts_rechecked':len(tracked),'frozen_manifest_payloads':sum(len(x['payloads']) for x in sources['frozen_manifests']),'imported_unary_artifacts':len(sources['imported_unary_dependency']),'author_replay_byte_identical':True,'before_after_identity':True,'scope':'Artifact identity and replay only; no uniform numerical guarantee, physical validation, integration or T20 closure.'},indent=2))

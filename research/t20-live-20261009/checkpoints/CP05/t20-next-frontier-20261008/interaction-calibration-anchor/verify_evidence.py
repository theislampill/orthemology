#!/usr/bin/env python3
"""Verify frozen ancestry, optional author manifest, and isolated deterministic replays."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
here=Path(__file__).resolve().parent;root=here.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
bindings=json.loads((here/'SOURCE_BINDINGS.json').read_text())
checked={}
for rec in bindings['frozen_manifests']:
    base=root/rec['directory'];manifest=base/'MANIFEST.json'
    assert sha(manifest)==rec['manifest_sha256'],str(manifest)
    checked[str(manifest)]=sha(manifest)
    for item in rec['payloads']:
        p=base/item['path'];assert sha(p)==item['sha256'],str(p);checked[str(p)]=sha(p)
for item in bindings['individually_inspected']:
    p=root/item['path'];assert sha(p)==item['sha256'],str(p);checked[str(p)]=sha(p)
author_manifest=here/'MANIFEST.json'
if author_manifest.exists():
    for item in json.loads(author_manifest.read_text())['files']:
        p=here/item['path'];assert sha(p)==item['sha256'],str(p);checked[str(p)]=sha(p)
replays=[]
with tempfile.TemporaryDirectory(prefix='interaction-calibration-replay-') as tmp:
    td=Path(tmp);(td/'results').mkdir()
    for script,output in [('exact_controls.py','exact_controls'),('panel_controls.py','panel_controls')]:
        shutil.copyfile(here/script,td/script)
        proc=subprocess.run([sys.executable,str(td/script)],check=True,capture_output=True,text=True)
        assert proc.stdout==(here/'results'/f'{output}.log').read_text(),script+' log differs'
        assert (td/'results'/f'{output}.json').read_bytes()==(here/'results'/f'{output}.json').read_bytes(),script+' JSON differs'
        replays.append({'script':script,'status':'PASS','byte_identical_json_and_log':True})
for path,digest in checked.items():assert sha(Path(path))==digest,'changed during verification: '+path
report={'status':'PASS','bound_artifacts_rechecked':len(checked),
        'frozen_predecessor_payloads':sum(len(x['payloads']) for x in bindings['frozen_manifests']),
        'replays':replays,'before_after_identity':True,
        'scope':'Artifact identity and reproducibility only; no new proof, physical certification, integration or T20 closure.'}
print(json.dumps(report,indent=2))

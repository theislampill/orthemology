#!/usr/bin/env python3
"""Read-only, portable verification of explicitly bound inputs and manifests."""
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
bound=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
checks=[]
def verify(path,expected,kind):
    p=BASE/path
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    assert actual==expected,(path,actual,expected)
    checks.append({'path':path,'sha256':actual,'kind':kind})
for row in bound['inputs']:
    verify(row['path'],row['sha256'],'explicit input')
manifest=BASE/'finite-replay-sampling-lower-bound/MANIFEST.json'
for row in json.loads(manifest.read_text())['files']:
    verify('finite-replay-sampling-lower-bound/'+row['path'],row['sha256'],'lower author manifest payload')
for line in (BASE/'finite-panel-replay-robustness/MANIFEST.sha256').read_text().splitlines():
    digest,path=line.split(None,1)
    verify(path.strip(),digest,'upper manifest payload')
print(json.dumps({'status':'PASS','checks':checks,'count':len(checks),'scope':'Hashes only; source reading/review scope is separately stated'},indent=2,sort_keys=True))

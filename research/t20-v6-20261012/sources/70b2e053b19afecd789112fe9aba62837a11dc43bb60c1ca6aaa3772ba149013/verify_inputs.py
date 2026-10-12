from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
def check(p,d,kind):
    actual=sha(p); assert actual==d,(str(p),actual,d)
    records.append({'path':str(p.relative_to(W)),'sha256':actual,'kind':kind})
prev=W/'hase-complete-development-review-20261010'
check(prev/'MANIFEST.json','c6a199702e0df3ade78b2d84b38dba59f48a2faf2ad621ff84cfbfbd28bdb1bd','predecessor_manifest')
for row in json.loads((prev/'MANIFEST.json').read_text())['files']:
    check(prev/row['path'],row['sha256'],'predecessor_manifest_file')
for row in json.loads((prev/'INPUT_VERIFICATION.json').read_text())['records']:
    check(W/row['path'],row['sha256'],'predecessor_input_'+row['kind'])
for row in json.loads((prev/'REVIEW_RECEIPT.json').read_text())['accepted_replays']:
    for key in ['source','object','log','author_source']:
        if key in row: check(W/row[key]['path'],row[key]['sha256'],'accepted_predecessor_'+key)
base=W/'hase-church-structural-20261010'
for row in json.loads((base/'MANIFEST.json').read_text())['files']:
    check(base/row['path'],row['sha256'],'structural_manifest_file')
for row in json.loads((base/'INPUTS.json').read_text())['pinned_files']:
    check(W/row['path'],row['sha256'],'structural_pinned_file')
for directory,pinned in [
    ('hase-church-structural-20261010','29661fe1d0e20339bfb33e26633e06f0f2bf679dd42418ac5c15adcb0c16715f'),
    ('hase-closed-church-identity-20261010','b6e50d551371ecd2b52bc994766274849a19e4b8150c982aaa90eaca139ec6b3')]:
    base=W/directory
    check(base/'MANIFEST.json',pinned,'frozen_author_manifest')
    for row in json.loads((base/'MANIFEST.json').read_text())['files']:
        check(base/row['path'],row['sha256'],'frozen_author_manifest_file')
        if row['path'].endswith('.lean'):
            check(R/'sources'/row['path'],row['sha256'],'independent_frozen_source_copy')
    for row in json.loads((base/'INPUTS.json').read_text())['pinned_files']:
        check(W/row['path'],row['sha256'],'frozen_author_pinned_file')
(ROOT:=R/'INPUT_VERIFICATION.json').write_text(json.dumps({'status':'PASS','records':records,
    'baseline_rebuilt':False,'toolchain_bootstrap_verified':False,
    'predecessor_manifest_sha256':sha(prev/'MANIFEST.json')},indent=2)+'\n')
print('PASS',len(records),'input bindings; no baseline recompilation.')

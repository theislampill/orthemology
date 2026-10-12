import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
W=ROOT.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
def check(p,digest,kind):
    actual=sha(p)
    assert actual==digest,(str(p),actual,digest)
    records.append({'path':str(p.relative_to(W)),'sha256':actual,'kind':kind})
inputs=json.loads((W/'hase-closed-scalar-instances-20261010/INPUTS.json').read_text())
check(W/'.toolchains/lean-4.19.0-linux/bin/lean',inputs['lean_binary_sha256'],'lean_binary')
for group in ['receipts_and_manifests','frozen_source_files']:
    for row in inputs[group]: check(W/row['path'],row['sha256'],group)
for row in inputs['reused_objects']:
    check(W/'hase-full-per-review-20261010/fresh-lib'/(row['module'].replace('.','/')+'.olean'),row['sha256'],'reused_object')
for directory in ['hase-closed-scalar-instances-20261010','hase-closed-scalar-review-20261010','hase-full-per-extension-20261010']:
    base=W/directory
    manifest=json.loads((base/'MANIFEST.json').read_text())
    for row in manifest['files']:
        check(base/row['path'],row['sha256'],'predecessor_manifest_file')
model=json.loads((W/'hase-full-per-review-20261010/REVIEW_RECEIPT.json').read_text())
for row in model['new_replays']:
    for key in ['source','review_copy','object','log']:
        r=row[key]; check(W/r['path'],r['sha256'],'full_per_review_binding')
prereq=json.loads((W/'hase-full-per-review-20261010/PREREQUISITE_REBUILD.json').read_text())
for row in prereq['manifest_checks']:
    base=W/row['package']
    check(base/'MANIFEST.json',row['manifest_sha256'],'prerequisite_manifest')
    for entry in json.loads((base/'MANIFEST.json').read_text())['files']:
        check(base/entry['path'],entry['sha256'],'prerequisite_manifest_file')
for row in prereq['source_checks']:
    p=W/'hase-imported-compiler-transport-20261010/sources'/(row['module']+'.lean')
    check(p,row['sha256'],'pinned_original_source')
    data=p.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob']
review=json.loads((W/'hase-closed-scalar-review-20261010/REVIEW_RECEIPT.json').read_text())
for row in review['new_replays'][:2]:
    for key in ['source','object','log','author_source']:
        r=row[key]; check(W/r['path'],r['sha256'],'closed_source_review_binding')
(ROOT/'INPUT_VERIFICATION.json').write_text(json.dumps({'status':'PASS','records':records,'reused_main_objects':len(inputs['reused_objects']),'replayed_predecessors':False,'third_party_libraries_reused':True},indent=2)+'\n')
print('PASS',len(records),'bindings; predecessor objects reused without rebuild.')

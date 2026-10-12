#!/usr/bin/env python3
"""Recheck inherited source and object hashes; does not rebuild predecessors."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent
checks=[]
def check(p,expected):
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    checks.append({'path':str(p.relative_to(BASE)),'expected':expected,'actual':actual,'matches':actual==expected})
    assert actual==expected,(p,actual,expected)
full=BASE/'hase-full-per-review-20261010'
prereq=json.loads((full/'PREREQUISITE_REBUILD.json').read_text())
check(BASE/'.toolchains/lean-4.19.0-linux/bin/lean',prereq['lean_binary_sha256'])
for row in prereq['build_records']:
    check(full/'fresh-lib'/(row['module'].replace('.', '/')+'.olean'),row['object_sha256'])
receipt=json.loads((full/'REVIEW_RECEIPT.json').read_text())
for row in receipt['new_replays']:
    for kind in ['source','review_copy','object']:
        rec=row[kind];check(BASE/rec['path'],rec['sha256'])
closed=BASE/'hase-closed-scalar-review-20261010'
for row in json.loads((closed/'MANIFEST.json').read_text())['files']:
    if row['path'].startswith(('fresh-lib/','sources/')):
        check(closed/row['path'],row['sha256'])
report={'status':'PASS','checks':checks,'count':len(checks),
        'trust_boundary':'Inherited Lean/mathlib/bootstrap objects remain trusted as recorded; no new bootstrap verification.'}
(ROOT/'validation'/'CERTIFICATE_INPUT_HASHES.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS:',len(checks),'inherited source/object hashes, including Lean executable')

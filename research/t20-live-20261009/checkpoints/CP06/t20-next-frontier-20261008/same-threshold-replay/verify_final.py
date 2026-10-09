#!/usr/bin/env python3
"""Read-only verifier for the frozen author and review packets; writes nothing."""
from pathlib import Path
from hashlib import sha256
import json
A=Path(__file__).resolve().parent
R=A.parent/'same-threshold-replay-review'
def digest(p):return sha256(p.read_bytes()).hexdigest()
def verify(root,rec):
 p=root/rec['path'];assert digest(p)==rec['sha256'],str(p)
 if 'bytes' in rec:assert p.stat().st_size==rec['bytes'],str(p)
def manifest(root,want):
 assert digest(root/'MANIFEST.json')==want
 m=json.loads((root/'MANIFEST.json').read_text())
 for rec in m['files']:verify(root,rec)
 return len(m['files'])
ac=manifest(A,'f58c75e855e51be1bf4818b2b4ea6a91b1b5e685cbd45cfe304e9c3627fcbf53')
rc=manifest(R,'68a23ddfdb42ce093ad4ff8a6a929800caf88984b70b0db0c7c4f7029ceec1a9')
assert digest(R/'REVIEW_RECEIPT.json')=='dd10f56ae9a8f9aa91fe4e2fe2af53fa1458969c350d9da4ce2015341969a0cf'
receipt=json.loads((R/'REVIEW_RECEIPT.json').read_text())
assert receipt['verdict']=='PASS_WITHIN_DECLARED_PROBABILITY_AND_OBSERVATION_MODEL'
verify(R,receipt['reviewed_author_manifest'])
for rec in receipt['evidence']:verify(R,rec)
b=json.loads((A/'SOURCE_BINDINGS.json').read_text())
for rec in b['inputs']:verify(A,rec)
pcount=0
for rec in b['predecessor_manifests']:
 verify(A,rec);p=(A/rec['path']).resolve();m=json.loads(p.read_text())
 for item in m['files']:verify(p.parent,item);pcount+=1
ind=json.loads((R/'exact_controls.json').read_text());assert ind['status']=='PASS'
auth=json.loads((A/'results/exact_controls.json').read_text())
assert auth['status']=='PASS' and auth['assertions']==16598 and len(auth['families'])==29
for x,y in [('exact_controls.py','replay/exact_controls.py'),('results/exact_controls.json','replay/results/exact_controls.json'),('results/exact_controls.log','replay/results/stdout.log')]:
 assert (A/x).read_bytes()==(R/y).read_bytes()
print(json.dumps({'status':'PASS','author_payloads':ac,'review_payloads':rc,'source_inputs':len(b['inputs']),'predecessor_payloads':pcount,'author_replay_assertions':16598,'author_replay_families':29,'independent_controls_status':ind['status'],'review_manifest_sha256':digest(R/'MANIFEST.json'),'review_receipt_sha256':digest(R/'REVIEW_RECEIPT.json'),'all_frozen_inputs_unchanged':True,'verification_mode':'read-only; no reviewer evidence files rewritten'},indent=2))

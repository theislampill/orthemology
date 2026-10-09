#!/usr/bin/env python3
"""Artifact-currentness and diagnostic-replay checker; not a theorem kernel."""
from pathlib import Path
import hashlib,json
B=Path(__file__).resolve().parent;A=B.parent/'finite-geometric-score'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,h,size=None):
    assert p.is_file(),str(p)
    assert sha(p)==h,str(p)
    if size is not None:assert p.stat().st_size==size,str(p)
author_result='d7cfa67248e06786e1c4acaae6e61138498ef8e6dc1f14287d7d2664302ee96f'
author_manifest='f7d1033b6f4d269155f1e6dc5950c267414e6d498ab94166aeb55e0cf341b4a3'
check(A/'RESULT.md',author_result);check(A/'MANIFEST.json',author_manifest)
for x in json.loads((A/'MANIFEST.json').read_text())['files']:check(A/x['path'],x['sha256'],x['bytes'])
sources=json.loads((B/'SOURCE_BINDINGS.json').read_text())['sources']
for x in sources:check(B/x['path'],x['sha256'],x['bytes'])
S=B.parent/'sharp-skyline-information';R=B.parent/'sharp-skyline-information-review'
old=json.loads((R/'REVIEW_RECEIPT.json').read_text())
assert old['result']=='PASS' and not old['blocking_findings']
check(S/'RESULT.md',old['accepted_author_result_sha256']);check(S/'MANIFEST.json',old['author_manifest_sha256'])
check(R/'REVIEW.md',old['review_sha256']);check(R/'SOURCE_BINDINGS.json',old['source_bindings_sha256'])
transitive=0
for p,filename,key in [(S,'MANIFEST.json','files'),(S,'SOURCE_BINDINGS.json','sources'),(R,'MANIFEST.json','files'),(R,'SOURCE_BINDINGS.json','sources')]:
    for x in json.loads((p/filename).read_text())[key]:check(p/x['path'],x['sha256'],x.get('bytes'));transitive+=1
assert (A/'CONTROL_RESULTS.json').read_bytes()==(B/'author_replay/CONTROL_RESULTS.json').read_bytes()
assert (A/'CONTROL_RUN.log').read_bytes()==(B/'AUTHOR_REPLAY.log').read_bytes()
assert json.loads((B/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
receipt=json.loads((B/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS' and not receipt['blocking_findings']
assert receipt['accepted_author_result_sha256']==author_result and receipt['author_manifest_sha256']==author_manifest
check(B/'REVIEW.md',receipt['review_sha256']);check(B/'SOURCE_BINDINGS.json',receipt['source_bindings_sha256'])
check(B/'CONTROL_RESULTS.json',receipt['independent_controls_sha256'])
manifest=json.loads((B/'MANIFEST.json').read_text())
for x in manifest['files']:check(B/x['path'],x['sha256'],x['bytes'])
assert receipt['explicit_cutoff_certified'] is False and receipt['historical_floor']=='UNVERIFIED'
print(json.dumps({'status':'PASS','accepted_author_result_sha256':author_result,'author_manifest_sha256':author_manifest,
  'review_sha256':sha(B/'REVIEW.md'),'review_receipt_sha256':sha(B/'REVIEW_RECEIPT.json'),
  'review_manifest_sha256':sha(B/'MANIFEST.json'),'source_bindings_checked':len(sources),
  'sharp_transitive_bound_files_checked':transitive,'review_payload_files_checked':len(manifest['files']),
  'author_replay_json_and_stdout_byte_identical':True,'independent_controls':'PASS',
  'explicit_cutoff_certified':False,'historical_floor':'UNVERIFIED'},indent=2))

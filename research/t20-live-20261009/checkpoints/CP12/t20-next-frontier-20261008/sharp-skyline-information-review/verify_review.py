#!/usr/bin/env python3
"""Verify exact artifact currentness, control status and replay equality.
This is not a mathematical theorem checker or an audit-closure authority.
"""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
AUTHOR=BASE.parent/'sharp-skyline-information'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def check(path,want,size=None):
    assert path.is_file(),str(path)
    assert sha(path)==want,(str(path),sha(path),want)
    if size is not None:assert path.stat().st_size==size
sources=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
for item in sources['sources']:check(BASE/item['path'],item['sha256'],item['bytes'])
author_manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
for item in author_manifest['files']:check(AUTHOR/item['path'],item['sha256'],item['bytes'])
author_sources=json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())
for item in author_sources['sources']:check(AUTHOR/item['path'],item['sha256'],item.get('bytes'))
manifest=json.loads((BASE/'MANIFEST.json').read_text())
for item in manifest['files']:check(BASE/item['path'],item['sha256'],item['bytes'])
receipt=json.loads((BASE/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS' and receipt['blocking_findings']==[]
check(AUTHOR/'RESULT.md',receipt['accepted_author_result_sha256'])
check(AUTHOR/'MANIFEST.json',receipt['author_manifest_sha256'])
check(BASE/'REVIEW.md',receipt['review_sha256'])
check(BASE/'SOURCE_BINDINGS.json',receipt['source_bindings_sha256'])
assert receipt['historical_floor']=='UNVERIFIED'
for name in ['controls.py','CONTROL_RESULTS.json','CONTROL_RUN.log']:
    assert (BASE/'author_replay'/name).read_bytes()==(AUTHOR/name).read_bytes(),name
assert json.loads((BASE/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
assert json.loads((AUTHOR/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
output={'status':'PASS','scope':'Artifact currentness and deterministic replay; not a formal mathematical kernel, physical certification, protected integration, or closure.',
    'source_files_checked':len(sources['sources']),'author_manifest_files_checked':len(author_manifest['files']),
    'author_source_files_checked':len(author_sources['sources']),'review_payload_files_checked':len(manifest['files']),
    'accepted_author_result_sha256':receipt['accepted_author_result_sha256'],
    'author_manifest_sha256':receipt['author_manifest_sha256'],'review_sha256':receipt['review_sha256'],
    'author_replay_byte_identical':True,'independent_controls_status':'PASS','historical_floor':'UNVERIFIED'}
(BASE/'VERIFICATION.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))

#!/usr/bin/env python3
"""Checks immutable review/source bindings; not a mathematical proof checker."""
from pathlib import Path
import hashlib, json
BASE=Path(__file__).resolve().parent
AUTHOR=BASE.parent/'full-skyline-log-squared'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(path, sha):
    assert path.is_file(),str(path)
    got=digest(path)
    assert got==sha,(str(path),got,sha)
source=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
for item in source['sources']:
    check(BASE/item['path'],item['sha256'])
author_manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
for item in author_manifest['files']:
    check(AUTHOR/item['path'],item['sha256'])
    assert (AUTHOR/item['path']).stat().st_size==item['bytes']
author_sources=json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())
for item in author_sources['sources']:
    check(AUTHOR/item['path'],item['sha256'])
manifest=json.loads((BASE/'MANIFEST.json').read_text())
for item in manifest['files']:
    check(BASE/item['path'],item['sha256'])
    assert (BASE/item['path']).stat().st_size==item['bytes']
receipt=json.loads((BASE/'REVIEW_RECEIPT.json').read_text())
assert receipt['result']=='PASS'
check(AUTHOR/'RESULT.md',receipt['accepted_author_result_sha256'])
check(AUTHOR/'MANIFEST.json',receipt['author_manifest_sha256'])
check(BASE/'REVIEW.md',receipt['review_sha256'])
check(BASE/'SOURCE_BINDINGS.json',receipt['source_bindings_sha256'])
assert receipt['blocking_findings']==[]
assert json.loads((BASE/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
assert json.loads((AUTHOR/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
check(BASE/'author_replay/controls.py',digest(AUTHOR/'controls.py'))
check(BASE/'author_replay/CONTROL_RESULTS.json',digest(AUTHOR/'CONTROL_RESULTS.json'))
check(BASE/'author_replay/CONTROL_RUN.log',digest(AUTHOR/'CONTROL_RUN.log'))
assert receipt['historical_floor']=='UNVERIFIED'
assert receipt['author_replay_byte_identical'] is True
result={'status':'PASS','scope':'Artifact currentness and replay verification; no kernel proof, integration, or closure',
 'review_source_files_checked':len(source['sources']),
 'author_manifest_files_checked':len(author_manifest['files']),
 'author_dependency_files_checked':len(author_sources['sources']),
 'review_payload_files_checked':len(manifest['files']),
 'author_replay_byte_identical':True,
 'accepted_author_result_sha256':receipt['accepted_author_result_sha256'],
 'review_sha256':receipt['review_sha256'],
 'historical_floor':'UNVERIFIED'}
(BASE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

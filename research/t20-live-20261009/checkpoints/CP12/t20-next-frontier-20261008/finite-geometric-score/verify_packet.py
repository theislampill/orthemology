#!/usr/bin/env python3
"""Verify this frozen candidate's artifact bindings; not a mathematical proof checker."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
manifest=json.loads((BASE/'MANIFEST.json').read_text())
for item in manifest['files']:
    path=BASE/item['path']
    assert path.is_file(),str(path)
    assert sha(path)==item['sha256'],str(path)
    assert path.stat().st_size==item['bytes'],str(path)
assert sha(BASE/'RESULT.md')==manifest['result_sha256']
for item in json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['sources']:
    path=BASE/item['path']
    assert sha(path)==item['sha256'] and path.stat().st_size==item['bytes'],str(path)
assert json.loads((BASE/'CONTROL_RESULTS.json').read_text())['status']=='PASS'
assert manifest['historical_floor']=='UNVERIFIED'
print(json.dumps({'status':'PASS','payload_files_checked':len(manifest['files']),
                  'source_bindings_checked':len(json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['sources']),
                  'result_sha256':manifest['result_sha256'],'manifest_sha256':sha(BASE/'MANIFEST.json'),
                  'status_scope':'Frozen candidate currentness only; independent review pending.',
                  'explicit_cutoff_certified':False,'historical_floor':'UNVERIFIED'},indent=2))

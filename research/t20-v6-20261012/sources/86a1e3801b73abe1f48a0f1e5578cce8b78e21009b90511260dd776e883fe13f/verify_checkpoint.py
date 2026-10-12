#!/usr/bin/env python3
"""Read-only authored-payload integrity check, not philosophical validation."""
import hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
expected={item['path'] for item in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
assert expected==actual, {'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}
for item in manifest['files']:
 data=(root/item['path']).read_bytes()
 assert len(data)==item['bytes'], item['path']
 assert hashlib.sha256(data).hexdigest()==item['sha256'], item['path']
print(json.dumps({'status':'PASS','checked_payload_files':len(expected),'scope':'authored-payload integrity only'},indent=2))

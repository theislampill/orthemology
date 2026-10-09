"""Verify sealed review files using only Python's standard library."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
receipt=json.loads((root/'REVIEW_RECEIPT.json').read_text())
for record in receipt['files']:
    raw=(root/record['path']).read_bytes()
    assert len(raw)==record['bytes'], record['path']
    assert hashlib.sha256(raw).hexdigest()==record['sha256'], record['path']
manifest=json.loads((root/'frozen/MANIFEST.json').read_text())
assert hashlib.sha256((root/'frozen/MANIFEST.json').read_bytes()).hexdigest()==receipt['author_manifest_sha256']
for record in manifest['files']:
    raw=(root/'frozen'/record['path']).read_bytes()
    assert len(raw)==record['bytes'] and hashlib.sha256(raw).hexdigest()==record['sha256'],record['path']
print('PASS review receipt and all six frozen author file bindings')

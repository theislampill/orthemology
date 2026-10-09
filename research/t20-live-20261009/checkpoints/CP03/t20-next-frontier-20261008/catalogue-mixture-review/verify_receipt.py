from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
receipt=json.loads((root/'REVIEW_RECEIPT.json').read_text())
for f in receipt['files']:
    b=(root/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
b=(root/'frozen/MANIFEST.json').read_bytes()
assert hashlib.sha256(b).hexdigest()==receipt['author_manifest_sha256']
for f in json.loads(b)['files']:
    b=(root/'frozen'/f['path']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256'],f['path']
print('PASS review receipt and all eight frozen author payload bindings')

#!/usr/bin/env python3
"""Read-only verification of the review's frozen inputs, outputs and receipts."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
AUTHOR=HERE.parent/'dependent-gate-transport'
EXPECTED={
    'MANIFEST.json':'3ef066a690d014d22bfafb4cadb40e3506ead0c2f576b98345ab42da46af0661',
    'ADDENDUM_MANIFEST.json':'66a631d04cfe92964aaf8829f3668e362b589004d1c1c66dba287c4155513716'
}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def verify_manifest(root,name,expected=None):
    path=root/name
    if expected: assert sha(path)==expected,(name,'manifest digest')
    data=json.loads(path.read_text())
    for item in data['files']:
        p=root/item['path']
        assert sha(p)==item['sha256'],str(p)
        assert p.stat().st_size==item['bytes'],str(p)
    return len(data['files'])

input_counts={name:verify_manifest(AUTHOR,name,digest) for name,digest in EXPECTED.items()}
addendum=json.loads((AUTHOR/'ADDENDUM_MANIFEST.json').read_text())
assert addendum['author_manifest']['sha256']==EXPECTED['MANIFEST.json']
bindings=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
for item in bindings['local_inputs']:
    assert sha(HERE/item['path'])==item['sha256'],item['path']
for item in bindings['external_reads']:
    assert sha(HERE/item['snapshot'])==item['snapshot_sha256'],item['snapshot']
for item in bindings['predecessor_manifest_payloads']:
    assert sha(HERE/item['path'])==item['sha256'],item['path']

for original,replay in [('exact_controls.py','replay/exact_controls.py'),
                        ('results/exact_controls.json','replay/results/exact_controls.json'),
                        ('results/exact_controls.log','replay/results/stdout.log')]:
    assert (AUTHOR/original).read_bytes()==(HERE/replay).read_bytes(),replay
ind=json.loads((HERE/'results/independent_controls.json').read_text())
replay=json.loads((HERE/'replay/results/exact_controls.json').read_text())
assert (ind['status'],ind['assertions'],len(ind['families']))==('PASS',6543,35)
assert (replay['status'],replay['assertions'],len(replay['families']))==('PASS',3618,30)
assert sum(ind['families'].values())==ind['assertions']
assert sum(replay['families'].values())==replay['assertions']
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
assert receipt['status']=='PASS_SCOPED'
for item in receipt['evidence']:
    assert sha(HERE/item['path'])==item['sha256'],item['path']
for name,digest in EXPECTED.items():
    assert receipt['author_manifests'][name]==digest
review_files=verify_manifest(HERE,'MANIFEST.json')
print(json.dumps({'status':'PASS','author_payload_counts':input_counts,
                  'review_payloads':review_files,'independent_assertions':ind['assertions'],
                  'supplementary_replay_assertions':replay['assertions'],
                  'review_manifest_sha256':sha(HERE/'MANIFEST.json'),
                  'review_receipt_sha256':sha(HERE/'REVIEW_RECEIPT.json'),
                  'source_bindings_sha256':sha(HERE/'SOURCE_BINDINGS.json'),
                  'author_and_predecessor_bindings_unchanged':True},indent=2))

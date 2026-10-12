#!/usr/bin/env python3
"""Read-only identity checks for this review and its untouched input packet."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def verify(base,entry):
    p=base/entry['path'];data=p.read_bytes()
    assert len(data)==entry['bytes'],f'Byte count mismatch: {p}'
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],f'Digest mismatch: {p}'

bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for entry in bindings['author_packet']: verify(ROOT,entry)
for entry in bindings['direct_inputs']:
    verify(ROOT,entry);verify(HERE/'author_replay',entry)
for entry in json.loads((HERE/'author_replay/hierarchical-marginal-core-20261010/MANIFEST.json').read_text())['files']:
    verify(HERE/'author_replay/hierarchical-marginal-core-20261010',entry)
before=json.loads((HERE/'ORIGINAL_PACKET_BEFORE.json').read_text())
after=json.loads((HERE/'ORIGINAL_PACKET_AFTER.json').read_text())
assert before==after
original=ROOT/'hierarchical-marginal-core-20261010/CONTROL_RESULTS.json'
replay=HERE/'author_replay/hierarchical-marginal-core-20261010/CONTROL_RESULTS.json'
assert original.read_bytes()==replay.read_bytes()
assert json.loads(replay.read_text())['assertion_groups']==34
independent=json.loads((HERE/'INDEPENDENT_CONTROL_RESULTS.json').read_text())
assert independent['status']=='passed' and independent['assertion_groups']==25
for entry in json.loads((HERE/'MANIFEST.json').read_text())['files']: verify(HERE,entry)
print('PASS: original packet and direct-input identities; isolated replay identities; byte-identical author output; 34 author groups; 25 independent groups; unchanged original files; review manifest.')

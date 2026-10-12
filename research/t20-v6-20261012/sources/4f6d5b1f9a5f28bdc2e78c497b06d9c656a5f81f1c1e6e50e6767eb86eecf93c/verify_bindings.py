#!/usr/bin/env python3
"""Read-only identity check for the independent event-feasibility review."""
from pathlib import Path
import argparse
import hashlib
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
parser=argparse.ArgumentParser()
parser.add_argument('--portable',action='store_true',help='Do not require original workspace source paths.')
args=parser.parse_args()
count=0

def check(base,entry):
    global count
    p=base/entry['path']
    data=p.read_bytes()
    assert len(data)==entry['bytes'],f'Byte count changed: {p}'
    assert hashlib.sha256(data).hexdigest()==entry['sha256'],f'Digest changed: {p}'
    count+=1

bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for entry in bindings['target']:
    check(HERE/'author_replay',entry)
    if not args.portable:check(ROOT,entry)
for entry in bindings['direct_inputs']:
    check(HERE/'author_replay',entry)
    if not args.portable:check(ROOT,entry)
for entry in bindings['additional_inspected_inputs']:
    check(HERE/'inspected_sources',entry)
    if not args.portable:check(ROOT,entry)

before=json.loads((HERE/'ORIGINAL_PACKET_BEFORE.json').read_text())
after=json.loads((HERE/'ORIGINAL_PACKET_AFTER.json').read_text())
assert before==after, 'Original target file snapshot changed during review'
assert before['files']==bindings['target']
original=HERE/'author_replay/event-feasibility-descent-20261010'
authorm=json.loads((original/'MANIFEST.json').read_text())
for entry in authorm['files']:check(original,entry)
assert (original/'verification.txt').read_bytes()==(HERE/'author_replay.txt').read_bytes()
author=json.loads((original/'CONTROL_RESULTS.json').read_text())
assert author['status']=='PASS' and author['assertion_groups']==29
assert (author['support_patterns'],author['exact_support_certificates'],author['explicit_fibre_ambiguities'])==(304,252,52)
independent=json.loads((HERE/'INDEPENDENT_CONTROL_RESULTS.json').read_text())
assert independent['status']=='PASS' and independent['groups']==29
receipt=json.loads((HERE/'AUTHOR_REPLAY_RESULTS.json').read_text())
assert receipt['json_byte_identical'] and receipt['stdout_byte_identical'] and receipt['exit_code']==0
manifest=json.loads((HERE/'MANIFEST.json').read_text())
for entry in manifest['files']:check(HERE,entry)
actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
# Nested author manifests are delivered and must not be accidentally excluded.
actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p!=HERE/'MANIFEST.json'}
assert actual=={entry['path'] for entry in manifest['files']},'Unbound or missing review files'
print(f'PASS: {count} byte/hash bindings; original target unchanged; exact replay receipts and 29 independent groups verified.')
print('Mode: '+('portable copied sources only' if args.portable else 'portable copies plus original workspace source paths'))

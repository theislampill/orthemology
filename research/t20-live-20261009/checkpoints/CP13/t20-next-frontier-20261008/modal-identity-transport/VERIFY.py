#!/usr/bin/env python3
"""Validate the local payload and unchanged bound inputs; optionally replay controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parent.parent
bindings = json.loads((here / 'INPUT_BINDINGS.json').read_text())
manifest = json.loads((here / 'MANIFEST.json').read_text())
checked = []
for row in bindings['inputs']:
    path = root / row['path']
    raw = path.read_bytes()
    assert len(raw) == row['bytes'], row['path']
    assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
    checked.append(row['path'])
for row in manifest['payload']:
    raw = (here / row['path']).read_bytes()
    assert len(raw) == row['bytes'], row['path']
    assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
recorded = json.loads((here / 'CONTROL_RESULTS.json').read_text())
assert recorded['status'] == 'PASS'
assert recorded['source_sha256'] == hashlib.sha256((here / 'controls.py').read_bytes()).hexdigest()
assert recorded['total_assertions'] == sum(recorded['assertions_by_group'].values())
replayed = '--replay' in sys.argv
if replayed:
    fresh = subprocess.run([sys.executable, str(here / 'controls.py')], check=True,
                           text=True, capture_output=True)
    assert json.loads(fresh.stdout) == recorded, 'Replay differs from saved exact controls'
print(json.dumps({'status': 'PASS', 'bound_inputs_unchanged': len(checked),
                  'payload_files': len(manifest['payload']),
                  'controls_replayed': replayed,
                  'control_assertions': recorded['total_assertions'],
                  'historical_floor': 'UNVERIFIED',
                  'scope': 'Local artifact integrity and finite mathematical controls only'}, indent=2))

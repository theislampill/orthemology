#!/usr/bin/env python3
"""Verify the inspected inputs and rerun the narrow support-scope controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parent
bindings = json.loads((here / 'INPUT_BINDINGS.json').read_text())
for row in bindings['inputs']:
    data = (root / row['path']).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise RuntimeError('Changed inspected input: ' + row['path'])
for flag in ([], ['-O']):
    subprocess.run([sys.executable, *flag, str(here / 'support_scope_check.py')], check=True)
print('PASS: %d source bindings; 33 support-scope checks in both Python modes.' % len(bindings['inputs']))

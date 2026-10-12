#!/usr/bin/env python3
"""Verify the distributed packet's SHA256SUMS; no source code execution."""
from pathlib import Path
from hashlib import sha256
import json, sys
base = Path(__file__).resolve().parents[1]
manifest = base / 'SHA256SUMS'
failures = []
checked = 0
for n, line in enumerate(manifest.read_text(encoding='utf-8').splitlines(), 1):
    if not line.strip():
        continue
    try:
        expected, name = line.split('  ', 1)
        p = (base / name).resolve()
        if not p.is_relative_to(base):
            raise ValueError('Path escapes the package.')
        actual = sha256(p.read_bytes()).hexdigest()
        checked += 1
        if actual != expected:
            failures.append({'line': n, 'path': name, 'reason': 'hash mismatch'})
    except Exception as exc:
        failures.append({'line': n, 'reason': str(exc)})
print(json.dumps({'status': 'PASS' if not failures else 'FAIL', 'checked': checked, 'failures': failures}, indent=2))
sys.exit(0 if not failures else 1)

#!/usr/bin/env python3
"""Verify a T20 Pro-to-Dot ZIP against its embedded SHA-256 member manifest.

Usage: python verify_handoff.py /path/to/Orthemology_T20_Pro_Research_Handoff_to_Dot_20261011.zip
No external packages needed. Integrity only, not semantic or mathematical verification.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path


def verify(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError('Duplicate ZIP member names')
        if any(n.startswith('/') or '..' in Path(n).parts for n in names):
            raise RuntimeError('Unsafe ZIP member')
        expected = json.loads(z.read('MANIFEST.json'))
        actual = {n for n in names if n != 'MANIFEST.json'}
        declared = set(expected['members'])
        if actual != declared:
            raise RuntimeError(f'Member mismatch: missing={declared-actual}, extras={actual-declared}')
        for name, facts in expected['members'].items():
            data = z.read(name)
            if hashlib.sha256(data).hexdigest() != facts['sha256'] or len(data) != facts['bytes']:
                raise RuntimeError(f'Hash or size mismatch: {name}')
        assert z.testzip() is None
    print(f'VERIFIED {len(expected["members"])} members; all SHA-256 matches; CRC good')
    print('Qualification: byte integrity ONLY; no substantive research verification implied')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    verify(sys.argv[1])

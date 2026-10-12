#!/usr/bin/env python3
"""Verify this kernel checkpoint's file bytes only. This is not a proof checker."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def fail(message: str) -> None:
    raise RuntimeError(message)


def verify(base: Path) -> dict:
    base = base.resolve()
    manifest_path = base / 'MANIFEST.json'
    if manifest_path.is_symlink() or not manifest_path.is_file():
        fail('Missing or symlinked MANIFEST.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('schema') != 'literal-shift-kernel-checkpoint-integrity-v1':
        fail('Unexpected manifest schema')
    entries = manifest.get('files')
    if not isinstance(entries, list):
        fail('Manifest files is not an array')
    expected = {'MANIFEST.json'}
    for entry in entries:
        name = entry.get('path')
        if not isinstance(name, str):
            fail('Non-string member path')
        rel = PurePosixPath(name)
        if rel.is_absolute() or '..' in rel.parts or not rel.parts or '\\' in name:
            fail('Unsafe member path: ' + name)
        if name in expected:
            fail('Duplicate/reserved member path: ' + name)
        expected.add(name)
        current = base
        for part in rel.parts:
            current = current / part
            if current.is_symlink():
                fail('Symlinked member: ' + name)
        if not current.is_file() or current.resolve().parent != (base / rel.parent).resolve():
            fail('Missing or unsafe file: ' + name)
        data = current.read_bytes()
        if len(data) != entry.get('bytes'):
            fail('Byte length mismatch: ' + name)
        if hashlib.sha256(data).hexdigest() != entry.get('sha256'):
            fail('SHA-256 mismatch: ' + name)
    actual = set()
    for path in base.rglob('*'):
        if path.is_symlink():
            fail('Unmanifested symlink: ' + str(path.relative_to(base)))
        if path.is_file():
            actual.add(path.relative_to(base).as_posix())
    if actual != expected:
        fail('Member set mismatch: ' + repr({'missing': sorted(expected-actual), 'extra': sorted(actual-expected)}))
    return {
        'status': 'PASS',
        'files_checked': len(entries),
        'manifest_sha256': hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        'scope': 'Byte identity and member set only; no mathematical proof or kernel verification.'
    }


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) == 2 else Path(__file__).resolve().parent
    if len(sys.argv) > 2:
        fail('Usage: verify_integrity.py [supplement-directory]')
    print(json.dumps(verify(root), indent=2, sort_keys=True))

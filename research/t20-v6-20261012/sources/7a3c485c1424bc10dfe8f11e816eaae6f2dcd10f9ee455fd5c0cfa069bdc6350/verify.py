#!/usr/bin/env python3
"""Read-only digest verification. Does not traverse dependency/build directories."""
import hashlib
import json
from pathlib import Path, PurePosixPath

PACKAGES = {
    'hase-open-term-standardness-20261010': '887852b8eecc09e105306403c31a91beed5e9190e9dabc1cd9a8c7113f27ac86',
    'hase-imported-compiler-transport-20261010': '53c1303c989753f5c290ce587cc986424a75d53723795a4471c90468af023e38',
}
sha = lambda data: hashlib.sha256(data).hexdigest()

def checked_path(root, name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    assert not {'build', 'independent-lib'}.intersection(p.parts), name
    assert not any(part.startswith('replay-') for part in p.parts), name
    dest = root / p
    assert not dest.is_symlink(), name
    return dest

def verify(root):
    packages = []
    for name, expected in PACKAGES.items():
        base = root / name
        raw = (base / 'MANIFEST.json').read_bytes()
        assert sha(raw) == expected, name
        records = json.loads(raw)['files']
        assert len({r['path'] for r in records}) == len(records)
        for record in records:
            data = checked_path(base, record['path']).read_bytes()
            assert len(data) == record['bytes'], record['path']
            assert sha(data) == record['sha256'], record['path']
        packages.append({'directory': name, 'manifest_sha256': expected,
                         'payload_files': len(records), 'payload_bytes': sum(r['bytes'] for r in records)})
    index = root / 'ARCHIVE_CONTENTS.json'
    archive_files = None
    if index.exists():
        records = json.loads(index.read_text())['files']
        assert len({r['path'] for r in records}) == len(records)
        for record in records:
            data = checked_path(root, record['path']).read_bytes()
            assert len(data) == record['bytes'] and sha(data) == record['sha256'], record['path']
        archive_files = len(records)
    return {'status': 'PASS', 'packages': packages, 'archive_indexed_files': archive_files,
            'frozen_payload_files': sum(p['payload_files'] for p in packages),
            'frozen_manifests': len(packages)}

if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parent), indent=2))

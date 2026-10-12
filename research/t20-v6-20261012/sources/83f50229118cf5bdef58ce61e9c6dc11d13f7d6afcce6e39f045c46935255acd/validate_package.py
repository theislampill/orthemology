#!/usr/bin/env python3
"""Offline integrity checks for this proposed research projection, not proof replay."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise ValueError('invalid relative path')
    if value.startswith('/') or any(x in ('', '.', '..') for x in value.split('/')):
        raise ValueError('unsafe relative path')
    return PurePosixPath(value)


def read_json(path):
    def pairs(rows):
        out = {}
        for key, value in rows:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key] = value
        return out
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs)


def verify_files(root):
    root = Path(root)
    if root.is_symlink():
        raise ValueError('package root is a symlink')
    manifest = read_json(root / 'PACKAGE_CONTENTS.json')
    expected = {'PACKAGE_CONTENTS.json'}
    for row in manifest['files']:
        rel = str(safe_path(row['path']))
        if rel in expected:
            raise ValueError('duplicate manifest path')
        expected.add(rel)
        path = root / rel
        for part in [path, *path.parents]:
            if part == root:
                break
            if part.is_symlink():
                raise ValueError('symlink in package')
        if not path.is_file():
            raise ValueError('missing package file: ' + rel)
        raw = path.read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('changed package file: ' + rel)
    actual = set()
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError('symlink in package')
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError('unexpected or missing package members: ' + repr(sorted(actual ^ expected)))
    return len(expected) - 1


def verify_projection(root):
    root = Path(root)
    data = read_json(root / 'PUBLIC_PROJECTION.json')
    seen = set()
    for row in data['files']:
        key = row['original_sha256']
        if key in seen:
            raise ValueError('duplicate source-object identity')
        seen.add(key)
        for name in ('original_sha256', 'public_sha256'):
            if not re.fullmatch('[0-9a-f]{64}', row[name]):
                raise ValueError('invalid source digest')
        if row['disposition'] == 'included':
            raw = (root / str(safe_path(row['public_path']))).read_bytes()
            if hashlib.sha256(raw).hexdigest() != row['public_sha256'] or len(raw) != row['public_bytes']:
                raise ValueError('source/public binding mismatch')
        elif row['disposition'] == 'pinned_existing_public_source':
            if not row['public_url'].startswith(data['repository']['pinned_blob_prefix']):
                raise ValueError('unpinned inherited source')
        else:
            raise ValueError('unknown projection disposition')
        if row['projection'] == 'EXACT' and (row['original_sha256'] != row['public_sha256'] or row['original_bytes'] != row['public_bytes']):
            raise ValueError('false exact-byte claim')
        if row['projection'] != 'EXACT' and not row.get('transformations'):
            raise ValueError('missing transformation disclosure')
    return len(seen)


def main():
    root = Path(__file__).resolve().parent
    print(json.dumps({'status': 'PASS', 'manifest_files': verify_files(root),
                      'source_bindings': verify_projection(root),
                      'scope': 'Package byte integrity and source/public bindings only; not repository validation or scientific replay.'}))


if __name__ == '__main__':
    main()

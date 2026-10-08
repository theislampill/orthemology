"""Separate package-byte verification; requires an independently supplied manifest digest.

This does not authenticate source-reading history, mathematical assumptions,
external companion DOCX files, or a later archive's container bytes.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys


def check(root, trusted_manifest_sha256):
    if not re.fullmatch(r'[0-9a-f]{64}', trusted_manifest_sha256):
        raise ValueError('invalid_trusted_manifest_digest')
    manifest_path = root / 'MANIFEST.json'
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('manifest_missing_or_not_regular_file')
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != trusted_manifest_sha256:
        raise ValueError('manifest_digest_mismatch')
    manifest = json.loads(raw)
    allowed = manifest['allowlist']
    if not isinstance(allowed, list) or not all(isinstance(p, str) for p in allowed):
        raise ValueError('invalid_allowlist')
    if len(allowed) != len(set(allowed)) or 'MANIFEST.json' not in allowed:
        raise ValueError('duplicate_or_incomplete_allowlist')
    if type(manifest['member_count']) is not int or manifest['member_count'] != len(allowed):
        raise ValueError('manifest_member_count_mismatch')
    for rel in allowed:
        p = PurePosixPath(rel)
        if p.is_absolute() or str(p) != rel or '\\' in rel or any(part in {'.', '..'} or part.startswith('.') for part in p.parts):
            raise ValueError('unsafe_or_hidden_member_name')
    expected_dirs = {str(parent) for p in allowed for parent in PurePosixPath(p).parents if str(parent) != '.'}
    actual_files, actual_dirs = set(), set()
    for p in root.rglob('*'):
        rel = p.relative_to(root).as_posix()
        if p.is_symlink():
            raise ValueError('symlink_member')
        if p.is_file():
            actual_files.add(rel)
        elif p.is_dir():
            actual_dirs.add(rel)
        else:
            raise ValueError('nonregular_member')
    if actual_files != set(allowed) or actual_dirs != expected_dirs:
        raise ValueError('exact_inventory_mismatch')
    entries = manifest['files']
    entry_paths = [f['path'] for f in entries]
    if len(entry_paths) != len(set(entry_paths)) or set(entry_paths) != set(allowed) - {'MANIFEST.json'}:
        raise ValueError('manifest_entry_set_mismatch')
    for f in entries:
        if type(f['bytes']) is not int or f['bytes'] < 0 or not re.fullmatch(r'[0-9a-f]{64}', f['sha256']):
            raise ValueError('invalid_manifest_entry')
        data = (root / f['path']).read_bytes()
        if len(data) != f['bytes'] or hashlib.sha256(data).hexdigest() != f['sha256']:
            raise ValueError('member_size_or_digest_mismatch')
    return len(allowed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-manifest-sha256', required=True,
                        help='Exact trusted digest obtained independently of this directory.')
    args = parser.parse_args()
    try:
        count = check(Path(__file__).resolve().parent, args.expected_manifest_sha256)
    except (ValueError, KeyError, TypeError, OSError, json.JSONDecodeError) as exc:
        print('FAIL: package integrity check rejected the supplied directory.', file=sys.stderr)
        print(type(exc).__name__, file=sys.stderr)
        return 1
    print(f'PASS: trusted manifest and all {count} exact allowlisted member identities match.')
    print('This verifies directory bytes and inventory, not reading history or external documents.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

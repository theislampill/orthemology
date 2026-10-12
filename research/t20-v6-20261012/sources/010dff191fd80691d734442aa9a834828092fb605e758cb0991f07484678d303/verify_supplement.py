#!/usr/bin/env python3
"""Verify only package integrity, using Python's standard library. No scientific claim."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tempfile
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_directory(root):
    root = Path(root)
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    expected = {r['path']: r for r in manifest['files']}
    allowed = set(expected) | {'MANIFEST.json', 'SHA256SUMS'}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual == allowed, f'member mismatch: missing={allowed-actual}; extra={actual-allowed}'
    for name, row in expected.items():
        data = (root/name).read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], name
    checksums = {}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert name not in checksums, 'duplicate checksum entry'
        checksums[name] = digest
    assert set(checksums) == allowed - {'SHA256SUMS'}
    for name, digest in checksums.items():
        assert sha((root/name).read_bytes()) == digest, name
    locators = json.loads((root/'LOCATOR_MAP.json').read_text())
    for row in locators['deduplicated_paths']:
        p = root/row['canonical_path']
        assert p.is_file() and sha(p.read_bytes()) == row['sha256'], row['original_path']
    return {'status': 'PASS', 'payload_files': len(expected), 'total_files': len(actual),
            'alias_bindings': len(locators['deduplicated_paths']),
            'manifest_sha256': sha((root/'MANIFEST.json').read_bytes())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('package', help='ZIP file or extracted supplement root')
    args = parser.parse_args()
    p = Path(args.package).resolve()
    if p.is_dir():
        result = verify_directory(p)
    else:
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
            assert len(names) == len(set(names)), 'duplicate ZIP member'
            assert z.testzip() is None, 'ZIP CRC failure'
            for name in names:
                q = PurePosixPath(name)
                assert not q.is_absolute() and '..' not in q.parts and '\\' not in name
                info = z.getinfo(name)
                assert (info.external_attr >> 16) & 0o170000 != 0o120000, 'symlink'
            roots = {PurePosixPath(n).parts[0] for n in names}
            assert len(roots) == 1, 'ZIP must have exactly one top-level folder'
            with tempfile.TemporaryDirectory(prefix='t20-supplement-verify-') as tmp:
                z.extractall(tmp)
                result = verify_directory(Path(tmp)/next(iter(roots)))
            result.update(zip_crc='PASS', extracted_member_hashes='PASS',
                          zip_sha256=sha(p.read_bytes()), zip_bytes=p.stat().st_size)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

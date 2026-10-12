#!/usr/bin/env python3
"""Verify distributed file identities. No philosophical or source-truth proof."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--zip', type=Path, dest='archive')
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--original-snapshot', type=Path,
                        help='Optional reviewed original, to check the historical text identities.')
    args = parser.parse_args()
    errors = []
    files = {}
    if args.archive:
        with zipfile.ZipFile(args.archive) as z:
            for entry in z.infolist():
                name = entry.filename
                if entry.is_dir():
                    errors.append('Unexpected directory entry: ' + name)
                    continue
                if name in files:
                    errors.append('Duplicate archive member: ' + name)
                if stat.S_ISLNK(entry.external_attr >> 16):
                    errors.append('Symlink member: ' + name)
                if PurePosixPath(name).is_absolute() or '..' in PurePosixPath(name).parts:
                    errors.append('Unsafe member name: ' + name)
                files[name] = z.read(entry)
    else:
        for path in args.directory.rglob('*'):
            name = path.relative_to(args.directory).as_posix()
            if path.is_symlink():
                errors.append('Symlink entry: ' + name)
            elif path.is_file():
                files[name] = path.read_bytes()
    manifest_bytes = files.get('MANIFEST.json')
    if manifest_bytes is None:
        raise ValueError('MANIFEST.json is missing')
    manifest_hash = digest(manifest_bytes)
    if args.expected_manifest_sha256 and manifest_hash != args.expected_manifest_sha256:
        errors.append('Manifest differs from the independently supplied expected digest')
    manifest = json.loads(manifest_bytes)
    expected = {entry['file']: entry for entry in manifest['files']}
    if len(expected) != len(manifest['files']):
        errors.append('Duplicate manifest file record')
    if set(files) != set(expected) | {'MANIFEST.json'}:
        errors.append('Inventory mismatch: missing=' + repr(sorted(set(expected) - set(files))) +
                      '; extra=' + repr(sorted(set(files) - set(expected) - {'MANIFEST.json'})))
    for name, record in expected.items():
        data = files.get(name)
        if data is None:
            continue
        if len(data) != record['bytes'] or digest(data) != record['sha256']:
            errors.append('Size or digest mismatch: ' + name)
    binding = json.loads(files['PROJECTION_BINDING.json'])
    for record in binding['files']:
        data = files.get(record['file'])
        if data is None or len(data) != record['public_bytes'] or digest(data) != record['public_sha256']:
            errors.append('Public projection binding mismatch: ' + record['file'])
    historical_status = 'recorded identity only; original not supplied'
    if args.original_snapshot:
        original = args.original_snapshot
        if digest((original / 'MANIFEST.json').read_bytes()) != binding['reviewed_original_manifest_sha256']:
            errors.append('Original snapshot manifest mismatch')
        for record in binding['files']:
            if record['file'] == 'PUBLIC_REVIEW.md':
                continue  # Review is a separately identified public document.
            if digest((original / record['file']).read_bytes()) != record['reviewed_original_sha256']:
                errors.append('Reviewed original text mismatch: ' + record['file'])
        historical_status = 'original manifest and three text bindings checked'
    report = {
        'status': 'PASS' if not errors else 'FAIL',
        'manifest_sha256': manifest_hash,
        'manifest_digest_checked_against_external_value': bool(args.expected_manifest_sha256),
        'distributed_files_including_manifest': len(files),
        'historical_binding': historical_status,
        'scope': 'Byte identities, file inventory and projection bindings only. No philosophical validity, source truth, necessity or independent manifest authenticity is established.',
        'errors': errors,
    }
    print(json.dumps(report, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}))
        sys.exit(1)

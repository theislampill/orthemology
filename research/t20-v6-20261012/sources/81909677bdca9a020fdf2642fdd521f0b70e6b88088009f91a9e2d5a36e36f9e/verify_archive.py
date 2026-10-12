#!/usr/bin/env python3
"""Authenticate the exact archive file set; hashes do not prove research claims."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root):
    root = Path(root).resolve()
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    expected = {entry['path']: entry for entry in manifest['files']}
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    if actual != set(expected) | {'MANIFEST.json'}:
        raise RuntimeError({'missing': sorted(set(expected) - actual),
                            'unexpected': sorted(actual - set(expected) - {'MANIFEST.json'})})
    for name, entry in expected.items():
        p = root / name
        if p.is_symlink() or p.stat().st_size != entry['bytes'] or digest(p) != entry['sha256']:
            raise RuntimeError('Archive byte mismatch: ' + name)
    for p in root.rglob('*'):
        if p.is_symlink():
            raise RuntimeError('Unexpected symbolic link: ' + str(p))
    # These manifest checks are binding/integrity checks, not mathematical controls.
    bindings = json.loads((root / 'SOURCE_BINDINGS.json').read_text())['files']
    for entry in bindings:
        p = root / entry['path']
        if p.stat().st_size != entry['bytes'] or digest(p) != entry['sha256']:
            raise RuntimeError('Original-source binding mismatch: ' + entry['path'])
    nested_freeze_entries = 0
    for freeze in sorted(root.rglob('*FREEZE.json')):
        data = json.loads(freeze.read_text())
        if isinstance(data.get('files'), dict):
            for name, value in data['files'].items():
                expected_digest = value['sha256'] if isinstance(value, dict) else value
                if digest(freeze.parent / name) != expected_digest:
                    raise RuntimeError('Nested freeze mismatch: ' + str(freeze) + ' ' + name)
                nested_freeze_entries += 1
        elif isinstance(data.get('files'), list):
            for entry in data['files']:
                p = freeze.parent / entry['path']
                if p.stat().st_size != entry['bytes'] or digest(p) != entry['sha256']:
                    raise RuntimeError('Nested freeze mismatch: ' + str(p))
                nested_freeze_entries += 1
        if data.get('manifest_sha256'):
            if digest(freeze.parent / 'MANIFEST.json') != data['manifest_sha256']:
                raise RuntimeError('Conditional author historical manifest changed')
            nested_freeze_entries += 1
        if data.get('result_sha256'):
            if digest(freeze.parent / 'RESULT.md') != data['result_sha256']:
                raise RuntimeError('Conditional author result changed')
            nested_freeze_entries += 1
    omissions = json.loads((root / 'OMITTED_SOURCE_BODIES.json').read_text())['omitted']
    omitted = {entry['path']: entry for entry in omissions}
    for name in omitted:
        if (root / name).exists():
            raise RuntimeError('Source-body exclusion violated: ' + name)
    author_root = root / 'conditional-entropy-control-20261011'
    author_manifest = json.loads((author_root / 'MANIFEST.json').read_text())
    author_available = author_omitted = 0
    for entry in author_manifest['files']:
        p = author_root / entry['path']
        archive_path = p.relative_to(root).as_posix()
        if archive_path in omitted:
            metadata = omitted[archive_path]
            if metadata['sha256'] != entry['sha256'] or metadata['bytes'] != entry['bytes']:
                raise RuntimeError('Omitted source metadata mismatch: ' + archive_path)
            author_omitted += 1
        else:
            if p.stat().st_size != entry['bytes'] or digest(p) != entry['sha256']:
                raise RuntimeError('Available author-manifest binding mismatch: ' + archive_path)
            author_available += 1
    if (author_available, author_omitted) != (15, 3):
        raise RuntimeError('Unexpected conditional author manifest availability')
    source_root = root / 'cumulative-warrant-primary-check-20261011'
    source_manifest = json.loads((source_root / 'MANIFEST.json').read_text())
    for entry in source_manifest['files']:
        p = source_root / entry['path']
        b = p.read_bytes()
        if len(b) != entry['bytes'] or hashlib.sha256(b).hexdigest() != entry['sha256']:
            raise RuntimeError('Shareable source-manifest mismatch: ' + entry['path'])
        if entry.get('git_blob_sha1') and hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() != entry['git_blob_sha1']:
            raise RuntimeError('Shareable source Git-blob mismatch: ' + entry['path'])
    source_expected = {entry['path'] for entry in source_manifest['files']} | {'MANIFEST.json'}
    source_actual = {p.relative_to(source_root).as_posix() for p in source_root.rglob('*') if p.is_file()}
    if source_actual != source_expected:
        raise RuntimeError('Source packet exceeds its shareable manifest')
    return {'status': 'pass', 'archive_files_excluding_manifest': len(expected),
            'original_file_bindings': len(bindings), 'nested_freeze_bindings': nested_freeze_entries,
            'source_shareable_manifest_bindings': len(source_manifest['files']),
            'conditional_author_manifest_available_bindings': author_available,
            'conditional_author_manifest_intentionally_omitted': author_omitted,
            'source_bodies_intentionally_omitted': len(omitted),
            'private_sources_included': False,
            'scope': 'File-set and byte integrity only, not mathematical proof or source-interpretation verification.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(args.root)
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        output = args.output.resolve()
        if output == args.root.resolve() or args.root.resolve() in output.parents:
            raise RuntimeError('Write verification outputs outside the preserved archive tree')
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered)
    print(rendered, end='')

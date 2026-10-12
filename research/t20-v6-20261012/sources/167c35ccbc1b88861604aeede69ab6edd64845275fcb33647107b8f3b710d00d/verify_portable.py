#!/usr/bin/env python3
"""Checkpoint23 integrity-only verifier. Executes no source research code.

Python 3.8+ standard library. No network, installation, sources, theorem prover,
imported research program or earlier checkpoint archive is required.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_path(text):
    require(isinstance(text, str), 'Path must be a string.')
    p = PurePosixPath(text)
    require(bool(text) and str(p) == text and not p.is_absolute()
            and '..' not in p.parts and '\\' not in text,
            'Unsafe or noncanonical package path: ' + repr(text))
    return p


def snapshot(root):
    files, directories = {}, set()
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Symlink forbidden: ' + str(path))
        relative = path.relative_to(root).as_posix()
        if path.is_file():
            files[relative] = {'bytes': path.stat().st_size, 'sha256': digest(path)}
        else:
            require(path.is_dir(), 'Unexpected filesystem entry: ' + str(path))
            directories.add(relative)
    return files, directories


def read_json(path):
    def reject_nonfinite(value):
        raise ValueError('Nonstandard JSON constant: ' + value)
    return json.loads(path.read_text(encoding='utf-8'), parse_constant=reject_nonfinite)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True,
                        help='A new output directory outside the package')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    requested = Path(args.output).expanduser()
    require(not requested.exists() and not requested.is_symlink(),
            'Output already exists; refusing to overwrite.')
    output = requested.resolve()
    require(output != root and root not in output.parents,
            'Output must be outside the package.')
    before, before_dirs = snapshot(root)
    manifest = read_json(root / 'MANIFEST.json')
    require(manifest['checkpoint_number'] == 23, 'Wrong checkpoint.')
    require(manifest['status'] == 'INTERMEDIATE_T20_ACTIVE', 'Wrong checkpoint status.')
    entries = manifest['files']
    require(manifest['file_count'] == len(entries), 'Manifest count mismatch.')
    paths = [str(safe_path(row['path'])) for row in entries]
    require(len(paths) == len(set(paths)), 'Duplicate manifest path.')
    require(set(before) == set(paths) | {'MANIFEST.json', 'MANIFEST.sha256'},
            'Distributed-file inventory mismatch.')
    expected_dirs = {str(p) for text in before for p in PurePosixPath(text).parents
                     if str(p) != '.'}
    require(before_dirs == expected_dirs, 'Distributed-directory inventory mismatch.')
    forbidden_parts = {'sources', 'research-intermediates', 'reading', 'user_notes',
                       'agent_notes', 'dream_notes', '__pycache__', 'read-selections', 'development'}
    for text in before:
        p = safe_path(text)
        require(not (set(p.parts) & forbidden_parts), 'Excluded directory in package: ' + text)
        require(p.suffix.lower() in {'.md', '.json', '.sha256', '.py', '.sh', '.lean', '.log', '.txt', '.zip', '.sha256sums'}
                or p.name == 'SHA256SUMS' or text == 'replay/verify_portable.py',
                'Excluded file type: ' + text)
    for row in entries:
        require(before[row['path']] == {'bytes': row['bytes'], 'sha256': row['sha256']},
                'Payload hash or size mismatch: ' + row['path'])
    sums = {}
    for line in (root / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected, text = line.split('  ', 1)
        safe_path(text)
        require(text not in sums, 'Duplicate checksum path.')
        require(len(expected) == 64 and all(c in '0123456789abcdef' for c in expected),
                'Malformed SHA-256.')
        sums[text] = expected
    require(set(sums) == set(paths) | {'MANIFEST.json'}, 'Checksum inventory mismatch.')
    for text, expected in sums.items():
        require(before[text]['sha256'] == expected, 'Checksum mismatch: ' + text)
    parsed = []
    for text in before:
        if text.endswith('.json'):
            read_json(root / text)
            parsed.append(text)
    preserved = read_json(root / 'PRESERVED_INPUTS.json')
    require(preserved['file_count'] == len(preserved['files']), 'Preserved-input count mismatch.')
    preserved_paths = [r['archive_path'] for r in preserved['files']]
    require(len(preserved_paths) == len(set(preserved_paths)), 'Duplicate preserved path.')
    for row in preserved['files']:
        text = str(safe_path(row['archive_path']))
        require(before[text] == {'bytes': row['bytes'], 'sha256': row['sha256']},
                'Preserved-original identity mismatch: ' + text)
    component_checks = read_json(root / 'COMPONENT_MANIFEST_CHECKS.json')
    for row in component_checks['entries']:
        if row['distributed']:
            text = str(safe_path(row['archive_path']))
            require(before[text]['sha256'] == row['expected_sha256'],
                    'Included component-manifest identity mismatch: ' + text)
        else:
            require(row['archive_path'] not in before,
                    'Omitted component witness unexpectedly distributed.')
    prior = read_json(root / 'PRIOR_CHECKPOINT.json')
    delivery_path = str(safe_path(prior['exact_delivery_record_copy']))
    delivery = read_json(root / delivery_path)
    require(delivery['checkpoint'] == 22 and prior['checkpoint'] == 22,
            'Wrong predecessor checkpoint.')
    require(delivery['files'][0]['sha256'] == prior['archive']['sha256'],
            'Predecessor archive identity mismatch.')
    require(before[delivery_path]['sha256'] == prior['delivery_record_sha256'],
            'Predecessor delivery record mismatch.')
    require(delivery['send']['message_id'] == prior['accepted_message_id'],
            'Predecessor message identity mismatch.')
    scope = read_json(root / 'SCOPE_AND_HISTORY.json')
    for key in ('research_closed', 'integrated', 'owner_accepted',
                'historical_duration_certified', 'new_theorem_or_kernel_result_claimed',
                'research_code_executed'):
        require(scope[key] is False, 'Unsupported scope claim: ' + key)
    require(scope['status'] == 'INTERMEDIATE_T20_ACTIVE', 'Research must remain active.')
    delta = read_json(root / 'DELTA_MANIFEST.json')
    require(delta['checkpoint'] == 23 and delta['predecessor'] == 22, 'Wrong delta identity.')
    for component in delta['components']:
        for row in component['entrypoints']:
            text = str(safe_path(row['path']))
            require(before[text]['sha256'] == row['sha256'], 'Delta entrypoint hash mismatch.')
    supplied = read_json(root / 'SUPPLIED_COMPANION.json')
    companion_path = str(safe_path(supplied['archive_path']))
    require(before[companion_path] == {'bytes': supplied['bytes'], 'sha256': supplied['sha256']},
            'Supplied companion identity mismatch.')
    with zipfile.ZipFile(root / companion_path) as archive:
        require(archive.testzip() is None, 'Nested companion CRC failure.')
        members = archive.infolist()
        names = [m.filename for m in members]
        require(len(names) == len(set(names)), 'Duplicate nested member.')
        for member in members:
            safe_path(member.filename)
            require(not member.is_dir(), 'Unexpected explicit nested directory.')
            require((member.external_attr >> 16) & 0o170000 != 0o120000,
                    'Nested symlink forbidden.')
        prefix = 'Orthemology_T20_Deep_Dive_20261009/'
        nested = json.loads(archive.read(prefix + 'MANIFEST.json'))
        require(len(names) == supplied['member_count'], 'Nested member count mismatch.')
        expected = {prefix + row['path'] for row in nested['files']}
        expected |= {prefix + 'MANIFEST.json', prefix + 'MANIFEST.sha256'}
        require(set(names) == expected, 'Nested inventory mismatch.')
        require(hashlib.sha256(archive.read(prefix + 'MANIFEST.json')).hexdigest() ==
                supplied['manifest_sha256'], 'Nested manifest identity mismatch.')
        for row in nested['files']:
            safe_path(row['path'])
            data = archive.read(prefix + row['path'])
            require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                    'Nested payload hash/size mismatch.')
    after, after_dirs = snapshot(root)
    require(before == after and before_dirs == after_dirs,
            'Package changed during verification.')
    # No filesystem output is created until all checks above pass.
    output.mkdir(parents=True, exist_ok=False)
    receipt = {
        'status': 'PASS',
        'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'checkpoint': 23,
        'distributed_file_count': len(before),
        'exact_file_and_directory_inventory_verified': True,
        'manifest_hashes_and_sizes_verified': True,
        'manifest_and_payload_checksum_inventory_verified': True,
        'json_files_parsed': parsed,
        'preserved_original_count': len(preserved['files']),
        'component_manifest_entries_checked': len(component_checks['entries']),
        'component_manifest_omitted_witnesses_not_required': True,
        'checkpoint22_delivery_and_archive_identity_consistent': True,
        'supplied_companion_crc_and_payload_hashes_verified': True,
        'delta_entrypoints_hash_verified': True,
        'research_code_executed': False,
        'source_research_controls_executed': 0,
        'lean_or_kernel_replay': False,
        'network_or_installation_requested': False,
        'package_bytes_unchanged': True,
        'scope': 'Byte integrity, exact inventory and JSON readability only. No source-research code execution, philosophical premise certification, new theorem, integration, acceptance, closure or historical-duration certification.'}
    with (output / 'VERIFICATION_RECEIPT.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'research_code_executed': False,
                      'receipt': str(output / 'VERIFICATION_RECEIPT.json')}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(1)

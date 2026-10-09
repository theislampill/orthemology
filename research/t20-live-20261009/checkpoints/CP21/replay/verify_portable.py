#!/usr/bin/env python3
"""Checkpoint21 byte verifier; executes exactly two bundled analyst controls.

No network, imported code, Lean invocation, package installation, or primary
source body is required. Historical nested manifests are provenance records.
The top-level manifest is the authoritative distributed-file inventory.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys

CONTROLS = (
    ('modal-premise-independence.py', 'modal-premise-independence-results.json'),
    ('symmetry-premise-control.py', 'symmetry-premise-control-results.json'),
)
CONTROL_DIR = 'complete-explanation-modal-review-20261009'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for part in iter(lambda: stream.read(1048576), b''):
            h.update(part)
    return h.hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(text):
    p = PurePosixPath(text)
    require(bool(text) and str(p) == text and not p.is_absolute()
            and '..' not in p.parts and '\\' not in text,
            'Unsafe or noncanonical package path: ' + repr(text))
    return p


def snapshot(root):
    result = {}
    for path in sorted(root.rglob('*')):
        require(not path.is_symlink(), 'Symlink forbidden: ' + str(path))
        if path.is_file():
            result[path.relative_to(root).as_posix()] = {
                'bytes': path.stat().st_size, 'sha256': digest(path)}
        else:
            require(path.is_dir(), 'Unexpected non-file entry: ' + str(path))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True,
                        help='A new output directory outside the extracted package')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    output_arg = Path(args.output).expanduser()
    require(not output_arg.exists() and not output_arg.is_symlink(),
            'Output already exists; refusing to overwrite.')
    output = output_arg.resolve()
    require(output != root and root not in output.parents,
            'Output must be outside the package.')
    before = snapshot(root)
    manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
    require(manifest['checkpoint_number'] == 21, 'Wrong checkpoint.')
    require(manifest['status'] == 'INTERMEDIATE_T20_ACTIVE', 'Wrong status.')
    entries = manifest['files']
    require(manifest['file_count'] == len(entries), 'Manifest count mismatch.')
    paths = [str(safe_path(row['path'])) for row in entries]
    require(len(paths) == len(set(paths)), 'Duplicate manifest path.')
    require(set(before) == set(paths) | {'MANIFEST.json', 'MANIFEST.sha256'},
            'Distributed-file inventory mismatch.')
    for row in entries:
        require(before[row['path']] == {'bytes': row['bytes'], 'sha256': row['sha256']},
                'Payload hash or size mismatch: ' + row['path'])
    checksum_rows = {}
    for line in (root / 'MANIFEST.sha256').read_text(encoding='utf-8').splitlines():
        expected, path = line.split('  ', 1)
        safe_path(path)
        require(path not in checksum_rows, 'Duplicate checksum path.')
        require(len(expected) == 64 and all(c in '0123456789abcdef' for c in expected),
                'Malformed SHA-256.')
        checksum_rows[path] = expected
    require(set(checksum_rows) == set(paths) | {'MANIFEST.json'},
            'Checksum inventory mismatch.')
    for path, expected in checksum_rows.items():
        require(before[path]['sha256'] == expected, 'Checksum mismatch: ' + path)
    json_paths = []
    for path in before:
        if path.endswith('.json'):
            json.loads((root / path).read_text(encoding='utf-8'))
            json_paths.append(path)
    preserved = json.loads((root / 'PRESERVED_INPUTS.json').read_text(encoding='utf-8'))
    require(preserved['file_count'] == len(preserved['files']), 'Original-input count mismatch.')
    for row in preserved['files']:
        path = str(safe_path(row['archive_path']))
        require(before[path] == {'bytes': row['bytes'], 'sha256': row['sha256']},
                'Preserved-input mismatch: ' + path)
    # Check MIT reference blob identities without importing or executing any of them.
    refs = json.loads((root / 'REFERENCE_ONLY_CODE.json').read_text(encoding='utf-8'))
    reference_checks = []
    for row in refs['retained_files']:
        path = str(safe_path(row['archive_path']))
        data = (root / path).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()
        require(blob == row['git_blob_sha1'], 'Reference Git-blob mismatch: ' + path)
        reference_checks.append({'path': path, 'git_blob_sha1': blob, 'executed': False})
    # No output or control execution occurs until all package checks pass.
    output.mkdir(parents=True, exist_ok=False)
    work = output / 'isolated-controls'
    work.mkdir()
    runs = []
    for script_name, result_name in CONTROLS:
        source = root / CONTROL_DIR / script_name
        isolated = work / script_name
        shutil.copyfile(source, isolated)
        require(digest(source) == digest(isolated), 'Control copy changed.')
        proc = subprocess.run([sys.executable, '-I', '-B', str(isolated)], cwd=str(work),
                              env=dict(os.environ, PYTHONHASHSEED='0', PYTHONDONTWRITEBYTECODE='1'),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
        (output / (script_name + '.stdout.json')).write_bytes(proc.stdout)
        (output / (script_name + '.stderr.txt')).write_bytes(proc.stderr)
        require(proc.returncode == 0, 'Control failed: ' + script_name)
        require(proc.stderr == b'', 'Unexpected control stderr: ' + script_name)
        expected = (root / CONTROL_DIR / result_name).read_bytes()
        require(proc.stdout == expected, 'Control result is not byte-identical: ' + script_name)
        json.loads(proc.stdout.decode('utf-8'))
        require(digest(source) == digest(isolated), 'Control changed its copied script.')
        runs.append({'script': CONTROL_DIR + '/' + script_name,
                     'expected_result': CONTROL_DIR + '/' + result_name,
                     'returncode': proc.returncode, 'stderr_empty': True,
                     'stdout_byte_identical': True,
                     'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest()})
    after = snapshot(root)
    require(before == after, 'Package bytes changed during verification.')
    receipt = {
        'status': 'PASS', 'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'checkpoint': 21, 'payload_file_count': len(before),
        'manifest_payload_hashes_and_sizes_verified': True,
        'manifest_and_payload_checksum_inventory_verified': True,
        'json_files_parsed': json_paths, 'preserved_original_count': len(preserved['files']),
        'reference_only_git_blob_checks': reference_checks,
        'executed_controls': runs, 'controls_executed': 2,
        'imported_spinoza_code_executed': False, 'lean_or_kernel_replay': False,
        'network_or_installation_requested': False, 'package_bytes_unchanged': True,
        'scope': 'Byte integrity and finite Python illustrations only. No philosophical premise certification, new theorem, research closure, integration, acceptance, or historical-duration certification.'}
    with (output / 'REPLAY_RECEIPT.json').open('x', encoding='utf-8') as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'status': 'PASS', 'controls_executed': 2,
                      'receipt': str(output / 'REPLAY_RECEIPT.json')}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(type(error).__name__ + ': ' + str(error), file=sys.stderr)
        sys.exit(1)

#!/usr/bin/env python3
"""Guarded shared-proof attainment supplement integrity-only verifier. Executes no source research code.

Python 3.8+ standard library. No network, installation, sources, theorem prover,
imported research program or earlier checkpoint archive is required.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


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
    require(manifest['supplement_id'] == 'guarded-shared-proof-attainment-supplement-20261009', 'Wrong supplement identity.')
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
    forbidden_parts = {'sources', 'research-intermediates', 'reading', 'scan-controls', 'user_notes',
                       'agent_notes', 'dream_notes', '__pycache__', 'read-selections', 'development'}
    for text in before:
        p = safe_path(text)
        require(p.name != 'REFLECTIVE_NOTES.md', 'Excluded working notes in package.')
        require(not (set(p.parts) & forbidden_parts), 'Excluded directory in package: ' + text)
        require(p.suffix.lower() in {'.md', '.json', '.jsonl', '.sha256', '.py', '.sh', '.lean', '.log', '.txt', '.zip', '.sha256sums'}
                or text in {'third-party/mathlib/LICENSE', 'executable-guarded-table-kernel-20261009/LICENSE.mathlib', 'constructive-guarded-witness-kernel-20261009/LICENSE.mathlib'} or p.name in {'SHA256SUMS', 'REVIEW_SHA256SUMS'} or text == 'replay/verify_portable.py',
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
        elif text.endswith('.jsonl'):
            for number, line in enumerate((root / text).read_text(encoding='utf-8').splitlines(), 1):
                require(bool(line.strip()), 'Empty JSONL record: ' + text)
                json.loads(line, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
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
    require(prior['anchor_checkpoint'] == 24 and prior['artifact_name'] == 'T20_Shared_Proof_Cost_and_Information_Update_20261009', 'Wrong predecessor checkpoint.')
    if 'archive_sha256' in delivery:
        require(delivery['archive_sha256'] == prior['archive']['sha256'], 'Prior delivery hash mismatch.')
    else:
        require(any(row.get('file_name') == prior['archive']['name']
                    and row.get('status') == 'succeeded' for row in delivery['results']),
                'Prior delivery archive filename mismatch.')
    checksums_path = str(safe_path(prior['exact_checksums_record_copy']))
    require(before[checksums_path]['sha256'] == prior['checksums_record_sha256'],
            'Prior checksum record identity mismatch.')
    prior_sums = dict((name, h) for h, name in
                      (line.split('  ', 1) for line in (root / checksums_path).read_text().splitlines()))
    require(prior_sums[prior['archive']['name']] == prior['archive']['sha256'],
            'Prior archive checksum mismatch.')
    require(before[delivery_path]['sha256'] == prior['delivery_record_sha256'],
            'Predecessor delivery record mismatch.')
    scope = read_json(root / 'SCOPE_AND_HISTORY.json')
    for key in ('research_closed', 'integrated', 'owner_accepted',
                'historical_duration_certified', 'new_theorem_or_kernel_result_claimed',
                'research_code_executed', 'packaging_credited_as_research'):
        require(scope[key] is False, 'Unsupported scope claim: ' + key)
    require(scope['status'] == 'INTERMEDIATE_T20_ACTIVE', 'Research must remain active.')
    delta = read_json(root / 'DELTA_MANIFEST.json')
    require(delta['supplement_id'] == 'guarded-shared-proof-attainment-supplement-20261009' and delta['predecessor_anchor_checkpoint'] == 24 and delta['predecessor_artifact'] == prior['artifact_name'], 'Wrong delta identity.')
    for component in delta['components']:
        for row in component['entrypoints']:
            text = str(safe_path(row['path']))
            require(before[text]['sha256'] == row['sha256'], 'Delta entrypoint hash mismatch.')
    for row in delta['root_readback_entrypoints']:
        text = str(safe_path(row['path']))
        require(before[text] == {'bytes': row['bytes'], 'sha256': row['sha256']},
                'Root entrypoint identity mismatch.')
    provenance = read_json(root / 'THIRD_PARTY_PROVENANCE.json')
    require(provenance['status'] == 'NO_THIRD_PARTY_LIBRARY_SOURCE_VENDORED'
            and provenance['distributed_source_paths'] == [], 'Wrong third-party distribution declaration.')
    require(not any(PurePosixPath(p).suffix == '.lean' for p in before),
            'Unexpected Lean source in no-new-Lean distribution.')
    replay_inputs = read_json(root / 'LOCAL_REPLAY_INPUTS.json')
    inherited = read_json(root / 'guarded-shared-dag-attainment-20261009/INPUT_HASHES.json')
    require(len(replay_inputs['files']) == 2, 'Wrong replay-input count.')
    for row in replay_inputs['files']:
        path = str(safe_path(row['path']))
        require(before[path] == {'bytes': row['bytes'], 'sha256': row['sha256']}
                and inherited[path] == row['sha256'], 'Local replay-input binding mismatch.')
    # Independently enumerate the unchanged component manifests, including their original path conventions.
    derived = []
    for ap in preserved_paths:
        p = root / ap
        if ap.startswith('prior-checkpoint-identities/'):
            continue
        rows = []
        if p.name in {'MANIFEST.sha256', 'FILES.sha256', 'SHA256SUMS', 'REVIEW_SHA256SUMS'}:
            for line in p.read_text(encoding='utf-8').splitlines():
                if line.strip():
                    h, n = line.split('  ', 1)
                    rows.append({'path': n, 'sha256': h})
        elif p.name == 'MANIFEST.json':
            data = read_json(p)
            rows = data.get('files', data.get('artifacts', []))
            if isinstance(rows, dict):
                rows = [{'path': n, 'sha256': h} for n, h in rows.items()]
            if isinstance(data.get('sha256'), dict):
                rows = [{'path': n, 'sha256': h} for n, h in data['sha256'].items()]
        for row in rows:
            n = str(safe_path(row['path']))
            top = PurePosixPath(ap).parts[0]
            relative = n if PurePosixPath(n).parts[0] == top else str(PurePosixPath(ap).parent / n)
            present = relative in before
            derived.append((ap, n, relative, row['sha256'], present))
            if present:
                require(before[relative]['sha256'] == row['sha256'], 'Original component hash mismatch.')
                if 'bytes' in row:
                    require(before[relative]['bytes'] == row['bytes'], 'Original component size mismatch.')
    recorded = [(r['component_manifest'], r['original_binding_path'], r['archive_path'],
                 r['expected_sha256'], r['distributed']) for r in component_checks['entries']]
    require(derived == recorded, 'Component-binding inventory mismatch.')
    after, after_dirs = snapshot(root)
    require(before == after and before_dirs == after_dirs,
            'Package changed during verification.')
    # No filesystem output is created until all checks above pass.
    output.mkdir(parents=True, exist_ok=False)
    receipt = {
        'status': 'PASS',
        'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'supplement_id': 'guarded-shared-proof-attainment-supplement-20261009',
        'distributed_file_count': len(before),
        'exact_file_and_directory_inventory_verified': True,
        'manifest_hashes_and_sizes_verified': True,
        'manifest_and_payload_checksum_inventory_verified': True,
        'json_and_jsonl_files_parsed': parsed,
        'preserved_original_count': len(preserved['files']),
        'component_manifest_entries_checked': len(component_checks['entries']),
        'component_manifest_omitted_witnesses_not_required': True,
        'prior_supplement_delivery_and_archive_identity_consistent': True,
        'third_party_distribution_declaration_verified': True,
        'two_exact_local_predecessor_replay_inputs_verified': True,
        'original_component_binding_inventory_verified': True,
        'delta_and_root_entrypoints_hash_verified': True,
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

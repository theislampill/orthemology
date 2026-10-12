#!/usr/bin/env python3
"""Scoped offline integrity/source-binding checks and isolated mathematical replay.

This is a preservation checker, not a whole-source extraction or proof checker.
The default run does not acquire or reconstruct omitted Word/PDF/full-book files.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import subprocess
import sys


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def resolve(root, name):
    p = PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name:
        raise ValueError('unsafe relative path: ' + name)
    target = root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('unsafe relative path: ' + name)
    return target


def match(path, expected):
    if not path.is_file():
        raise ValueError('missing bound file: ' + str(path))
    actual = digest(path)
    if any(actual[k] != expected[k] for k in ('sha256', 'bytes') if k in expected):
        raise ValueError('digest mismatch: ' + str(path))
    return actual


def verify_integrity(root):
    files = read_json(root / 'MANIFEST.json')['files']
    for name, record in files.items():
        match(resolve(root, name), record)
    return len(files)


def new_output(out):
    if out.exists():
        raise ValueError('replay output already exists: ' + str(out))
    out.mkdir(parents=True)


def entries(manifest):
    data = manifest['files']
    return list(data.items()) if isinstance(data, dict) else [(r['path'], r) for r in data]


def verify_bindings(root):
    workspace = root / 'workspace'
    scope = read_json(root / 'SCOPE.json')
    omitted = {r['original_path']: r for r in scope['external_resources']}
    checked = {'nested_manifest_bundled': 0, 'nested_manifest_external_bindings': 0,
               'direct_bundled_bindings': 0, 'direct_external_bindings': 0}

    def binding(name, expected, bundled_key, external_key):
        path = resolve(workspace, name)
        if path.is_file():
            match(path, expected); checked[bundled_key] += 1
        else:
            record = omitted.get(name)
            if not record or any(record[k] != expected[k] for k in ('bytes', 'sha256') if k in expected):
                raise ValueError('unaccounted missing source binding: ' + name)
            checked[external_key] += 1

    for name in scope['packet_manifests']:
        parent = PurePosixPath(name).parent
        for child, record in entries(read_json(resolve(workspace, name))):
            binding(str(parent / child), record, 'nested_manifest_bundled', 'nested_manifest_external_bindings')
    for record in scope['final_review_manifests']:
        match(resolve(workspace, record['path']), record)
    for name, key in scope['binding_records']:
        record = read_json(resolve(workspace, name))
        rows = record if key is None else record[key]
        for row in rows:
            binding(row['path'], row, 'direct_bundled_bindings', 'direct_external_bindings')
    preservation = read_json(root / 'ORIGINALS_BEFORE_AFTER.json')
    if preservation['before'] != preservation['after'] or not preservation['all_unchanged']:
        raise ValueError('original preservation record is not byte-identical')
    for name, record in preservation['before'].items():
        binding(name, record, 'direct_bundled_bindings', 'direct_external_bindings')
    return checked


def verify_source_scope(root):
    base = root / 'workspace' / 'sufficient-reasons-contrast-20261010' / 'sources'
    text = (base / 'SHIFA_EDITED_2_180_188.txt').read_text(encoding='utf-8')
    images = [f'page-{n}.png' for n in range(180, 189)] + [f'title-{n:03d}.png' for n in range(1, 4)]
    for image in images:
        if not (base / image).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('invalid preserved PNG signature: ' + image)
    for page in range(180, 189):
        if f'(2/{page})' not in text:
            raise ValueError('missing edited page marker: ' + str(page))
    source = (base / 'SHIFA_RECEIVED_e213_e216.txt').read_text(encoding='utf-8')
    for page in range(213, 217):
        if f'ص -{page}-' not in source:
            raise ValueError('missing received page marker: ' + str(page))
    return {'preserved_edited_page_images': 9, 'preserved_title_or_frontmatter_images': 3,
            'edited_excerpt_page_markers': list(range(180, 189)),
            'received_excerpt_page_markers': list(range(213, 217)),
            'status': 'Excerpt/image integrity and source bindings checked; no fresh raw Word/PDF extraction or visual reading asserted.'}


def verify_external(root, external_root):
    scope = read_json(root / 'SCOPE.json')
    for record in scope['external_resources']:
        match(resolve(external_root, record['original_path']), record)
    base = external_root / 'sufficient-reasons-contrast-20261010' / 'sources'
    decoded = (base / 'shifa-edited.doc').read_bytes().decode('utf-16le', errors='replace')
    a = decoded.index('(2/179)') + len('(2/179)')
    b = decoded.index('(2/188)', a) + len('(2/188)')
    selected = decoded[a:b].replace('\v', '\n').replace('\x01', '').replace('\r\n', '\n').replace('\r', '\n')
    retained = root / 'workspace' / 'sufficient-reasons-contrast-20261010' / 'sources'
    if selected.encode('utf-8') != (retained / 'SHIFA_EDITED_2_180_188.txt').read_bytes():
        raise ValueError('external Word selection does not match exact retained excerpt')
    received = (external_root / 'particular-determination-semantics-20261010' / 'sources' / 'shifa003.txt').read_text(encoding='utf-8')
    selected = received[received.index('ص -213-'):received.index('ص -217-')].strip()
    if selected != (retained / 'SHIFA_RECEIVED_e213_e216.txt').read_text(encoding='utf-8').strip():
        raise ValueError('external received-text selection does not match retained excerpt')
    return {'external_resources_byte_verified': len(scope['external_resources']),
            'fresh_bounded_word_extraction_exact': True,
            'fresh_bounded_received_extraction_boundary_trim_equal': True,
            'pdf_rerender_performed': False,
            'scope': 'Optional local raw-resource verification and selected text extraction only; no network, OCR, or whole-volume reading.'}


def computational_content(record):
    return {key: value for key, value in record.items() if key not in ('python', 'sympy')}


def replay_math(root, out):
    import sympy
    new_output(out)
    workspace = out / 'workspace'
    shutil.copytree(root / 'workspace', workspace)
    logs = out / 'logs'; logs.mkdir()
    operations = [
        ('author', 'leafwise-noetic-geometry-20261010/verify.py', 'CONTROL_RESULTS.json', 43, 'control_groups'),
        ('independent', 'leafwise-noetic-review-20261010/independent_controls.py', 'INDEPENDENT_CONTROL_RESULTS.json', 37, 'assertions'),
        ('reviewer-author-snapshot', 'leafwise-noetic-review-20261010/author-replay/verify.py', 'CONTROL_RESULTS.json', 43, 'control_groups'),
    ]
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    for label, name, output_name, count, key in operations:
        script = resolve(workspace, name)
        original_output = resolve(root / 'workspace', str(PurePosixPath(name).parent / output_name))
        expected = read_json(original_output)
        run = subprocess.run([sys.executable, str(script)], cwd=script.parent, env=env, text=True, capture_output=True)
        (logs / (label + '.stdout.txt')).write_text(run.stdout, encoding='utf-8')
        (logs / (label + '.stderr.txt')).write_text(run.stderr, encoding='utf-8')
        if run.returncode:
            raise ValueError(label + ' replay failed; see ' + str(logs))
        output = script.parent / output_name
        actual = read_json(output)
        if actual.get(key) != count or not actual.get('all_passed') or computational_content(actual) != computational_content(expected):
            raise ValueError(label + ' replay result differs from bound controls')
        results.append({'label': label, 'groups': count, 'passed': True,
                        'computational_content_equal': True,
                        'output_byte_identical': digest(output) == digest(original_output),
                        'output': digest(output)})
    return {'python': platform.python_version(), 'sympy': sympy.__version__, 'runs': results,
            'scope': 'Exact finite controls, not formal-kernel proofs or empirical validation.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--out', type=Path, help='New, absent directory for isolated mathematical replay and receipt')
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--external-root', type=Path, help='Optional existing original workspace with all SHA-bound omitted resources; no download is attempted')
    args = parser.parse_args()
    root = args.root.resolve()
    receipt = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'manifest': digest(root / 'MANIFEST.json'),
               'integrity_files': verify_integrity(root),
               'bindings': verify_bindings(root), 'source_scope': verify_source_scope(root),
               'raw_resources_in_portable_bundle': False,
               'default_fresh_raw_source_extraction_replayed': False}
    if args.external_root:
        receipt['optional_external_check'] = verify_external(root, args.external_root.resolve())
    if not args.integrity_only:
        if args.out is None:
            parser.error('--out must name a new directory unless --integrity-only is used')
        receipt['mathematical_replay'] = replay_math(root, args.out.resolve())
        receipt['post_replay_integrity_files'] = verify_integrity(root)
        (args.out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, ImportError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)

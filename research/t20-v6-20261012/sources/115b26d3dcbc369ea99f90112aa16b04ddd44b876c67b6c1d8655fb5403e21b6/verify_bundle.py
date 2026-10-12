#!/usr/bin/env python3
"""Offline exact-byte preservation checks and isolated finite SymPy replays.

This checks a compact evidence archive, not a general theorem in a formal kernel.
Only new copies are executed. No dependency is downloaded or installed.
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
    if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts:
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
    extras = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()} - set(files) - {'MANIFEST.json'}
    if extras:
        raise ValueError('uninventoried files: ' + ', '.join(sorted(extras)))
    return len(files)


def new_output(out):
    if out.exists():
        raise ValueError('replay output already exists: ' + str(out))
    out.mkdir(parents=True)


def entries(manifest):
    data = manifest['files']
    return list(data.items()) if isinstance(data, dict) else [(r['path'], r) for r in data]


def verify_script_dependencies(workspace, records):
    count = 0
    for record in records:
        match(resolve(workspace, record['script']['path']), record['script'])
        for dependency in record['dependencies']:
            match(resolve(workspace, dependency['path']), dependency)
            count += 1
    return {'scripts': len(records), 'dependency_bindings': count}


def verify_bindings(root):
    workspace = root / 'workspace'
    scope = read_json(root / 'SCOPE.json')
    checked = {'nested_manifest_files': 0, 'direct_bindings': 0, 'freeze_bindings': 0}
    for name in scope['packet_manifests']:
        parent = PurePosixPath(name).parent
        for child, record in entries(read_json(resolve(workspace, name))):
            match(resolve(workspace, str(parent / child)), record)
            checked['nested_manifest_files'] += 1
    for record in scope['freeze_bindings']:
        match(resolve(workspace, record['path']), record)
        checked['freeze_bindings'] += 1
    for record in scope['binding_records']:
        data = read_json(resolve(workspace, record['path']))
        rows = data if record.get('key') is None else data[record['key']]
        for row in rows:
            match(resolve(workspace, str(PurePosixPath(record.get('base', '.')) / row[record.get('path_key', 'path')])), row)
            checked['direct_bindings'] += 1
    preservation = read_json(root / 'ORIGINALS_BEFORE_AFTER.json')
    if preservation['before'] != preservation['after'] or not preservation['all_unchanged']:
        raise ValueError('original preservation record is not byte-identical')
    for name, record in preservation['before'].items():
        match(resolve(workspace, name), record)
    checked['preserved_original_files'] = len(preservation['before'])
    checked['script_dependencies'] = verify_script_dependencies(workspace, scope['script_dependency_bindings'])
    declared = {r['script']['path'] for r in scope['script_dependency_bindings']}
    actual = {str(p.relative_to(workspace)) for p in workspace.rglob('*.py')}
    if actual != declared:
        raise ValueError('script dependency coverage mismatch')
    return checked


def computational_content(record):
    ignored = {'python', 'sympy', 'platform', 'python_version', 'sympy_version'}
    return {key: value for key, value in record.items() if key not in ignored}


def replay_math(root, out):
    import sympy
    new_output(out)
    operations = read_json(root / 'SCOPE.json')['replay_operations']
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
    results = []
    for operation in operations:
        label = operation['label']
        run_root = resolve(out, label)
        workspace = run_root / 'workspace'
        shutil.copytree(root / 'workspace', workspace)
        substitutions = {'workspace': str(workspace), 'run': str(run_root)}
        def expanded(name):
            return name.format(**substitutions)
        command_results = []
        for index, command in enumerate(operation['commands'], 1):
            script = resolve(workspace, command['script'])
            args = [expanded(x) for x in command.get('args', [])]
            process = subprocess.run([sys.executable, '-B', str(script), *args], cwd=script.parent,
                                     env=env, capture_output=True, text=True)
            (run_root / ('command-%d.stdout.txt' % index)).write_text(process.stdout, encoding='utf-8')
            (run_root / ('command-%d.stderr.txt' % index)).write_text(process.stderr, encoding='utf-8')
            if process.returncode:
                raise ValueError(label + ' replay failed; see ' + str(run_root))
            command_results.append({'script': command['script'], 'args': command.get('args', []), 'exit_code': 0})
        result = {'label': label, 'commands': command_results, 'role': operation['role'], 'comparisons': []}
        for comparison in operation['comparisons']:
            output = Path(expanded(comparison['actual']))
            original = resolve(root / 'workspace', comparison['preserved'])
            item = {'actual': comparison['actual'], 'preserved': comparison['preserved'],
                    'output': digest(output), 'output_byte_identical': digest(output) == digest(original)}
            if comparison.get('json'):
                actual, expected = read_json(output), read_json(original)
                for key, value in comparison.get('expected_fields', {}).items():
                    if actual.get(key) != value:
                        raise ValueError(label + ' expected count/status mismatch: ' + key)
                actual, expected = computational_content(actual), computational_content(expected)
                if comparison.get('normalize_python_command'):
                    actual['command'][0] = expected['command'][0] = '<python executable>'
                if actual != expected:
                    raise ValueError(label + ' computational content mismatch: ' + comparison['actual'])
                item['computational_content_equal'] = True
                item['expected_fields'] = comparison.get('expected_fields', {})
            elif not item['output_byte_identical']:
                raise ValueError(label + ' output bytes differ: ' + comparison['actual'])
            result['comparisons'].append(item)
        for check in operation.get('receipts', []):
            actual = read_json(Path(expanded(check['path'])))
            if any(actual.get(k) != v for k,v in check['expected_fields'].items()):
                raise ValueError(label + ' replay receipt fields differ')
            result.setdefault('receipts', []).append({'path': check['path'], 'checked_fields': check['expected_fields']})
        results.append(result)
        print('PASS ' + label, file=sys.stderr, flush=True)
    return {'python': platform.python_version(), 'sympy': sympy.__version__,
            'operations': results,
            'scope': 'Fresh exact finite controls and binding checks only; snapshots are replays, not additional independent reviews.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--out', type=Path, help='New absent directory outside the package for isolated replay')
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    receipt = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'manifest': digest(root / 'MANIFEST.json'),
               'integrity_files': verify_integrity(root), 'bindings': verify_bindings(root)}
    if not args.integrity_only:
        if args.out is None:
            parser.error('--out must name a new directory unless --integrity-only is used')
        out = args.out.resolve()
        if out.is_relative_to(root):
            raise ValueError('replay output must be outside the frozen package')
        receipt['mathematical_replay'] = replay_math(root, out)
        receipt['post_replay_integrity_files'] = verify_integrity(root)
        (out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, ImportError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)

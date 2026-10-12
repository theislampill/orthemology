#!/usr/bin/env python3
"""Verify exact evidence bytes; optionally extract or replay in fresh directories.

Python 3.10+ standard library only. Verification does not execute component code.
Supply an independently received MANIFEST.json digest for authenticity binding.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

MAX_ENTRIES = 50000
MAX_FILE_BYTES = 100 * 1024 * 1024
MAX_TOTAL_BYTES = 500 * 1024 * 1024
MAX_PATH_UNITS = 240  # conservative legacy Windows full-path extraction ceiling
RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|CLOCK\$|COM[0-9¹²³]|LPT[0-9¹²³])$', re.I)

class Invalid(ValueError):
    pass

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def path_units(s):
    return len(s.encode('utf-16-le')) // 2

def safe_path(name, directory=False):
    if not isinstance(name, str) or not name or name.startswith(('/', '\\')) or '\\' in name:
        raise Invalid(f'unsafe path: {name!r}')
    bare = name[:-1] if directory and name.endswith('/') else name
    parts = bare.split('/')
    for p in parts:
        if not p or p in ('.', '..') or p.endswith(('.', ' ')) or any(ord(c) < 32 or ord(c) == 127 or c in '<>:"|?*' for c in p):
            raise Invalid(f'unsafe path: {name!r}')
        if RESERVED.fullmatch(p.split('.')[0]):
            raise Invalid(f'Windows reserved name: {name!r}')
    if path_units(bare) > MAX_PATH_UNITS:
        raise Invalid(f'Windows path length exceeds {MAX_PATH_UNITS}: {name!r}')
    return bare

def check_namespace(items):
    """Reject aliases, implicit-directory collisions and file/dir overlaps."""
    seen, kinds, explicit = {}, {}, set()
    for name, directory in items:
        bare = safe_path(name, directory)
        if bare in explicit:
            raise Invalid(f'duplicate member: {name}')
        explicit.add(bare)
        parts = bare.split('/')
        for idx in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:idx])
            key = unicodedata.normalize('NFC', prefix).casefold()
            if key in seen and seen[key] != prefix:
                raise Invalid(f'casefold collision: {seen[key]} / {prefix}')
            seen[key] = prefix
            kind = 'directory' if directory or idx < len(parts) else 'file'
            if key in kinds and kinds[key] != kind:
                raise Invalid(f'file/directory conflict: {prefix}')
            kinds[key] = kind

def disk_inventory(root):
    names = set()
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            if p.is_symlink():
                raise Invalid(f'symlink in collection: {p.relative_to(root)}')
            if not p.is_dir() and not p.is_file():
                raise Invalid(f'nonregular file in collection: {p.relative_to(root)}')
        for name in files:
            names.add((Path(base) / name).relative_to(root).as_posix())
    return names

def verify_archive(path, component):
    entries = component['entries']
    check_namespace([(e['path'], e.get('directory', False)) for e in entries])
    expected = {e['path']: e for e in entries}
    prefix = component.get('strip_prefix', '')
    if prefix:
        if not prefix.endswith('/'):
            raise Invalid('strip prefix must name a wrapper directory and end in /')
        safe_path(prefix, True)
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        if len(infos) > MAX_ENTRIES:
            raise Invalid('archive entry limit exceeded')
        check_namespace([(i.filename, i.is_dir()) for i in infos])
        if set(expected) != {i.filename for i in infos}:
            raise Invalid(f'member inventory mismatch: {path.name}')
        if sum(i.file_size for i in infos) > MAX_TOTAL_BYTES:
            raise Invalid('archive decompressed size limit exceeded')
        output_names = []
        max_relative = 0
        for i in infos:
            mode = i.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise Invalid(f'archive symlink: {i.filename}')
            kind = stat.S_IFMT(mode)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise Invalid(f'archive nonregular member: {i.filename}')
            if kind == stat.S_IFDIR and not i.is_dir():
                raise Invalid(f'archive nonregular directory encoding: {i.filename}')
            if i.flag_bits & 1:
                raise Invalid(f'encrypted member is unsupported: {i.filename}')
            if i.file_size > MAX_FILE_BYTES:
                raise Invalid(f'archive member size limit exceeded: {i.filename}')
            if not i.filename.startswith(prefix):
                raise Invalid(f'strip prefix mismatch: {i.filename}')
            stripped = i.filename[len(prefix):]
            if not stripped and not i.is_dir():
                raise Invalid('strip prefix cannot remove a non-directory member')
            if stripped:
                safe_path(stripped, i.is_dir())
                output_names.append((stripped, i.is_dir()))
                max_relative = max(max_relative, path_units(component['id'] + '/' + stripped.rstrip('/')))
            data = z.read(i)  # validates CRC, decompresses to bounded declared size
            expected_entry = expected[i.filename]
            if len(data) != expected_entry['bytes'] or sha256(data) != expected_entry['sha256'] or i.is_dir() != expected_entry.get('directory', False):
                raise Invalid(f'member hash/size mismatch: {i.filename}')
        check_namespace(output_names)
    return {'id': component['id'], 'entries': len(entries), 'uncompressed_bytes': sum(e['bytes'] for e in entries), 'max_extracted_relative_units': max_relative}

def verify(root, manifest_sha256=None):
    if root.is_symlink():
        raise Invalid('symlink collection root')
    manifest_path = root / 'MANIFEST.json'
    if manifest_path.is_symlink():
        raise Invalid('symlink manifest')
    raw = manifest_path.read_bytes()
    if manifest_sha256 is not None and sha256(raw) != manifest_sha256.lower():
        raise Invalid('manifest digest mismatch')
    m = json.loads(raw)
    if m.get('schema') != 'orthemology.seventh.collection.v1':
        raise Invalid('unsupported manifest schema')
    files = m['files']
    check_namespace([(e['path'], False) for e in files] + [('MANIFEST.json', False)])
    actual = disk_inventory(root)
    expected = {e['path'] for e in files} | {'MANIFEST.json'}
    if actual != expected:
        raise Invalid(f'inventory mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
    expected_dirs = {'/'.join(name.split('/')[:n]) for name in expected for n in range(1, len(name.split('/')))}
    actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    if actual_dirs != expected_dirs:
        raise Invalid(f'directory inventory mismatch: missing={sorted(expected_dirs-actual_dirs)}, extra={sorted(actual_dirs-expected_dirs)}')
    for e in files:
        path = root / e['path']
        if path.stat().st_size > MAX_FILE_BYTES:
            raise Invalid(f'file size limit exceeded: {e["path"]}')
        data = path.read_bytes()
        if len(data) != e['bytes'] or sha256(data) != e['sha256']:
            raise Invalid(f'hash/size mismatch: {e["path"]}')
    components = m['components']
    check_namespace([(c['id'], True) for c in components])
    records, component_paths = [], set()
    for c in components:
        safe_path(c['path'])
        if c['path'] not in expected or c['path'] == 'MANIFEST.json' or c['path'] in component_paths:
            raise Invalid('component archive missing, duplicated or unbound')
        component_paths.add(c['path'])
        records.append(verify_archive(root / c['path'], c))
    return m, {'status': 'VERIFIED', 'manifest_sha256': sha256(raw), 'files': len(files), 'components': records}

def fresh_destination(dest, root):
    if dest.exists() or dest.is_symlink():
        raise Invalid(f'destination already exists: {dest}')
    dest = dest.absolute()
    if not dest.parent.is_dir():
        raise Invalid('destination parent must already exist')
    resolved = dest.resolve()
    if resolved == root.resolve() or root.resolve() in resolved.parents:
        raise Invalid('output must be outside the immutable collection')
    return resolved

def extract(root, manifest, dest):
    dest = fresh_destination(dest, root)
    for c in manifest['components']:
        for e in c['entries']:
            relative = e['path'][len(c.get('strip_prefix', '')):].rstrip('/')
            if relative and path_units(str(dest / c['id'] / relative)) > MAX_PATH_UNITS:
                raise Invalid(f'Windows full path length exceeds {MAX_PATH_UNITS}; choose a shorter destination: {relative}')
    stage = Path(tempfile.mkdtemp(prefix='.seventh-extract-', dir=dest.parent))
    try:
        for c in manifest['components']:
            for e in c['entries']:
                relative = e['path'][len(c.get('strip_prefix', '')):].rstrip('/')
                if relative and path_units(str(stage / c['id'] / relative)) > MAX_PATH_UNITS:
                    raise Invalid(f'Windows staging path length exceeds {MAX_PATH_UNITS}; choose a shorter destination parent: {relative}')
            base = stage / c['id']
            base.mkdir()
            with zipfile.ZipFile(root / c['path']) as z:
                for e in c['entries']:
                    relative = e['path'][len(c.get('strip_prefix', '')):]
                    if not relative:
                        continue
                    target = base / relative
                    if e.get('directory', False):
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        data = z.read(e['path'])
                        with target.open('xb') as out:
                            out.write(data)
                        if sha256(target.read_bytes()) != e['sha256']:
                            raise Invalid(f'post-extraction hash mismatch: {e["path"]}')
        if dest.exists():
            raise Invalid('destination appeared during extraction; refusing overwrite')
        stage.rename(dest)
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise
    return dest

def verify_extracted(extracted, manifest):
    expected, directories = {}, set()
    for c in manifest['components']:
        directories.add(c['id'])
        for e in c['entries']:
            part = e['path'][len(c.get('strip_prefix', '')):].rstrip('/')
            if not part:
                continue
            name = c['id'] + '/' + part
            if e.get('directory', False):
                directories.add(name)
            else:
                expected[name] = e
            directories.update('/'.join(name.split('/')[:i]) for i in range(1, len(name.split('/'))))
    try:
        actual = disk_inventory(extracted)
        actual_dirs = {p.relative_to(extracted).as_posix() for p in extracted.rglob('*') if p.is_dir()}
        if actual != set(expected) or actual_dirs != directories:
            raise Invalid('inventory changed')
        for name, e in expected.items():
            p = extracted / name
            if p.stat().st_size != e['bytes'] or sha256(p.read_bytes()) != e['sha256']:
                raise Invalid(f'bytes changed: {name}')
    except (Invalid, OSError) as error:
        raise Invalid(f'extracted input integrity failure: {error}') from error


def terminal_path(spec_path, values, must_exist=False):
    # Lexical roots are captured before commands. Never resolve them through a
    # newly introduced symlink, and never follow a link during cleanup/read.
    path = Path(os.path.abspath(expand(spec_path, values)))
    anchor = Path(values['replay_root'])
    allowed = [Path(os.path.abspath(values[k])) for k in ('out', 'build')]
    if not any(path == base or base in path.parents for base in allowed) or anchor not in path.parents:
        raise Invalid('terminal evidence must stay within the original fresh replay output')
    chain = list(reversed(path.relative_to(anchor).parents))
    for relative in chain:
        ancestor = anchor / relative
        try:
            mode = ancestor.lstat().st_mode
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(mode):
            raise Invalid(f'terminal evidence symlink ancestor: {ancestor}')
        if not stat.S_ISDIR(mode):
            raise Invalid(f'terminal evidence non-directory ancestor: {ancestor}')
    try:
        info = path.lstat()
    except FileNotFoundError:
        if must_exist:
            raise Invalid(f'terminal evidence missing after generating command: {path}')
        return path, None
    if stat.S_ISLNK(info.st_mode):
        raise Invalid(f'terminal evidence symlink: {path}')
    if not stat.S_ISREG(info.st_mode):
        raise Invalid(f'terminal evidence must be a regular file: {path}')
    if info.st_size > MAX_FILE_BYTES:
        raise Invalid('terminal evidence size limit exceeded')
    return path, info


def read_terminal(path):
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(path, flags)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise Invalid('terminal evidence must be a regular file')
        if info.st_size > MAX_FILE_BYTES:
            raise Invalid('terminal evidence size limit exceeded')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise Invalid('terminal evidence size limit exceeded')
        return data
    finally:
        os.close(descriptor)


def expand(token, values):
    for key, value in values.items():
        token = token.replace('{' + key + '}', str(value))
    if re.search(r'\{(?:python|lean|lean_bin|mathlib|out|component|build|extracted|mathlib_archive)\}', token):
        raise Invalid(f'unresolved replay argument: {token}')
    return token

def run_commands(commands, cwd, values, logdir, after_command, results=None):
    if results is None:
        results = []
    logdir.mkdir(parents=True, exist_ok=True)
    for number, spec in enumerate(commands):
        argv = [expand(arg, values) for arg in spec['argv']]
        for key, arguments in spec.get('optional_args', {}).items():
            if key in values:
                argv.extend(expand(arg, values) for arg in arguments)
        env = os.environ.copy()
        env['PYTHONDONTWRITEBYTECODE'] = '1'
        env.update({key: expand(value, values) for key, value in spec.get('env', {}).items()})
        work = Path(expand(spec.get('cwd', str(cwd)), values))
        prepared = set()
        for expected in spec.get('expect_json', []):
            target, info = terminal_path(expected['path'], values)
            if target not in prepared and info is not None:
                target.unlink()
            prepared.add(target)
        log = logdir / f'{number:02d}.log'
        try:
            p = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=spec.get('timeout_seconds', 1800))
        except subprocess.TimeoutExpired as error:
            data = error.stdout or b''
            if isinstance(data, str):
                data = data.encode('utf-8')
            if error.stderr:
                data += error.stderr.encode('utf-8') if isinstance(error.stderr, str) else error.stderr
            log.write_bytes(data)
            results.append({'command': argv, 'exit_code': None, 'status': 'TIMEOUT', 'resource_inconclusive': True, 'log': str(log), 'log_sha256': sha256(data), 'timeout_seconds': spec.get('timeout_seconds', 1800)})
            after_command()
            raise Invalid(f'command wall-clock timeout; resource outcome INCONCLUSIVE; see {log}') from error
        log.write_bytes(p.stdout)
        results.append({'command': argv, 'exit_code': p.returncode, 'log_sha256': sha256(p.stdout)})
        after_command()
        if p.returncode != 0:
            raise Invalid(f'replay/validation command failed with exit {p.returncode}; see {log}')
        terminal = []
        for expected in spec.get('expect_json', []):
            evidence_path, _ = terminal_path(expected['path'], values, must_exist=True)
            data = read_terminal(evidence_path)
            value = json.loads(data)
            try:
                for key in expected['field'].split('.'):
                    if isinstance(value, list):
                        value = len(value) if key == 'length' else value[int(key)]
                    else:
                        value = value[key]
            except (KeyError, TypeError, ValueError, IndexError) as error:
                raise Invalid(f'terminal evidence missing field: {expected["field"]}') from error
            if value != expected['equals']:
                raise Invalid(f'terminal evidence mismatch: {expected["field"]} is {value!r}, expected {expected["equals"]!r}')
            terminal.append({'path': str(evidence_path), 'sha256': sha256(data), 'field': expected['field'], 'value': value, 'status': 'MATCH'})
        if terminal:
            results[-1]['terminal_evidence'] = terminal
    return results

def replay(root, manifest, extracted, selected, lean_bin, mathlib, mathlib_archive, out, verify_only=False):
    out = fresh_destination(out, root)
    if out == extracted or extracted in out.parents:
        raise Invalid('replay output must be outside extracted component inputs')
    requested = {c['id'] for c in manifest['components']} if selected == ['all'] else set(selected)
    known = {c['id'] for c in manifest['components']}
    if requested - known:
        raise Invalid('unknown component selection: ' + ', '.join(sorted(requested-known)))
    out.mkdir()
    output_identity = (out.stat().st_dev, out.stat().st_ino)
    input_manifest_sha256 = sha256((root / 'MANIFEST.json').read_bytes())
    def unchanged_inputs():
        verify_extracted(extracted, manifest)
        verify(root, input_manifest_sha256)
    unchanged_inputs()
    receipt = {'status': 'RUNNING', 'components': []}
    receipt_path = out / 'COLLECTION_REPLAY.json'
    try:
        for c in manifest['components']:
            if c['id'] not in requested:
                continue
            base = extracted / c['id']
            values = {'python': sys.executable, 'component': base, 'extracted': extracted, 'replay_root': out, 'out': out / c['id'] / 'output', 'build': out / c['id'] / 'work'}
            if lean_bin:
                values.update(lean_bin=lean_bin.resolve(), lean=lean_bin.resolve() / ('lean.exe' if os.name == 'nt' else 'lean'))
            if mathlib:
                values['mathlib'] = mathlib.resolve()
            if mathlib_archive:
                values['mathlib_archive'] = mathlib_archive.resolve()
            commands = c.get('verify_commands', []) if verify_only else c.get('replay_commands', [])
            entry = {'id': c['id'], 'kind': 'COMPONENT_PACKAGING_VALIDATION' if verify_only else 'REPLAY', 'status': 'NO_EXECUTABLE_ENTRYPOINT' if not commands else 'RUNNING'}
            receipt['components'].append(entry)
            if commands:
                if c.get('replay_workspace_copy') and not verify_only:
                    shutil.copytree(base, values['build'])
                try:
                    entry['commands'] = []
                    run_commands(commands, base, values, out / c['id'] / 'logs', unchanged_inputs, entry['commands'])
                    entry['status'] = 'PASS'
                except BaseException as error:
                    entry['status'] = 'FAILED'
                    entry['error'] = str(error)
                    raise
        receipt['status'] = 'PASS_WITH_DECLARED_NONEXECUTABLE_COMPONENTS'
    except BaseException as error:
        receipt['status'] = 'FAILED_OR_INCOMPLETE'
        receipt['error'] = str(error)
        raise
    finally:
        info = out.lstat()
        if not stat.S_ISDIR(info.st_mode) or (info.st_dev, info.st_ino) != output_identity:
            raise Invalid('replay output root replaced; refusing receipt write')
        if receipt_path.is_symlink() or (receipt_path.exists() and not stat.S_ISREG(receipt_path.lstat().st_mode)):
            raise Invalid('unsafe replay receipt destination; refusing write')
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--manifest-sha256')
    parser.add_argument('--extract-to', type=Path)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--validate-components', nargs='+', metavar='ID')
    group.add_argument('--replay', nargs='+', metavar='ID')
    parser.add_argument('--lean-bin', type=Path)
    parser.add_argument('--mathlib', type=Path)
    parser.add_argument('--mathlib-archive', type=Path, help='Exact pinned official Mathlib source archive, for optional controls source-archive mode')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    try:
        m, result = verify(args.root, args.manifest_sha256)
        print(json.dumps(result, indent=2))
        if args.replay or args.validate_components:
            if not args.extract_to or not args.out:
                raise Invalid('component validation/replay requires --extract-to and --out, both absent directories')
        if args.extract_to:
            extracted = extract(args.root, m, args.extract_to)
            print('EXTRACTED:', extracted)
            if args.replay or args.validate_components:
                receipt = replay(args.root, m, extracted, args.replay or args.validate_components, args.lean_bin, args.mathlib, args.mathlib_archive, args.out, bool(args.validate_components))
                print(receipt['status'])
        return 0
    except (Invalid, OSError, KeyError, TypeError, ValueError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        print('REJECTED:', error, file=sys.stderr)
        return 1
if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Hosted-only, reversible 1,180-source alias absence regression.

Uses one exact existing CI checkout. Protected bodies remain metadata-only.
The complete public/index/directory state is restored after success or failure.
Consumer results do not themselves qualify scientific acceptance or retirement.
"""
from pathlib import Path
import argparse
import contextlib
import datetime
import errno
import hashlib
import importlib.util
import json
import os
import re
import runpy
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import traceback
import uuid

MANIFEST = 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
GENERATED = ['docs/project-closure/ar8r-v11/SHA256SUMS', 'docs/current-state.yaml',
             'docs/provenance/RELEASE-MANIFEST.sha256']
EXCLUDED258 = 'experiments/orthemology-v5-continuations/source-store/b4d8348961420e0b0ec7459d0ddc0276090fb34349e6b26823ac90afb8ef4183.lean'
PUBLIC_HELPERS = {
    'guard.py': 'scripts/source_alias_absence_guard.py',
    'metadata.py': 'scripts/source_alias_absence_metadata.py',
    '258.py': 'scripts/source_alias_absence_continuations.py',
    'reader_adapter.py': 'scripts/source_alias_absence_reader.py',
    'population.py': 'scripts/source_alias_absence_population.py',
    'boundary.py': 'scripts/source_alias_absence_boundary.py',
    'context.py': 'scripts/source_alias_absence_context.py',
    'evidence.py': 'scripts/source_alias_absence_evidence.py',
}
PHASES = ['metadata', '824', 'owners', '258-source_objects', '258-legacy_suites',
          '258-preservation', '258-t20_graph', '98', '258-reader', '258-reference',
          'public-references', 'negative-controls', 'post-controls']


def require(value, message):
    if not value:
        raise RuntimeError(message)


def identity(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()}


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()


def fsync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def ordinary_dir(path):
    path = Path(path).absolute()
    for item in [path, *path.parents]:
        require(not item.is_symlink(), 'Symlink directory: ' + str(item))
    require(path.is_dir(), 'Missing ordinary directory: ' + str(path))
    return path


def mkdir_durable(path):
    path = Path(path)
    if path.exists():
        ordinary_dir(path)
        return
    mkdir_durable(path.parent)
    path.mkdir()
    fsync_dir(path.parent)


def atomic_bytes(path, body, mode=0o600, *, replace=False):
    """Durably install bytes; immutable evidence refuses accidental replacement."""
    path = Path(path)
    mkdir_durable(path.parent)
    require(not os.path.lexists(path) or replace, 'Refuse evidence overwrite: ' + str(path))
    require(not path.is_symlink(), 'Refuse symlink destination')
    fd, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        if not replace:
            os.link(temporary, path)
            os.unlink(temporary)
        else:
            os.replace(temporary, path)
        fsync_dir(path.parent)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def save(path, value, *, replace=False):
    atomic_bytes(path, json_bytes(value), replace=replace)


def mutation_write(repo, state, relative, body, mode, protected=()):
    """Journal the exact temporary name before any product-directory creation."""
    target = repo / '.git/index' if relative == '.git/index' else safe_path(repo, relative, protected=protected)
    require(not target.is_symlink(), 'Symlink mutation target')
    mkdir_durable(target.parent)
    token = uuid.uuid4().hex
    temporary = target.parent / ('.' + target.name + '.combined1180.' + token + '.tmp')
    save(state / 'writes' / (token + '.json'), {'target': relative,
         'temporary': temporary.relative_to(repo).as_posix(), 'body': identity(body), 'mode': mode})
    fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        fsync_dir(target.parent)
    finally:
        if os.path.lexists(temporary):
            temporary.unlink()
            fsync_dir(temporary.parent)


def cleanup_owned_temporaries(repo, state, allowed, protected):
    for record in sorted((state / 'writes').glob('*.json')):
        item = json.loads(record.read_bytes())
        relative = item['target']
        require(relative in allowed or relative == '.git/index', 'Unreceived mutation target in journal')
        target = repo / '.git/index' if relative == '.git/index' else safe_path(repo, relative, protected=protected)
        temporary = target.parent / ('.' + target.name + '.combined1180.' + record.stem + '.tmp')
        require(item['temporary'] == temporary.relative_to(repo).as_posix(), 'Temporary journal path differs')
        if os.path.lexists(temporary):
            info = temporary.lstat()
            require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Unexpected temporary file identity')
            temporary.unlink()
            fsync_dir(temporary.parent)


def safe_path(root, relative, *, protected=(), allow_missing=True):
    require(isinstance(relative, str) and relative and not relative.startswith('/')
            and '\\' not in relative and all(x not in ('', '.', '..') for x in relative.split('/')),
            'Unsafe relative path')
    require(relative not in protected and not relative.startswith('.git/'), 'Protected mutation/read path')
    path = Path(root)
    for part in relative.split('/')[:-1]:
        path /= part
        require(not path.is_symlink(), 'Symlink parent: ' + str(path))
        if path.exists():
            require(path.is_dir(), 'Non-directory parent')
        else:
            require(allow_missing, 'Missing parent')
    return Path(root) / relative


def proc_metadata(path):
    """Use mounted-proc coordinates, which may differ from the caller PID namespace."""
    path = Path(path)
    first = (path / 'stat').read_text()
    tail = first.rsplit(')', 1)[1].split()
    proc_pid = int(first.split(' ', 1)[0])
    namespace_ids = {}
    for line in (path / 'status').read_text().splitlines():
        key, separator, values = line.partition(':')
        if separator and key in ('NSpid', 'NSpgid', 'NSsid'):
            namespace_ids[key] = [int(value) for value in values.split()]
    require(all(namespace_ids.get(key) for key in ('NSpid', 'NSpgid', 'NSsid')), 'Missing PID namespace metadata')
    result = {'pid': namespace_ids['NSpid'][-1], 'proc_pid': proc_pid, 'state': tail[0],
              'ppid': int(tail[1]), 'proc_pgid': int(tail[2]), 'proc_sid': int(tail[3]),
              'pgid': namespace_ids['NSpgid'][-1], 'sid': namespace_ids['NSsid'][-1], 'start_ticks': tail[19]}
    result['pid_namespace'] = os.readlink(path / 'ns/pid') if result['state'] != 'Z' else None
    again = (path / 'stat').read_text().rsplit(')', 1)[1].split()
    require(again[19] == tail[19] and again[2:4] == tail[2:4], 'Process identity changed during receiving')
    return result


def identity_from_proc(row):
    return {key: row[key] for key in ('pid', 'proc_pid', 'start_ticks', 'pid_namespace')}


def validate_process_record(value):
    require(isinstance(value, dict) and set(value) == {'pid', 'proc_pid', 'start_ticks', 'pid_namespace'},
            'Missing recorded process identity cannot prove quiescence')
    require(all(type(value[key]) is int and value[key] > 0 for key in ('pid', 'proc_pid'))
            and isinstance(value['start_ticks'], str) and value['start_ticks'].isdecimal()
            and isinstance(value['pid_namespace'], str)
            and re.fullmatch(r'pid:\[[0-9]+\]', value['pid_namespace']) is not None,
            'Malformed recorded process identity')


def validate_group_record(value):
    require(isinstance(value, dict) and set(value) == {'process', 'pgid', 'sid', 'proc_pgid', 'proc_sid'},
            'Malformed recorded group identity')
    validate_process_record(value['process'])
    require(all(type(value[key]) is int and value[key] > 0 for key in ('pgid', 'sid', 'proc_pgid', 'proc_sid')),
            'Malformed recorded group coordinates')


def process_identity(pid=None):
    pid = os.getpid() if pid is None else pid
    require(pid == os.getpid(), 'Receive another process through its durable self-identity handshake')
    own = proc_metadata('/proc/self')
    require(own['pid'] == pid, 'Current PID namespace cannot be resolved')
    return identity_from_proc(own)


def live_process(value):
    validate_process_record(value)
    try:
        row = proc_metadata('/proc/' + str(value['proc_pid']))
    except OSError as error:
        if error.errno in (errno.ENOENT, errno.ESRCH):
            return False
        raise
    if row['state'] == 'Z':
        return False
    return identity_from_proc(row) == value


def group_record(pid=None):
    identity = process_identity(pid)
    require(identity is not None, 'Cannot record an unavailable process')
    row = proc_metadata('/proc/' + str(identity['proc_pid']))
    require(identity_from_proc(row) == identity, 'Process changed before group receipt')
    return {'process': identity, **{key: row[key] for key in ('pgid', 'sid', 'proc_pgid', 'proc_sid')}}


def group_members(group):
    members = []
    validate_group_record(group)
    with os.scandir('/proc') as entries:
        for entry in entries:
            if not entry.name.isdigit():
                continue
            try:
                # Both the group and its entire owned session are received.
                # Only a process that vanished during this scan may be skipped.
                tail = (Path(entry.path) / 'stat').read_text().rsplit(')', 1)[1].split()
                if int(tail[2]) == group['proc_pgid'] or int(tail[3]) == group['proc_sid']:
                    members.append(proc_metadata(entry.path))
            except OSError as error:
                if error.errno not in (errno.ENOENT, errno.ESRCH):
                    raise
    return sorted(members, key=lambda row: row['proc_pid'])


def receive_quiescence(state, *, allow_current=False):
    received = []
    own = process_identity()
    for path in sorted((state / 'groups').glob('*.json')):
        group = json.loads(path.read_bytes())
        validate_group_record(group)
        require(group['pgid'] == group['sid'] == group['process']['pid']
                and group['proc_pgid'] == group['proc_sid'] == group['process']['proc_pid'],
                'Recorded session leader coordinates differ')
        members = group_members(group)
        active = [r for r in members if r['state'] != 'Z' and not
                  (allow_current and group['process'] == own and identity_from_proc(r) == own)]
        if live_process(group['process']) and group['process'] != own and not any(
                identity_from_proc(row) == group['process'] for row in members):
            active.append({'escaped_recorded_leader': group['process']})
        received.append({'record': str(path), 'group': group, 'observed_members': members, 'active_members': active})
    return {'groups': received, 'quiescent': not any(row['active_members'] for row in received)}


@contextlib.contextmanager
def operation_lock(state, operation, *, recover=False):
    lock = state / 'operation.lock'
    if lock.exists():
        old = json.loads(lock.read_bytes())
        require(recover and not live_process(old['process']), 'Live or unreceived operation lock')
        received = receive_quiescence(state, allow_current=True)
        save(state / 'quiescence' / (uuid.uuid4().hex + '.json'), received)
        require(received['quiescent'], 'Recorded native/consumer process group still active; establish quiescence first')
        os.rename(lock, state / ('stale-lock-' + uuid.uuid4().hex + '.json'))
        fsync_dir(state)
    own = {'operation': operation, 'process': process_identity(), 'group': group_record(), 'token': uuid.uuid4().hex}
    require(own['group']['pgid'] == own['process']['pid'] == own['group']['sid'], 'Harness must own its session/process group')
    save(state / 'groups' / (own['token'] + '.json'), own['group'])
    atomic_bytes(lock, json_bytes(own))
    try:
        yield own
    finally:
        if lock.exists() and json.loads(lock.read_bytes()) == own:
            lock.unlink()
            fsync_dir(state)


def sanitized_env():
    env = dict(os.environ)
    for key in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR', 'GIT_OBJECT_DIRECTORY',
                'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_CONFIG_PARAMETERS'):
        env.pop(key, None)
    for key in list(env):
        if key.startswith(('GIT_CONFIG_KEY_', 'GIT_CONFIG_VALUE_')):
            env.pop(key)
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1',
               GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null', PYTHONDONTWRITEBYTECODE='1',
               GIT_CONFIG_COUNT='4', GIT_CONFIG_KEY_0='core.fsmonitor', GIT_CONFIG_VALUE_0='false',
               GIT_CONFIG_KEY_1='core.hooksPath', GIT_CONFIG_VALUE_1='/dev/null',
               GIT_CONFIG_KEY_2='gc.auto', GIT_CONFIG_VALUE_2='0',
               GIT_CONFIG_KEY_3='maintenance.auto', GIT_CONFIG_VALUE_3='false')
    return env


def git(repo, *args, shadow=False, state=None):
    env = sanitized_env()
    command = ['git', '--no-replace-objects', '--literal-pathspecs', *args]
    if args[0] in ('add', 'update-index'):
        require(state is not None and not shadow, 'Native index mutation must be journaled')
        save(state / 'native-index-mutations' / (uuid.uuid4().hex + '.json'),
             {'repo': str(repo), 'command': command, 'group': group_record(), 'process': process_identity()})
    if shadow:
        require(state is not None, 'Shadow index requires external state directory')
        with tempfile.TemporaryDirectory(prefix='shadow-index-', dir=state) as temporary:
            index = Path(temporary) / 'index'
            index.write_bytes((repo / '.git/index').read_bytes())
            env['GIT_INDEX_FILE'] = str(index)
            return subprocess.run(command, cwd=repo, env=env, check=True, capture_output=True).stdout
    return subprocess.run(command, cwd=repo, env=env, check=True, capture_output=True).stdout


def stage_map(repo):
    raw = git(repo, 'ls-files', '--stage', '-z')
    rows = {}
    for entry in raw.split(b'\0'):
        if entry:
            meta, name = entry.split(b'\t', 1)
            mode, oid, level = meta.decode().split()
            path = name.decode()
            require(level == '0' and path not in rows, 'Conflicted or repeated index path')
            rows[path] = (mode, oid)
    return raw, rows


def held_stat(root, held):
    result = {}
    for row in held:
        path = safe_path(root, row['path'], allow_missing=False)
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and not info.st_mode & 0o111
                and info.st_size == row['bytes'], 'Held ordinary metadata changed')
        result[row['path']] = {name: getattr(info, name) for name in
                              ('st_dev', 'st_ino', 'st_nlink', 'st_size', 'st_mode', 'st_mtime_ns', 'st_ctime_ns')}
    return result


def receive_module(path, name, expected=None):
    body = Path(path).read_bytes()
    require(expected is None or identity(body)['sha256'] == expected, 'Authenticated helper changed')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(body, str(path), 'exec'), module.__dict__)
    return module


def install_guard(repo, state):
    held = json.loads((state / 'inputs/hold.json').read_bytes())['held']
    module = helper_module(state, 'guard.py', 'hosted_source_held_guard')
    guard = module.HeldBodyGuard()
    guard.add(repo, held)
    guard.install()
    return held, guard


def vector(repo, state, held, *, expected_paths=None):
    """Complete public body/mode/directory vector; never opens a held body."""
    raw_index = (repo / '.git/index').read_bytes()
    require(not os.path.lexists(repo / '.git/index.lock'), 'Native Git index lock is present')
    stage, entries = stage_map(repo)
    protected = {row['path']: row for row in held}
    held_oids = {row['published_metadata']['git_blob'] for row in held}
    require({p for p, (_, oid) in entries.items() if oid in held_oids} == set(protected), 'Held index alias population differs')
    rows = []
    for path, (mode, oid) in sorted(entries.items()):
        p = safe_path(repo, path, allow_missing=False)
        info = p.lstat()
        row = {'path': path, 'index_mode': mode, 'index_oid': oid,
               'mode': stat.S_IMODE(info.st_mode), 'bytes': info.st_size}
        if path in protected:
            known = protected[path]
            require(mode == known['published_metadata']['mode'] and oid == known['published_metadata']['git_blob']
                    and stat.S_ISREG(info.st_mode) and not info.st_mode & 0o111
                    and info.st_size == known['bytes'], 'Held path identity metadata differs')
            row['body_receiving'] = 'EXCLUDED_HELD'
        else:
            require(stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode), 'Unsupported tracked file type')
            actual_mode = '120000' if stat.S_ISLNK(info.st_mode) else ('100755' if info.st_mode & 0o111 else '100644')
            require(actual_mode == mode, 'Index/worktree mode differs: ' + path)
            body = os.fsencode(os.readlink(p)) if stat.S_ISLNK(info.st_mode) else p.read_bytes()
            row.update(identity(body))
            require(row['git_blob'] == oid, 'Index/worktree body differs: ' + path)
            if stat.S_ISLNK(info.st_mode):
                row['symlink_target'] = os.fsdecode(body)
        rows.append(row)
    leaves, directories = set(), []
    for directory, dirs, files in os.walk(repo, followlinks=False):
        parent = Path(directory)
        if parent == repo:
            dirs[:] = [name for name in dirs if name != '.git']
        directories.append({'path': parent.relative_to(repo).as_posix(), 'mode': stat.S_IMODE(parent.stat().st_mode)})
        for name in files + [name for name in dirs if (parent / name).is_symlink()]:
            leaves.add((parent / name).relative_to(repo).as_posix())
    require(leaves == set(entries), 'Untracked or absent filesystem entries')
    require(expected_paths is None or leaves == set(expected_paths), 'Exact path-set changed')
    tree = git(repo, 'write-tree', shadow=True, state=state).decode().strip()
    require((repo / '.git/index').read_bytes() == raw_index, 'Read-only observation changed raw index')
    return {'rows': rows, 'directories': sorted(directories, key=lambda r: r['path']),
            'raw_index': identity(raw_index), 'index_mode': stat.S_IMODE((repo / '.git/index').stat().st_mode),
            'stage': identity(stage), 'head': git(repo, 'rev-parse', 'HEAD').decode().strip(), 'tree': tree,
            'held_stat': held_stat(repo, held)}


def save_preimages(repo, state, paths, protected):
    result = []
    for relative in sorted(set(paths)):
        path = safe_path(repo, relative, protected=protected, allow_missing=False)
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Preimage must be an ordinary unaliased public file')
        body = path.read_bytes()
        meta = identity(body)
        target = state / 'bodies' / meta['sha256']
        if target.exists():
            require(identity(target.read_bytes()) == meta, 'Existing backup body differs')
        else:
            atomic_bytes(target, body)
        result.append({'path': relative, **meta, 'mode': stat.S_IMODE(info.st_mode)})
    atomic_bytes(state / 'original-index', (repo / '.git/index').read_bytes())
    save(state / 'preimages.json', result)
    return result


def validate_backups(state, prepared):
    map_body = saved_input_path(state, 'preimages.json').read_bytes()
    require(identity(map_body) == prepared['preimages'], 'Preimage map changed')
    require(identity(saved_input_path(state, 'original-index').read_bytes()) == prepared['raw_index'],
            'Raw index backup changed')
    rows = json.loads(map_body)
    for row in rows:
        require(isinstance(row['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', row['sha256']) is not None,
                'Invalid backup body identity')
        body = saved_input_path(state, 'bodies/' + row['sha256']).read_bytes()
        require(identity(body) == {k: row[k] for k in ('bytes', 'sha256', 'git_blob')}, 'Preimage body changed')
    return rows


def restore_preimages(repo, state, prepared, before, protected):
    """Idempotent durable restore; validates every backup before its first write."""
    rows = validate_backups(state, prepared)
    for row in rows:
        path = safe_path(repo, row['path'], protected=protected)
        require(not path.is_symlink() and (not path.exists() or path.is_file()), 'Unsafe restore destination')
    cleanup_owned_temporaries(repo, state, {r['path'] for r in rows}, protected)
    for row in sorted(before['directories'], key=lambda r: (len(Path(r['path']).parts), r['path'])):
        relative = row['path']
        path = repo if relative == '.' else safe_path(repo, relative, protected=protected)
        mkdir_durable(path)
    for row in rows:
        path = safe_path(repo, row['path'], protected=protected)
        mutation_write(repo, state, row['path'], (state / 'bodies' / row['sha256']).read_bytes(), row['mode'], protected)
    for row in sorted(before['directories'], key=lambda r: (-len(Path(r['path']).parts), r['path'])):
        path = repo if row['path'] == '.' else safe_path(repo, row['path'], protected=protected)
        path.chmod(row['mode'])
        fsync_dir(path)
    mutation_write(repo, state, '.git/index', (state / 'original-index').read_bytes(), before['index_mode'], protected)


def recover_native_boundary(repo, state, prepared, attempt):
    """Receive all owned groups and quarantine a proven stale trial index lock."""
    quiet = receive_quiescence(state, allow_current=True)
    save(attempt / 'QUIESCENCE.json', quiet)
    require(quiet['quiescent'], 'Owned process groups are still active; no restore writes allowed')
    lock = repo / '.git/index.lock'
    if not os.path.lexists(lock):
        return
    mutations = sorted((state / 'native-index-mutations').glob('*.json'))
    require(prepared['index_lock_before'] == 'ABSENT' and (state / 'EXECUTION-START.json').exists()
            and mutations, 'Unowned index.lock is not quarantinable')
    known_groups = [row['group'] for row in quiet['groups']]
    for path in mutations:
        row = json.loads(path.read_bytes())
        require(row['repo'] == str(repo) and row['group'] in known_groups
                and row['command'][:3] == ['git', '--no-replace-objects', '--literal-pathspecs']
                and row['command'][3] in ('add', 'update-index'), 'Unreceived native mutation intent')
    info = lock.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Unsafe index.lock')
    body = lock.read_bytes()
    atomic_bytes(attempt / 'index.lock.quarantine', body)
    after = lock.lstat()
    require((info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'Lock changed while receiving quarantine')
    save(attempt / 'INDEX-LOCK-QUARANTINE.json', {'identity': identity(body),
         'mode': stat.S_IMODE(info.st_mode), 'native_mutation_intents': [str(p) for p in mutations],
         'scope': 'Previously absent lock in sole-writer trial after all recorded groups are quiescent'})
    lock.unlink()
    fsync_dir(lock.parent)


def class_rows(state):
    rows = json.loads((state / 'classes.json').read_bytes())
    aliases = {row['alias'] for row in rows}
    retained = {row['canonical'] for row in rows}
    require(len(rows) == len(aliases) == 1180 and len(retained) == 1082 and not aliases & retained,
            'Combined finite membership differs')
    require({name: sum(row['cohort'] == name for row in rows) for name in ('824', '258', '98')}
            == {'824': 824, '258': 258, '98': 98} and EXCLUDED258 not in aliases,
            'Combined class or exclusion differs')
    require({row['canonical'] for row in rows if row['cohort'] == '98'} <=
            {row['canonical'] for row in rows if row['cohort'] == '824'}, 'Shared retained population differs')
    return rows


def runtime():
    import importlib.metadata
    require(sys.version_info[:3] == (3, 11, 9) and __debug__, 'Exact normal CPython3.11.9 required')
    packages = {name: importlib.metadata.version(name) for name in ('markdown-it-py', 'PyYAML')}
    require(packages == {'markdown-it-py': '4.0.0', 'PyYAML': '6.0.3'}, 'Qualified runtime packages changed')
    return {'executable': sys.executable, 'version': sys.version, 'packages': packages}


def authenticate_state(repo, state):
    prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
    require(prepared['repo'] == str(repo) and prepared['state'] == str(state), 'Prepared root binding changed')
    info = repo.stat()
    require(prepared['repo_inode'] == [info.st_dev, info.st_ino], 'Prepared root replaced')
    require(identity(Path(__file__).read_bytes()) == prepared['harness'], 'Harness bytes changed; use saved exact harness for recovery')
    for relative, digest in prepared['input_files'].items():
        require(identity(saved_input_path(state, relative).read_bytes()) == digest, 'Prepared input changed: ' + relative)
    before_body = saved_input_path(state, 'before.json').read_bytes()
    require(identity(before_body) == prepared['before'], 'Prepared full vector changed')
    require(admit_hosted_checkout(repo, state, fresh=False, saved=True) == prepared['admission'], 'Hosted run admission changed')
    before = json.loads(before_body)
    validate_backups(state, prepared)
    require(runtime() == prepared['runtime'], 'Runtime changed')
    return prepared, before


def prepare(repo, state):
    runtime_record = runtime()
    admission = admit_hosted_checkout(repo, state, fresh=True)
    mkdir_durable(state)
    save(state / 'ADMISSION.json', admission)
    with operation_lock(state, 'prepare'):
        require(not os.path.lexists(repo / '.git/index.lock'), 'Preexisting index lock is not owned by this trial')
        _, stage = stage_map(repo)
        received, helpers = {}, {}
        for name, relative in PUBLIC_HELPERS.items():
            path = safe_path(repo, relative, allow_missing=False)
            info = path.lstat()
            require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
                    and info.st_nlink == 1, 'Helper must be an ordinary current public file')
            body = path.read_bytes()
            digest = identity(body)
            expected = ('100644 blob ' + digest['git_blob'] + '\t' + relative).encode() + b'\0'
            require(stage.get(relative) == ('100644', digest['git_blob'])
                    and git(repo, 'ls-tree', '-z', 'HEAD', '--', relative) == expected,
                    'Helper differs from the exact checkout commit or index')
            atomic_bytes(state / 'inputs' / name, body)
            received['inputs/' + name] = digest
            helpers[name] = dict(digest, source_path=relative)
        save(state / 'inputs/SOURCE-IDENTITIES.json', helpers)
        received['inputs/SOURCE-IDENTITIES.json'] = identity((state / 'inputs/SOURCE-IDENTITIES.json').read_bytes())
        population = helper_module(state, 'population.py', 'source_alias_absence_population')
        boundary = helper_module(state, 'boundary.py', 'hosted_prepared_boundary')
        context = helper_module(state, 'context.py', 'hosted_prepared_context')
        originals = population.original_tree(repo)
        require(set(originals) <= set(stage), 'Original census is not completely present before the trial')
        manifest = {}
        for line in (repo / GENERATED[2]).read_text().splitlines():
            digest, relative = line.split('  ', 1)
            require(relative not in manifest, 'Duplicate release-manifest path')
            manifest[relative] = digest
        held = boundary.derive_held_metadata(repo, originals, stage, manifest)
        save(state / 'inputs/hold.json', {'held': held, 'held_worktree_body_integrity': 'UNKNOWN'})
        received['inputs/hold.json'] = identity((state / 'inputs/hold.json').read_bytes())
        held, guard = install_guard(repo, state)
        protected = {row['path'] for row in held}
        classes = population.derive_classes(repo)
        require(not protected & {row[key] for row in classes for key in ('alias', 'canonical')}, 'Protected member selected')
        required = population.derive_required(repo, classes)
        required_rows = []
        for relative in required:
            value = population.public_identity(repo, relative, originals[relative])
            required_rows.append({'path': relative, 'identity': {'bytes': value['bytes'], 'sha256': value['sha256'],
                'git_blob': value['blob'], 'mode': value['mode']}})
        save(state / 'inputs/33.json', required_rows)
        save(state / 'inputs/98-context.json', context.derive_context(repo, classes))
        for relative in ('inputs/33.json', 'inputs/98-context.json', 'ADMISSION.json'):
            received[relative] = identity((state / relative).read_bytes())
        harness = Path(__file__).read_bytes()
        require(stage.get('scripts/check_source_alias_absence.py') == ('100644', identity(harness)['git_blob']),
                'Harness differs from the current checkout index')
        atomic_bytes(state / 'inputs/harness.py', harness)
        received['inputs/harness.py'] = identity(harness)
        adapter = helper_module(state, 'reader_adapter.py', 'hosted_prepared_reader_adapter')
        with adapter.bounded_git_environment():
            boundary = adapter.install(repo, held)
            save(state / 'READER-BOUNDARY-PREFLIGHT.json', boundary.receipt())
        before = vector(repo, state, held)
        require(before['head'] == admission['head']
                and before['tree'] == git(repo, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                'Current complete checkout differs from the admitted hosted commit')
        rows = {row['path']: row for row in before['rows']}
        for row in classes:
            for key in ('alias', 'canonical'):
                current = rows[row[key]]
                require((current['sha256'], current['bytes'], current['git_blob'], current['index_mode'], current['mode']) ==
                        (row['sha256'], row['bytes'], row['blob'], row['mode'], 0o644), 'Finite public source differs')
        save(state / 'before.json', before)
        save(state / 'classes.json', classes)
        received['classes.json'] = identity((state / 'classes.json').read_bytes())
        preimages = save_preimages(repo, state, {row[key] for row in classes for key in ('alias', 'canonical')}
                                  | set(GENERATED), protected)
        require(len(preimages) == 2265, 'Restoration preimage count differs')
        require((repo / '.git/index').read_bytes() == (state / 'original-index').read_bytes(), 'Index changed during backup')
        require(vector(repo, state, held) == before and guard.denials == 0, 'Preparation observation or boundary drift')
        info = repo.stat()
        prepared = {'schema': 'hosted-source-alias-durable-preparation-v1', 'status': 'PREPARED_NO_ABSENCE',
            'repo': str(repo), 'state': str(state), 'repo_inode': [info.st_dev, info.st_ino],
            'head': admission['head'], 'tree': before['tree'], 'admission': admission, 'runtime': runtime_record,
            'harness': identity(harness), 'input_files': received, 'before': identity((state / 'before.json').read_bytes()),
            'preimages': identity((state / 'preimages.json').read_bytes()),
            'raw_index': identity((state / 'original-index').read_bytes()), 'original_census_paths': len(originals),
            'originals': 1180, 'unique_canonicals': 1082, 'preimage_paths': 2265,
            'tracked_before': len(before['rows']), 'expected_absent_tracked': len(before['rows']) - 1180,
            'held_denials': guard.denials, 'held_worktree_body_integrity': 'UNKNOWN', 'index_lock_before': 'ABSENT'}
        save(state / 'PREPARED.json', prepared)
        print(json.dumps({'status': prepared['status'], 'preimages': len(preimages),
                          'prepared': identity((state / 'PREPARED.json').read_bytes())}))


def restore(repo, state, *, held=None, guard=None):
    prepared, before = authenticate_state(repo, state)
    if held is None:
        held, guard = install_guard(repo, state)
    require(held_stat(repo, held) == before['held_stat'],
            'Held metadata changed; stop before restore writes')
    require(git(repo, 'rev-parse', 'HEAD').decode().strip() == before['head'], 'Trial HEAD changed')
    attempt = state / 'restoration' / uuid.uuid4().hex
    mkdir_durable(attempt)
    save(attempt / 'START.json', {'mode': 'RECOVER_ONLY', 'prepared': identity((state / 'PREPARED.json').read_bytes())})
    try:
        recover_native_boundary(repo, state, prepared, attempt)
        restore_preimages(repo, state, prepared, before, {r['path'] for r in held})
        after = vector(repo, state, held, expected_paths={r['path'] for r in before['rows']})
        require(after == before, 'Complete restored public/index/tree/directory/held-metadata vector differs')
        # No native command follows this final exact index install and byte comparison.
        mutation_write(repo, state, '.git/index', (state / 'original-index').read_bytes(), before['index_mode'], {r['path'] for r in held})
        require((repo / '.git/index').read_bytes() == (state / 'original-index').read_bytes()
                and stat.S_IMODE((repo / '.git/index').stat().st_mode) == before['index_mode'], 'Final raw index differs')
        require(guard.denials == 0, 'Held body request occurred')
        save(attempt / 'after.json', after)
        result = {'status': 'PASS_EXACT_RESTORATION_ONLY', 'after': identity((attempt / 'after.json').read_bytes()),
                  'raw_index': identity((repo / '.git/index').read_bytes()), 'held_denials': guard.denials,
                  'held_worktree_body_integrity': 'UNKNOWN', 'consumers_resumed': False}
        save(attempt / 'TERMINAL.json', result)
        return {'receipt': str(attempt / 'TERMINAL.json'), **result}
    except BaseException as error:
        save(attempt / 'TERMINAL.json', {'status': 'FAIL_RESTORATION', 'error': repr(error), 'traceback': traceback.format_exc()})
        raise


def prune_empty_parents(repo, aliases):
    parents = set()
    for path in aliases:
        parent = (repo / path).parent
        while parent != repo:
            parents.add(parent)
            parent = parent.parent
    removed = []
    for parent in sorted(parents, key=lambda p: (-len(p.parts), str(p))):
        require(not parent.is_symlink(), 'Symlink parent in absence')
        try:
            parent.rmdir()
        except OSError as error:
            if error.errno not in (errno.ENOTEMPTY, errno.EEXIST):
                raise
        else:
            fsync_dir(parent.parent)
            removed.append(parent.relative_to(repo).as_posix())
    return sorted(removed)


def observe_absence(repo, aliases):
    """Receive every selected public path, preserving errors and disagreements."""
    rows = []
    for relative in sorted(aliases):
        target = repo / relative
        row = {'path': relative}
        try:
            info = os.lstat(target)
        except OSError as error:
            row['lstat'] = {'state': 'absent' if error.errno == errno.ENOENT else 'error',
                            'errno': error.errno, 'error': repr(error)}
        else:
            row['lstat'] = {'state': 'present', **{name: getattr(info, name) for name in
                ('st_dev', 'st_ino', 'st_nlink', 'st_size', 'st_mode', 'st_mtime_ns', 'st_ctime_ns')}}
        try:
            row['lexists'] = os.path.lexists(target)
        except OSError as error:
            row['lexists'] = None
            row['lexists_error'] = {'errno': error.errno, 'error': repr(error)}
        row['inconsistent'] = (row['lstat']['state'] == 'absent' and row['lexists'] is not False
                               or row['lstat']['state'] == 'present' and row['lexists'] is not True)
        rows.append(row)
    return {'schema': 'combined1180-public-absence-observation-v1', 'repo': str(repo),
            'observed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'complete': bool(rows) and all(row['lstat']['state'] == 'absent'
                and row['lexists'] is False and not row['inconsistent'] for row in rows), 'rows': rows}


def run_phase(repo, state, phase, aliases):
    out = state / 'phases' / phase
    mkdir_durable(out)
    token = uuid.uuid4().hex
    save(out / 'START.json', {'phase': phase, 'token': token, 'process': process_identity()})
    read_fd, write_fd = os.pipe()
    command = [sys.executable, '-B', str(Path(__file__).absolute()), '_phase', '--repo', str(repo), '--state', str(state), '--phase', phase, '--token', token, '--identity-fd', str(write_fd)]
    with (out / 'stdout.log').open('xb') as log:
        child = subprocess.Popen(command, env=sanitized_env(), stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT, start_new_session=True, pass_fds=(write_fd,))
        os.close(write_fd)
        with os.fdopen(read_fd, 'rb') as receiving:
            child_group = json.loads(receiving.readline())
        require(child_group['process']['pid'] == child.pid == child_group['pgid'] == child_group['sid']
                and child_group['process']['pid_namespace'] == process_identity()['pid_namespace']
                and live_process(child_group['process']), 'Child self-identity does not match its owned session')
        save(state / 'groups' / (token + '.json'), child_group)
        save(out / 'child.json', {'process': child_group['process'], 'group': child_group, 'command': command})
        # Child cannot enter consumer code until its process record is durable.
        try:
            absence = observe_absence(repo, aliases)
            save(out / 'ABSENCE-BEFORE-LEASE.json', absence)
            require(absence['complete'], 'Complete absence before child lease is required')
            child.stdin.write((token + '\n').encode())
            child.stdin.close()
            code = child.wait()
        except BaseException:
            if live_process(child_group['process']):
                os.killpg(child_group['pgid'], signal.SIGTERM)
            try:
                child.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Preserve all evidence and refuse restoration while a group
                # member is alive; never kill a possibly reused unrelated PID.
                pass
            raise
        finally:
            if not child.stdin.closed:
                with contextlib.suppress(BrokenPipeError):
                    child.stdin.close()
            log.flush()
            os.fsync(log.fileno())
    fsync_dir(out)
    members = group_members(child_group)
    save(out / 'QUIESCENCE.json', {'group': child_group, 'observed_members': members,
                                 'quiescent': not any(r['state'] != 'Z' for r in members)})
    terminal = out / 'TERMINAL.json'
    result = {'phase': phase, 'exit_code': code, 'stdout': identity((out / 'stdout.log').read_bytes()),
              'terminal': identity(terminal.read_bytes()) if terminal.exists() else None}
    save(out / 'PROCESS.json', result)
    require(code == 0 and terminal.exists() and not any(r['state'] != 'Z' for r in members), 'Phase failed, has no terminal, or has a live descendant: ' + phase)
    receipt = json.loads(terminal.read_bytes())
    require(receipt['status'] == 'PASS_BOUNDED_PHASE_ONLY' and receipt['held_denials'] == 0, 'Phase boundary failed: ' + phase)
    return result


def execute(repo, state):
    prepared, before = authenticate_state(repo, state)
    held, guard = install_guard(repo, state)
    with operation_lock(state, 'execute'):
        require(not (state / 'EXECUTION-START.json').exists(), 'Trial is single-use; restore rather than resume')
        require(vector(repo, state, held) == before, 'Prepared trial changed')
        classes = class_rows(state)
        aliases = {r['alias'] for r in classes}
        save(state / 'EXECUTION-START.json', {'prepared': identity((state / 'PREPARED.json').read_bytes()), 'process': process_identity(),
                                           'intended_absences': sorted(aliases), 'status': 'STARTED_NOT_TERMINAL'})
        result = {'status': 'RUNNING', 'phases': [], 'held_worktree_body_integrity': 'UNKNOWN'}
        failure = None
        try:
            for relative in sorted(aliases):
                path = safe_path(repo, relative, protected={r['path'] for r in held}, allow_missing=False)
                path.unlink()
                fsync_dir(path.parent)
            observation = observe_absence(repo, aliases)
            save(state / 'ABSENCE-AFTER-UNLINK.json', observation)
            require(observation['complete'], 'Complete absence after unlink is required')
            git(repo, 'update-index', '--force-remove', '--', *sorted(aliases), state=state)
            with (repo / '.git/index').open('rb') as stream:
                os.fsync(stream.fileno())
            fsync_dir(repo / '.git')
            observation = observe_absence(repo, aliases)
            save(state / 'ABSENCE-AFTER-INDEX.json', observation)
            require(observation['complete'], 'Complete absence after index removal is required')
            removed = prune_empty_parents(repo, aliases)
            observation = observe_absence(repo, aliases)
            save(state / 'ABSENCE-AFTER-PRUNE.json', observation)
            require(observation['complete'], 'Complete absence after pruning is required')
            save(state / 'ABSENCE.json', {'absent': sorted(aliases), 'pruned_directories': removed,
                                        'observation': identity((state / 'ABSENCE-AFTER-PRUNE.json').read_bytes())})
            for phase in PHASES:
                result['phases'].append(run_phase(repo, state, phase, aliases))
            absent = vector(repo, state, held, expected_paths={r['path'] for r in before['rows']} - aliases)
            require(len(absent['rows']) == prepared['expected_absent_tracked'], 'Absent denominator differs')
            save(state / 'absent-final.json', absent)
            result['status'] = 'PASS_BOUNDED_CONSUMERS_PENDING_RESTORATION'
        except BaseException as error:
            failure = error
            result.update(status='FAIL_OR_INTERRUPTED', error=repr(error), traceback=traceback.format_exc())
        finally:
            try:
                save(state / 'CONSUMERS-TERMINAL.json', result)
            except BaseException as error:
                failure = failure or error
                result['consumer_terminal_write_error'] = repr(error)
            try:
                quiet = receive_quiescence(state, allow_current=True)
                save(state / 'QUIESCENCE-BEFORE-RESTORE.json', quiet)
                require(quiet['quiescent'], 'Native/consumer group active; restore blocked until quiescent')
                result['restoration'] = restore(repo, state, held=held, guard=guard)
            except BaseException as error:
                failure = failure or error
                result['restoration_error'] = repr(error)
            result['held_denials'] = guard.denials
            result['status'] = 'PASS_BOUNDED_EXECUTION_AND_RESTORATION' if failure is None and not guard.denials else 'FAIL_OR_INTERRUPTED'
            save(state / 'EXECUTION-TERMINAL.json', result)
        print(json.dumps({'status': result['status'], 'terminal': str(state / 'EXECUTION-TERMINAL.json')}))
        if failure is not None:
            raise failure


def metadata_phase(repo, state, held, prepared):
    """Exact v6 two-route metadata adapter; newly derive the changed V11 domain."""
    meta = helper_module(state, 'metadata.py', 'hosted_source_metadata')
    def metadata_git(root, *args, shadow=False):
        require(Path(root).resolve() == repo, 'Unexpected metadata Git root')
        if args == ('ls-files', '--stage', '-z') and not shadow:
            return git(repo, *args)
        expected = ('diff', '--quiet', 'HEAD', '--', *sorted(r['path'] for r in held))
        if args == expected and shadow:
            return git(repo, 'diff', '--cached', '--quiet', 'HEAD', '--', *expected[4:], shadow=True, state=state)
        raise RuntimeError('Unexpected metadata Git operation')
    generator = repo / 'scripts/generate_ar8r_v11_sha256s.py'
    exec(compile(generator.read_bytes(), str(generator), 'exec'), {'__name__': '__main__', '__file__': str(generator)})
    rounds = []
    for _ in (1, 2):
        body, state_receipt = meta.state_bytes(repo, held, metadata_git)
        mutation_write(repo, state, GENERATED[1], body, 0o644, {r['path'] for r in held})
        body, manifest_receipt = meta.manifest_bytes(repo, held, metadata_git)
        mutation_write(repo, state, GENERATED[2], body, 0o644, {r['path'] for r in held})
        for relative in GENERATED:
            with (repo / relative).open('rb') as stream:
                os.fsync(stream.fileno())
        git(repo, 'add', '--', *GENERATED, state=state)
        require(state_receipt['tracked_paths'] == prepared['expected_absent_tracked']
                and manifest_receipt['manifest_rows'] == prepared['expected_absent_tracked'] - 1, 'Generated denominator differs')
        rounds.append({p: identity((repo / p).read_bytes()) for p in GENERATED})
    require(rounds[0] == rounds[1], 'Generated metadata did not converge')
    return {'generated_rounds': rounds, 'state': meta.check_state(repo, held, metadata_git),
            'public_state': meta.check_public_state_surfaces(repo, held, metadata_git),
            'held_worktree_body_integrity': 'UNKNOWN', 'prior_v11_absent_hash_reused': False}


OWNER_PINS = {
    'tests/test_ar8r_v11_reconciliation.py': ('30b8c5ff2679423af0d8231852fd2dd826f91972db891cc461894709d9840606', 91370, '17101e63d0041ba3ad277835933f1e0203ff78a0'),
    'docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-DEEP-A-AP-ADOPTION-BOUNDARY-CORRECTION.md': ('327fd8a2e5ea986f785270f3713e6e034975ecbea9bda2cf5bca04ef374112b6', 1977, 'ea983301a40b60b1180dc4087b68d3e68d0e27ad'),
    'scripts/validate_ar8r_reconciliation.py': ('84cd7f17f9961142e76f76fa427bb49aaf4b29fdc8d9d5056c3c53e8c8c20669', 168547, 'b399786dc10322c5d95b522c4e224e96d0b8cde1'),
    'scripts/validate_research_continuations.py': ('5157341400df0d327cb39f698838ac8ba49f82eb6bf71c8e40f84f670b3e55f7', 29272, 'ef5422f8e877f628e8aedbe61dc4dd2af614cb0a'),
    'docs/project-closure/ar8r-v11/post-merge-proposals/PMR007-ROUNDS11-20-ADOPTION-BOUNDARY-CORRECTION.md': ('66cc0fbc5ab06ab0dfffdb1e6fe1845775cfa0f12233f7517d12042ae16d9486', 1354, '6240db1cb6e2f844506a989ee2cfa14783c6d6d6'),
    'docs/project-closure/ar8r-v11/post-merge-proposals/README.md': ('d20707cf0d24dd5b2b966f2b1f3640ec7672092ef8a19b57f60fc61897cd6b50', 4073, '9628152cf22670418bc2c88aa13e496047fba40c'),
}


def phase824(repo, state, classes, objects):
    import validate_t20_v6_projection as projection
    import resolve_t20_v6_source as resolver
    import validate_ar8r_reconciliation as snapshot
    aliases = {r['alias'] for r in classes if r['cohort'] == '824'}
    rows = {r['source_sha256']: r for r in objects if r.get('repository_path') in aliases}
    require(len(rows) == 584 and snapshot.pmr007_deep_duplicate_paths(repo) == aliases, '824/T20 finite population differs')
    received = []
    for sha, row in rows.items():
        errors = projection.check_object(repo, row)
        body = identity(resolver.source_bytes(repo, row))
        require(not errors and (body['sha256'], body['bytes'], body['git_blob']) ==
                (sha, row['source_bytes'], row['git_blob']), 'Actual824 T20 object failed')
        received.append({'source': sha, 'path': row['repository_path'], 'body': body, 'errors': errors})
    require(snapshot.validate_pmr007_deep_snapshot(repo) == [], 'Actual824 snapshot failed')
    sample = rows[sorted(rows)[0]]
    controls = []
    for field, value in [('repository_revision', 'HEAD'), ('source_sha256', '0' * 64), ('public_bytes', sample['public_bytes'] + 1)]:
        errors = projection.check_object(repo, dict(sample, **{field: value}))
        require(errors, 'Mutated824 identity admitted')
        controls.append({'field': field, 'errors': errors})
    return {'source_paths': 824, 'actual_t20_rows': received, 'negative_controls': controls,
            'historical_red_evidence': 'SEPARATE_EXTERNAL_RECEIPT_NOT_REPLAYED'}


def owner_phase(repo, objects):
    import validate_t20_v6_projection as projection
    selected = [row for row in objects if row.get('repository_path') in OWNER_PINS]
    require(len(selected) == 6, 'Original-owner pin population differs')
    for row in selected:
        sha, size, blob = OWNER_PINS[row['repository_path']]
        require((row['source_sha256'], row['source_bytes'], row['public_sha256'], row['public_bytes'], row['git_blob'], row['repository_revision']) ==
                (sha, size, sha, size, blob, '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'), 'Original-owner pin changed')
        require(projection.check_object(repo, row) == [], 'Original-owner object rejected')
    return {'actual_owner_objects': 6, 'new_owner_objects': 3, 'identities': selected}


def phase98(repo, state, classes):
    import validate_ar8r_reconciliation as snapshot
    selected = {r['alias'] for r in classes if r['cohort'] == '98'}
    require(snapshot.pmr007_rounds_duplicate_paths(repo) == selected, 'Actual98 finite set differs')
    require(snapshot.validate_pmr007_rounds_snapshot(repo) == [], 'Actual98 snapshot rejected')
    navigation = snapshot.pmr007_rounds_formalization_navigation(repo)
    require(snapshot.pmr007_rounds_formalization_navigation(repo, indexed=True) == navigation, 'Independent index navigation differs')
    current_map = snapshot.load_yaml(snapshot.PMR_MAP)
    crosswalk = snapshot.load_yaml(snapshot.FAMILY_CROSSWALK)
    require(snapshot.validate_formalization_owners(current_map, snapshot.load_yaml(snapshot.LEAN_QUEUE),
            snapshot.load_yaml(snapshot.TEN_CONFLICT), crosswalk) == [], 'Current scientific map rejected')
    require(snapshot.validate_pmr007_correction(snapshot.PMR007_CORRECTION.read_text()) == [], 'Actual correction rejected')
    context = json.loads((state / 'inputs/98-context.json').read_bytes())
    # Exact current artifact identity was frozen at prepare; receive the declared
    # nine source_path changes through the product navigation validator, plus
    # the unchanged current Round19 conflict object itself.
    def dictionaries(value):
        if isinstance(value, dict):
            yield value
            for child in value.values():
                yield from dictionaries(child)
        elif isinstance(value, list):
            for child in value:
                yield from dictionaries(child)
    require(context['excluded_conflict_row'] in list(dictionaries(crosswalk)), 'Round19 context conflict changed')
    excluded = context['excluded_locator'].split('#', 1)[0]
    require(excluded not in selected and (repo / excluded).is_file(), 'Round19 exclusion changed')
    rows = {r['path']: r for r in json.loads((state / 'before.json').read_bytes())['rows']}
    for member in json.loads((state / 'inputs/33.json').read_bytes()):
        relative = member['path']
        require(identity((repo / relative).read_bytes()) == {k: rows[relative][k] for k in ('bytes', 'sha256', 'git_blob')}
                and stat.S_IMODE((repo / relative).stat().st_mode) == rows[relative]['mode'], 'Required rounds original changed')
    return {'selected': len(selected), 'required_originals': 33, 'navigation': navigation,
            'scientific_source_field_changes': len(context['changed_formalization_fields']),
            'unchanged_conflict': context['excluded_conflict_row'], 'excluded_locator': context['excluded_locator']}


def public_references(repo, held):
    import validate_internal_references as references
    corpus = references._corpus_files()
    protected = {r['path'] for r in held}
    require(protected <= set(corpus), 'Held reference corpus membership differs')
    selected = [path for path in corpus if path not in protected]
    original = references._corpus_files
    references._corpus_files = lambda: selected[:]
    code = None
    try:
        try:
            references.main()
        except SystemExit as error:
            code = error.code
    finally:
        references._corpus_files = original
    require(code == 0 and not references.FAILS, 'Actual public reference main failed')
    return {'corpus_files': len(selected), 'corpus_paths': selected, 'excluded_held_paths': sorted(protected),
            'failures': references.FAILS, 'exit_code': code, 'full_protected_cli': 'NOT_RUN'}


def negative_controls(repo, state, classes, out):
    import validate_ar8r_reconciliation as snapshot
    import resolve_t20_v6_source as source
    import validate_research_continuations as legacy
    backups = {r['path']: r for r in json.loads((state / 'preimages.json').read_bytes())}
    results = []
    for cohort in ('258', '98'):
        row = sorted((r for r in classes if r['cohort'] == cohort), key=lambda r: r['alias'])[0]
        relative = row['canonical']
        target = safe_path(repo, relative, allow_missing=False)
        backup = backups[relative]
        save(out / ('negative-' + cohort + '-START.json'), {'temporary_retained_absence': relative, 'backup': backup})
        try:
            target.unlink()
            fsync_dir(target.parent)
            if cohort == '258':
                original = source._continuation_copy_catalog(repo)[row['alias']]['sources'][0]
                errors = []
                try:
                    legacy.source_bytes(repo, original)
                except (ValueError, OSError) as error:
                    errors = [repr(error)]
                require(errors, 'Actual continuation missing-copy control admitted')
            else:
                errors = snapshot.validate_pmr007_rounds_snapshot(repo)
                deep_errors = snapshot.validate_pmr007_deep_snapshot(repo)
                require(errors and deep_errors, 'Actual shared retained-copy control admitted')
            result = {'cohort': cohort, 'canonical': relative, 'errors': errors}
            if cohort == '98':
                result['shared824_errors'] = deep_errors
        finally:
            mutation_write(repo, state, relative, (state / 'bodies' / backup['sha256']).read_bytes(), backup['mode'])
            require(identity(target.read_bytes()) == {k: backup[k] for k in ('bytes', 'sha256', 'git_blob')}
                    and stat.S_IMODE(target.stat().st_mode) == backup['mode'], 'Retained control restoration failed')
        result['exact_retained_restoration'] = True
        save(out / ('negative-' + cohort + '-TERMINAL.json'), result)
        results.append(result)
    return {'actual_retained_controls': results, 'excluded_originals_removed': False}


def bounded_phase(repo, state, phase, token, identity_fd):
    # This self-receipt bridges executor PID namespaces without guessing /proc
    # coordinates or inspecting unrelated processes' namespace symlinks.
    with os.fdopen(identity_fd, 'wb') as pipe:
        pipe.write(json.dumps(group_record()).encode() + b'\n')
        pipe.flush()
    # Parent persists PID before sending this one-time lease over stdin.
    require(sys.stdin.readline().rstrip('\n') == token and token, 'Missing durable parent phase lease')
    prepared, before = authenticate_state(repo, state)
    out = state / 'phases' / phase
    require(json.loads((out / 'START.json').read_bytes())['token'] == token, 'Phase lease differs')
    held, guard = install_guard(repo, state)
    receipt = {'phase': phase, 'status': 'RUNNING', 'held_worktree_body_integrity': 'UNKNOWN'}
    boundary = None
    try:
        classes = class_rows(state)
        aliases = {r['alias'] for r in classes}
        observation = observe_absence(repo, aliases)
        save(out / 'ABSENCE-CHILD-ENTRY.json', observation)
        receipt['absence_observation'] = identity((out / 'ABSENCE-CHILD-ENTRY.json').read_bytes())
        require(observation['complete'], 'Complete1180 absence is required')
        require(held_stat(repo, held) == before['held_stat'], 'Held metadata changed')
        sys.path.insert(0, str(repo / 'scripts'))
        os.chdir(repo)
        objects = json.loads((repo / MANIFEST).read_bytes())['objects']
        require(len(objects) == 28478, 'Original projection universe changed')
        if phase == 'metadata':
            receipt['result'] = metadata_phase(repo, state, held, prepared)
        elif phase == '824':
            receipt['result'] = phase824(repo, state, classes, objects)
        elif phase == 'owners':
            receipt['result'] = owner_phase(repo, objects)
        elif phase == '98':
            receipt['result'] = phase98(repo, state, classes)
        elif phase.startswith('258-'):
            # This invocation adapter is independently reviewed and byte-bound.
            if phase == '258-reader':
                adapter = receive_module(state / 'inputs/reader_adapter.py', 'combined_reader_adapter')
                boundary = adapter.install(repo, held)
            helper = state / 'inputs/258.py'
            old_argv = sys.argv
            sys.argv = [str(helper), '--repo', str(repo), '--state', str(state), '--expected-head', prepared['head'],
                        '--phase', phase.removeprefix('258-'), '--output', str(out / 'actual258.json')]
            try:
                if phase == '258-reader':
                    with adapter.bounded_git_environment():
                        runpy.run_path(str(helper), run_name='__main__')
                else:
                    runpy.run_path(str(helper), run_name='__main__')
            finally:
                sys.argv = old_argv
            actual = json.loads((out / 'actual258.json').read_bytes())
            require(actual['status'] == 'PASS_BOUNDED_PHASE_ONLY' and actual['held_denials'] == 0, '258 phase boundary failed')
            receipt['result'] = actual
        elif phase == 'public-references':
            receipt['result'] = public_references(repo, held)
        elif phase == 'negative-controls':
            receipt['result'] = negative_controls(repo, state, classes, out)
        elif phase == 'post-controls':
            import validate_ar8r_reconciliation as snapshot
            import resolve_t20_v6_source as source
            require(snapshot.validate_pmr007_deep_snapshot(repo) == [] and snapshot.validate_pmr007_rounds_snapshot(repo) == [], 'Post-control snapshots failed')
            sample = sorted((r for r in classes if r['cohort'] == '258'), key=lambda r: r['alias'])[0]
            require(identity(source.continuation_copy_bytes(repo, sample['alias']))['sha256'] == sample['sha256'], 'Post-control continuation failed')
            actual = vector(repo, state, held, expected_paths={r['path'] for r in before['rows']} - aliases)
            receipt['result'] = {'post_control_paths': len(actual['rows']), 'post_control_tree': actual['tree']}
        else:
            raise RuntimeError('Unknown bounded phase')
        if boundary is not None:
            receipt['reader_boundary'] = boundary.receipt()
            surfaces = {r['surface'] for r in receipt['reader_boundary']['events']}
            require(surfaces == {'index', 'public_worktree'}, 'Reader did not exercise both bounded currentness surfaces')
        require(guard.denials == 0, 'Held body request occurred')
        receipt['status'] = 'PASS_BOUNDED_PHASE_ONLY'
    except BaseException as error:
        receipt.update(status='FAIL_OR_INTERRUPTED', error=repr(error), traceback=traceback.format_exc())
        raise
    finally:
        receipt['held_denials'] = guard.denials
        receipt['held_events'] = guard.events
        save(out / 'TERMINAL.json', receipt)



def admit_hosted_checkout(repo, state, *, fresh, saved=False):
    require(os.environ.get('GITHUB_ACTIONS') == 'true', 'Actual hosted execution is required')
    require(git(repo, 'rev-parse', '--show-object-format=storage') == b'sha1\n', 'Unexpected Git object format')
    require(git(repo, 'rev-parse', '--is-shallow-repository') == b'false\n', 'Complete public history is required')
    if saved:
        require((state / 'PREPARED.json').is_file(), 'Saved admission requires the prepared input pins')
        boundary = helper_module(state, 'boundary.py', 'hosted_saved_boundary')
    else:
        boundary = checkout_module(repo, 'boundary.py', 'hosted_checkout_boundary')
    return boundary.validate_hosted_coordinates(repo, state, os.environ,
        git(repo, 'rev-parse', 'HEAD').decode().strip(),
        Path(os.fsdecode(git(repo, 'rev-parse', '--show-toplevel').rstrip(b'\n'))), fresh=fresh)


def checkout_module(repo, name, module_name):
    relative = PUBLIC_HELPERS[name]
    path = safe_path(repo, relative, allow_missing=False)
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == 0o644
            and info.st_nlink == 1, 'Public checkout helper must be an ordinary file')
    body = path.read_bytes()
    digest = identity(body)
    _, stage = stage_map(repo)
    expected = ('100644 blob ' + digest['git_blob'] + '\t' + relative).encode() + b'\0'
    require(stage.get(relative) == ('100644', digest['git_blob'])
            and git(repo, 'ls-tree', '-z', 'HEAD', '--', relative) == expected,
            'Public helper differs from the exact checkout commit or index')
    return receive_module(path, module_name, digest['sha256'])


def saved_input_path(state, relative):
    ordinary_dir(state)
    path = safe_path(state, relative, allow_missing=False)
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1,
            'Saved input must be an unaliased ordinary file')
    return path


def helper_module(state, name, module_name):
    manifest_path = saved_input_path(state, 'inputs/SOURCE-IDENTITIES.json')
    manifest_body = manifest_path.read_bytes()
    identities = json.loads(manifest_body)
    if os.path.lexists(state / 'PREPARED.json'):
        prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
        require(identity(manifest_body) == prepared['input_files']['inputs/SOURCE-IDENTITIES.json'],
                'Prepared helper identity map changed')
        require({key: identities[name][key] for key in ('bytes', 'sha256', 'git_blob')}
                == prepared['input_files']['inputs/' + name], 'Prepared selected helper identity changed')
    path = saved_input_path(state, 'inputs/' + name)
    return receive_module(path, module_name, identities[name]['sha256'])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('run', 'restore', 'export', '_phase'))
    parser.add_argument('--repo', type=Path, default=Path(os.environ.get('GITHUB_WORKSPACE', '.')))
    parser.add_argument('--state', type=Path,
                        default=Path(os.environ.get('RUNNER_TEMP', '.')) / 'r0002-source-alias-absence')
    parser.add_argument('--phase', choices=PHASES)
    parser.add_argument('--token')
    parser.add_argument('--identity-fd', type=int)
    args = parser.parse_args()
    environment = sanitized_env()
    os.environ.clear()
    os.environ.update(environment)
    repo = ordinary_dir(args.repo)
    state = args.state.absolute()
    if args.command == 'export':
        admit_hosted_checkout(repo, state, fresh=not os.path.lexists(state))
        evidence = checkout_module(repo, 'evidence.py', 'hosted_checkout_evidence')
        evidence.export_evidence(state, PHASES)
        return
    require(os.getsid(0) == os.getpid() == os.getpgrp(), 'Invoke the actual runner in its own session with setsid')
    def interrupted(signum, frame):
        raise KeyboardInterrupt('Hosted runner interrupted by signal ' + str(signum))
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGHUP, interrupted)
    if args.command == 'run':
        prepare(repo, state)
        execute(repo, state)
    elif args.command == 'restore':
        admit_hosted_checkout(repo, state, fresh=False, saved=True)
        with operation_lock(state, 'restore', recover=True):
            print(json.dumps(restore(repo, state)))
    else:
        require(args.phase and args.token and args.identity_fd is not None, 'Internal phase requires its durable lease')
        bounded_phase(repo, state, args.phase, args.token, args.identity_fd)


if __name__ == '__main__':
    main()



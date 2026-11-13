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


def trial_partition(prepared, before, classes):
    """Bind the claimed trial profile to the authenticated pre-trial vector."""
    aliases = {row['alias'] for row in classes}
    present = aliases & {row['path'] for row in before['rows']}
    retired = aliases - present
    profile = prepared.get('profile', 'historical-all-present1180-v1')
    require(profile in ('historical-all-present1180-v1', 'current-checkout1180-v1'),
            'Unknown alias trial profile')
    require(profile != 'historical-all-present1180-v1' or not retired,
            'Historical profile cannot contain initially absent aliases')
    require(prepared.get('initially_absent_aliases', []) == sorted(retired)
            and prepared.get('trial_removed_aliases', sorted(aliases)) == sorted(present),
            'Prepared current alias partition differs')
    require(prepared['expected_absent_tracked'] == len(before['rows']) - len(present)
            and prepared['preimage_paths'] == len(present)
                + len({row['canonical'] for row in classes}) + len(GENERATED),
            'Current trial denominator or backup count differs')
    return {'profile': profile, 'historical_aliases_observed': len(aliases),
            'planned_trial_removals': len(present), 'previously_absent_aliases': len(retired)}


def require_retired_absence(repo, prepared):
    require(all(not os.path.lexists(Path(repo) / path)
                for path in prepared.get('initially_absent_aliases', [])),
            'Previously absent alias reappeared; preserve for inspection, restoration blocked')


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
    trial_partition(prepared, before, class_rows(state))
    require(runtime() == prepared['runtime'], 'Runtime changed')
    return prepared, before


def prepare(repo, state, *, current_checkout=False):
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
        if not current_checkout:
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
        classes = (population.derive_classes(repo, current_stage=stage) if current_checkout
                   else population.derive_classes(repo))
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
        trial_aliases = {row['alias'] for row in classes if row['alias'] in rows}
        retired_aliases = {row['alias'] for row in classes} - trial_aliases
        require(current_checkout or not retired_aliases, 'Historical trial requires all aliases present')
        require(all(not os.path.lexists(repo / path) for path in retired_aliases),
                'Retired alias is not absent before trial')
        for row in classes:
            for key in ('alias', 'canonical'):
                if key == 'alias' and row[key] in retired_aliases:
                    continue
                current = rows[row[key]]
                require((current['sha256'], current['bytes'], current['git_blob'], current['index_mode'], current['mode']) ==
                        (row['sha256'], row['bytes'], row['blob'], row['mode'], 0o644), 'Finite public source differs')
        save(state / 'before.json', before)
        save(state / 'classes.json', classes)
        received['classes.json'] = identity((state / 'classes.json').read_bytes())
        preimages = save_preimages(repo, state, trial_aliases
                                  | {row['canonical'] for row in classes} | set(GENERATED), protected)
        require(len(preimages) == 2265 - len(retired_aliases), 'Restoration preimage count differs')
        require((repo / '.git/index').read_bytes() == (state / 'original-index').read_bytes(), 'Index changed during backup')
        require(vector(repo, state, held) == before and guard.denials == 0, 'Preparation observation or boundary drift')
        info = repo.stat()
        prepared = {'schema': 'hosted-source-alias-durable-preparation-v1', 'status': 'PREPARED_NO_ABSENCE',
            'repo': str(repo), 'state': str(state), 'repo_inode': [info.st_dev, info.st_ino],
            'head': admission['head'], 'tree': before['tree'], 'admission': admission, 'runtime': runtime_record,
            'harness': identity(harness), 'input_files': received, 'before': identity((state / 'before.json').read_bytes()),
            'preimages': identity((state / 'preimages.json').read_bytes()),
            'raw_index': identity((state / 'original-index').read_bytes()), 'original_census_paths': len(originals),
            'originals': 1180, 'unique_canonicals': 1082, 'preimage_paths': len(preimages),
            'profile': 'current-checkout1180-v1' if current_checkout else 'historical-all-present1180-v1',
            'initially_absent_aliases': sorted(retired_aliases), 'trial_removed_aliases': sorted(trial_aliases),
            'tracked_before': len(before['rows']), 'expected_absent_tracked': len(before['rows']) - len(trial_aliases),
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
        require_retired_absence(repo, prepared)
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
        trial_aliases = aliases & {row['path'] for row in before['rows']}
        require(sorted(aliases - trial_aliases) == prepared.get('initially_absent_aliases', [])
                and sorted(trial_aliases) == prepared.get('trial_removed_aliases', sorted(aliases)),
                'Prepared current alias partition differs')
        require(all(not os.path.lexists(repo / path) for path in aliases - trial_aliases),
                'Previously retired alias reappeared')
        save(state / 'EXECUTION-START.json', {'prepared': identity((state / 'PREPARED.json').read_bytes()), 'process': process_identity(),
                                           'intended_absences': sorted(aliases), 'status': 'STARTED_NOT_TERMINAL'})
        result = {'status': 'RUNNING', 'phases': [], 'held_worktree_body_integrity': 'UNKNOWN',
                  'trial_scope': trial_partition(prepared, before, classes)}
        failure = None
        try:
            for relative in sorted(trial_aliases):
                path = safe_path(repo, relative, protected={r['path'] for r in held}, allow_missing=False)
                path.unlink()
                fsync_dir(path.parent)
            observation = observe_absence(repo, aliases)
            save(state / 'ABSENCE-AFTER-UNLINK.json', observation)
            require(observation['complete'], 'Complete absence after unlink is required')
            git(repo, 'update-index', '--force-remove', '--', *sorted(trial_aliases), state=state)
            with (repo / '.git/index').open('rb') as stream:
                os.fsync(stream.fileno())
            fsync_dir(repo / '.git')
            observation = observe_absence(repo, aliases)
            save(state / 'ABSENCE-AFTER-INDEX.json', observation)
            require(observation['complete'], 'Complete absence after index removal is required')
            removed = prune_empty_parents(repo, trial_aliases)
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
        receipt['trial_scope'] = trial_partition(prepared, before, classes)
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


# Separate public-only generated fixture profile. The original1180 entrypoints,
# population and receipt contract above retain their original meaning.
PUBLIC_FIXTURE_PHASES = ['fixtures123-present', 'fixtures123-unstaged', 'fixtures123-staged',
                         'fixtures123-controls', 'fixtures123-post-controls']
PUBLIC_FIXTURE_PROFILE = 'public-fixtures123'
PUBLIC_FIXTURE_OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
PUBLIC_FIXTURE_CROSSWALK = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
PUBLIC_FIXTURE_CENSUS = 'docs/project-closure/reader-refactor-issue-35/CENSUS.json'
PUBLIC_FIXTURE_SOURCE_PATHS = (
    'scripts/check_reader_pilot.py', 'scripts/reader_census.py', 'scripts/resolve_t20_v6_source.py',
    'scripts/validate_ar8r_reconciliation.py', 'scripts/validate_internal_references.py',
    'scripts/validate_repo.py', 'scripts/validate_research_continuations.py',
    'scripts/validate_t20_v6_projection.py', 'scripts/validate_v5_successors.py')
_PUBLIC_FIXTURE_NATIVE = None


class PublicFixtureNativeRecorder:
    """Transparent actual subprocess.run receipt, scoped only to the new profile."""
    def __init__(self, repo, state):
        self.repo, self.state = Path(repo).absolute(), Path(state).absolute()
        self.rows, self.active = [], []
        self.enabled = False
        self.bound = self.state.exists()

    def write(self, row):
        if self.bound:
            path = self.state/row['record']
            save(path, row, replace=path.exists())

    def bind(self):
        require(self.state.is_dir(), 'Native evidence state does not exist')
        self.bound = True
        for row in self.rows: self.write(row)

    def audit(self, event, args):
        if not self.enabled or event != 'subprocess.Popen': return
        argv = [os.fsdecode(value) for value in args[1]]
        if Path(argv[0]).name != 'git': return
        require(self.active, 'Native public123 process has no actual outcome recorder')
        row = self.active[-1]
        require('observed_argv' not in row, 'One native command spawned multiple unbound processes')
        cwd = Path(args[2] if args[2] is not None else os.getcwd()).absolute()
        effective = Path(argv[argv.index('-C')+1]).absolute() if '-C' in argv else cwd
        require(effective == self.repo and argv == row['requested_argv'], 'Observed native command/root differs')
        resolved = shutil.which(os.fsdecode(args[0]))
        require(resolved == '/usr/bin/git', 'Native outcome recorder requires the real approved Git executable')
        row.update(observed_argv=argv, observed_cwd=str(cwd), effective_repo=str(effective),
                   observed_executable=os.fsdecode(args[0]), resolved_executable=resolved)
        self.write(row)

    @staticmethod
    def output(value):
        if value is None: return {'capture': 'NOT_CAPTURED'}
        body = value.encode('utf-8') if isinstance(value, str) else bytes(value)
        return {'capture': 'UTF8_TEXT' if isinstance(value, str) else 'BYTES', 'identity': identity(body)}

    def run(self, *args, **kwargs):
        command = args[0] if args else kwargs.get('args')
        if not isinstance(command, (list, tuple)) or not command or Path(os.fsdecode(command[0])).name != 'git':
            return self.original(*args, **kwargs)
        token = uuid.uuid4().hex
        row = {'record': 'native-executions/'+token+'.json', 'token': token, 'process': process_identity(),
               'requested_argv': [os.fsdecode(value) for value in command], 'status': 'STARTED_NOT_TERMINAL'}
        self.rows.append(row); self.active.append(row); self.write(row)
        try:
            result = self.original(*args, **kwargs)
            row.update(status='TERMINAL', exit_code=result.returncode,
                       stdout=self.output(result.stdout), stderr=self.output(result.stderr))
            return result
        except subprocess.CalledProcessError as error:
            row.update(status='TERMINAL', exit_code=error.returncode,
                       stdout=self.output(error.stdout), stderr=self.output(error.stderr))
            raise
        except BaseException as error:
            row.update(status='FAILED_WITHOUT_RECEIVED_RESULT', error_type=type(error).__name__)
            raise
        finally:
            self.write(row); self.active.pop()

    def snapshot(self):
        return [{'record': row['record'], 'identity': identity(json_bytes(row))} for row in self.rows]

    def __enter__(self):
        global _PUBLIC_FIXTURE_NATIVE
        require(_PUBLIC_FIXTURE_NATIVE is None, 'Overlapping public native outcome recorder')
        self.original = subprocess.run
        _PUBLIC_FIXTURE_NATIVE = self
        self.enabled = True
        sys.addaudithook(self.audit)
        subprocess.run = self.run
        return self

    def __exit__(self, kind, value, trace):
        global _PUBLIC_FIXTURE_NATIVE
        self.enabled = False
        require(subprocess.run == self.run, 'Public native transport recorder was replaced')
        subprocess.run = self.original
        _PUBLIC_FIXTURE_NATIVE = None


def public_fixture_native_receipts():
    require(_PUBLIC_FIXTURE_NATIVE is not None, 'Public profile has no native outcome recorder')
    return _PUBLIC_FIXTURE_NATIVE.snapshot()


def public_fixture_environment():
    env = sanitized_env()
    env.update(GIT_ALLOW_PROTOCOL='', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_SYSTEM=os.devnull,
               PATH='/usr/bin:/bin', PYTHONDONTWRITEBYTECODE='1')
    return env


def public_fixture_index(repo):
    path = Path(repo)/'.git/index'
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'Native index is not ordinary')
        pieces = []
        while True:
            piece = os.read(fd, 1048576)
            if not piece:
                break
            pieces.append(piece)
        body = b''.join(pieces)
        after = os.fstat(fd)
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        require(tuple(getattr(before, key) for key in fields) == tuple(getattr(after, key) for key in fields)
                == tuple(getattr(path.lstat(), key) for key in fields), 'Native index changed while receiving')
    finally:
        os.close(fd)
    require(body[:4] == b'DIRC' and int.from_bytes(body[4:8], 'big') in (2, 3, 4)
            and hashlib.sha1(body[:-20]).digest() == body[-20:], 'Native index structure/checksum differs')
    return body


def public_fixture_git(repo, state, *args):
    require(args and args[0] in ('ls-tree', 'ls-files', 'rev-parse', 'diff', 'update-index'),
            'Unadmitted public fixture native command')
    require('-l' not in args and '--long' not in args and not any(value in args for value in
            ('fetch', 'push', 'pull', 'clone', 'reset', 'checkout')), 'Object-size or transport query is forbidden')
    index_before = None
    if args[0] == 'update-index':
        index_before = public_fixture_index_preflight(repo, state)
        before = json.loads(saved_input_path(Path(state), 'before.json').read_bytes())
        parked = Path(state)/'PARKING-DONE.json'
        members = set(json.loads(parked.read_bytes())['members']) if parked.exists() else set()
        public_fixture_transition_preflight(repo, state, before, members, absent=bool(members))
    command = ['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args]
    record = {'command': command, 'repo': str(repo), 'process': process_identity(),
              'exit_code': None, 'status': 'STARTED_NOT_TERMINAL'}
    path = Path(state)/'native-commands'/(uuid.uuid4().hex+'.json')
    save(path, record)
    mutation_path = None
    if args[0] == 'update-index':
        mutation_path = Path(state)/'native-index-mutations'/(uuid.uuid4().hex+'.json')
        mutation = {'repo': str(repo), 'command': command, 'group': group_record(), 'process': process_identity(),
                    'command_record': path.relative_to(state).as_posix(), 'before': index_before,
                    'status': 'STARTED_NOT_TERMINAL'}
        save(mutation_path, mutation)
    result = subprocess.run(command, cwd=repo, env=public_fixture_environment(), capture_output=True)
    record.update(status='TERMINAL', exit_code=result.returncode,
                  stdout=identity(result.stdout), stderr=identity(result.stderr))
    if _PUBLIC_FIXTURE_NATIVE is not None:
        record['native_record'] = _PUBLIC_FIXTURE_NATIVE.rows[-1]['record']
    save(path, record, replace=True)
    if mutation_path is not None:
        mutation.update(status='TERMINAL', exit_code=result.returncode,
                        command_identity=identity(path.read_bytes()), native_record=record.get('native_record'),
                        after=identity(public_fixture_index(repo)))
        save(mutation_path, mutation, replace=True)
    require(result.returncode == 0, 'Actual native public fixture command failed: '+args[0])
    return result.stdout


def public_fixture_stage_map(repo, state):
    before = public_fixture_index(repo)
    raw = public_fixture_git(repo, state, 'ls-files', '--sparse', '--stage', '-z')
    rows = {}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        header, name = entry.split(b'\t', 1)
        mode, oid, stage = header.decode('ascii').split()
        path = name.decode('utf-8')
        require(stage == '0' and mode in ('100644', '100755', '120000') and path not in rows,
                'Public fixture requires an ordinary unconflicted native index')
        rows[path] = (mode, oid)
    require(public_fixture_index(repo) == before, 'Native metadata observation changed the active index')
    return raw, rows


def public_fixture_file(repo, relative):
    """A stable ordinary public file vector; reading does not change its atime."""
    path = safe_path(Path(repo), relative, allow_missing=False)
    fields = ('st_dev', 'st_ino', 'st_nlink', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_atime_ns')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOATIME)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1
                and stat.S_IMODE(before.st_mode) == 0o644, 'Public fixture source must be ordinary and nonexecutable')
        parts = []
        while True:
            body = os.read(fd, 1048576)
            if not body:
                break
            parts.append(body)
        body = b''.join(parts)
        after = os.fstat(fd)
        require(tuple(getattr(before, key) for key in fields) == tuple(getattr(after, key) for key in fields)
                == tuple(getattr(path.lstat(), key) for key in fields), 'Public fixture source changed during read')
    finally:
        os.close(fd)
    return {**identity(body), 'mode': stat.S_IMODE(before.st_mode), 'device': before.st_dev,
            'inode': before.st_ino, 'links': before.st_nlink, 'atime_ns': before.st_atime_ns,
            'mtime_ns': before.st_mtime_ns}


def capture_public_fixture_sources(repo, paths):
    names = sorted(set(paths))
    require(len(names) == len(paths), 'Repeated finite public fixture source')
    return {name: public_fixture_file(repo, name) for name in names}


def public_fixture_namespace(repo):
    """Whole checkout path/type metadata; no file or held-object body reads."""
    repo = Path(repo)
    files, directories = {}, {}
    for directory, dirs, names in os.walk(repo, followlinks=False):
        parent = Path(directory)
        if parent == repo:
            dirs[:] = [name for name in dirs if name != '.git']
        directories[parent.relative_to(repo).as_posix()] = stat.S_IMODE(parent.lstat().st_mode)
        links = [name for name in dirs if (parent/name).is_symlink()]
        for name in names + links:
            path = parent/name
            value = path.lstat()
            files[path.relative_to(repo).as_posix()] = {'mode': value.st_mode, 'device': value.st_dev,
                'inode': value.st_ino, 'bytes': value.st_size, 'links': value.st_nlink, 'mtime_ns': value.st_mtime_ns}
    return {'files': files, 'directories': directories}


def check_public_fixture_namespace(repo, state, absent):
    original = json.loads((state/'before-namespace.json').read_bytes())
    expected = {'files': {path: row for path, row in original['files'].items() if path not in absent},
                'directories': original['directories']}
    actual = public_fixture_namespace(repo)
    require(actual == expected, 'Checkout namespace metadata diverged outside the exact declared public123 state')
    return actual


def _public_fixture_same_source(actual, expected):
    # Read access time is restored later. ctime/continuous custody are not claimed.
    return {key: value for key, value in actual.items() if key != 'atime_ns'} == {
        key: value for key, value in expected.items() if key != 'atime_ns'}


def public_fixture_index_preflight(repo, state, *, expected=None, mode=None):
    """Observe the admitted index before any owned mutation; never adopt drift."""
    repo, state = Path(repo), Path(state)
    require(not os.path.lexists(repo/'.git/index.lock'),
            'Foreign index lock blocks public fixture mutation or cleanup')
    if expected is None:
        expected = saved_input_path(state, 'expected-index').read_bytes()
    admitted_mode = json.loads(saved_input_path(state, 'index-mode.json').read_bytes())['mode']
    require(type(admitted_mode) is int and 0 <= admitted_mode <= 0o777,
            'Saved ordinary index mode is missing or invalid')
    if mode is None:
        mode = admitted_mode
    require(mode == admitted_mode, 'Controlled cleanup cannot admit a new index permission mode')
    actual = public_fixture_index(repo)
    require(actual == expected and stat.S_IMODE((repo/'.git/index').stat().st_mode) == mode,
            'Unexplained public fixture index divergence before controlled native mutation or cleanup')
    require(not os.path.lexists(repo/'.git/index.lock'), 'Index lock appeared during read-only preflight')
    return {'raw_index': identity(actual), 'mode': mode, 'foreign_lock': False}


def public_fixture_transition_preflight(repo, state, before, members, *, absent,
                                        index_expected=None, index_mode=None, provider_override=None):
    """Exact applicable endpoints; parked originals are metadata-only in children."""
    repo, state = Path(repo), Path(state)
    members = set(members)
    require(members <= set(before), 'Transition members differ from the admitted source vector')
    index = public_fixture_index_preflight(repo, state, expected=index_expected, mode=index_mode)
    original_namespace = json.loads(saved_input_path(state, 'before-namespace.json').read_bytes())
    expected_namespace = {'files': dict(original_namespace['files']),
                          'directories': original_namespace['directories']}
    override = {} if provider_override is None else dict([provider_override])
    require(not set(override) & members and set(override) <= set(before),
            'Controlled provider override is not a fixed admitted source')
    for path, original in before.items():
        if absent and path in members:
            require(not os.path.lexists(repo/path), 'Selected original reappeared before owned mutation: '+path)
            parked = safe_path(state/'park', path, allow_missing=False)
            info = parked.lstat()
            require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == original['mode']
                    and (info.st_dev, info.st_ino, info.st_nlink, info.st_size, info.st_mtime_ns)
                    == (original['device'], original['inode'], original['links'], original['bytes'], original['mtime_ns']),
                    'Parked original metadata diverged before owned mutation: '+path)
            expected_namespace['files'].pop(path)
        else:
            expected = override.get(path, original)
            require(_public_fixture_same_source(public_fixture_file(repo, path), expected),
                    'Finite public source diverged before owned mutation: '+path)
            if path in override:
                expected_namespace['files'][path] = {
                    'mode': stat.S_IFREG | expected['mode'], 'device': expected['device'],
                    'inode': expected['inode'], 'bytes': expected['bytes'],
                    'links': expected['links'], 'mtime_ns': expected['mtime_ns']}
    require(public_fixture_namespace(repo) == expected_namespace,
            'Applicable checkout namespace diverged before owned mutation')
    public_fixture_index_preflight(repo, state, expected=index_expected, mode=index_mode)
    return {'index': index, 'sources': len(before), 'members': len(members),
            'absent': absent, 'parked_body_reads': False}


def restore_public_fixture_control_index(repo, state, before, members, saved, changed, mode):
    """Restore only an exact owned control postimage; foreign drift stays failed."""
    public_fixture_transition_preflight(repo, state, before, members, absent=True,
                                        index_expected=changed, index_mode=mode)
    writes_before = {path.name for path in (state/'writes').glob('*.json')}
    mutation_write(repo, state, '.git/index', saved, mode)
    public_fixture_index_preflight(repo, state, expected=saved, mode=mode)
    new_writes = sorted(path.name for path in (state/'writes').glob('*.json') if path.name not in writes_before)
    require(len(new_writes) == 1, 'Controlled index restoration lacks its exact owned write receipt')
    return {'status': 'RESTORED_EXACT_OWNED_INDEX_CONTROL', 'before': identity(changed),
            'after': identity(saved), 'mode': mode, 'write_record': 'writes/'+new_writes[0]}


def _public_fixture_rename_noreplace(source, destination):
    """Linux hosted primitive: a racing destination can never be overwritten."""
    import ctypes
    libc = ctypes.CDLL(None, use_errno=True)
    operation = getattr(libc, 'renameat2', None)
    require(operation is not None, 'Atomic no-replace rename is unavailable; refuse before mutation')
    operation.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    operation.restype = ctypes.c_int
    # AT_FDCWD and RENAME_NOREPLACE; this profile separately admits Linux only.
    if operation(-100, os.fsencode(source), -100, os.fsencode(destination), 1) != 0:
        number = ctypes.get_errno()
        raise OSError(number, 'Atomic no-replace public fixture move failed: '+os.strerror(number), str(destination))


def park_public_fixture_members(repo, state, before, members):
    repo, state = Path(repo), Path(state)
    members = sorted(set(members))
    require(members and set(members) <= set(before), 'Invalid finite parking members')
    require(not os.path.lexists(state/'park'), 'Public fixture park is single-use')
    require(repo.stat().st_dev == state.stat().st_dev, 'Original parking requires one filesystem')
    public_fixture_transition_preflight(repo, state, before, members, absent=False)
    save(state/'PARKING-START.json', {'members': members, 'original_inodes': {
        name: [before[name]['device'], before[name]['inode']] for name in members}})
    mkdir_durable(state/'park')
    moved = []
    for name in members:
        destination = safe_path(state/'park', name)
        mkdir_durable(destination.parent)
        require(not os.path.lexists(destination), 'Park destination unexpectedly exists')
        _public_fixture_rename_noreplace(safe_path(repo, name, allow_missing=False), destination)
        fsync_dir(destination.parent)
        fsync_dir((repo/name).parent)
        moved.append(name)
        save(state/'PARKING-PROGRESS.json', {'moved': moved}, replace=len(moved) > 1)
    save(state/'PARKING-DONE.json', {'members': moved})


def public_fixture_restore_gate(repo, state, before, members):
    """Complete read-only gate before any original, source-time or index restore."""
    repo, state = Path(repo), Path(state)
    members = set(members)
    require(members and members <= set(before), 'Invalid finite restoration population')
    require(not os.path.lexists(repo/'.git/index.lock'), 'Index lock blocks public fixture restoration')
    expected = (state/'expected-index').read_bytes()
    require(public_fixture_index(repo) == expected, 'Unexplained public fixture index divergence; no reset')
    index_mode = json.loads((state/'index-mode.json').read_bytes())['mode']
    require(stat.S_IMODE((repo/'.git/index').stat().st_mode) == index_mode,
            'Unexplained public fixture index mode divergence')
    completed_park = (state/'PARKING-DONE.json').exists()
    recovering_own_restore = (state/'FIXTURE-RESTORATION-START.json').exists()
    for name, original in before.items():
        present = os.path.lexists(repo/name)
        parked = name in members and os.path.lexists(state/'park'/name)
        require(not (parked and present), 'Selected original reappeared while its parked inode remains: '+name)
        if parked:
            require(_public_fixture_same_source(public_fixture_file(state/'park', name), original),
                    'Parked original source diverged: '+name)
        else:
            require(present, 'Unparked public fixture source is missing: '+name)
            require(not (name in members and completed_park and not recovering_own_restore),
                    'Selected original reappeared without an authorized restoration: '+name)
            require(_public_fixture_same_source(public_fixture_file(repo, name), original),
                    'Finite public fixture source diverged: '+name)
    return {'status': 'PASS_READ_ONLY_RESTORATION_GATE', 'members': len(members), 'sources': len(before)}


def restore_public_fixture_members(repo, state, before, members):
    repo, state = Path(repo), Path(state)
    gate = public_fixture_restore_gate(repo, state, before, members)
    save(state/'FIXTURE-RESTORATION-GATE.json', gate, replace=(state/'FIXTURE-RESTORATION-GATE.json').exists())
    if not (state/'FIXTURE-RESTORATION-START.json').exists():
        save(state/'FIXTURE-RESTORATION-START.json', {'gate': identity((state/'FIXTURE-RESTORATION-GATE.json').read_bytes())})
    for name in sorted(members):
        parked = state/'park'/name
        if os.path.lexists(parked):
            require(not os.path.lexists(repo/name), 'Original reappeared during restoration; stop before overwrite')
            _public_fixture_rename_noreplace(parked, repo/name)
            fsync_dir(parked.parent)
            fsync_dir((repo/name).parent)
    for name, original in before.items():
        require(_public_fixture_same_source(public_fixture_file(repo, name), original),
                'Public fixture source changed during restoration')
        os.utime(repo/name, ns=(original['atime_ns'], original['mtime_ns']), follow_symlinks=False)
    original_index = (state/'original-index').read_bytes()
    require(public_fixture_index(repo) == (state/'expected-index').read_bytes(),
            'Index changed before final restore; no reset')
    mode = json.loads((state/'index-mode.json').read_bytes())['mode']
    writes_before = {path.name for path in (state/'writes').glob('*.json')}
    mutation_write(repo, state, '.git/index', original_index, mode)
    writes = sorted(path.name for path in (state/'writes').glob('*.json') if path.name not in writes_before)
    require(len(writes) == 1, 'Final index restoration lacks its single owned write record')
    after = capture_public_fixture_sources(repo, before)
    require(after == before and public_fixture_index(repo) == original_index,
            'Finite public fixture vectors or raw index were not restored exactly')
    save(state/'after.json', after)
    result = {'status': 'PASS_FIXTURE_MEMBERS_AND_INDEX_RESTORATION_ONLY', 'members': len(members),
              'sources': len(before), 'after': identity((state/'after.json').read_bytes()),
              'raw_index': identity(original_index), 'ctime_or_continuous_custody_claimed': False}
    result['index_write_record'] = 'writes/'+writes[0]
    save(state/'FIXTURE-RESTORATION-TERMINAL.json', result)
    return result


class PublicFixtureAudit:
    """Finite access/process observation; not a sandbox against hostile native code."""
    def __init__(self, repo, state, members=(), *, parent=False):
        self.repo, self.state = Path(repo).absolute(), Path(state).absolute()
        self.members, self.parent = set(members), parent
        self.absent = False
        self.restoring = False
        self.allowed_index = None
        self.events, self.private_denials, self.absence_observations = [], [], []
        hold = self.state/'inputs/hold.json'
        rows = json.loads(hold.read_bytes())['held'] if hold.exists() else []
        self.held_coordinates = {value for row in rows for value in
                                 (row['path'], row['published_metadata']['git_blob'])}

    def observation(self, label):
        result = observe_absence(self.repo, self.members)
        self.absence_observations.append({'label': label, 'complete': result['complete'],
                                         'members': len(result['rows']),
                                         'population_sha256': identity(json_bytes(sorted(self.members)))['sha256'],
                                         **({'failure_observation': result} if not result['complete'] else {})})
        require(result['complete'], 'Public123 namespace divergence at '+label)
        return result

    def audit(self, event, args):
        if event == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):
            name = Path(os.path.abspath(os.fsdecode(args[0])))
            text = str(name)
            protected = (text.endswith('/fixtures/KEYS.json') or 'OWNER-ADJUDICATOR' in text
                         or name.name.lower() in ('answers.json', 'scoring-keys.json'))
            parked = name.is_relative_to(self.state/'park')
            if protected or parked and not self.parent:
                self.private_denials.append({'event': 'forbidden body open', 'path': text})
                raise PermissionError('Protected or parked body is outside the public consumer scope')
            if self.absent and not self.restoring and any(name == self.repo/path for path in self.members):
                self.private_denials.append({'event': 'absent original open', 'path': text})
                raise PermissionError('Absent original must derive from current public providers')
        if event in ('compile', 'exec'):
            filename = args[1] if event == 'compile' and len(args) > 1 else getattr(args[0], 'co_filename', '')
            if isinstance(filename, str) and filename.endswith('/analysis/analyze_er2.py'):
                self.private_denials.append({'event': 'scorer execution', 'path': filename})
                raise PermissionError('Public scorer source is inert only')
        if event == 'subprocess.Popen':
            argv = [os.fsdecode(value) for value in args[1]]
            if self.parent and argv[:4] == [sys.executable, '-B', str(Path(__file__).absolute()), '_fixture-phase']:
                return
            executable = argv[0]
            require(executable == '/usr/bin/git' or executable == 'git' and shutil.which('git') == '/usr/bin/git',
                    'Only real native Git is allowed in a public fixture consumer')
            require(not any(value in argv for value in ('fetch', 'push', 'pull', 'clone', 'reset', 'checkout', '-l', '--long')),
                    'Transport, reset or object-size query is forbidden')
            require(not ('cat-file' in argv and any(value in argv for value in ('-s', '--batch', '--batch-check'))),
                    'Object-size or broad object query is forbidden')
            if 'cat-file' in argv and any(any(value in item for value in self.held_coordinates) for item in argv):
                self.private_denials.append({'event': 'protected native body', 'argv': argv})
                raise PermissionError('Protected native object body is outside public fixture scope')
            position = 1
            while position < len(argv) and argv[position].startswith('-'):
                position += 2 if argv[position] in ('-c', '-C', '--git-dir', '--work-tree') else 1
            require(position < len(argv) and argv[position] in
                    ('ls-files', 'ls-tree', 'cat-file', 'diff', 'rev-parse', 'config', 'update-index'),
                    'Unadmitted native Git command in public fixture scope')
            cwd = Path(argv[argv.index('-C')+1]) if '-C' in argv else Path(args[2] if args[2] is not None else os.getcwd())
            require(cwd.absolute() == self.repo, 'Native public fixture root differs')
            if 'update-index' in argv or 'add' in argv:
                command = argv[argv.index('update-index'):] if 'update-index' in argv else argv[argv.index('add'):]
                require(tuple(command) == self.allowed_index, 'Unjournaled public fixture index mutation')
            if self.absent and not self.restoring:
                self.observation('native-'+str(len(self.events)))
            self.events.append({'argv': argv, 'cwd': str(cwd), 'native_record':
                _PUBLIC_FIXTURE_NATIVE.active[-1]['record'] if _PUBLIC_FIXTURE_NATIVE is not None
                and _PUBLIC_FIXTURE_NATIVE.active else None})


def admit_public_fixture_checkout(repo, state, *, fresh, saved=False):
    require(os.environ.get('GITHUB_ACTIONS') == 'true', 'Actual hosted public fixture execution is required')
    require(Path(repo).absolute() == Path(os.environ.get('GITHUB_WORKSPACE', '')).absolute(),
            'Public fixture root differs from actual hosted workspace')
    ordinary_dir(repo)
    ordinary_dir(Path(repo)/'.git')
    public_fixture_index(repo)
    def metadata(*args):
        result = subprocess.run(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=repo, env=public_fixture_environment(), capture_output=True)
        require(result.returncode == 0, 'Native hosted admission observation failed')
        return result.stdout
    require(metadata('rev-parse', '--show-object-format=storage') == b'sha1\n', 'Unexpected native object format')
    require(metadata('rev-parse', '--is-shallow-repository') == b'false\n', 'Complete public history is required')
    if saved:
        helper = helper_module(state, 'boundary.py', 'fixture_saved_boundary')
    else:
        helper = checkout_module(repo, 'boundary.py', 'fixture_checkout_boundary')
    return helper.validate_public_fixture_coordinates(repo, state, os.environ,
        metadata('rev-parse', 'HEAD').decode().strip(),
        Path(os.fsdecode(metadata('rev-parse', '--show-toplevel').rstrip(b'\n'))), fresh=fresh)


def public_fixture_runtime(repo):
    import importlib.metadata
    result = runtime()
    body = (Path(repo)/'requirements-ci.lock.txt').read_bytes()
    versions = {}
    for line in body.decode('utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        require(re.fullmatch(r'[A-Za-z0-9_.-]+==[A-Za-z0-9_.+-]+', line), 'CI dependency pin is not exact')
        name, expected = line.split('==')
        actual = importlib.metadata.version(name)
        require(name not in versions and actual == expected, 'Actual public fixture dependency pin differs')
        versions[name] = actual
    require(len(versions) == 11, 'Complete eleven-package runtime receipt is required')
    return {**result, 'all_pinned_packages': versions, 'lock': identity(body)}


def authenticate_public_fixture_export_sources(repo, state):
    """Read-only HEAD/public-code gate independent of the live native index."""
    repo, state = ordinary_dir(repo), ordinary_dir(state)
    ordinary_dir(repo/'.git')
    require(not os.path.lexists(repo/'.git/objects/info/alternates'), 'Alternate public source store is unadmitted')
    prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
    require(prepared['profile'] == PUBLIC_FIXTURE_PROFILE and prepared['repo'] == str(repo)
            and prepared['state'] == str(state)
            and prepared['repo_inode'] == [repo.stat().st_dev, repo.stat().st_ino],
            'Failure-export saved checkout/state coordinate differs')
    observations = []
    def metadata(*args):
        command = ['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args]
        result = subprocess.run(command, cwd=repo, env=public_fixture_environment(), capture_output=True)
        observations.append({'command': command, 'cwd': str(repo), 'exit_code': result.returncode,
                             'stdout': identity(result.stdout), 'stderr': identity(result.stderr)})
        require(result.returncode == 0, 'Read-only public source authentication failed')
        return result.stdout
    require(metadata('rev-parse', '--show-object-format=storage') == b'sha1\n', 'Unexpected public object format')
    head = metadata('rev-parse', 'HEAD').decode().strip()
    root = Path(os.fsdecode(metadata('rev-parse', '--show-toplevel').rstrip(b'\n')))
    require(head == prepared['head'] and root == repo, 'Failure-export native HEAD/root differs')
    require(metadata('rev-parse', 'HEAD^{tree}').decode().strip() == prepared['tree'],
            'Failure-export native tree differs')
    identities_body = saved_input_path(state, 'inputs/SOURCE-IDENTITIES.json').read_bytes()
    require(identity(identities_body) == prepared['input_files']['inputs/SOURCE-IDENTITIES.json'],
            'Failure-export helper identity map changed')
    helpers = json.loads(identities_body)
    require(set(helpers) == set(PUBLIC_HELPERS), 'Failure-export helper population differs')
    sources = {**PUBLIC_HELPERS, 'harness.py': 'scripts/check_source_alias_absence.py'}
    received = {}
    for name, relative in sources.items():
        body = saved_input_path(state, 'inputs/'+name).read_bytes()
        expected = identity(body)
        require(prepared['input_files']['inputs/'+name] == expected, 'Failure-export saved public code changed')
        if name != 'harness.py':
            require(helpers[name] == dict(expected, source_path=relative), 'Failure-export helper owner changed')
        else:
            require(prepared['harness'] == expected, 'Failure-export saved harness identity changed')
        actual = public_fixture_file(repo, relative)
        require({key: actual[key] for key in expected} == expected, 'Failure-export live public code differs')
        row = ('100644 blob '+expected['git_blob']+'\t'+relative).encode()+b'\0'
        require(metadata('ls-tree', '-z', head, '--', relative) == row,
                'Failure-export public source is not the exact native HEAD edition')
        received[relative] = expected
    return {'profile': PUBLIC_FIXTURE_PROFILE, 'head': head, 'tree': prepared['tree'],
            'repo': str(repo), 'state': str(state), 'public_sources': received,
            'native_observations': observations, 'live_index_required_for_authentication': False}


def public_fixture_export_index_observation(repo, state):
    """Failure metadata only: never repairs an invalid or unexplained index."""
    try:
        prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
        raw = public_fixture_index(repo)
        mode = json.loads(saved_input_path(state, 'index-mode.json').read_bytes())['mode']
        restored = (Path(state)/'FIXTURE-RESTORATION-TERMINAL.json').exists()
        expected = prepared['raw_index'] if restored else identity(saved_input_path(state, 'expected-index').read_bytes())
        exact = (identity(raw) == expected and stat.S_IMODE((Path(repo)/'.git/index').stat().st_mode) == mode
                 and not os.path.lexists(Path(repo)/'.git/index.lock'))
        return {'exact': exact, 'raw_index': identity(raw), 'mode': stat.S_IMODE((Path(repo)/'.git/index').stat().st_mode),
                'expected_restored_endpoint': restored, 'restoration_performed': False}
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        return {'exact': False, 'error': repr(error), 'restoration_performed': False}


def export_public_fixture_execution(repo, state):
    received = authenticate_public_fixture_export_sources(repo, state)
    prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
    require(Path(__file__).absolute() == Path(repo)/'scripts/check_source_alias_absence.py'
            and identity(Path(__file__).read_bytes()) == prepared['harness'],
            'Actual failure exporter source differs')
    boundary = helper_module(state, 'boundary.py', 'fixture_export_boundary')
    actual = boundary.validate_public_fixture_coordinates(repo, state, os.environ,
        received['head'], Path(received['repo']), fresh=False)
    require(actual == prepared['admission'] == json.loads(saved_input_path(state, 'ADMISSION.json').read_bytes()),
            'Actual failure-export run/root/head admission differs')
    received['actual_admission'] = actual
    received['live_index'] = public_fixture_export_index_observation(repo, state)
    evidence = helper_module(state, 'evidence.py', 'fixture_export_evidence')
    evidence.export_public_fixture_evidence(state, admission=received)


def prepare_public_fixtures(repo, state):
    repo, state = Path(repo), Path(state)
    os.environ.update(public_fixture_environment())
    runtime_record = public_fixture_runtime(repo)
    admission = admit_public_fixture_checkout(repo, state, fresh=True)
    mkdir_durable(state)
    require(_PUBLIC_FIXTURE_NATIVE is not None, 'Preparation requires complete native outcome custody')
    _PUBLIC_FIXTURE_NATIVE.bind()
    save(state/'ADMISSION.json', admission)
    with operation_lock(state, 'prepare-public-fixtures123') as operation:
        require(not os.path.lexists(repo/'.git/index.lock'), 'Preexisting index lock is not owned')
        original_index = public_fixture_index(repo)
        raw_stage, stage = public_fixture_stage_map(repo, state)
        atomic_bytes(state/'native-stage-before.z', raw_stage)
        received, helpers = {}, {}
        for name, relative in PUBLIC_HELPERS.items():
            path = safe_path(repo, relative, allow_missing=False)
            value = public_fixture_file(repo, relative)
            expected = ('100644 blob '+value['git_blob']+'\t'+relative).encode()+b'\0'
            require(stage.get(relative) == ('100644', value['git_blob'])
                    and public_fixture_git(repo, state, 'ls-tree', '-z', admission['head'], '--', relative) == expected,
                    'Current public helper differs from native HEAD/index')
            body = path.read_bytes()
            atomic_bytes(state/'inputs'/name, body)
            received['inputs/'+name] = identity(body)
            helpers[name] = {**identity(body), 'source_path': relative}
        save(state/'inputs/SOURCE-IDENTITIES.json', helpers)
        received['inputs/SOURCE-IDENTITIES.json'] = identity((state/'inputs/SOURCE-IDENTITIES.json').read_bytes())
        population = helper_module(state, 'population.py', 'fixture_population')
        boundary = helper_module(state, 'boundary.py', 'fixture_boundary')
        originals = population.original_metadata_tree(repo)
        require(len(originals) == 16103 and set(originals) <= set(stage),
                'Original native path metadata is not completely present before the trial')
        objects = json.loads((repo/MANIFEST).read_bytes())['objects']
        require(len(objects) == 28478, 'Public projection universe differs')
        sizes = {}
        for relative in boundary.PROTECTED_PATHS:
            digest = Path(relative).parent.name
            matched = [row for row in objects if row.get('repository_path') == relative]
            require(len(matched) == 1 and matched[0]['source_sha256'] == matched[0]['public_sha256'] == digest
                    and type(matched[0]['source_bytes']) is int
                    and matched[0]['source_bytes'] == matched[0]['public_bytes'],
                    'Published protected size/digest metadata differs')
            sizes[relative] = matched[0]['source_bytes']
        public_manifest = {}
        for line in (repo/GENERATED[2]).read_text().splitlines():
            digest, relative = line.split('  ', 1)
            require(relative not in public_manifest, 'Duplicate public release metadata path')
            public_manifest[relative] = digest
        # Unknown sizes remain None; only five already published sizes enter the
        # existing metadata-only boundary. No native size/object lookup occurs.
        held_originals = {path: (*row, sizes.get(path)) for path, row in originals.items()}
        held = boundary.derive_held_metadata(repo, held_originals, stage, public_manifest)
        save(state/'inputs/hold.json', {'held': held, 'held_worktree_body_integrity': 'UNKNOWN'})
        received['inputs/hold.json'] = identity((state/'inputs/hold.json').read_bytes())
        held, held_guard = install_guard(repo, state)
        audit = PublicFixtureAudit(repo, state, parent=True)
        sys.addaudithook(audit.audit)
        initial_sources = set(PUBLIC_FIXTURE_SOURCE_PATHS) | set(PUBLIC_HELPERS.values()) | {
            'scripts/check_source_alias_absence.py', MANIFEST, PUBLIC_FIXTURE_OWNER,
            PUBLIC_FIXTURE_CROSSWALK, PUBLIC_FIXTURE_CENSUS,
            GENERATED[2], 'requirements-ci.lock.txt'}
        for relative in sorted(initial_sources):
            value = public_fixture_file(repo, relative)
            expected = ('100644 blob '+value['git_blob']+'\t'+relative).encode()+b'\0'
            require(stage.get(relative) == ('100644', value['git_blob'])
                    and public_fixture_git(repo, state, 'ls-tree', '-z', admission['head'], '--', relative) == expected,
                    'Current finite consumer source differs from native HEAD/index')
        rows, providers = population.derive_public_fixture_population(repo, originals, objects)
        members = {row['path'] for row in rows}
        require(not members & set(boundary.PROTECTED_PATHS), 'Protected original selected')
        audit.members = members
        for provider in providers:
            path = provider['path']
            actual = public_fixture_file(repo, path)
            require({key: actual[key] for key in ('bytes', 'sha256', 'git_blob')} == {
                        key: provider[key] for key in ('bytes', 'sha256', 'git_blob')}
                    and stage.get(path) == ('100644', provider['git_blob']), 'Current provider native identity differs')
            atomic_bytes(state/'provider-bodies'/provider['sha256'], (repo/path).read_bytes())
        finite_sources = initial_sources | members | {row['path'] for row in providers}
        before = capture_public_fixture_sources(repo, finite_sources)
        namespace = public_fixture_namespace(repo)
        require(set(namespace['files']) == set(stage), 'Unexpected initial untracked or absent checkout path')
        save(state/'before-namespace.json', namespace)
        fixed = {path: value for path, value in before.items() if path not in members}
        save(state/'inputs/fixture-sources.json', fixed)
        save(state/'inputs/fixture-population.json', {'records': rows, 'providers': providers})
        save(state/'before.json', before)
        atomic_bytes(state/'original-index', original_index)
        atomic_bytes(state/'expected-index', original_index)
        save(state/'index-mode.json', {'mode': stat.S_IMODE((repo/'.git/index').stat().st_mode)})
        harness = Path(__file__).read_bytes()
        require(identity(harness) == {key: before['scripts/check_source_alias_absence.py'][key]
                                     for key in ('bytes', 'sha256', 'git_blob')}, 'Executing runner source differs')
        atomic_bytes(state/'inputs/harness.py', harness)
        for relative in ('inputs/fixture-sources.json', 'inputs/fixture-population.json', 'inputs/harness.py',
                         'ADMISSION.json', 'index-mode.json', 'native-stage-before.z', 'before-namespace.json'):
            received[relative] = identity((state/relative).read_bytes())
        require(public_fixture_index(repo) == original_index and held_guard.denials == 0
                and not audit.private_denials, 'Preparation index or protected boundary changed')
        prepared = {'schema': 'hosted-public-fixtures123-preparation-v1', 'profile': PUBLIC_FIXTURE_PROFILE,
                    'status': 'PREPARED_NO_ABSENCE', 'repo': str(repo), 'state': str(state),
                    'repo_inode': [repo.stat().st_dev, repo.stat().st_ino], 'head': admission['head'],
                    'tree': public_fixture_git(repo, state, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                    'admission': admission, 'runtime': runtime_record, 'harness': identity(harness),
                    'operation': operation,
                    'input_files': received, 'before': identity((state/'before.json').read_bytes()),
                    'raw_index': identity(original_index), 'originals': 123, 'providers': 3,
                    'source_paths': len(before), 'original_census_paths': 16103,
                    'held_stat': held_stat(repo, held), 'held_denials': 0, 'private_denials': 0,
                    'held_events': held_guard.events, 'private_events': audit.private_denials,
                    'held_worktree_body_integrity': 'UNKNOWN', 'full_reader_or_scoring_claimed': False}
        save(state/'PREPARED.json', prepared)
        save(state/'PREPARATION-BOUNDARY.json', {'native_observations': audit.events,
             'native_receipts': public_fixture_native_receipts(), 'operation': operation,
             'private_denials': len(audit.private_denials), 'private_events': audit.private_denials,
             'held_denials': held_guard.denials, 'held_events': held_guard.events})
    return prepared, held, held_guard, audit


def authenticate_public_fixture_state(repo, state):
    repo, state = Path(repo), Path(state)
    prepared = json.loads(saved_input_path(state, 'PREPARED.json').read_bytes())
    require(prepared['profile'] == PUBLIC_FIXTURE_PROFILE and prepared['originals'] == 123
            and prepared['providers'] == 3 and prepared['repo'] == str(repo) and prepared['state'] == str(state),
            'Saved public123 profile or coordinate differs')
    require(prepared['repo_inode'] == [repo.stat().st_dev, repo.stat().st_ino], 'Hosted checkout root was replaced')
    require(identity(Path(__file__).read_bytes()) == prepared['harness'], 'Executing public123 runner changed')
    for relative, value in prepared['input_files'].items():
        require(identity(saved_input_path(state, relative).read_bytes()) == value, 'Prepared public123 input changed: '+relative)
    helper_identities = json.loads(saved_input_path(state, 'inputs/SOURCE-IDENTITIES.json').read_bytes())
    require(set(helper_identities) == set(PUBLIC_HELPERS), 'Complete saved helper population differs')
    for name, path in PUBLIC_HELPERS.items():
        body = saved_input_path(state, 'inputs/'+name).read_bytes()
        require(helper_identities[name]['source_path'] == path, 'Saved helper source owner differs')
        expected = ('100644 blob '+identity(body)['git_blob']+'\t'+path).encode()+b'\0'
        require(public_fixture_git(repo, state, 'ls-tree', '-z', prepared['head'], '--', path) == expected,
                'Saved helper does not equal the native published source')
    require(admit_public_fixture_checkout(repo, state, fresh=False, saved=True) == prepared['admission'],
            'Actual hosted public123 admission changed')
    require(public_fixture_runtime(repo) == prepared['runtime'], 'Public123 runtime changed')
    before_body = saved_input_path(state, 'before.json').read_bytes()
    require(identity(before_body) == prepared['before'], 'Prepared public123 source vector changed')
    population = helper_module(state, 'population.py', 'fixture_received_population')
    value = json.loads(saved_input_path(state, 'inputs/fixture-population.json').read_bytes())
    population.validate_public_fixture_population(value['records'])
    require(len(value['providers']) == 3 and {row['path']: (row['git_blob'], row['sha256'], row['bytes'])
            for row in value['providers']} == population.PUBLIC_FIXTURE_PROVIDER_IDENTITIES,
            'Current public123 provider population differs')
    require(identity(saved_input_path(state, 'original-index').read_bytes()) == prepared['raw_index'],
            'Original public123 raw index backup changed')
    fixed = json.loads(saved_input_path(state, 'inputs/fixture-sources.json').read_bytes())
    fixed_names = set(PUBLIC_FIXTURE_SOURCE_PATHS) | set(PUBLIC_HELPERS.values()) | {
        'scripts/check_source_alias_absence.py', MANIFEST, PUBLIC_FIXTURE_OWNER,
        PUBLIC_FIXTURE_CROSSWALK, PUBLIC_FIXTURE_CENSUS,
        GENERATED[2], 'requirements-ci.lock.txt'} | set(population.PUBLIC_FIXTURE_PROVIDER_IDENTITIES)
    require(set(fixed) == fixed_names and set(json.loads(before_body)) == fixed_names | {
                row['path'] for row in value['records']}, 'Complete finite public source closure differs')
    _, stage = public_fixture_stage_map(repo, state)
    for path, original in fixed.items():
        require(_public_fixture_same_source(public_fixture_file(repo, path), original),
                'Current public123 fixed source changed: '+path)
        expected = ('100644 blob '+original['git_blob']+'\t'+path).encode()+b'\0'
        require(stage.get(path) == ('100644', original['git_blob'])
                and public_fixture_git(repo, state, 'ls-tree', '-z', prepared['head'], '--', path) == expected,
                'Finite current public source native HEAD/index differs: '+path)
    return prepared, json.loads(before_body), value


def public_fixture_consumers(repo, state, value, audit):
    """Four actual public consumer routes; no whole-reader or science verdict."""
    sys.path.insert(0, str(repo/'scripts'))
    source = __import__('resolve_t20_v6_source')
    projection = __import__('validate_t20_v6_projection')
    references = __import__('validate_internal_references')
    adapter = helper_module(state, 'reader_adapter.py', 'fixture_reader_adapter')
    held = json.loads((state/'inputs/hold.json').read_bytes())['held']
    boundary = adapter.install(repo, held)
    reader = __import__('check_reader_pilot')
    require(Path(references.ROOT) == repo and all(Path(module.__file__).resolve().parent == repo/'scripts'
            for module in (source, projection, references, reader)), 'Actual public consumer import root differs')
    result = {'public_objects': [], 'source_bytes': [], 'references': [], 'currentness_errors': [],
              'whole_reader_or_scoring_claimed': False}
    saved_index = public_fixture_index(repo)
    for row in value['records']:
        path, public = row['path'], row['public_row']
        if audit.absent:
            audit.observation('before-object-'+path)
        errors = projection.check_object(repo, public)
        result['public_objects'].append({'path': path, 'errors': errors})
        try:
            data = source.source_bytes(repo, public)
            exact = identity(data) == {key: row[key] for key in ('sha256', 'bytes', 'git_blob')}
            source_errors = [] if exact else ['Original generated bytes differ']
        except (ValueError, OSError) as error:
            source_errors = [repr(error)]
        result['source_bytes'].append({'path': path, 'errors': source_errors})
        relative = os.path.relpath(path, Path(MANIFEST).parent)
        result['references'].append({'path': path, 'root': references._resolves(MANIFEST, path),
                                     'relative': references._resolves(MANIFEST, relative)})
    owner_body = (repo/PUBLIC_FIXTURE_OWNER).read_bytes()
    require(identity(owner_body)['sha256'] == adapter.OWNER_MAP_SHA256,
            'Actual public reader owner map changed after adapter admission')
    owner = json.loads(owner_body)
    cross = json.loads((repo/PUBLIC_FIXTURE_CROSSWALK).read_bytes())
    require(owner.get('schema') == 'orthemology-reader-owner-map-v1'
            and owner.get('external_body_admissions') == []
            and cross.get('schema') == 'orthemology-reader-crosswalk-v1'
            and cross.get('coverage_stage') in ('representative-pilot', 'reader-candidate'),
            'Actual public reader context schema or external admission differs')
    with adapter.bounded_git_environment():
        indexed = boundary.currentness_baseline(reader, owner, (repo/PUBLIC_FIXTURE_CENSUS).read_bytes())
        contexts, context_errors = reader.corpus_currentness_context(repo, indexed, owner, cross)
        frontier_paths, frontier_errors = reader.check_frontier_record_absences(
            repo, indexed, owner, cross, contexts[0])
        result['currentness_errors'] = context_errors + frontier_errors + reader.check_corpus_currentness(
            repo, owner['baseline']['commit'], *contexts, frontier_paths)
    result['reader_boundary'] = boundary.receipt()
    require(public_fixture_index(repo) == saved_index, 'Actual consumer changed the raw native index')
    if audit.absent:
        audit.observation('after-four-consumer-groups')
    result['passed'] = (len(result['public_objects']) == len(result['source_bytes']) == len(result['references']) == 123
        and all(not row['errors'] for row in result['public_objects'] + result['source_bytes'])
        and all(row['root'] and row['relative'] for row in result['references'])
        and not result['currentness_errors'])
    return result


def _public_fixture_write_same_inode(repo, path, body, expected):
    current = public_fixture_file(repo, path)
    require(_public_fixture_same_source(current, expected), 'Controlled provider changed before own write')
    fd = os.open(repo/path, os.O_WRONLY | os.O_NOFOLLOW)
    try:
        now = os.fstat(fd)
        require((now.st_dev, now.st_ino, now.st_nlink) == (expected['device'], expected['inode'], 1),
                'Controlled provider inode changed before write')
        require(now.st_size == expected['bytes'] and now.st_mtime_ns == expected['mtime_ns']
                and stat.S_IMODE(now.st_mode) == expected['mode'], 'Controlled provider changed before truncation')
        os.ftruncate(fd, 0)
        view = memoryview(body)
        while view:
            written = os.write(fd, view)
            require(written > 0, 'Controlled provider write made no progress')
            view = view[written:]
        os.fsync(fd)
    finally:
        os.close(fd)
    return public_fixture_file(repo, path)


def public_fixture_controls(repo, state, value, before, audit):
    """Actual bounded contrary checks, with exact owned-control restoration."""
    source = __import__('resolve_t20_v6_source')
    projection = __import__('validate_t20_v6_projection')
    sample = value['records'][0]
    results = []
    for provider in value['providers']:
        path = provider['path']
        original = (state/'provider-bodies'/provider['sha256']).read_bytes()
        require(identity(original) == {key: provider[key] for key in ('bytes', 'sha256', 'git_blob')},
                'Provider control preimage changed')
        original_vector = public_fixture_file(repo, path)
        require(path in before and _public_fixture_same_source(original_vector, before[path]),
                'Unexplained public fixture source divergence before controlled provider mutation')
        public_fixture_transition_preflight(repo, state, before, audit.members, absent=True)
        control_path = state/'provider-controls'/(uuid.uuid4().hex+'.json')
        control = {'path': path, 'before': original_vector, 'status': 'STARTED_NOT_TERMINAL'}
        save(control_path, control)
        changed = _public_fixture_write_same_inode(repo, path, original+b'\nCONTROLLED_INVALID_PROVIDER\n', original_vector)
        control.update(changed=changed, status='CONTROL_POSTIMAGE_RECEIVED')
        save(control_path, control, replace=True)
        rejection = []
        try:
            try:
                source.generated_fixture_bytes(repo, sample['path'])
            except (ValueError, OSError) as error:
                rejection = [repr(error)]
        finally:
            # A foreign replacement/drift stops here; it is never overwritten.
            public_fixture_transition_preflight(repo, state, before, audit.members, absent=True,
                                                provider_override=(path, changed))
            _public_fixture_write_same_inode(repo, path, original, changed)
            os.utime(repo/path, ns=(original_vector['atime_ns'], original_vector['mtime_ns']), follow_symlinks=False)
            require(public_fixture_file(repo, path) == original_vector, 'Provider control restoration differs')
        control.update(after=public_fixture_file(repo, path), status='RESTORED_EXACT_PROVIDER_CONTROL', errors=rejection)
        save(control_path, control, replace=True)
        results.append({'kind': 'provider-body', 'path': path, 'errors': rejection, 'exact_restoration': True,
                        'control_record': control_path.relative_to(state).as_posix()})
        require(rejection, 'Actual wrong-provider control was admitted')
    # Three genuine native staged-provider mode corruptions; body is unchanged.
    for provider in value['providers']:
        public_fixture_transition_preflight(repo, state, before, audit.members, absent=True)
        saved = public_fixture_index(repo)
        arguments = ('update-index', '--cacheinfo', '100755,'+provider['git_blob']+','+provider['path'])
        audit.allowed_index = arguments
        try:
            public_fixture_git(repo, state, *arguments)
        finally:
            audit.allowed_index = None
        changed = public_fixture_index(repo)
        rejection = []
        try:
            try:
                source.generated_fixture_bytes(repo, sample['path'])
            except (ValueError, OSError) as error:
                rejection = [repr(error)]
        finally:
            mode = json.loads((state/'index-mode.json').read_bytes())['mode']
            cleanup = restore_public_fixture_control_index(repo, state, before, audit.members, saved, changed, mode)
        results.append({'kind': 'provider-index-mode', 'path': provider['path'], 'errors': rejection,
                        'exact_restoration': True, 'restoration': cleanup})
        require(rejection, 'Actual staged-provider control was admitted')
    for field, replacement in [('role', 'unadmitted_proof'), ('public_sha256', '0'*64)]:
        errors = projection.check_object(repo, dict(sample['public_row'], **{field: replacement}))
        results.append({'kind': 'public-row-'+field, 'path': sample['path'], 'errors': errors,
                        'exact_restoration': True})
        require(errors, 'Changed original public row control was admitted')
    for path in ('not-an-admitted-public-fixture.json', 'experiments/episode-reification-v2/fixtures/KEYS.json'):
        rejection = []
        try:
            source.generated_fixture_bytes(repo, path)
        except (ValueError, OSError) as error:
            rejection = [repr(error)]
        results.append({'kind': 'nonmember-request', 'path': path, 'errors': rejection, 'exact_restoration': True})
        require(rejection, 'Nonmember public fixture request was admitted')
    require(len(results) == 10 and public_fixture_index(repo) == (state/'expected-index').read_bytes(),
            'Contrary control count or restored native index differs')
    for path, original in before.items():
        if path not in audit.members:
            require(_public_fixture_same_source(public_fixture_file(repo, path), original),
                    'Post-control current source differs')
    audit.observation('after-ten-contrary-controls')
    return {'controls': results, 'passed': True, 'public_originals_remain_absent': True}


def bounded_public_fixture_phase(repo, state, phase, token, identity_fd):
    with os.fdopen(identity_fd, 'wb') as pipe:
        pipe.write(json.dumps(group_record()).encode()+b'\n')
        pipe.flush()
    require(sys.stdin.readline().rstrip('\n') == token and token, 'Missing durable public123 parent lease')
    require(phase in PUBLIC_FIXTURE_PHASES, 'Unknown public123 phase')
    prepared, before, value = authenticate_public_fixture_state(repo, state)
    out = state/'phases'/phase
    require(json.loads((out/'START.json').read_bytes())['token'] == token, 'Public123 phase lease differs')
    held, guard = install_guard(repo, state)
    audit = PublicFixtureAudit(repo, state, [row['path'] for row in value['records']])
    audit.absent = phase != 'fixtures123-present'
    sys.addaudithook(audit.audit)
    receipt = {'profile': PUBLIC_FIXTURE_PROFILE, 'phase': phase, 'status': 'RUNNING',
               'lease_token': token, 'process': process_identity(), 'group': group_record(),
               'held_worktree_body_integrity': 'UNKNOWN'}
    try:
        require(held_stat(repo, held) == prepared['held_stat'], 'Held metadata changed before public123 phase')
        if audit.absent:
            observation = audit.observation('child-entry')
            save(out/'ABSENCE-CHILD-ENTRY.json', observation)
        else:
            require(all(_public_fixture_same_source(public_fixture_file(repo, row['path']), before[row['path']])
                        for row in value['records']), 'Public123 present phase original identity differs')
        check_public_fixture_namespace(repo, state, audit.members if audit.absent else set())
        sys.path.insert(0, str(repo/'scripts'))
        os.chdir(repo)
        if phase == 'fixtures123-controls':
            receipt['result'] = public_fixture_controls(repo, state, value, before, audit)
        else:
            receipt['result'] = public_fixture_consumers(repo, state, value, audit)
        require(receipt['result']['passed'], 'Actual public123 consumer/control result failed; see exact result')
        check_public_fixture_namespace(repo, state, audit.members if audit.absent else set())
        require(guard.denials == 0 and not audit.private_denials, 'Public123 protected/access boundary failed')
        receipt['status'] = 'PASS_PUBLIC_FIXTURE_PHASE_ONLY'
    except BaseException as error:
        receipt.update(status='FAIL_OR_INTERRUPTED', error=repr(error), traceback=traceback.format_exc())
        raise
    finally:
        receipt.update(held_denials=guard.denials, held_events=guard.events,
                       private_denials=len(audit.private_denials), private_events=audit.private_denials,
                       native_argv_observations=audit.events, absence_boundaries=audit.absence_observations,
                       native_receipts=public_fixture_native_receipts(),
                       scope='Actual finite public consumer calls; no full-reader/scoring/science acceptance.')
        save(out/'TERMINAL.json', receipt)


def public_fixture_child_custody(repo, state, out, phase, token, prefix, before_lease, *, handshake_timeout=30):
    """Own every child from before Popen through actual wait, including failed startup."""
    import selectors
    import time
    require(re.fullmatch(r'[0-9a-f]{32}', token) is not None, 'Invalid child custody token')
    require(0 < handshake_timeout <= 30, 'Unbounded public child handshake')
    custody_path = state/'children'/(token+'.json')
    custody = {'profile': PUBLIC_FIXTURE_PROFILE, 'phase': phase, 'token': token,
               'parent': process_identity(), 'command_prefix': prefix, 'pid': None,
               'group': None, 'group_record_persisted': False, 'lease_sent': False,
               'status': 'DECLARED_NO_CHILD', 'exit_code': None, 'quiescent': False}
    save(custody_path, custody)
    child = None
    group = None
    read_fd = write_fd = None
    log = None
    try:
        read_fd, write_fd = os.pipe()
        command = prefix + ['--identity-fd', str(write_fd)]
        custody['command'] = command
        log = (out/'stdout.log').open('xb')
        child = subprocess.Popen(command, cwd=repo, env=public_fixture_environment(), stdin=subprocess.PIPE,
                                 stdout=log, stderr=subprocess.STDOUT, start_new_session=True, pass_fds=(write_fd,))
        custody.update(pid=child.pid, status='SPAWNED_NO_HANDSHAKE')
        save(custody_path, custody, replace=True)
        os.close(write_fd); write_fd = None
        body = b''
        deadline = time.monotonic()+handshake_timeout
        with selectors.DefaultSelector() as selector:
            selector.register(read_fd, selectors.EVENT_READ)
            while b'\n' not in body:
                remaining = deadline-time.monotonic()
                require(remaining > 0 and selector.select(remaining), 'Actual child identity handshake timed out')
                piece = os.read(read_fd, 4096-len(body))
                require(piece and len(body)+len(piece) < 4096, 'Missing or oversized child identity handshake')
                body += piece
        require(body.endswith(b'\n') and body.count(b'\n') == 1, 'Malformed child handshake framing')
        candidate_group = json.loads(body)
        validate_group_record(candidate_group)
        require(candidate_group['process']['pid'] == child.pid == candidate_group['pgid'] == candidate_group['sid']
                and candidate_group['process']['proc_pid'] == candidate_group['proc_pgid'] == candidate_group['proc_sid']
                and candidate_group['process']['pid_namespace'] == process_identity()['pid_namespace']
                and live_process(candidate_group['process']), 'Actual public123 child session identity differs')
        group = candidate_group
        custody.update(group=group, status='HANDSHAKE_RECEIVED_UNLEASED')
        save(custody_path, custody, replace=True)
        save(state/'groups'/(token+'.json'), group)
        custody['group_record_persisted'] = True
        save(out/'child.json', {'process': group['process'], 'group': group, 'command': command,
                                'token': token, 'custody_record': 'children/'+token+'.json'})
        before_lease()
        lease = {'token': token, 'phase': phase, 'child': group['process'],
                 'command': command, 'status': 'DURABLE_INTENT_BEFORE_SEND'}
        save(out/'LEASE.json', lease)
        child.stdin.write((token+'\n').encode()); child.stdin.close()
        custody.update(lease_sent=True, status='LEASED')
        save(custody_path, custody, replace=True)
        lease['status'] = 'SENT_TO_CHILD'
        save(out/'LEASE.json', lease, replace=True)
        custody['exit_code'] = child.wait()
        return custody
    except BaseException as error:
        custody.update(error_type=type(error).__name__, error=str(error))
        raise
    finally:
        for fd in (read_fd, write_fd):
            if fd is not None:
                with contextlib.suppress(OSError): os.close(fd)
        if child is not None:
            if child.stdin is not None and not child.stdin.closed:
                with contextlib.suppress(BrokenPipeError): child.stdin.close()
            if child.poll() is None:
                if group is not None and live_process(group['process']):
                    with contextlib.suppress(ProcessLookupError): os.killpg(group['pgid'], signal.SIGTERM)
                else:
                    child.terminate()
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if group is not None and live_process(group['process']):
                        with contextlib.suppress(ProcessLookupError): os.killpg(group['pgid'], signal.SIGKILL)
                    else:
                        child.kill()
                    child.wait(timeout=5)
            custody['exit_code'] = child.returncode
        members = group_members(group) if group is not None else None
        custody['quiescent'] = bool(child is not None and type(child.returncode) is int
            and group is not None and custody['group_record_persisted']
            and not any(row['state'] != 'Z' for row in members))
        custody['status'] = 'TERMINAL_RECEIVED' if child is not None and type(child.returncode) is int else 'UNRESOLVED'
        quiet = {'group': group, 'observed_members': members, 'quiescent': custody['quiescent'],
                 'custody_record': 'children/'+token+'.json', 'token': token}
        save(out/'QUIESCENCE.json', quiet)
        if log is not None:
            log.flush(); os.fsync(log.fileno()); log.close()
            custody['stdout'] = identity((out/'stdout.log').read_bytes())
        save(custody_path, custody, replace=True)
        save(out/'CHILD-RESULT.json', custody)


def public_fixture_quiescence(state, *, allow_current=False):
    """Missing pending child/group custody cannot disappear from restoration gates."""
    received = receive_quiescence(state, allow_current=allow_current)
    children = []
    for path in sorted((state/'children').glob('*.json')):
        child = json.loads(saved_input_path(state, path.relative_to(state).as_posix()).read_bytes())
        group_path = state/'groups'/path.name
        exact = (child.get('status') == 'TERMINAL_RECEIVED' and type(child.get('exit_code')) is int
                 and child.get('quiescent') is True and child.get('group_record_persisted') is True
                 and group_path.exists() and json.loads(group_path.read_bytes()) == child.get('group'))
        if exact:
            exact = not any(row['state'] != 'Z' for row in group_members(child['group']))
        children.append({'record': path.relative_to(state).as_posix(), 'child': child, 'exact_quiescent': exact})
    received['children'] = children
    received['quiescent'] = received['quiescent'] and all(row['exact_quiescent'] for row in children)
    return received


def run_public_fixture_phase(repo, state, phase, value):
    require(phase in PUBLIC_FIXTURE_PHASES, 'Unadmitted public123 phase')
    out = state/'phases'/phase
    mkdir_durable(out)
    token = uuid.uuid4().hex
    save(out/'START.json', {'profile': PUBLIC_FIXTURE_PROFILE, 'phase': phase,
                            'token': token, 'process': process_identity()})
    command = [sys.executable, '-B', str(Path(__file__).absolute()), '_fixture-phase',
               '--repo', str(repo), '--state', str(state), '--phase', phase, '--token', token]
    def before_lease():
        if phase != 'fixtures123-present':
            observation = observe_absence(repo, {row['path'] for row in value['records']})
            save(out/'ABSENCE-BEFORE-LEASE.json', observation)
            require(observation['complete'], 'Complete public123 absence is required before the child lease')
        else:
            before = json.loads((state/'before.json').read_bytes())
            rows = [{'path': row['path'], 'exact': _public_fixture_same_source(
                public_fixture_file(repo, row['path']), before[row['path']])} for row in value['records']]
            save(out/'PRESENT-BEFORE-LEASE.json', {'rows': rows, 'complete': all(row['exact'] for row in rows)})
            require(len(rows) == 123 and all(row['exact'] for row in rows), 'Complete present original population differs')
    try:
        custody = public_fixture_child_custody(repo, state, out, phase, token, command, before_lease)
    finally:
        custody_path = state/'children'/(token+'.json')
        custody = json.loads(custody_path.read_bytes()) if custody_path.exists() else {}
        terminal = out/'TERMINAL.json'
        result = {'phase': phase, 'token': token, 'exit_code': custody.get('exit_code'),
                  'stdout': custody.get('stdout'), 'custody_record': 'children/'+token+'.json',
                  'terminal': identity(terminal.read_bytes()) if terminal.exists() else None}
        save(out/'PROCESS.json', result)
    require(type(result['exit_code']) is int and result['exit_code'] == 0 and terminal.exists()
            and custody.get('quiescent') is True and custody.get('lease_sent') is True,
            'Actual public123 phase process failed or is not quiescent')
    receipt = json.loads(terminal.read_bytes())
    require(receipt['status'] == 'PASS_PUBLIC_FIXTURE_PHASE_ONLY'
            and receipt['held_denials'] == receipt['private_denials'] == 0,
            'Actual public123 phase boundary failed')
    return result


def restore_public_fixture_execution(repo, state, *, guards=None):
    require(not (state/'FIXTURE-RESTORATION-FAILURE.json').exists(),
            'A previous restoration abnormality is contained; no reset or retry is admitted')
    require(not (state/'FIXTURE-RESTORATION-TERMINAL.json').exists(),
            'Public123 restoration is already complete; no duplicate action is admitted')
    if guards is None:
        held, guard = install_guard(repo, state)
        audit = PublicFixtureAudit(repo, state, parent=True)
        sys.addaudithook(audit.audit)
    else:
        held, guard, audit = guards
    quiet = public_fixture_quiescence(state, allow_current=True)
    save(state/'QUIESCENCE-BEFORE-RESTORE.json', quiet)
    require(quiet['quiescent'], 'Owned child or native process remains; public123 restoration is blocked')
    prepared, before, value = authenticate_public_fixture_state(repo, state)
    members = {row['path'] for row in value['records']}
    require(held_stat(repo, held) == prepared['held_stat'], 'Protected metadata changed; restoration is blocked')
    save(state/'RESTORATION-NAMESPACE.json', observe_absence(repo, members))
    # A partial park after interruption is permitted only at paths whose exact
    # original inode is in the private park; all other metadata must be intact.
    parked = {path for path in members if os.path.lexists(state/'park'/path)}
    check_public_fixture_namespace(repo, state, parked)
    audit.restoring = True
    result = restore_public_fixture_members(repo, state, before, members)
    namespace = check_public_fixture_namespace(repo, state, set())
    save(state/'after-namespace.json', namespace)
    require(guard.denials == 0 and not audit.private_denials, 'Public123 protected boundary failed')
    return result


def execute_public_fixtures(repo, state, received):
    _, held, guard, audit = received
    prepared, before, value = authenticate_public_fixture_state(repo, state)
    members = {row['path'] for row in value['records']}
    audit.members = members
    with operation_lock(state, 'execute-public-fixtures123') as operation:
        require(not (state/'EXECUTION-START.json').exists(), 'Public123 trial is single-use; never replay a failed trial')
        save(state/'EXECUTION-START.json', {'profile': PUBLIC_FIXTURE_PROFILE,
             'prepared': identity((state/'PREPARED.json').read_bytes()), 'process': process_identity(),
             'operation': operation,
             'members': sorted(members), 'status': 'STARTED_NOT_TERMINAL'})
        result = {'profile': PUBLIC_FIXTURE_PROFILE, 'status': 'RUNNING', 'phases': [],
                  'held_worktree_body_integrity': 'UNKNOWN'}
        failure = None
        try:
            require(public_fixture_index(repo) == (state/'original-index').read_bytes(), 'Initial raw index differs')
            result['phases'].append(run_public_fixture_phase(repo, state, 'fixtures123-present', value))
            park_public_fixture_members(repo, state, before, members)
            audit.absent = True
            save(state/'ABSENCE-AFTER-PARK.json', audit.observation('after-original-parking'))
            _, unstaged = public_fixture_stage_map(repo, state)
            require(all(unstaged.get(row['path']) == ('100644', row['git_blob']) for row in value['records'])
                    and public_fixture_index(repo) == (state/'original-index').read_bytes(),
                    'Exact unstaged public123 deletion membership differs')
            save(state/'UNSTAGED-MEMBERSHIP.json', {'paths': sorted(members), 'all_original_index_entries_retained': True,
                                                  'raw_index': identity(public_fixture_index(repo))})
            result['phases'].append(run_public_fixture_phase(repo, state, 'fixtures123-unstaged', value))
            arguments = ('update-index', '--force-remove', '--', *sorted(members))
            audit.allowed_index = arguments
            try:
                public_fixture_git(repo, state, *arguments)
            finally:
                audit.allowed_index = None
            atomic_bytes(state/'expected-index', public_fixture_index(repo), replace=True)
            raw_staged, staged = public_fixture_stage_map(repo, state)
            atomic_bytes(state/'native-stage-absent.z', raw_staged)
            expected = dict(unstaged)
            for path in members:
                expected.pop(path)
            require(staged == expected, 'Native index changed outside exact public123 deletion membership')
            save(state/'STAGED-MEMBERSHIP.json', {'paths': sorted(members), 'all_original_index_entries_removed': True,
                                                'other_entries_unchanged': True, 'raw_index': identity(public_fixture_index(repo))})
            save(state/'ABSENCE-AFTER-INDEX.json', audit.observation('after-exact-index-removal'))
            for phase in PUBLIC_FIXTURE_PHASES[2:]:
                result['phases'].append(run_public_fixture_phase(repo, state, phase, value))
            result['status'] = 'PASS_PUBLIC_FIXTURE_CONSUMERS_PENDING_RESTORATION'
        except BaseException as error:
            failure = error
            result.update(status='FAIL_OR_INTERRUPTED', error=repr(error), traceback=traceback.format_exc())
        finally:
            save(state/'CONSUMERS-TERMINAL.json', result)
            try:
                result['restoration'] = restore_public_fixture_execution(repo, state, guards=(held, guard, audit))
            except BaseException as error:
                failure = failure or error
                result['restoration_error'] = repr(error)
                save(state/'FIXTURE-RESTORATION-FAILURE.json', {'status': 'STOPPED_WITHOUT_RESET_OR_REPLAY',
                    'error': repr(error), 'namespace': observe_absence(repo, members),
                    'park_preserved': True, 'no_restoration_success_claimed': True})
            result.update(held_denials=guard.denials, private_denials=len(audit.private_denials),
                          held_events=guard.events, private_events=audit.private_denials,
                          native_argv_observations=audit.events, absence_boundaries=audit.absence_observations)
            result['native_receipts'] = public_fixture_native_receipts()
            result['status'] = ('PASS_PUBLIC_FIXTURE_EXECUTION_AND_RESTORATION'
                                if failure is None and not guard.denials and not audit.private_denials
                                else 'FAIL_OR_INTERRUPTED')
            save(state/'EXECUTION-TERMINAL.json', result)
        print(json.dumps({'profile': PUBLIC_FIXTURE_PROFILE, 'status': result['status'],
                          'terminal': str(state/'EXECUTION-TERMINAL.json')}))
        if failure is not None:
            raise failure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('run', 'run-current', 'restore', 'export', '_phase', 'run-fixtures', 'restore-fixtures', 'export-fixtures', '_fixture-phase'))
    parser.add_argument('--repo', type=Path, default=Path(os.environ.get('GITHUB_WORKSPACE', '.')))
    parser.add_argument('--state', type=Path,
                        default=Path(os.environ.get('RUNNER_TEMP', '.')) / 'r0002-source-alias-absence')
    parser.add_argument('--phase', choices=PHASES + PUBLIC_FIXTURE_PHASES)
    parser.add_argument('--token')
    parser.add_argument('--identity-fd', type=int)
    args = parser.parse_args()
    environment = sanitized_env()
    os.environ.clear()
    os.environ.update(environment)
    repo = ordinary_dir(args.repo)
    state = args.state.absolute()
    if args.command in ('run-fixtures', 'restore-fixtures', 'export-fixtures', '_fixture-phase'):
        os.environ.update(public_fixture_environment())
        if args.command == 'export-fixtures':
            export_public_fixture_execution(repo, state)
            return
        require(os.getsid(0) == os.getpid() == os.getpgrp(), 'Invoke the actual public123 runner with setsid')
        def fixture_interrupted(signum, frame):
            raise KeyboardInterrupt('Hosted public123 runner interrupted by signal '+str(signum))
        signal.signal(signal.SIGTERM, fixture_interrupted)
        signal.signal(signal.SIGHUP, fixture_interrupted)
        with PublicFixtureNativeRecorder(repo, state):
            if args.command == 'run-fixtures':
                received = prepare_public_fixtures(repo, state)
                execute_public_fixtures(repo, state, received)
            elif args.command == 'restore-fixtures':
                admit_public_fixture_checkout(repo, state, fresh=False, saved=True)
                require(public_fixture_quiescence(state, allow_current=True)['quiescent'],
                        'Unreceived child custody blocks restore lock recovery')
                with operation_lock(state, 'restore-public-fixtures123', recover=True):
                    print(json.dumps(restore_public_fixture_execution(repo, state)))
            else:
                require(args.phase in PUBLIC_FIXTURE_PHASES and args.token and args.identity_fd is not None,
                        'Public123 internal phase requires its exact durable lease')
                bounded_public_fixture_phase(repo, state, args.phase, args.token, args.identity_fd)
        return
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
    if args.command in ('run', 'run-current'):
        prepare(repo, state, current_checkout=args.command == 'run-current')
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



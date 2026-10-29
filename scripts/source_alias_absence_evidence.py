"""Whitelisted public metadata export for the hosted absence regression."""
from pathlib import Path
import hashlib
import json
import os
import re
import stat


def require(value, message):
    if not value: raise RuntimeError(message)


def identity(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()}


def ordinary_source(state, relative):
    require(isinstance(relative, str) and relative and not relative.startswith('/')
            and all(part not in ('', '.', '..') for part in relative.split('/')), 'Unsafe evidence path')
    state = Path(state).absolute()
    require(stat.S_ISDIR(state.lstat().st_mode), 'Evidence state is not an ordinary directory')
    node = state
    for part in relative.split('/')[:-1]:
        node /= part
        require(stat.S_ISDIR(node.lstat().st_mode), 'Evidence ancestor is not an ordinary directory')
    path = state / relative
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'Evidence must be an unaliased ordinary file')
    return path


def read(state, relative):
    return ordinary_source(state, relative).read_bytes()


def read_json(state, relative):
    return json.loads(read(state, relative))

def terminal_complete(record, phases):
    try:
        return (record['status'] == 'PASS_BOUNDED_EXECUTION_AND_RESTORATION'
            and type(record['held_denials']) is int and record['held_denials'] == 0
            and len(phases) == 13 and len(set(phases)) == 13
            and [row['phase'] for row in record['phases']] == list(phases)
            and all(row['exit_code'] == 0 and row['terminal'] for row in record['phases'])
            and record['restoration']['status'] == 'PASS_EXACT_RESTORATION_ONLY'
            and record['restoration']['held_denials'] == 0)
    except (KeyError, TypeError):
        return False

def whitelisted_files(state, phases):
    state = Path(state).absolute()
    require(len(phases) == len(set(phases)) == 13
            and all(re.fullmatch(r'[a-z0-9_-]+', name) for name in phases), 'Invalid phase whitelist')
    names = {
        'ADMISSION.json', 'PREPARED.json', 'before.json', 'classes.json', 'preimages.json', 'original-index',
        'READER-BOUNDARY-PREFLIGHT.json', 'ABSENCE-AFTER-UNLINK.json', 'ABSENCE-AFTER-INDEX.json',
        'ABSENCE-AFTER-PRUNE.json', 'ABSENCE.json', 'EXECUTION-START.json', 'CONSUMERS-TERMINAL.json',
        'QUIESCENCE-BEFORE-RESTORE.json', 'absent-final.json', 'EXECUTION-TERMINAL.json',
        'inputs/hold.json', 'inputs/33.json', 'inputs/98-context.json', 'inputs/SOURCE-IDENTITIES.json',
    }
    phase_files = ('START.json', 'child.json', 'ABSENCE-BEFORE-LEASE.json', 'ABSENCE-CHILD-ENTRY.json',
                   'QUIESCENCE.json', 'PROCESS.json', 'TERMINAL.json', 'stdout.log', 'actual258.json')
    for phase in phases:
        names.update(f'phases/{phase}/{name}' for name in phase_files)
    for cohort in ('258', '98'):
        for endpoint in ('START', 'TERMINAL'):
            names.add(f'phases/negative-controls/negative-{cohort}-{endpoint}.json')
    for category in ('groups', 'writes', 'native-index-mutations', 'quiescence', 'restoration'):
        directory = state / category
        if not os.path.lexists(directory): continue
        require(stat.S_ISDIR(directory.lstat().st_mode), 'Evidence category is not an ordinary directory')
        for path in directory.iterdir():
            if category == 'restoration' and re.fullmatch(r'[0-9a-f]{32}', path.name):
                require(stat.S_ISDIR(path.lstat().st_mode), 'Restoration evidence directory is unsafe')
                for name in ('START.json', 'QUIESCENCE.json', 'after.json', 'TERMINAL.json', 'INDEX-LOCK-QUARANTINE.json'):
                    names.add(f'{category}/{path.name}/{name}')
            elif category != 'restoration' and re.fullmatch(r'[0-9a-f]{32}\.json', path.name):
                names.add(f'{category}/{path.name}')
    return [ordinary_source(state, name) for name in sorted(names) if os.path.lexists(state / name)]

def receive_execution(state, phases):
    state = Path(state).absolute()
    try:
        record = read_json(state, 'EXECUTION-TERMINAL.json')
        require(terminal_complete(record, phases), 'Execution is failed, incomplete, denied or unrestored')
        prepared = read_json(state, 'PREPARED.json')
        require(prepared['held_denials'] == 0 and prepared['originals'] == 1180
                and prepared['unique_canonicals'] == 1082 and prepared['preimage_paths'] == 2265
                and prepared['original_census_paths'] == 16103, 'Prepared population or boundary differs')
        for relative, expected in prepared['input_files'].items():
            require(identity(read(state, relative)) == expected, 'Frozen input changed: ' + relative)
        classes = read_json(state, 'classes.json')
        aliases = {row['alias'] for row in classes}
        require(len(classes) == len(aliases) == 1180, 'Complete alias vector is required')
        for phase, process in zip(phases, record['phases']):
            prefix = 'phases/' + phase + '/'
            terminal_bytes = read(state, prefix + 'TERMINAL.json')
            require(identity(terminal_bytes) == process['terminal'], 'Actual phase terminal identity differs')
            terminal = json.loads(terminal_bytes)
            require(terminal['status'] == 'PASS_BOUNDED_PHASE_ONLY' and terminal['phase'] == phase
                    and terminal['held_denials'] == 0, 'Actual phase did not pass its boundary')
            require(read_json(state, prefix + 'PROCESS.json') == process
                    and identity(read(state, prefix + 'stdout.log')) == process['stdout'], 'Actual process endpoint differs')
            require(read_json(state, prefix + 'QUIESCENCE.json')['quiescent'] is True, 'Phase descendant is not quiet')
            for name in ('ABSENCE-BEFORE-LEASE.json', 'ABSENCE-CHILD-ENTRY.json'):
                observation = read_json(state, prefix + name)
                require(observation['complete'] is True and len(observation['rows']) == 1180
                        and {row['path'] for row in observation['rows']} == aliases
                        and all(row['lstat']['state'] == 'absent' and row['lexists'] is False
                                and row['inconsistent'] is False for row in observation['rows']),
                        'Complete absence is not established at phase entry')
        consumers = read_json(state, 'CONSUMERS-TERMINAL.json')
        require(consumers['status'] == 'PASS_BOUNDED_CONSUMERS_PENDING_RESTORATION'
                and consumers['phases'] == record['phases'], 'Consumer aggregate endpoint differs')
        negatives = read_json(state, 'phases/negative-controls/TERMINAL.json')['result']['actual_retained_controls']
        require([row['cohort'] for row in negatives] == ['258', '98']
                and all(row['errors'] and row['exact_retained_restoration'] is True for row in negatives)
                and negatives[1]['shared824_errors'], 'Required retained-source rejections are absent')
        controls824 = read_json(state, 'phases/824/TERMINAL.json')['result']['negative_controls']
        require(len(controls824) == 3 and all(row['errors'] for row in controls824), 'Required T20 rejections are absent')
        restoration = record['restoration']
        relative = Path(restoration['receipt']).absolute().relative_to(state).as_posix()
        require(re.fullmatch(r'restoration/[0-9a-f]{32}/TERMINAL\.json', relative) is not None,
                'Restoration receipt is outside the finite whitelist')
        terminal = read_json(state, relative)
        require(terminal == {key: value for key, value in restoration.items() if key != 'receipt'},
                'Restoration aggregate does not equal its actual terminal')
        after_relative = relative.rsplit('/', 1)[0] + '/after.json'
        after = read(state, after_relative)
        before = read(state, 'before.json')
        require(identity(after) == terminal['after'] and identity(before) == prepared['before']
                and json.loads(after) == json.loads(before), 'Complete before/after restoration vector differs')
        require(identity(read(state, 'original-index')) == terminal['raw_index'] == prepared['raw_index'],
                'Exact original index identity differs')
        require(read_json(state, 'QUIESCENCE-BEFORE-RESTORE.json')['quiescent'] is True,
                'Restoration did not receive owned process quiescence')
        return {'qualified': True, 'status': 'COMPLETE_PHASES_AND_EXACT_RESTORATION', 'phases': len(phases),
                'aliases': 1180, 'head': prepared['head'], 'tree': prepared['tree'],
                'held_worktree_body_integrity': 'UNKNOWN', 'retirement_credit': 'NOT_GRANTED_BY_THIS_PROGRAM'}
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        return {'qualified': False, 'status': 'FAILED_INCOMPLETE_OR_INCONSISTENT', 'error': repr(error),
                'retirement_credit': 'NONE'}


def export_evidence(state, phases):
    from check_source_alias_absence import atomic_bytes, save
    state = Path(state).absolute()
    destination = state.parent / 'r0002-source-alias-receipts'
    require(not os.path.lexists(destination), 'Evidence export is immutable and single-use')
    outcome = receive_execution(state, phases)
    rows = []
    for source in whitelisted_files(state, phases):
        relative = source.relative_to(state).as_posix()
        body = source.read_bytes()
        if relative.endswith('.json'):
            json.loads(body)
        elif relative == 'original-index':
            require(body[:4] == b'DIRC' and hashlib.sha1(body[:-20]).digest() == body[-20:],
                    'Original index metadata is corrupt')
        else:
            require(relative.endswith('/stdout.log'), 'Unexpected nonmetadata export')
            body.decode('utf-8')
        atomic_bytes(destination / relative, body)
        rows.append({'path': relative, **identity(body)})
    summary = {'schema': 'hosted-source-alias-evidence-export-v1', 'outcome': outcome, 'files': rows,
               'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
               'export_policy': 'Explicit metadata, process logs and raw index only; no backup bodies, proof exports, Git objects or credentials.'}
    save(destination / 'EXPORT-SUMMARY.json', summary)
    print(json.dumps({'status': outcome['status'], 'files': len(rows), 'destination': str(destination)}))
    if not outcome['qualified']:
        raise SystemExit(1)

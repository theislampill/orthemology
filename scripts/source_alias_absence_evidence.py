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

def prepared_alias_scope(prepared, before, classes):
    """Receive historical/current scope from authenticated identities, not labels."""
    aliases = {row['alias'] for row in classes}
    retained = {row['canonical'] for row in classes}
    paths = {row['path'] for row in before['rows']}
    require(len(classes) == len(aliases) == 1180 and len(retained) == 1082
            and not aliases & retained and retained <= paths, 'Complete retained population differs')
    require(len(paths) == len(before['rows']), 'Repeated before-vector path')
    present, retired = aliases & paths, aliases - paths
    profile = prepared.get('profile', 'historical-all-present1180-v1')
    require(profile in ('historical-all-present1180-v1', 'current-checkout1180-v1'), 'Unknown alias profile')
    require(profile != 'historical-all-present1180-v1' or not retired,
            'Historical scope cannot claim previously absent aliases')
    require(prepared.get('initially_absent_aliases', []) == sorted(retired)
            and prepared.get('trial_removed_aliases', sorted(aliases)) == sorted(present),
            'Prepared alias partition differs from original current vector')
    require(prepared['preimage_paths'] == len(present) + len(retained) + 3
            and prepared['expected_absent_tracked'] == len(paths) - len(present),
            'Prepared current backup or absent denominator differs')
    return {'profile': profile, 'historical_aliases_observed': 1180,
            'planned_trial_removals': len(present), 'previously_absent_aliases': len(retired)}


def receive_execution(state, phases):
    state = Path(state).absolute()
    try:
        record = read_json(state, 'EXECUTION-TERMINAL.json')
        require(terminal_complete(record, phases), 'Execution is failed, incomplete, denied or unrestored')
        prepared = read_json(state, 'PREPARED.json')
        require(prepared['held_denials'] == 0 and prepared['originals'] == 1180
                and prepared['unique_canonicals'] == 1082
                and prepared['original_census_paths'] == 16103, 'Prepared population or boundary differs')
        for relative, expected in prepared['input_files'].items():
            require(identity(read(state, relative)) == expected, 'Frozen input changed: ' + relative)
        classes = read_json(state, 'classes.json')
        aliases = {row['alias'] for row in classes}
        require(len(classes) == len(aliases) == 1180, 'Complete alias vector is required')
        before_body = read(state, 'before.json')
        require(identity(before_body) == prepared['before'], 'Authenticated before vector differs')
        scope = prepared_alias_scope(prepared, json.loads(before_body), classes)
        if prepared.get('profile') == 'current-checkout1180-v1':
            require(record.get('trial_scope') == scope, 'Current terminal trial scope differs')
            preimage_body = read(state, 'preimages.json')
            require(identity(preimage_body) == prepared['preimages'], 'Current preimage map changed')
            preimages = json.loads(preimage_body)
            expected_backup = (set(prepared['trial_removed_aliases'])
                | {row['canonical'] for row in classes}
                | {'docs/project-closure/ar8r-v11/SHA256SUMS', 'docs/current-state.yaml',
                   'docs/provenance/RELEASE-MANIFEST.sha256'})
            require(len(preimages) == len(expected_backup) == prepared['preimage_paths']
                    and {row['path'] for row in preimages} == expected_backup,
                    'Current preimage membership differs')
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
                'aliases': 1180, 'head': prepared['head'], 'tree': prepared['tree'], 'trial_scope': scope,
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


PUBLIC_FIXTURE_PHASES = ['fixtures123-present', 'fixtures123-unstaged', 'fixtures123-staged',
                         'fixtures123-controls', 'fixtures123-post-controls']
PUBLIC_FIXTURE_SOURCE_EXPORTS = frozenset('inputs/'+name for name in (
    '258.py', 'boundary.py', 'context.py', 'evidence.py', 'guard.py', 'harness.py',
    'metadata.py', 'population.py', 'reader_adapter.py'))
PUBLIC_FIXTURE_PREPARED_INPUTS = PUBLIC_FIXTURE_SOURCE_EXPORTS | frozenset((
    'inputs/SOURCE-IDENTITIES.json', 'inputs/hold.json', 'inputs/fixture-sources.json',
    'inputs/fixture-population.json', 'ADMISSION.json', 'index-mode.json',
    'native-stage-before.z', 'before-namespace.json'))


def public_fixture_export_inputs(state):
    """Complete finite transport closure; body identities come from preparation."""
    prepared = read_json(state, 'PREPARED.json')
    inputs = prepared['input_files']
    require(set(inputs) == PUBLIC_FIXTURE_PREPARED_INPUTS, 'Exact seventeen prepared inputs are required')
    for relative, expected in inputs.items():
        require(identity(read(state, relative)) == expected, 'Prepared export input changed: '+relative)
    return inputs


def public_fixture_terminal_complete(record):
    try:
        return (record['profile'] == 'public-fixtures123'
                and record['status'] == 'PASS_PUBLIC_FIXTURE_EXECUTION_AND_RESTORATION'
                and type(record['held_denials']) is int and record['held_denials'] == 0
                and type(record['private_denials']) is int and record['private_denials'] == 0
                and [row['phase'] for row in record['phases']] == PUBLIC_FIXTURE_PHASES
                and all(type(row['exit_code']) is int and row['exit_code'] == 0 and row['terminal']
                        for row in record['phases'])
                and record['restoration']['status'] == 'PASS_FIXTURE_MEMBERS_AND_INDEX_RESTORATION_ONLY')
    except (KeyError, TypeError):
        return False


def public_fixture_whitelisted_files(state):
    state = Path(state).absolute()
    names = {'ADMISSION.json', 'PREPARED.json', 'PREPARATION-BOUNDARY.json', 'before.json', 'after.json',
             'before-namespace.json', 'after-namespace.json',
             'original-index', 'expected-index', 'native-stage-before.z', 'native-stage-absent.z',
             'index-mode.json', 'inputs/hold.json', 'inputs/SOURCE-IDENTITIES.json',
             'inputs/fixture-sources.json', 'inputs/fixture-population.json', 'EXECUTION-START.json',
             'PARKING-START.json', 'PARKING-PROGRESS.json', 'PARKING-DONE.json',
             'ABSENCE-AFTER-PARK.json', 'ABSENCE-AFTER-INDEX.json', 'UNSTAGED-MEMBERSHIP.json',
             'STAGED-MEMBERSHIP.json', 'CONSUMERS-TERMINAL.json', 'QUIESCENCE-BEFORE-RESTORE.json',
             'RESTORATION-NAMESPACE.json', 'FIXTURE-RESTORATION-GATE.json', 'FIXTURE-RESTORATION-START.json',
             'FIXTURE-RESTORATION-TERMINAL.json', 'FIXTURE-RESTORATION-FAILURE.json', 'EXECUTION-TERMINAL.json'}
    names.update(PUBLIC_FIXTURE_SOURCE_EXPORTS)
    for phase in PUBLIC_FIXTURE_PHASES:
        names.update('phases/'+phase+'/'+name for name in ('START.json', 'child.json', 'LEASE.json', 'CHILD-RESULT.json', 'PRESENT-BEFORE-LEASE.json',
                     'ABSENCE-BEFORE-LEASE.json', 'ABSENCE-CHILD-ENTRY.json', 'QUIESCENCE.json',
                     'PROCESS.json', 'TERMINAL.json', 'stdout.log'))
    for category in ('groups', 'children', 'writes', 'native-index-mutations', 'native-commands',
                     'native-executions', 'provider-controls', 'quiescence'):
        directory = state/category
        if not os.path.lexists(directory):
            continue
        require(stat.S_ISDIR(directory.lstat().st_mode), 'Public123 evidence category is unsafe')
        for path in directory.iterdir():
            if re.fullmatch(r'[0-9a-f]{32}\.json', path.name):
                names.add(category+'/'+path.name)
    return [ordinary_source(state, name) for name in sorted(names) if os.path.lexists(state/name)]


def receive_public_fixture_execution(state):
    """Receive actual finite phase/source/process/restoration endpoints, never labels alone."""
    state = Path(state).absolute()
    try:
        record = read_json(state, 'EXECUTION-TERMINAL.json')
        require(public_fixture_terminal_complete(record), 'Public123 execution is incomplete, failed or denied')
        require(not os.path.lexists(state/'FIXTURE-RESTORATION-FAILURE.json'),
                'A preserved restoration failure cannot become a public123 pass')
        prepared = read_json(state, 'PREPARED.json')
        public_fixture_export_inputs(state)
        require(prepared['profile'] == 'public-fixtures123' and prepared['originals'] == 123
                and prepared['providers'] == 3 and prepared['original_census_paths'] == 16103
                and prepared['held_denials'] == prepared['private_denials'] == 0
                and prepared['full_reader_or_scoring_claimed'] is False, 'Public123 preparation scope differs')
        for relative, expected in prepared['input_files'].items():
            require(identity(read(state, relative)) == expected, 'Actual public123 prepared input changed: '+relative)
        require(identity(read(state, 'before.json')) == prepared['before']
                and identity(read(state, 'original-index')) == prepared['raw_index'], 'Public123 original snapshot changed')
        value = read_json(state, 'inputs/fixture-population.json')
        from source_alias_absence_population import validate_public_fixture_population, PUBLIC_FIXTURE_PROVIDER_IDENTITIES
        validate_public_fixture_population(value['records'])
        require({row['path']: (row['git_blob'], row['sha256'], row['bytes']) for row in value['providers']}
                == PUBLIC_FIXTURE_PROVIDER_IDENTITIES, 'Exact public123 current provider identity differs')
        members = {row['path'] for row in value['records']}
        sources = read_json(state, 'inputs/fixture-sources.json')
        before = read_json(state, 'before.json')
        require(set(before) == set(sources) | members and not set(sources) & members
                and len(before) == prepared['source_paths'], 'Finite source closure differs')
        for phase, process in zip(PUBLIC_FIXTURE_PHASES, record['phases']):
            prefix = 'phases/'+phase+'/'
            terminal = read(state, prefix+'TERMINAL.json')
            require(identity(terminal) == process['terminal']
                    and identity(read(state, prefix+'stdout.log')) == process['stdout']
                    and read_json(state, prefix+'PROCESS.json') == process, 'Actual phase source/process endpoint differs')
            actual = json.loads(terminal)
            require(actual['profile'] == 'public-fixtures123' and actual['phase'] == phase
                    and actual['status'] == 'PASS_PUBLIC_FIXTURE_PHASE_ONLY'
                    and actual['held_denials'] == actual['private_denials'] == 0
                    and not actual['held_events'] and not actual['private_events'], 'Actual public123 phase did not pass')
            require(read_json(state, prefix+'QUIESCENCE.json')['quiescent'] is True,
                    'Public123 child process is not received quiescent')
            if phase == 'fixtures123-present':
                present = read_json(state, prefix+'PRESENT-BEFORE-LEASE.json')
                require(present['complete'] is True and len(present['rows']) == 123
                        and {row['path'] for row in present['rows']} == members
                        and all(row['exact'] is True for row in present['rows']), 'Complete actual present population is unreceived')
            else:
                for endpoint in ('ABSENCE-BEFORE-LEASE.json', 'ABSENCE-CHILD-ENTRY.json'):
                    absent = read_json(state, prefix+endpoint)
                    require(absent['complete'] is True and len(absent['rows']) == 123
                            and {row['path'] for row in absent['rows']} == members
                            and all(row['lstat']['state'] == 'absent' and row['lexists'] is False
                                    and row['inconsistent'] is False for row in absent['rows']),
                            'Complete actual public123 absence is unreceived')
                require(actual['absence_boundaries'] and all(row['complete'] is True and row['members'] == 123
                        for row in actual['absence_boundaries']), 'Actual native/consumer absence boundaries failed')
            result = actual['result']
            require(result['passed'] is True, 'Actual public123 phase result failed')
            if phase == 'fixtures123-controls':
                controls = result['controls']
                require(len(controls) == 10 and all(row['errors'] and row['exact_restoration'] is True for row in controls),
                        'Ten actual contrary controls and their restoration are required')
                require([row['kind'] for row in controls] == ['provider-body']*3 + ['provider-index-mode']*3
                        + ['public-row-role', 'public-row-public_sha256'] + ['nonmember-request']*2,
                        'Exact public123 contrary-control classes differ')
            else:
                require(all(len(result[key]) == 123 and {row['path'] for row in result[key]} == members
                            for key in ('public_objects', 'source_bytes', 'references'))
                        and all(not row['errors'] for row in result['public_objects']+result['source_bytes'])
                        and all(row['root'] is True and row['relative'] is True for row in result['references'])
                        and not result['currentness_errors'] and result['whole_reader_or_scoring_claimed'] is False,
                        'Complete actual four-route public123 results are required')
        unstaged = read_json(state, 'UNSTAGED-MEMBERSHIP.json')
        staged = read_json(state, 'STAGED-MEMBERSHIP.json')
        require(unstaged['paths'] == staged['paths'] == sorted(members)
                and unstaged['all_original_index_entries_retained'] is True
                and staged['all_original_index_entries_removed'] is True
                and staged['other_entries_unchanged'] is True, 'Actual native deletion memberships differ')
        def stage_rows(relative):
            rows = {}
            for entry in read(state, relative).split(b'\0'):
                if not entry:
                    continue
                header, raw_path = entry.split(b'\t', 1)
                mode, oid, level = header.decode('ascii').split()
                path = raw_path.decode('utf-8')
                require(level == '0' and path not in rows and mode in ('100644', '100755', '120000'),
                        'Native stage endpoint is not ordinary and unique')
                rows[path] = (mode, oid)
            return rows
        original_stage = stage_rows('native-stage-before.z')
        absent_stage = stage_rows('native-stage-absent.z')
        require(all(original_stage.get(row['path']) == ('100644', row['git_blob']) for row in value['records'])
                and absent_stage == {path: row for path, row in original_stage.items() if path not in members},
                'Received real native stage maps differ outside the exact123 membership')
        require(identity(read(state, 'expected-index')) == staged['raw_index'], 'Exact staged native index differs')
        consumers = read_json(state, 'CONSUMERS-TERMINAL.json')
        require(consumers['status'] == 'PASS_PUBLIC_FIXTURE_CONSUMERS_PENDING_RESTORATION'
                and consumers['phases'] == record['phases'], 'Actual public123 consumer aggregate differs')
        terminal = read_json(state, 'FIXTURE-RESTORATION-TERMINAL.json')
        require(terminal == record['restoration'] and terminal['members'] == 123
                and terminal['sources'] == len(before) and terminal['ctime_or_continuous_custody_claimed'] is False,
                'Actual public123 restoration terminal differs')
        after = read(state, 'after.json')
        require(identity(after) == terminal['after'] and json.loads(after) == before
                and terminal['raw_index'] == prepared['raw_index'], 'Exact finite vectors/raw index were not restored')
        require(read_json(state, 'before-namespace.json') == read_json(state, 'after-namespace.json'),
                'Complete checkout namespace metadata was not restored')
        require(read_json(state, 'QUIESCENCE-BEFORE-RESTORE.json')['quiescent'] is True,
                'Public123 restoration was not preceded by received quiescence')
        graph = receive_public_fixture_graph(state, prepared, record, value, before)
        return {'qualified': True, 'status': 'COMPLETE_PUBLIC123_PHASES_AND_EXACT_RESTORATION',
                'profile': 'public-fixtures123', 'head': prepared['head'], 'tree': prepared['tree'],
                'originals': 123, 'providers': 3, 'phases': 5, 'contrary_controls': 10,
                'received_graph': graph,
                'held_worktree_body_integrity': 'UNKNOWN', 'retirement_credit': 'NOT_GRANTED_BY_THIS_PROGRAM'}
    except (OSError, ValueError, KeyError, IndexError, AttributeError, TypeError, RuntimeError) as error:
        return {'qualified': False, 'status': 'FAILED_INCOMPLETE_OR_INCONSISTENT_PUBLIC123',
                'error': repr(error), 'retirement_credit': 'NONE'}


def export_public_fixture_evidence(state, *, admission=None):
    from check_source_alias_absence import atomic_bytes, save
    state = Path(state).absolute()
    destination = state.parent/'r0002-public-fixtures123-receipts'
    require(not os.path.lexists(destination), 'Public123 export is immutable and single-use')
    public_fixture_export_inputs(state)
    outcome = receive_public_fixture_execution(state)
    if admission is None or admission.get('live_index', {}).get('exact') is not True:
        outcome = {'qualified': False, 'status': 'AUTHENTICATED_FAILURE_METADATA_ONLY',
                   'retirement_credit': 'NONE', 'execution_receiving': outcome,
                   'reason': 'No complete exact live-index endpoint; no restoration or reset performed.'}
    rows = []
    export_errors = []
    for source in public_fixture_whitelisted_files(state):
        relative = source.relative_to(state).as_posix()
        body = source.read_bytes()
        if relative in PUBLIC_FIXTURE_SOURCE_EXPORTS:
            require(identity(body) == read_json(state, 'PREPARED.json')['input_files'][relative],
                    'Unbound public helper export')
        elif relative.endswith('.json'):
            try:
                json.loads(body)
            except (ValueError, UnicodeError):
                export_errors.append({'path': relative, 'error': 'Invalid metadata JSON retained verbatim'})
        elif relative in ('original-index', 'expected-index'):
            if not (body[:4] == b'DIRC' and hashlib.sha1(body[:-20]).digest() == body[-20:]):
                export_errors.append({'path': relative, 'error': 'Corrupt saved index metadata retained verbatim'})
        elif relative in ('native-stage-before.z', 'native-stage-absent.z'):
            body.decode('utf-8')
        else:
            require(relative.endswith('/stdout.log'), 'Unexpected public123 nonmetadata export')
            body.decode('utf-8')
        atomic_bytes(destination/relative, body)
        rows.append({'path': relative, **identity(body)})
    if export_errors:
        outcome = {'qualified': False, 'status': 'CORRUPT_FAILURE_METADATA_ONLY',
                   'retirement_credit': 'NONE', 'execution_receiving': outcome}
    if admission is not None:
        save(destination/'EXPORT-ADMISSION.json', admission)
    save(destination/'EXPORT-SUMMARY.json', {'schema': 'hosted-public-fixtures123-export-v1', 'outcome': outcome,
         'files': rows, 'file_count': len(rows), 'bytes': sum(row['bytes'] for row in rows),
         'export_errors': export_errors,
         'export_policy': 'Finite metadata, process logs, native index and exactly nine authenticated public helper/harness inputs; no parked/provider/held bodies or Git objects.'})
    print(json.dumps({'status': outcome['status'], 'files': len(rows), 'destination': str(destination)}))
    if not outcome['qualified']:
        raise SystemExit(1)


def public_fixture_no_denials(record):
    require(all(type(record[key]) is int and record[key] == 0 for key in ('held_denials', 'private_denials'))
            and record['held_events'] == [] and record['private_events'] == [],
            'Denial counts and actual denial event arrays disagree or are nonzero')


def public_fixture_identity_shape(value):
    require(isinstance(value, dict) and set(value) == {'bytes', 'sha256', 'git_blob'}
            and type(value['bytes']) is int and value['bytes'] >= 0
            and re.fullmatch(r'[0-9a-f]{64}', value['sha256']) is not None
            and re.fullmatch(r'[0-9a-f]{40}', value['git_blob']) is not None,
            'Incomplete actual byte identity')


def public_fixture_group_shape(group):
    from check_source_alias_absence import validate_group_record
    validate_group_record(group)
    require(group['pgid'] == group['sid'] == group['process']['pid']
            and group['proc_pgid'] == group['proc_sid'] == group['process']['proc_pid'],
            'Recorded child/operation is not its exact session leader')


def public_fixture_live_members(group, rows, *, permitted_parent=None):
    from check_source_alias_absence import identity_from_proc, validate_process_record
    require(isinstance(rows, list), 'Actual group member observations are missing')
    active = []
    seen = set()
    for row in rows:
        require(type(row['proc_pid']) is int and row['proc_pid'] > 0 and row['proc_pid'] not in seen
                and (row['proc_pgid'] == group['proc_pgid'] or row['proc_sid'] == group['proc_sid']),
                'Observed process does not belong to the recorded group/session')
        seen.add(row['proc_pid'])
        require(isinstance(row['state'], str) and len(row['state']) == 1, 'Malformed observed process state')
        if row['state'] != 'Z':
            actual = identity_from_proc(row)
            validate_process_record(actual)
            if actual != permitted_parent:
                active.append(row)
    return active


def public_fixture_process_graph(prepared, start, terminal, preparation, frames, groups, children, quiet):
    """Serialization consistency only; actual success also requires every source/consumer gate."""
    from check_source_alias_absence import validate_process_record
    public_fixture_no_denials(prepared)
    public_fixture_no_denials(preparation)
    public_fixture_no_denials(terminal)
    require(preparation['operation'] == prepared['operation'], 'Preparation operation receipt differs')
    parent = start['process']
    validate_process_record(parent)
    expected_groups = {}
    for operation, name in ((prepared['operation'], 'prepare-public-fixtures123'),
                            (start['operation'], 'execute-public-fixtures123')):
        public_fixture_group_shape(operation['group'])
        require(operation['operation'] == name and operation['process'] == operation['group']['process'] == parent
                and re.fullmatch(r'[0-9a-f]{32}', operation['token']) is not None,
                'Exact parent operation identity is unreceived')
        expected_groups['groups/'+operation['token']+'.json'] = operation['group']
    require(len(expected_groups) == 2 and set(frames) == set(PUBLIC_FIXTURE_PHASES),
            'Complete distinct preparation/execution operations and five phases are required')
    expected_children, processes = {}, {}
    for phase in PUBLIC_FIXTURE_PHASES:
        frame = frames[phase]
        beginning, child, lease = frame['START'], frame['child'], frame['LEASE']
        result, phase_terminal, phase_quiet = frame['PROCESS'], frame['TERMINAL'], frame['QUIESCENCE']
        token = beginning['token']
        require(re.fullmatch(r'[0-9a-f]{32}', token) is not None and beginning['profile'] == 'public-fixtures123'
                and beginning['phase'] == phase and beginning['process'] == parent, 'Phase START identity differs')
        group = child['group']
        public_fixture_group_shape(group)
        require(child['process'] == group['process'] and child['token'] == token,
                'Child session/process/token differs')
        prefix = [prepared['runtime']['executable'], '-B', prepared['repo']+'/scripts/check_source_alias_absence.py',
                  '_fixture-phase', '--repo', prepared['repo'], '--state', prepared['state'],
                  '--phase', phase, '--token', token]
        command = child['command']
        require(command[:-2] == prefix and command[-2] == '--identity-fd'
                and command[-1].isdecimal() and int(command[-1]) > 0,
                'Actual child command differs from its exact source/root/phase/lease')
        child_ref = 'children/'+token+'.json'
        require(child['custody_record'] == result['custody_record'] == child_ref,
                'Child/process custody reference differs')
        custody = children[child_ref]
        require(frame['CHILD-RESULT'] == custody and custody['profile'] == 'public-fixtures123'
                and custody['phase'] == phase and custody['token'] == token and custody['parent'] == parent
                and custody['command_prefix'] == prefix and custody['command'] == command
                and custody['pid'] == group['process']['pid'] and custody['group'] == group
                and custody['group_record_persisted'] is True and custody['lease_sent'] is True
                and custody['status'] == 'TERMINAL_RECEIVED' and custody['quiescent'] is True
                and type(custody['exit_code']) is int and custody['exit_code'] == 0
                and custody['stdout'] == result['stdout'] and 'error' not in custody and 'error_type' not in custody,
                'Complete actual child lifetime/terminal custody is unreceived')
        require(lease == {'token': token, 'phase': phase, 'child': group['process'], 'command': command,
                          'status': 'SENT_TO_CHILD'}, 'Complete durable and sent child lease is unreceived')
        require(phase_terminal['lease_token'] == token and phase_terminal['process'] == group['process']
                and phase_terminal['group'] == group and result['token'] == token
                and result['phase'] == phase and type(result['exit_code']) is int and result['exit_code'] == 0,
                'Child received lease or terminal/process identity differs')
        public_fixture_no_denials(phase_terminal)
        require(phase_quiet['group'] == group and phase_quiet['token'] == token
                and phase_quiet['custody_record'] == child_ref and phase_quiet['quiescent'] is True
                and not public_fixture_live_members(group, phase_quiet['observed_members']),
                'Actual child quiescence contradicts its process observations')
        expected_groups['groups/'+token+'.json'] = group
        expected_children[child_ref] = custody
        processes[phase] = group['process']
    require(len(expected_groups) == 7 and groups == expected_groups and children == expected_children,
            'Missing, extra, duplicated or inconsistent group/child custody records')
    quiet_groups = {}
    for row in quiet['groups']:
        relative = Path(row['record']).relative_to(prepared['state']).as_posix()
        require(relative not in quiet_groups and row['group'] == groups[relative],
                'Final quiescence group reference differs')
        permitted = parent if row['group']['process'] == parent else None
        active = public_fixture_live_members(row['group'], row['observed_members'], permitted_parent=permitted)
        if permitted is not None:
            require(any(all(member.get(key) == value for key, value in parent.items())
                        and member['state'] != 'Z' for member in row['observed_members']),
                    'Actual restoring parent is absent from its own group observation')
        require(row['active_members'] == active == [], 'Final group member observations are not quiescent')
        quiet_groups[relative] = row['group']
    quiet_children = {}
    for row in quiet['children']:
        require(row['record'] not in quiet_children and row['child'] == children[row['record']]
                and row['exact_quiescent'] is True, 'Final child custody is incomplete')
        quiet_children[row['record']] = row['child']
    require(quiet['quiescent'] is True and quiet_groups == groups and quiet_children == children,
            'Final quiescence omitted an owned process/group')
    return {'scope': 'CONSISTENT_PROCESS_SERIALIZATION_ONLY', 'parent': parent, 'phases': processes}


def public_fixture_native_record(row, repo, protected):
    from check_source_alias_absence import validate_process_record
    validate_process_record(row['process'])
    require(re.fullmatch(r'[0-9a-f]{32}', row['token']) is not None
            and row['record'] == 'native-executions/'+row['token']+'.json'
            and row['status'] == 'TERMINAL' and type(row['exit_code']) is int,
            'Actual native process outcome is incomplete')
    argv = row['observed_argv']
    require(argv == row['requested_argv'] and argv and argv[0] in ('git', '/usr/bin/git')
            and row['resolved_executable'] == '/usr/bin/git'
            and row['observed_executable'] in ('git', '/usr/bin/git')
            and Path(row['observed_cwd']).is_absolute(), 'Observed native executable/argv/cwd is unreceived')
    effective = Path(row['observed_cwd'])
    if '-C' in argv:
        coordinate = Path(argv[argv.index('-C')+1])
        effective = coordinate if coordinate.is_absolute() else effective/coordinate
    require(os.path.normpath(str(effective)) == row['effective_repo'] == repo,
            'Actual native effective repository differs')
    require(not any(item in argv for item in ('fetch', 'push', 'pull', 'clone', 'reset', 'checkout',
            '-l', '--long', '--git-dir', '--work-tree')), 'Unadmitted native command surface')
    position = 1
    while position < len(argv) and argv[position].startswith('-'):
        position += 2 if argv[position] in ('-c', '-C') else 1
    require(position < len(argv) and argv[position] in
            ('ls-files', 'ls-tree', 'cat-file', 'diff', 'rev-parse', 'config', 'update-index'),
            'Native result has no admitted metadata/consumer command')
    if argv[position] == 'cat-file':
        require(not any(item in argv for item in ('-s', '--batch', '--batch-check'))
                and not any(value in item for value in protected for item in argv),
                'Protected/broad object-body native command is not public123 evidence')
    for key in ('stdout', 'stderr'):
        output = row[key]
        require(output.get('capture') in ('NOT_CAPTURED', 'BYTES', 'UTF8_TEXT'), 'Native output capture status is missing')
        if output['capture'] == 'NOT_CAPTURED':
            require(set(output) == {'capture'}, 'Uncaptured native output has fabricated bytes')
        else:
            require(set(output) == {'capture', 'identity'}, 'Captured native output is malformed')
            public_fixture_identity_shape(output['identity'])
    allowed_absent_config = (argv[position:] == ['config', '--type=bool', '--get', 'core.splitIndex']
        and row['exit_code'] == 1 and row['stdout'].get('identity') == identity(b''))
    require(row['exit_code'] == 0 or allowed_absent_config,
            'Actual native failure is not an explicitly admitted absent-configuration result')
    return {'scope': 'CONSISTENT_NATIVE_OUTCOME_ONLY', 'command': argv[position:]}


def public_fixture_native_refs(references, rows, identities, expected_process):
    seen = set()
    for ref in references:
        relative = ref['record']
        require(relative not in seen and relative in rows and ref['identity'] == identities[relative]
                and rows[relative]['process'] == expected_process, 'Native outcome reference/identity/process differs')
        seen.add(relative)
    return seen


def public_fixture_reader_graph(boundary, repo, held, baseline, native_rows):
    require(boundary['scope'] == 'Actual public reader with exact held metadata gate and explicit native worktree exclusions'
            and boundary['full_protected_local_reader_cli'] == 'NOT_RUN'
            and boundary['held_worktree_body_integrity'] == 'UNKNOWN'
            and boundary['baseline'] == baseline and boundary['root'] == repo
            and boundary['held_paths'] == sorted(held) and len(held) == 5
            and boundary['known_held_links_per_body'] == 1 and len(boundary['events']) == 2,
            'Actual bounded reader scope/baseline/protected metadata is incomplete')
    suffix = ['--no-ext-diff', '--no-textconv', '--no-renames', '--name-status', '-z', baseline, '--']
    for event, surface in zip(boundary['events'], ('index', 'public_worktree')):
        original = ['git', 'diff'] + (['--cached'] if surface == 'index' else []) + suffix
        executed = ['git', '--no-replace-objects', *original[1:]]
        if surface == 'public_worktree': executed += ['.', *(':(top,literal,exclude)'+path for path in sorted(held))]
        require(event == {'surface': surface, 'original_command': original, 'executed_command': executed,
                         'returncode': 0, 'held_worktree_exclusions': 0 if surface == 'index' else 5,
                         'held_stage_tree_metadata': 'EXACT', 'held_worktree_body_integrity': 'UNKNOWN'},
                'Actual reader diff/exclusion event differs')
        require(any(row['observed_argv'] == executed and row['exit_code'] == 0 for row in native_rows),
                'Reader event lacks its actual native outcome')
    return {'scope': 'CONSISTENT_READER_BOUNDARY_ONLY'}


def public_fixture_control_targets(controls, providers, records):
    expected = ([('provider-body', row['path']) for row in providers]
                + [('provider-index-mode', row['path']) for row in providers]
                + [(kind, records[0]['path']) for kind in ('public-row-role', 'public-row-public_sha256')]
                + [('nonmember-request', path) for path in (
                    'not-an-admitted-public-fixture.json', 'experiments/episode-reification-v2/fixtures/KEYS.json')])
    require(len(providers) == 3 and len({row['path'] for row in providers}) == 3
            and [(row['kind'], row['path']) for row in controls] == expected
            and all(isinstance(row['errors'], list) and row['errors'] and all(isinstance(error, str) for error in row['errors'])
                    and row['exact_restoration'] is True for row in controls),
            'Exact ten contrary-control targets, failures and restoration receipts are required')
    return {'scope': 'CONSISTENT_TEN_CONTROL_TARGETS_ONLY'}


def public_fixture_category(state, name):
    directory = state/name
    require(stat.S_ISDIR(directory.lstat().st_mode), 'Missing ordinary evidence category: '+name)
    rows, identities = {}, {}
    for path in sorted(directory.iterdir()):
        require(re.fullmatch(r'[0-9a-f]{32}\.json', path.name) is not None, 'Unreceived evidence category member')
        relative = name+'/'+path.name
        body = read(state, relative)
        rows[relative], identities[relative] = json.loads(body), identity(body)
    return rows, identities


def receive_public_fixture_graph(state, prepared, terminal, value, before):
    """Join all finite actual outcomes after the independent source/population gates."""
    from source_alias_absence_boundary import PROTECTED_PATHS
    from source_alias_absence_reader import BASELINE
    frames = {}
    for phase in PUBLIC_FIXTURE_PHASES:
        prefix = 'phases/'+phase+'/'
        frames[phase] = {name: read_json(state, prefix+name+'.json') for name in (
            'START', 'child', 'LEASE', 'CHILD-RESULT', 'PROCESS', 'TERMINAL', 'QUIESCENCE')}
    groups, _ = public_fixture_category(state, 'groups')
    children, _ = public_fixture_category(state, 'children')
    native, native_ids = public_fixture_category(state, 'native-executions')
    commands, command_ids = public_fixture_category(state, 'native-commands')
    mutations, _ = public_fixture_category(state, 'native-index-mutations')
    writes, _ = public_fixture_category(state, 'writes')
    provider_controls, _ = public_fixture_category(state, 'provider-controls')
    preparation = read_json(state, 'PREPARATION-BOUNDARY.json')
    start = read_json(state, 'EXECUTION-START.json')
    require(start['prepared'] == identity(read(state, 'PREPARED.json'))
            and start['profile'] == 'public-fixtures123' and start['status'] == 'STARTED_NOT_TERMINAL'
            and start['members'] == sorted(row['path'] for row in value['records']),
            'Execution START prepared/profile/population identity differs')
    admission = read_json(state, 'ADMISSION.json')
    require(prepared['status'] == 'PREPARED_NO_ABSENCE'
            and prepared['schema'] == 'hosted-public-fixtures123-preparation-v1'
            and prepared['admission'] == admission and admission['profile'] == 'public-fixtures123'
            and all(admission[key] == prepared[key] for key in ('head', 'repo', 'state')),
            'Saved preparation/admission scope or coordinates differ')
    processes = public_fixture_process_graph(prepared, start, terminal, preparation, frames, groups, children,
                                             read_json(state, 'QUIESCENCE-BEFORE-RESTORE.json'))
    held = read_json(state, 'inputs/hold.json')['held']
    require({row['path'] for row in held} == set(PROTECTED_PATHS), 'Exact five protected metadata coordinates differ')
    protected = {value for row in held for value in (row['path'], row['published_metadata']['git_blob'])}
    for relative, row in native.items():
        require(row['record'] == relative, 'Native outcome filename differs')
        public_fixture_native_record(row, prepared['repo'], protected)
    parent_refs = public_fixture_native_refs(terminal['native_receipts'], native, native_ids, processes['parent'])
    preparation_refs = public_fixture_native_refs(preparation['native_receipts'], native, native_ids, processes['parent'])
    require(preparation_refs and preparation_refs <= parent_refs, 'Preparation native outcomes are not cross-bound')
    all_refs = set(parent_refs)
    observed_scopes = [(terminal['native_argv_observations'], parent_refs), (preparation['native_observations'], preparation_refs)]
    for phase, frame in frames.items():
        phase_terminal = frame['TERMINAL']
        refs = public_fixture_native_refs(phase_terminal['native_receipts'], native, native_ids, processes['phases'][phase])
        require(refs and not all_refs & refs, 'Phase native outcomes are empty or shared with another process')
        all_refs.update(refs)
        observed_scopes.append((phase_terminal['native_argv_observations'], refs))
        if phase != 'fixtures123-controls':
            public_fixture_reader_graph(phase_terminal['result']['reader_boundary'], prepared['repo'],
                set(PROTECTED_PATHS), BASELINE, [native[ref] for ref in refs])
    require(all_refs == set(native), 'Unlinked or missing actual native outcomes')
    for observations, scope in observed_scopes:
        seen = set()
        for observation in observations:
            relative = observation['native_record']
            require(relative in scope and relative not in seen and observation['argv'] == native[relative]['observed_argv']
                    and observation['cwd'] == native[relative]['effective_repo'], 'Audit/native outcome cross-binding differs')
            seen.add(relative)
    for row in commands.values():
        actual = native[row['native_record']]
        require(row['status'] == 'TERMINAL' and type(row['exit_code']) is int and row['exit_code'] == actual['exit_code'] == 0
                and row['command'] == actual['observed_argv'] and row['repo'] == actual['effective_repo'] == prepared['repo']
                and row['process'] == actual['process']
                and actual['stdout'] == {'capture': 'BYTES', 'identity': row['stdout']}
                and actual['stderr'] == {'capture': 'BYTES', 'identity': row['stderr']},
                'Journaled native command is not its actual terminal outcome')
    require(len({row['native_record'] for row in commands.values()}) == len(commands),
            'Duplicate journal aliases for one actual native command')
    members = sorted(row['path'] for row in value['records'])
    providers = value['providers']
    expected_commands = [['update-index', '--force-remove', '--', *members]] + [
        ['update-index', '--cacheinfo', '100755,'+row['git_blob']+','+row['path']] for row in providers]
    received_mutations = {}
    for row in mutations.values():
        command = commands[row['command_record']]
        native_row = native[row['native_record']]
        actual_command = public_fixture_native_record(native_row, prepared['repo'], protected)['command']
        key = tuple(actual_command)
        require(key not in received_mutations and actual_command in expected_commands
                and row['status'] == 'TERMINAL' and type(row['exit_code']) is int and row['exit_code'] == 0
                and row['command_identity'] == command_ids[row['command_record']]
                and row['command'] == command['command'] == native_row['observed_argv']
                and row['repo'] == prepared['repo'] and row['process'] == native_row['process']
                and row['group'] in groups.values() and row['group']['process'] == row['process']
                and row['before']['foreign_lock'] is False,
                'Actual native index mutation is missing, duplicated or unbound')
        received_mutations[key] = row
    require(set(received_mutations) == {tuple(row) for row in expected_commands}, 'Exact four native index mutations are required')
    actual_mutations = {relative for relative, row in native.items()
        if public_fixture_native_record(row, prepared['repo'], protected)['command'][0] == 'update-index'}
    require(actual_mutations == {row['native_record'] for row in mutations.values()},
            'Actual native index mutation has no exact one-to-one journal binding')
    controls = frames['fixtures123-controls']['TERMINAL']['result']['controls']
    public_fixture_control_targets(controls, providers, value['records'])
    used_providers, used_writes = set(), set()
    staged = identity(read(state, 'expected-index'))
    mode = read_json(state, 'index-mode.json')['mode']
    removal = received_mutations[tuple(expected_commands[0])]
    require(removal['before']['raw_index'] == prepared['raw_index'] and removal['after'] == staged,
            'Actual staged removal index endpoints differ')
    for row in controls[:3]:
        ref = row['control_record']; actual = provider_controls[ref]
        original = {k: v for k, v in before[row['path']].items() if k != 'atime_ns'}
        require(ref not in used_providers and actual['status'] == 'RESTORED_EXACT_PROVIDER_CONTROL'
                and actual['path'] == row['path'] and actual['errors'] == row['errors']
                and actual['before'] == actual['after']
                and {k: v for k, v in actual['before'].items() if k != 'atime_ns'} == original
                and actual['changed']['sha256'] != actual['before']['sha256']
                and all(actual['changed'][key] == actual['before'][key] for key in ('device', 'inode', 'mode', 'links')),
                'Actual controlled provider postimage/restoration is unreceived')
        used_providers.add(ref)
    for row, provider in zip(controls[3:6], providers):
        actual = received_mutations[tuple(['update-index', '--cacheinfo', '100755,'+provider['git_blob']+','+provider['path']])]
        restoration = row['restoration']; ref = restoration['write_record']; write = writes[ref]
        require(ref not in used_writes and actual['before']['raw_index'] == staged
                and restoration['status'] == 'RESTORED_EXACT_OWNED_INDEX_CONTROL'
                and restoration['before'] == actual['after'] and restoration['after'] == staged
                and restoration['mode'] == actual['before']['mode'] == mode
                and write['target'] == '.git/index' and write['body'] == staged and write['mode'] == mode,
                'Actual native provider control cleanup is unbound')
        used_writes.add(ref)
    final_ref = terminal['restoration']['index_write_record']; final_write = writes[final_ref]
    require(final_ref not in used_writes and final_write['target'] == '.git/index'
            and final_write['body'] == prepared['raw_index'] and final_write['mode'] == mode,
            'Actual final index restoration write is unbound')
    used_writes.add(final_ref)
    require(used_writes == set(writes) and used_providers == set(provider_controls),
            'Unlinked filesystem write or provider-control evidence')
    return {'scope': 'COMPLETE_FINITE_PROCESS_NATIVE_READER_CONTROL_JOIN', 'native_outcomes': len(native),
            'children': len(children), 'groups': len(groups), 'index_mutations': len(mutations)}

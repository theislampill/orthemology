"""Public finite source-alias population for the bounded absence regression."""
from pathlib import Path
import hashlib
import importlib
import os
import stat
import subprocess
import sys

BASELINE = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'

def require(value, message):
    if not value:
        raise ValueError(message)

def original_tree(repo):
    env = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1',
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    data = subprocess.check_output(['git', '--no-replace-objects', '-c', 'core.fsmonitor=false',
        'ls-tree', '-r', '-l', '-z', '--full-tree', BASELINE], cwd=repo, env=env)
    rows = {}
    for raw in data.split(b'\0'):
        if raw:
            header, path = raw.split(b'\t', 1)
            mode, kind, blob, size = header.decode('ascii').split()
            rows[path.decode('utf-8')] = (mode, kind, blob, int(size))
    require(len(rows) == 16103, 'Original source denominator differs')
    return rows

def regular_public_file(repo, relative):
    require(isinstance(relative, str) and relative and not relative.startswith('/')
            and '\\' not in relative and all(p not in ('', '.', '..', '.git')
            for p in relative.split('/')), 'Unsafe public population path')
    node = repo
    for part in relative.split('/'):
        node = node / part
        require(not node.is_symlink(), 'Symlink in public population')
    require(node.is_file(), 'Missing public population member: ' + relative)
    return node

def public_identity(repo, relative, original):
    path = regular_public_file(repo, relative)
    mode, kind, blob, size = original
    require(kind == 'blob' and mode in ('100644', '100755'), 'Unsupported original mode/type')
    info = path.stat()
    require(stat.S_ISREG(info.st_mode) and stat.S_IMODE(info.st_mode) == (int(mode, 8) & 0o777)
            and info.st_nlink == 1 and info.st_size == size, 'Public member mode/size/link differs')
    body = path.read_bytes()
    actual_blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
    require(actual_blob == blob, 'Public member original Git identity differs')
    return {'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body), 'blob': blob, 'mode': mode}

def public_consumers(repo):
    sys.path.insert(0, str(repo / 'scripts'))
    result = []
    for name in ('validate_ar8r_reconciliation', 'resolve_t20_v6_source'):
        module = importlib.import_module(name)
        require(Path(module.__file__).resolve() == repo / 'scripts' / (name + '.py'),
                'Population consumer imported from another checkout')
        result.append(module)
    return result

def derive_classes(repo: Path) -> list[dict]:
    repo = Path(repo).resolve()
    snapshot, source = public_consumers(repo)
    originals = original_tree(repo)
    deep = snapshot._pmr007_deep_original_members(repo)
    copies824 = snapshot._pmr007_deep_duplicate_map(deep)
    catalog = source._continuation_copy_catalog(repo)
    rounds = snapshot._pmr007_rounds_original_members(repo)
    copies98 = {alias: alias.replace(snapshot.PMR007_ROUNDS_PREFIX,
                snapshot.PMR007_DEEP_PREFIX.replace('a-ap', 'a-bk'), 1)
                for alias in snapshot.pmr007_rounds_duplicate_paths(repo)}
    rows = []
    for cohort, copies in (('824', copies824), ('258', {p: r['canonical'] for p, r in catalog.items()}),
                           ('98', copies98)):
        for alias, canonical in sorted(copies.items()):
            require(originals.get(alias) == originals.get(canonical) and alias in originals,
                    'Alias and retained original tree identities differ')
            identity = public_identity(repo, canonical, originals[alias])
            require(public_identity(repo, alias, originals[alias]) == identity,
                    'Present original and retained identities differ')
            if cohort == '824':
                expected = deep[alias.removeprefix(snapshot.PMR007_DEEP_PREFIX + '/')]
            elif cohort == '98':
                expected = rounds[alias.removeprefix(snapshot.PMR007_ROUNDS_PREFIX + '/')]
            else:
                expected = catalog[alias]['sha256']
                require((identity['bytes'], identity['blob']) ==
                        (catalog[alias]['bytes'], catalog[alias]['blob']), 'Continuation binding differs')
            require(identity['sha256'] == expected, 'Public owner digest differs')
            rows.append(dict(alias=alias, canonical=canonical, cohort=cohort, **identity))
    aliases = {r['alias'] for r in rows}
    retained = {r['canonical'] for r in rows}
    require(len(rows) == len(aliases) == 1180 and len(retained) == 1082
            and not aliases & retained, 'Combined finite population differs')
    require({c: sum(r['cohort'] == c for r in rows) for c in ('824', '258', '98')}
            == {'824': 824, '258': 258, '98': 98}, 'Class population differs')
    excluded = source.CONTINUATION_COPY_ROOT + source.CONTINUATION_COPY_EXCLUDED + '.lean'
    context = snapshot.PMR007_ROUNDS_PREFIX + '/' + snapshot.PMR007_ROUNDS_CONTEXT_MEMBER
    require(excluded not in aliases and context not in aliases, 'Excluded original selected')
    public_identity(repo, excluded, originals[excluded])
    public_identity(repo, context, originals[context])
    require({r['canonical'] for r in rows if r['cohort'] == '98'} <=
            {r['canonical'] for r in rows if r['cohort'] == '824'}, 'Shared retained population differs')
    return sorted(rows, key=lambda row: row['alias'])

def derive_required(repo: Path, classes: list[dict]) -> list[str]:
    repo = Path(repo).resolve()
    snapshot, _ = public_consumers(repo)
    originals = original_tree(repo)
    selected = {r['alias'] for r in classes if r['cohort'] == '98'}
    required = sorted({p for p in originals if p.startswith(snapshot.PMR007_ROUNDS_PREFIX + '/')} - selected)
    require(len(selected) == 98 and len(required) == 33, 'Required rounds originals differ')
    require(snapshot.PMR007_ROUNDS_PREFIX + '/SHA256SUMS' in required
            and snapshot.PMR007_ROUNDS_PREFIX + '/' + snapshot.PMR007_ROUNDS_CONTEXT_MEMBER in required,
            'Required manifest/context original missing')
    for path in required:
        public_identity(repo, path, originals[path])
    return required


def derive_checkpoint_classes(repo: Path) -> list[dict]:
    """Separate checkpoint87 fixture population; inherited B1180 is unchanged."""
    repo = Path(repo).resolve()
    sys.path.insert(0, str(repo / 'scripts'))
    source = importlib.import_module('resolve_t20_v6_source')
    require(Path(source.__file__).resolve() == repo / 'scripts/resolve_t20_v6_source.py',
            'Checkpoint population consumer imported from another checkout')
    rows = []
    for alias, binding in source._checkpoint_copy_catalog().items():
        canonical = binding['canonical']
        body = source.checkpoint_copy_bytes(repo, alias)
        original = ('100644', 'blob', binding['blob'], binding['bytes'])
        identity = public_identity(repo, canonical, original)
        require(public_identity(repo, alias, original) == identity,
                'Checkpoint fixture requires every exact original alias present')
        require((len(body), hashlib.sha256(body).hexdigest()) ==
                (identity['bytes'], identity['sha256']), 'Checkpoint resolver and population differ')
        rows.append(dict(alias=alias, canonical=canonical, cohort='checkpoint87', **identity))
    aliases = {r['alias'] for r in rows}; retained = {r['canonical'] for r in rows}
    require(len(rows) == len(aliases) == 87 and len(retained) == 85 and not aliases & retained,
            'Checkpoint finite population differs')
    return sorted(rows, key=lambda row: row['alias'])


PUBLIC_FIXTURE_IDENTITY_SHA256 = '2b078fcd3245db2e5b967145e00b1de4cb2bb5cfe2456f7f6c73d18de3e27540'
PUBLIC_FIXTURE_PROVIDER_IDENTITIES = {
    'experiments/episode-reification-v2/scripts/generate_cases.py':
        ('e43f016e6a12594c29deef253cf1ba65d86462be', '3b449a7580426fdf89f85612018473f92c3c2c274d4eea47e7046d1bcfe1bc89', 9631),
    'experiments/episode-reification/scripts/generate_fixtures.py':
        ('be7dd10d2f60ad16c4cf9df2ea3316d778b0c8fc', '9c39be153165e8d1c5a074243fc5f4ba467862ccc0d433bb42e7471230e4b929', 8675),
    'tests/schema-negative/NEGATIVE-FIXTURES.json':
        ('20b6e5801823e87db6b5fb1638d0e3992eee36e6', 'b229103cc93bb15d046cb15a1794d99d0cb40200fbc8fe9ac7ceff358c88d3e9', 108213),
}


def original_metadata_tree(repo, revision=BASELINE):
    """Native path/mode/blob metadata only; no object-size or body request."""
    import re
    require(isinstance(revision, str) and re.fullmatch(r'[0-9a-f]{40}', revision),
            'A full immutable original revision is required')
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='',
               GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_CONFIG_NOSYSTEM='1',
               GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    data = subprocess.check_output(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs',
                                    'ls-tree', '-r', '-z', '--full-tree', revision], cwd=repo, env=env)
    rows = {}
    for entry in data.split(b'\0'):
        if not entry:
            continue
        header, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = header.decode('ascii').split()
        path = raw_path.decode('utf-8')
        require(path not in rows and kind == 'blob' and re.fullmatch(r'[0-9a-f]{40}', oid),
                'Repeated or unsupported native original metadata')
        rows[path] = (mode, kind, oid)
    return rows


def _expected_public_fixture_row(path, digest, size):
    argument = path.endswith('.md')
    return {'source_sha256': digest, 'source_action': 'include', 'source_bytes': size,
                'role': 'authored_argument' if argument else 'qualified_metadata',
                'declared_eligibility_basis': 'reviewed_owner_authored' if argument else 'reviewed_distribution_metadata',
                'required_dependencies': [], 'disposition': 'REUSE', 'repository_path': path,
                'public_sha256': digest, 'public_bytes': size,
                'publication_basis': 'exact_existing_public_repository_object'}


def public_fixture_row(path, body, row):
    """Preserve every field of one original public fixture identity/role row."""
    expected = _expected_public_fixture_row(path, hashlib.sha256(body).hexdigest(), len(body))
    require(row == expected, 'Original public fixture identity, role or complete row differs')
    return row


def validate_public_fixture_population(rows):
    import json
    require(isinstance(rows, list) and len(rows) == 123, 'Exact public123 population is required')
    paths = [row['path'] for row in rows]
    require(len(set(paths)) == 123 and paths == sorted(paths), 'Public123 paths repeat or are unordered')
    require(all(set(row) == {'path', 'mode', 'git_blob', 'sha256', 'bytes', 'public_row'}
                and row['mode'] == '100644'
                and row['public_row'] == _expected_public_fixture_row(row['path'], row['sha256'], row['bytes'])
                for row in rows), 'Complete public123 record roles or native modes differ')
    negative = {f'tests/invalid/I{number:02d}' for number in range(1, 49)}
    require(sum(path.startswith('tests/invalid/') for path in paths) == 48, 'Public negative population differs')
    require({path.split('-', 1)[0] for path in paths if path.startswith('tests/invalid/')} == negative,
            'Public negative case identity differs')
    require(sum(path.startswith('experiments/episode-reification/fixtures/E') for path in paths) == 15
            and sum(path.startswith('experiments/episode-reification-v2/fixtures/C') for path in paths) == 60,
            'Public renderer population differs')
    identities = [[row['path'], row['git_blob'], row['sha256'], row['bytes']] for row in rows]
    require(hashlib.sha256(json.dumps(identities, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
            == PUBLIC_FIXTURE_IDENTITY_SHA256, 'Complete original public123 identity binding differs')
    require(sum(row['bytes'] for row in rows) == 161223
            and sum(row['public_row']['role'] == 'authored_argument' for row in rows) == 25
            and sum(row['public_row']['role'] == 'qualified_metadata' for row in rows) == 98,
            'Public123 bytes or original role population differs')
    return rows


def derive_public_fixture_population(repo, originals, objects):
    """Bind the public-only current renderer/canonical population to native originals."""
    repo = Path(repo).absolute()
    sys.path.insert(0, str(repo/'scripts'))
    source = importlib.import_module('resolve_t20_v6_source')
    require(Path(source.__file__).resolve() == repo/'scripts/resolve_t20_v6_source.py',
            'Public fixture resolver comes from another checkout')
    require(source.GENERATED_FIXTURE_OWNERS == PUBLIC_FIXTURE_PROVIDER_IDENTITIES,
            'Exact frozen public provider edition differs')
    rendered, absent = source._generated_fixture_catalog(repo)
    require(not absent and len(rendered) == 123 and len(source.GENERATED_FIXTURE_OWNERS) == 3,
            'All public fixture originals and three current providers are required before admission')
    public = {}
    for row in objects:
        path = row.get('repository_path')
        if path in rendered:
            require(path not in public, 'Repeated original public fixture row')
            public[path] = row
    require(set(public) == set(rendered), 'Incomplete public fixture rows')
    rows = []
    for path, body in sorted(rendered.items()):
        oid = hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
        require(originals.get(path) == ('100644', 'blob', oid), 'Public fixture original native identity differs')
        rows.append({'path': path, 'mode': '100644', 'git_blob': oid, 'sha256': hashlib.sha256(body).hexdigest(),
                     'bytes': len(body), 'public_row': public_fixture_row(path, body, public[path])})
    validate_public_fixture_population(rows)
    providers = [{'path': path, 'git_blob': values[0], 'sha256': values[1], 'bytes': values[2]}
                 for path, values in sorted(source.GENERATED_FIXTURE_OWNERS.items())]
    return rows, providers

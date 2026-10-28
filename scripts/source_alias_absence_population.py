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

#!/usr/bin/env python3
"""Repository validator for the public orthemology repo.

Deterministic hygiene and honesty checks; run in CI on every push/PR.
"""
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
from markdown_it import MarkdownIt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []
_MARKDOWN_PARSER = MarkdownIt('commonmark')


def strip_markdown_math(text):
    """Mask complete equation spans while retaining line boundaries."""
    pattern = re.compile(r'\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\\)\$(?!\$)(?:\\.|[^$\n])*?(?<!\\)\$')
    return pattern.sub(lambda match: ''.join('\n' if c == '\n' else ' ' for c in match[0]), text)


def markdown_link_targets(text):
    """Read actual Markdown destinations, including angle URLs and fragments."""
    for block in _MARKDOWN_PARSER.parse(strip_markdown_math(text)):
        for token in block.children or ():
            if token.type == 'link_open':
                yield token.attrGet('href')
            elif token.type == 'image':
                yield token.attrGet('src')


def check(name, ok, detail=""):
    print("[%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILS.append(name)


def corpus_files():
    """Return Git-tracked plus non-ignored prospective worktree files."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(
            "git ls-files failed: "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    paths = {
        item.decode("utf-8").replace("\\", "/")
        for item in result.stdout.split(b"\0")
        if item
    }
    for rel in sorted(paths):
        path = os.path.join(ROOT, *rel.split("/"))
        if os.path.isfile(path):
            yield path


def text_files(corpus=None):
    for path in corpus if corpus is not None else corpus_files():
        if path.endswith((".md", ".patch", ".json", ".jsonl", ".py", ".yml", ".yaml", ".cff", ".txt",
                          ".gitignore", ".gitattributes", ".editorconfig", ".sha256")):
            yield path


BANNED = [
    (r"C:\\\\?Users", "absolute Windows user path"),
    (r"C:\\\\?workspace", "absolute workspace path"),
    (r"AppData", "AppData path"),
    (r"Temp\\\\?claude", "temp session path"),
    (r"gho_[A-Za-z0-9]{20,}", "credential-looking token"),
    (r"-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----", "private key"),
]

# artifact-file bans (check 13/14): no research-output dumps, no session dumps
BANNED_FILENAMES = re.compile(r"(\.output$|\.jsonl$|synthesis-checks|owner_messages)", re.I)


def exact_source_record(path, sources, root=None):
    """Recognise only an unmodified, uniquely registered COPY_EXACT source."""
    root = ROOT if root is None else root
    relative = os.path.relpath(path, root).replace("\\", "/")
    rows = [row for row in sources if row.get("destination_repository_path") == relative]
    if len(rows) != 1:
        return None
    row = rows[0]
    if row.get("operation") != "ADD" or row.get("transformation") != "COPY_EXACT":
        return None
    with open(path, "rb") as stream:
        actual = hashlib.sha256(stream.read()).hexdigest()
    if actual != row.get("source_sha256") or actual != row.get("output_sha256"):
        return None
    return row


def load_source_map(root=None):
    root = ROOT if root is None else root
    path = os.path.join(root, "docs", "provenance", "v5-consolidation", "SOURCE_MAP.json")
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as stream:
        return json.load(stream)["sources"]


def load_successor_source_map(root=None):
    """Keep the independently validated successor source owner separate."""
    root = ROOT if root is None else root
    path = os.path.join(root, 'docs', 'provenance', 'v5-successors', 'SOURCE_MAP.json')
    if not os.path.isfile(path):
        return []
    with open(path, encoding='utf-8') as stream:
        return json.load(stream)['sources']


def _successor_source_identity(row):
    """Recognise typed custody fields; the successor validator checks scope."""
    required = {'id', 'origin_input_id', 'origin_input_sha256', 'origin_archive_sha256',
                'member_chain', 'original_sha256', 'original_bytes', 'public_path', 'public_sha256',
                'public_bytes', 'projection', 'projection_basis', 'review_scope', 'derivation'}
    if not isinstance(row, dict) or set(row) != required:
        return False
    if any(not isinstance(row.get(name), str) or not row[name]
           for name in ('id', 'origin_input_id', 'projection_basis', 'review_scope')):
        return False
    for name in ('origin_input_sha256', 'original_sha256'):
        if not re.fullmatch('[0-9a-f]{64}', row.get(name) or ''):
            return False
    if type(row.get('original_bytes')) is not int or row['original_bytes'] < 0:
        return False
    chain = row.get('member_chain')
    if not isinstance(chain, list) or not chain:
        return False
    if not re.fullmatch('[0-9a-f]{64}', row.get('origin_archive_sha256') or ''):
        return False
    if any(not isinstance(name, str) or not name or name.startswith('/')
           or '\\' in name or ':' in name or any(p in ('', '.', '..') for p in name.split('/'))
           for name in chain):
        return False
    projection = row.get('projection')
    if projection == 'CUSTODY_ONLY':
        return all(row.get(name) is None for name in ('public_path', 'public_sha256', 'public_bytes', 'derivation'))
    if projection not in ('EXACT', 'DERIVED'):
        return False
    digest = row.get('public_sha256')
    if not re.fullmatch('[0-9a-f]{64}', digest or '') or type(row.get('public_bytes')) is not int or row['public_bytes'] < 0:
        return False
    path = row.get('public_path')
    prefix = 'experiments/orthemology-v5-successors/source-store/' + digest + '/'
    if not isinstance(path, str) or not path.startswith(prefix) or '\\' in path or ':' in path:
        return False
    if any(part in ('', '.', '..') for part in path.split('/')):
        return False
    if projection == 'EXACT':
        return (row['public_sha256'] == row['original_sha256']
                and row['public_bytes'] == row['original_bytes'] and row.get('derivation') is None)
    derivation = row.get('derivation')
    return bool(isinstance(derivation, dict) and re.fullmatch('[0-9a-f]{64}', derivation.get('diff_sha256') or '')
                and isinstance(derivation.get('review_id'), str) and derivation['review_id'])


_SUCCESSOR_FRAGMENT_FIELDS = set('schema cell sources reviews results statuses suites receipts supersession legacy_endpoints selectors obligations calculus empirical projection_reviews public_allowlist'.split())
_SUCCESSOR_SUITE_FIELDS = set('id family result_families origin_archive_sha256 source_ids review_ids targets controls toolchain replay'.split())
_SUCCESSOR_REPLAY_FIELDS = set('schema scope files modules module_order positive_roots audit_roots negative_roots runtime_roots official_imports target_names package_manifest_source_id packages tools external_inputs fixtures drivers stages build_roots'.split())
_FUSHA_REPOSITORY = 'https://github.com/theislampill/fusha'
_FUSHA_COMMIT = 'c8b5db593d88311e5a020607dba70ff838ab61c5'
_FUSHA_TREE = 'a5bd2b045bc36c78047b5d3f7e9c2807fbf4153c'
# D03's complete suite/public-byte approval plus the exact selected source rows.
# These admit only the reviewed configuration pair, not arbitrary build paths.
_APPROVED_SUCCESSOR_RELOCATIONS = {
    't11-substitution': ('39e05def1e6370039143ff47862774fc6dd1c4f9865f9b39827cdff43186f090',
                         'a533aa3d1ef8790a64562580a4e97531db6b730e58d087824889604000520b29'),
    't11-nucleus': ('f8d2057ed34df1260efafe16a2227400a9f9f5b2d9cc13b3d86105bf7d269160',
                    'a8c4f3688271927809d53fa0881f74f48891d66a0c13dbdaf0a5c6f37abbd643'),
    't11-dependent-all': ('b87aca15fb03afe740abc50aa8dfc00d5a9dbf59de7f0b61591123163f47ec8b',
                          '93f729bdd94de7b48d328bdeef9bd4ba35eac10fce88630d8dc97b7af079fa44'),
    't11-normalization': ('4653066edcd7df7c05addf7c81aa48ee9680c36f58a216ccd5c55d04d5763da6',
                          '5f0b424cf1441004c6ce611dee2eb052b6f8467173d98c68803c094c761d15ff'),
}
_SUCCESSOR_NEGATIVE_INVENTORY = {
    'owner': {
        'id': 'identity-src-078b4d813390f8a2229b', 'origin_input_id': 'T11-EVIDENCE',
        'origin_input_sha256': '3c96b40a0e8236fb6d58aef090db1483eab1ea1ac06153de60498665ffa35fa4',
        'origin_archive_sha256': '0017f0b08ca7231a3b5928d7c6e1a5db1acfc636ad3664c8524180c482e2015b',
        'member_chain': ['components/P01_Syntactic_Substitution_Admissibility_Public_20261003.zip',
                         'Syntactic_Substitution_Admissibility/PUBLIC_PROJECTION.json'],
        'original_sha256': '61b23329c0dc24c8533a922204769a2128e7574bcbf96ba52424bda2a6614fbb',
        'original_bytes': 23390,
        'public_path': 'experiments/orthemology-v5-successors/source-store/61b23329c0dc24c8533a922204769a2128e7574bcbf96ba52424bda2a6614fbb/PUBLIC_PROJECTION.json',
        'public_sha256': '61b23329c0dc24c8533a922204769a2128e7574bcbf96ba52424bda2a6614fbb',
        'public_bytes': 23390, 'projection': 'EXACT',
    },
    'omitted': [
        {'path': ('scripts/' + 'reconstruct.py'), 'sha256': 'dbe3b93b233c2c93671fcba9a1723bba72855b82a3e022b3d16ff5aceea9f93a',
         'bytes': 1451, 'reason': 'Preparation-only helper; not required for verification of the included exact sources.'},
        {'path': ('scripts/' + 'package.py'), 'sha256': '0761b485a73d0e206732ef7b6a253d11b786e84819ede3218b2ad6d2573ca936',
         'bytes': 2172, 'reason': 'Preparation-only helper; not required for verification of the included exact sources.'},
    ],
}
# This historical review did not distribute its input copy. Its exact record
# binds this key to the identical selected candidate in the original archive.
# Digests below cover the complete pinned source-map records.
_SUCCESSOR_EXECUTION_HASH_KEY = {
    'owner_public_path': 'experiments/orthemology-v5-successors/source-store/0748d78e938b178963f833decf2cafba3584b4262c534b6083168d59a0a1b3d6/FINAL_EXECUTION_RECORD.json',
    'owner_record_sha256': '88c962692a9c6ad4e761ca8ee15eeec8d2f67fd2dd79c49c456c66280cae6176',
    'archive_root': 'Orthemology_Tenth_Research_Evidence_v1_20261003',
    'selected_candidate': 'tranche10/research/occurrence-continuation/release-candidate-v1/checker',
    'key': ('tests/' + 'test_contract.py'),
    'target_id': 'T10-SOURCE-CHECKER-TESTS-TEST_CONTRACT',
    'target_record_sha256': 'e15ab7ca4cb18bba05ba3780f688adefde9a5161407718fafb962ce81c5e2df3',
}


class InvalidSuccessorSelector(ValueError):
    """Recognised typed metadata must not hide an escaping path from regexes."""


def _strict_selector_json(text):
    def pairs(items):
        result = {}
        for name, value in items:
            if name in result:
                raise ValueError('Duplicate selector key')
            result[name] = value
        return result
    def nonfinite(value):
        raise ValueError('Nonfinite selector value')
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=nonfinite)
    json.dumps(value, allow_nan=False)
    return value


def _selector_path(value):
    return (isinstance(value, str) and bool(value) and not value.startswith('/')
            and '\\' not in value and ':' not in value and '\0' not in value
            and all(part not in ('', '.', '..') for part in value.split('/')))


def _selector_hash(value, length=64):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{%d}' % length, value) is not None


def _public_successor_bytes(row, root):
    """A typed selector never excuses missing or changed public source bytes."""
    if not _successor_source_identity(row) or row['public_path'] is None:
        return None
    path = os.path.join(root, *row['public_path'].split('/'))
    if os.path.commonpath((os.path.realpath(root), os.path.realpath(path))) != os.path.realpath(root):
        return None
    current = os.fspath(root)
    for part in row['public_path'].split('/'):
        current = os.path.join(current, part)
        if os.path.islink(current):
            return None
    if not os.path.isfile(path):
        return None
    with open(path, 'rb') as stream:
        raw = stream.read()
    return raw if len(raw) == row['public_bytes'] and hashlib.sha256(raw).hexdigest() == row['public_sha256'] else None


def _unique_selector_source(sid, sources, root):
    rows = [row for row in sources if isinstance(row, dict) and row.get('id') == sid]
    if not rows or any(row != rows[0] for row in rows[1:]):
        return None
    row = rows[0]
    return row if _public_successor_bytes(row, root) is not None else None


def _source_owners(src, document, sources, root):
    owners = [row for row in sources if isinstance(row, dict) and row.get('public_path') == src]
    if not owners:
        return []
    for row in owners:
        raw = _public_successor_bytes(row, root)
        if raw is None or row['projection'] != 'EXACT' or _strict_selector_json(raw) != document:
            return []
    return owners


def _execution_hash_key(document, owners, sources, root):
    """Recognise one pinned original hash-map key, never arbitrary JSON keys."""
    pin = _SUCCESSOR_EXECUTION_HASH_KEY
    canonical = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    if not owners or any(canonical(owner) != pin['owner_record_sha256'] for owner in owners):
        return None
    target = _unique_selector_source(pin['target_id'], sources, root)
    hashes, projection = document.get('candidate_file_hashes'), document.get('public_projection')
    if (target is None or canonical(target) != pin['target_record_sha256'] or target['projection'] != 'EXACT'
            or not isinstance(hashes, dict) or '' in hashes or not _selector_hash(hashes.get(pin['key']))
            or hashes[pin['key']] != target['original_sha256'] or not isinstance(projection, dict)
            or projection.get('historical_reviewer_input_copy_distributed') is not False
            or projection.get('identical_selected_candidate') != pin['selected_candidate']):
        return None
    member = '/'.join((pin['archive_root'], pin['selected_candidate'], pin['key']))
    for owner in owners:
        if (any(target[field] != owner[field] for field in
                ('origin_input_id', 'origin_input_sha256', 'origin_archive_sha256'))
                or target['member_chain'] != owner['member_chain'][:-1] + [member]):
            return None
    return pin['key']


def _locked_external_files(document, owner):
    """Recognise exact external-source inventories without fetching them."""
    # Source-owned Mathlib/Batteries inventories describe the pinned dependency,
    # not this repository's docs directory. Require the complete exact document
    # as well as its source digest; arbitrary rows cannot borrow the exception.
    mathlib = {
        '1c4d1fa63acf416d7b965ed519d16faea965022cb8eb8d74725d59d801db16f0':
            'b681baebe9cc29157374228e49f24b6ba177a2dfb50ce78a053512c305c1e065',
        'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431':
            '1f98b610f3d37455c3fa2c18c58461bcbd7d033a7590ad15b26f23862ffc8292',
        'f461e480570d88a8b438fc332b6f3327216df187dedd09c979d47bedbaaa3bba':
            '38c7949b68ef4debf63ad23442182637185d17bf3b34e1a2850b3cf3ee06f6d8',
        '8e121ae7ace129ad9270db82ab6682609f5fec12a0d2de4fe567cf8898d6f039':
            'ebc8e528ba7c9d3d86d9184f7866768728f2770fa3ad8018fb968480e52845ca',
    }
    expected = mathlib.get(owner.get('original_sha256'))
    if expected is not None:
        observed = hashlib.sha256(json.dumps(document, sort_keys=True, ensure_ascii=False,
            separators=(',', ':'), allow_nan=False).encode()).hexdigest()
        if owner.get('public_sha256') != owner.get('original_sha256') or observed != expected:
            return None
        rows = document if isinstance(document, list) else document['files']
        return {row['path']: row for row in rows}
    members = {'occurrence-correspondence-source-lock-v1': 'language/source-lock.json',
               'sense-scope-supplemental-source-lock-v1': 'language/sense-source-lock.json'}
    if (not isinstance(document, dict) or set(document) != {'format', 'repository', 'commit', 'tree', 'scope', 'files'}
            or document['format'] not in members or document['repository'] != _FUSHA_REPOSITORY
            or document['commit'] != _FUSHA_COMMIT or document['tree'] != _FUSHA_TREE
            or not isinstance(document['scope'], str) or not document['scope'].strip()
            or not isinstance(document['files'], list) or not document['files']):
        return None
    member = owner['member_chain'][-1]
    expected_member = members[document['format']]
    if member != expected_member and not member.endswith('/' + expected_member):
        return None
    rows = {}
    for row in document['files']:
        if isinstance(row, dict) and 'path' in row and not _selector_path(row['path']):
            raise InvalidSuccessorSelector('Unsafe successor external lock path')
        if (not isinstance(row, dict) or set(row) != {'path', 'blob_sha1', 'sha256', 'bytes', 'url'}
                or not _selector_path(row['path']) or row['path'] in rows
                or not _selector_hash(row['blob_sha1'], 40) or not _selector_hash(row['sha256'])
                or type(row['bytes']) is not int or row['bytes'] < 0
                or row['url'] != _FUSHA_REPOSITORY + '/blob/' + _FUSHA_COMMIT + '/' + row['path']):
            return None
        rows[row['path']] = row
    return rows


def _empirical_public_files(document, owners, sources, root):
    fields = {'format_version', 'scope', 'runtime', 'numerical_core_provenance', 'synthetic_tests',
              'aggregate_reference_verification', 'source_hash_verification', 'public_files'}
    if (not isinstance(document, dict) or set(document) != fields or type(document['format_version']) is not int
            or document['format_version'] != 1 or not isinstance(document['scope'], str)
            or not document['scope'].strip() or not isinstance(document['public_files'], list)
            or not document['public_files']):
        return False
    runtime = document['runtime']; provenance = document['numerical_core_provenance']
    if (not isinstance(runtime, dict) or set(runtime) != {'python', 'numpy', 'scipy', 'pandas', 'openpyxl'}
            or not all(isinstance(v, str) and v for v in runtime.values())
            or not isinstance(provenance, dict)
            or set(provenance) != {'implementation_A_original_sha256', 'implementation_B_original_sha256', 'adaptation'}
            or not all(_selector_hash(provenance[k]) for k in ['implementation_A_original_sha256', 'implementation_B_original_sha256'])
            or not isinstance(provenance['adaptation'], str) or not provenance['adaptation'].strip()
            or any(document[k] not in {'pass', 'fail'} for k in
                   ['synthetic_tests', 'aggregate_reference_verification', 'source_hash_verification'])):
        return False
    names = set()
    for item in document['public_files']:
        if isinstance(item, dict) and 'file' in item and not _selector_path(item['file']):
            raise InvalidSuccessorSelector('Unsafe successor empirical member path')
        if (not isinstance(item, dict) or set(item) != {'file', 'sha256', 'bytes'}
                or not _selector_path(item['file']) or item['file'] in names
                or not _selector_hash(item['sha256']) or type(item['bytes']) is not int or item['bytes'] < 0):
            return False
        names.add(item['file'])
        candidates = []
        for owner in owners:
            member = owner['member_chain'][-1]
            if not member.endswith('/empirical/BINDING.json'):
                continue
            selector = posixpath.join(posixpath.dirname(member), item['file'])
            candidates.extend(row for row in sources if isinstance(row, dict)
                and row.get('origin_archive_sha256') == owner['origin_archive_sha256']
                and row.get('origin_input_sha256') == owner['origin_input_sha256']
                and row.get('member_chain') == owner['member_chain'][:-1] + [selector])
        if not candidates or any(_public_successor_bytes(row, root) is None
                or row['original_sha256'] != item['sha256'] or row['original_bytes'] != item['bytes'] for row in candidates):
            return False
    return True


def _suite_selectors(suite, sources, root):
    """Remove only declared local build and external-fixture path fields."""
    if not isinstance(suite, dict) or set(suite) != _SUCCESSOR_SUITE_FIELDS:
        return
    replay = suite['replay']
    if (not isinstance(replay, dict) or set(replay) != _SUCCESSOR_REPLAY_FIELDS
            or replay['schema'] != 'orthemology-v5-replay-v1'
            or replay['scope'] not in {'FINITE', 'COMPONENTS', 'DECLARED_SUITE'}
            or not isinstance(suite['source_ids'], list) or not suite['source_ids']
            or any(not isinstance(sid, str) for sid in suite['source_ids'])
            or len(set(suite['source_ids'])) != len(suite['source_ids'])
            or not isinstance(replay['files'], list)):
        return
    selected = {sid: _unique_selector_source(sid, sources, root) for sid in suite['source_ids']}
    if any(row is None for row in selected.values()):
        return
    canonical = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
        separators=(',', ':'), allow_nan=False).encode()).hexdigest()
    approval = canonical({'suite': suite, 'sources': {sid: row['public_sha256'] for sid, row in selected.items()}})
    approved_relocation = _APPROVED_SUCCESSOR_RELOCATIONS.get(suite['id']) == (approval, canonical(selected))
    paths, ids = set(), set()
    for row in replay['files']:
        if isinstance(row, dict) and 'path' in row and not _selector_path(row['path']):
            raise InvalidSuccessorSelector('Unsafe successor suite projection path')
        if (not isinstance(row, dict) or set(row) != {'source_id', 'path', 'role'}
                or row['source_id'] not in selected or row['source_id'] in ids
                or not _selector_path(row['path']) or row['path'] in paths
                or row['role'] not in {'PROOF', 'AUDIT', 'NEGATIVE', 'RUNTIME', 'DRIVER', 'CONFIG', 'DATA', 'LOCK', 'REVIEW'}):
            return
        member = selected[row['source_id']]['member_chain'][-1]
        if member != row['path'] and not member.endswith('/' + row['path']):
            manifest = member == 'lean/lake-manifest.json' and row['path'] == 'configuration/lake-manifest.json'
            environment = (row['source_id'] == 'identity-src-db1e24bbc42e41ce33ac'
                           and member == 'Syntactic_Substitution_Admissibility/ENVIRONMENT_AND_DESIGN_INPUTS.json'
                           and row['path'] == 'configuration/D10_ENVIRONMENT_AND_DESIGN_INPUTS.json')
            if not (approved_relocation and row['role'] == 'CONFIG' and (manifest or environment)):
                return
        paths.add(row['path']); ids.add(row['source_id'])
    if ids != set(selected):
        return
    # Bind external fixture selectors through the source-prescribed tree lock.
    inputs = {}
    for row in replay['external_inputs']:
        if (not isinstance(row, dict) or set(row) != {'id', 'source_id', 'kind', 'manifest_source_id',
                'manifest_key', 'expected_sha256', 'expected_bytes', 'role'} or not isinstance(row['id'], str)
                or not row['id'] or row['id'] in inputs):
            return
        inputs[row['id']] = row
    fixtures = []
    for fixture in replay['fixtures']:
        if (not isinstance(fixture, dict) or set(fixture) != {'id', 'input_id', 'operation', 'path'}
                or fixture['input_id'] not in inputs or fixture['operation'] not in {'ABSENT', 'NON_DIRECTORY', 'OMIT', 'APPEND_CHANGED_BYTES'}):
            return
        if fixture['path'] is None:
            continue
        if not _selector_path(fixture['path']):
            raise InvalidSuccessorSelector('Unsafe successor external fixture path')
        source_input = inputs[fixture['input_id']]
        if (source_input['kind'] != 'TREE' or source_input['role'] != 'INPUT'
                or source_input['source_id'] is not None or source_input['expected_sha256'] is not None
                or source_input['expected_bytes'] is not None or source_input['manifest_key'] != 'files'
                or fixture['operation'] not in {'OMIT', 'APPEND_CHANGED_BYTES'}
                or not _selector_path(fixture['path'])):
            return
        owner = selected.get(source_input['manifest_source_id'])
        if owner is None or owner['projection'] != 'EXACT':
            return
        locked = _locked_external_files(_strict_selector_json(_public_successor_bytes(owner, root)), owner)
        if locked is None or fixture['path'] not in locked:
            return
        fixtures.append(fixture)
    for row in replay['files']:
        row['path'] = ''
    for row in fixtures:
        row['path'] = ''


def successor_origin_document(src, text, sources=None, root=None):
    """Make an occurrence-local scan copy; native fields and links stay intact."""
    root = ROOT if root is None else root
    prefix = 'docs/provenance/v5-successors/'
    fragment = re.fullmatch(re.escape(prefix) + r'fragments/(D0[4-9]|D1[0-8])\.json', src)
    suite_owner = re.fullmatch(r'experiments/orthemology-v5-successors/suites/([A-Za-z0-9][A-Za-z0-9_-]*)\.json', src)
    try:
        document = _strict_selector_json(text)
        if isinstance(document, list):
            owners = _source_owners(src, document, list(sources or []), root)
            if owners and all(_locked_external_files(document, owner) is not None for owner in owners):
                for row in document:
                    row['path'] = ''
                return json.dumps(document, ensure_ascii=False, indent=2)
            return text
        if not isinstance(document, dict):
            return text
        if src == _SUCCESSOR_NEGATIVE_INVENTORY['owner']['public_path']:
            for row in document.get('omitted', []):
                if isinstance(row, dict) and 'path' in row and not _selector_path(row['path']):
                    raise InvalidSuccessorSelector('Unsafe successor omitted-inventory path')
        if src == _SUCCESSOR_EXECUTION_HASH_KEY['owner_public_path']:
            hashes = document.get('candidate_file_hashes')
            if isinstance(hashes, dict) and any(not _selector_path(key) for key in hashes):
                raise InvalidSuccessorSelector('Unsafe successor execution hash-map path')
        pool = list(sources or [])
        owned_fragment = bool(fragment and document.get('cell') == fragment.group(1)
            and document.get('schema') == 'orthemology-v5-successor-fragment-v1'
            and {'schema', 'cell', 'sources'} <= set(document) <= _SUCCESSOR_FRAGMENT_FIELDS
            and isinstance(document['sources'], list))
        owned_map = src == prefix + 'SOURCE_MAP.json' and set(document) == {'sources', 'reviews'} and isinstance(document['sources'], list)
        if owned_fragment or owned_map:
            for row in document['sources']:
                if row not in pool:
                    pool.append(row)
            if owned_fragment:
                for suite in document.get('suites', []):
                    _suite_selectors(suite, pool, root)
            for row in document['sources']:
                if isinstance(row, dict) and isinstance(row.get('member_chain'), list):
                    if any(not _selector_path(member) for member in row['member_chain']):
                        raise InvalidSuccessorSelector('Unsafe successor original-member path')
                if isinstance(row, dict) and row.get('public_path') is not None and not _selector_path(row['public_path']):
                    raise InvalidSuccessorSelector('Unsafe successor public projection path')
                if _successor_source_identity(row):
                    row['member_chain'] = []
            return json.dumps(document, ensure_ascii=False, indent=2)
        if suite_owner and document.get('id') == suite_owner.group(1):
            _suite_selectors(document, pool, root)
            return json.dumps(document, ensure_ascii=False, indent=2)
        owners = _source_owners(src, document, pool, root)
        if owners:
            execution_key = _execution_hash_key(document, owners, pool, root)
            if execution_key is not None:
                # Only the key is an original selector. Keep its digest and
                # every other field visible in this temporary scan copy.
                hashes = document['candidate_file_hashes']
                hashes[''] = hashes.pop(execution_key)
            if (all(all(owner.get(key) == value for key, value in _SUCCESSOR_NEGATIVE_INVENTORY['owner'].items())
                    for owner in owners) and document.get('omitted') == _SUCCESSOR_NEGATIVE_INVENTORY['omitted']):
                # Negative inventory: only these two fields state non-inclusion.
                # Other helper mentions remain ordinary checked references.
                for row in document['omitted']:
                    row['path'] = ''
            if all(_locked_external_files(document, owner) is not None for owner in owners):
                for row in document['files']:
                    row['path'] = ''
            elif _empirical_public_files(document, owners, pool, root):
                for row in document['public_files']:
                    row['file'] = ''
            return json.dumps(document, ensure_ascii=False, indent=2)
    except InvalidSuccessorSelector:
        raise
    except (ValueError, TypeError, KeyError, IndexError, OSError):
        # Invalid or ambiguous metadata has no exception to native-path checks.
        return text
    return text


# The final T20 reader files keep their sealed owner-archive links. This one
# finite public alias index binds the reconstruction context separately from
# original-member custody; it does not make archive links native checkout URLs.
_T20_READER_INDEX = (
    'experiments/orthemology-v5-successors/'
    'groups/t20-successor/CONTEXT_SOURCE_INDEX.json',
    'cb2acbc6c3dc795c91ef18192a2077d7cba513761eec291a01b99c7ef178b31e',
)


def _t20_reader_locator(path, target, sources, root, from_packet_root=False):
    """Resolve one sealed reader alias only while both exact source bytes match."""
    def checked_file(relative):
        if not _selector_path(relative):
            return None
        current = os.fspath(root)
        for part in relative.split('/'):
            current = os.path.join(current, part)
            if os.path.islink(current):
                return None
        if not os.path.isfile(current):
            return None
        with open(current, 'rb') as stream:
            return stream.read()

    try:
        raw = checked_file(_T20_READER_INDEX[0])
        if raw is None or hashlib.sha256(raw).hexdigest() != _T20_READER_INDEX[1]:
            return False
        index = _strict_selector_json(raw.decode('utf-8'))
        rows = index['public_sources']
        aliases = {row['owner_archive_path']: row for row in rows}
        if len(aliases) != len(rows):
            return False
        relative = os.path.relpath(path, root).replace('\\', '/')
        owners = [row for row in rows if row['public_path'] == relative]
        if len(owners) != 1 or not isinstance(target, str) or not target or target.startswith('/') or '\\' in target or ':' in target or '\0' in target:
            return False

        def exact_source(row):
            matches = [source for source in sources if source.get('id') == row['id']]
            if len(matches) != 1:
                return False
            source = matches[0]
            canonical = json.dumps(source, sort_keys=True, ensure_ascii=False,
                                   separators=(',', ':'), allow_nan=False).encode()
            if (hashlib.sha256(canonical).hexdigest() != row['source_record_sha256']
                    or source['public_path'] != row['public_path']
                    or source['public_sha256'] != row['public_sha256']
                    or source['public_bytes'] != row['public_bytes']):
                return False
            payload = checked_file(row['public_path'])
            return (payload is not None and len(payload) == row['public_bytes']
                    and hashlib.sha256(payload).hexdigest() == row['public_sha256'])

        owner = owners[0]
        if not exact_source(owner):
            return False
        candidates = {posixpath.normpath(posixpath.join(
            posixpath.dirname(owner['owner_archive_path']), target))}
        if from_packet_root:
            candidates.add(posixpath.normpath(target))
        matches = [aliases[name] for name in candidates
                   if name.startswith('t20/') and _selector_path(name) and name in aliases]
        return len(matches) == 1 and exact_source(matches[0])
    except (OSError, UnicodeDecodeError, ValueError, TypeError, KeyError):
        return False


def successor_packet_locator(path, target, sources, root=None, from_packet_root=False):
    """Resolve exact original-member custody or the pinned finite reader context."""
    root = ROOT if root is None else root
    if _t20_reader_locator(path, target, sources, root, from_packet_root):
        return True
    relative = os.path.relpath(path, root).replace('\\', '/')
    owners = [row for row in sources if row.get('public_path') == relative]
    if (not owners or any(_public_successor_bytes(row, root) is None for row in owners)
            or not isinstance(target, str) or not target or target.startswith('/') or '\\' in target or ':' in target
            or '\0' in target or (from_packet_root and not _selector_path(target))):
        return False
    for owner in owners:
        member = owner['member_chain'][-1]
        selector = posixpath.normpath(target if from_packet_root else posixpath.join(posixpath.dirname(member), target))
        if selector == '..' or selector.startswith('../'):
            continue
        candidates = {selector}
        if from_packet_root:
            # Retain the exact original owner's directory, including a leading
            # archive folder. Do not search by basename or arbitrary suffix.
            candidates.add(posixpath.join(posixpath.dirname(member), target))
        matched = []
        for candidate in candidates:
            rows = [row for row in sources
                    if all(row.get(key) == owner[key] for key in ('origin_input_id', 'origin_input_sha256', 'origin_archive_sha256'))
                    and row.get('member_chain') == owner['member_chain'][:-1] + [candidate]]
            if not rows:
                continue
            if any(not _successor_source_identity(row) for row in rows):
                return False
            if len({(row['original_sha256'], row['original_bytes']) for row in rows}) != 1:
                return False
            for row in rows:
                if row['projection'] == 'CUSTODY_ONLY' and candidate == selector:
                    continue
                if _public_successor_bytes(row, root) is None:
                    return False
            matched.append(candidate)
        if len(matched) > 1:
            return False
        if matched:
            return True
    return False


def historical_notation_source(path, sources, root=None):
    """Accepted historical originals retain their notation, never by path alone."""
    root = ROOT if root is None else root
    relative = os.path.relpath(path, root).replace("\\", "/")
    row = exact_source_record(path, sources, root)
    return bool(relative.startswith("theory/lineages/") and row
                and row.get("source_artifact") == "H14"
                and row.get("public_safety_tier") == "HISTORICAL_EVIDENCE")


def preserved_math_source(path, sources, root=None):
    """Original historical notation or exact generated quotations, not PDF inputs."""
    root = ROOT if root is None else root
    if historical_notation_source(path, sources, root):
        return True
    relative = os.path.relpath(path, root).replace("\\", "/")
    prefix = "docs/provenance/v5-consolidation/"
    if relative not in (prefix + "THEOREM_INDEX.md", prefix + "CRITICISM_INDEX.md"):
        return False
    rows = [r for r in sources if r.get("destination_repository_path") == relative]
    if (len(rows) != 1 or rows[0].get("operation") != "GENERATE"
            or rows[0].get("transformation") != "GENERATE_INDEXES"
            or rows[0].get("source_artifact") != "A5_SPEC"):
        return False
    manifest = os.path.join(root, "experiments", "orthemology-v5", "SOURCE_MANIFEST.json")
    if not os.path.isfile(manifest):
        return False
    with open(manifest, encoding="utf-8") as stream:
        entries = [r for r in json.load(stream)["files"] if r.get("path") == relative]
    with open(path, "rb") as stream:
        data = stream.read()
    return bool(len(entries) == 1 and entries[0].get("bytes") == len(data)
                and entries[0].get("sha256") == hashlib.sha256(data).hexdigest())


def compact_provenance_record(path, sources):
    relative = os.path.relpath(path, ROOT).replace("\\", "/")
    if not relative.startswith("docs/provenance/v5-consolidation/reconciliation/"):
        return False
    row = exact_source_record(path, sources)
    return bool(row and row.get("source_artifact") in ("A4C", "A4T")
                and row.get("public_safety_tier") == "COMPACT_PROVENANCE_RECORD")


def original_packet_locator(path, target, sources, root=None, from_packet_root=False):
    """Classify a digest-bound external locator; never claim it is a download."""
    source = exact_source_record(path, sources, root)
    if not source or source.get("source_artifact") not in ("V4", "V5"):
        return False
    if target.startswith("/") or "\\" in target or ":" in target:
        return False
    selector = posixpath.normpath(target if from_packet_root else
                                  posixpath.join(posixpath.dirname(source["source_path"]), target))
    if selector == ".." or selector.startswith("../"):
        return False
    rows = [row for row in sources
            if row.get("source_artifact") == source["source_artifact"]
            and row.get("source_path") == selector]
    if len(rows) != 1:
        return False
    row = rows[0]
    return bool(row.get("operation") == "EXTERNAL_CUSTODY"
                and row.get("transformation") == "NO_REPOSITORY_EFFECT"
                and row.get("destination_repository_path") is None
                and row.get("public_safety_tier") in ("HISTORICAL_EVIDENCE", "EXTERNAL_IMMUTABLE_CUSTODY_ITEM")
                and re.fullmatch(r"[0-9a-f]{64}", row.get("source_sha256") or ""))


def main():
    corpus = list(corpus_files())
    files = list(text_files(corpus))
    rel = lambda p: os.path.relpath(p, ROOT).replace("\\", "/")
    source_map = os.path.join(ROOT, "docs", "provenance", "v5-consolidation", "SOURCE_MAP.json")
    sources = []
    if os.path.isfile(source_map):
        with open(source_map, encoding="utf-8") as stream:
            sources = json.load(stream)["sources"]

    successor_sources = load_successor_source_map(ROOT)

    # 0: no tracked cache/bytecode artifact (R4 fresh review, Phase A4/E).
    # .gitignore excludes __pycache__/ but cannot un-track a force-added file;
    # this is the standing guard against that class entering history.
    try:
        tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT).decode()
        cached = sorted(f for f in tracked.splitlines()
                        if "__pycache__" in f or f.endswith((".pyc", ".pyo")))
        check("no cache/bytecode artifact is git-tracked", not cached, str(cached[:5]))
    except Exception as e:  # git absent: state the boundary instead of guessing
        check("no cache/bytecode artifact is git-tracked (git unavailable: %s)" % e, True)

    # 1-3: banned patterns / secrets
    offenders = {}
    for p in files:
        if rel(p) == "scripts/validate_repo.py":
            continue  # patterns appear here as rules
        try:
            c = open(p, "r", encoding="utf-8", errors="strict").read()
        except UnicodeDecodeError:
            # a file the repository itself declares binary (.gitattributes -text,
            # e.g. the binary-capable interruption patch) is exempt from the
            # utf-8 text contract; anything else must be utf-8 (R4 fresh review)
            try:
                attr = subprocess.check_output(
                    ["git", "check-attr", "text", "--", rel(p)], cwd=ROOT).decode()
                declared_binary = attr.strip().endswith("unset")
            except Exception:
                declared_binary = False
            check("utf-8 readable (or declared binary): " + rel(p), declared_binary)
            continue
        for pat, why in BANNED:
            if re.search(pat, c):
                offenders.setdefault(rel(p), []).append(why)
    check("no absolute local paths / banned private patterns / secrets", not offenders, str(offenders))
    check("no .env files", not any(f.endswith(".env") for f in files))
    check("no zip/bulk archives", not any(
        path.lower().endswith((".zip", ".7z", ".rar")) for path in corpus
    ))
    bad_names = [os.path.basename(path) for path in corpus
                 if BANNED_FILENAMES.search(os.path.basename(path))
                 and not (path.endswith(".jsonl") and compact_provenance_record(path, sources))]
    check("no research-output/session-dump artifact files", not bad_names, str(bad_names))

    # 4-5: exactly one manuscript, one core
    ms = [f for f in os.listdir(os.path.join(ROOT, "manuscript")) if f.endswith(".md")]
    check("exactly one current manuscript", ms == ["orthemma-ortheme-systems-revised-draft.md"], str(ms))
    check("formal core present and unique",
          os.path.exists(os.path.join(ROOT, "theory", "orthemic-core-formalization.md")))

    # 6: status labels on proposal/archive docs (pilot0 primers/items are frozen
    # exposure-matched INSTRUMENTS, deliberately status-free; the packet's status
    # lives in PILOT0-PROTOCOL.md and the readiness report)
    unlabeled = []
    for sub in ("companion", "terminology", "archive"):
        for dirpath, _, fns in os.walk(os.path.join(ROOT, sub)):
            if "primers" in dirpath or os.path.join("pilot0", "items") in dirpath:
                continue
            for fn in fns:
                if fn.endswith(".md"):
                    c = open(os.path.join(dirpath, fn), encoding="utf-8").read()[:4000].lower()
                    if not any(k in c for k in ("status", "not canonical", "designed", "proposed",
                                                "draft", "not run", "ledger", "validation report",
                                                "optional patch", "incomplete")):
                        unlabeled.append(fn)
    check("every proposal/archive doc carries a status label", not unlabeled, str(unlabeled))

    # 7: no candidate banners in published theory/manuscript
    bannered = []
    for sub in ("theory", "manuscript", "companion", "terminology"):
        for dirpath, _, fns in os.walk(os.path.join(ROOT, sub)):
            for fn in fns:
                if fn.endswith(".md"):
                    c = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                    if "PROPOSED D1 CANDIDATE" in c:
                        bannered.append(fn)
    check("no PROPOSED-candidate banner in published files", not bannered, str(bannered))

    # 8: internal relative links resolve
    broken = []
    packet_locators = []
    successor_locators = []
    for p in files:
        if not p.endswith(".md"):
            continue
        c = open(p, encoding="utf-8").read()
        for target in markdown_link_targets(c):
            tgt = target.split('#', 1)[0]
            if not tgt:
                continue
            if tgt.startswith(("http://", "https://", "mailto:")):
                continue
            full = os.path.normpath(os.path.join(os.path.dirname(p), tgt))
            if not os.path.exists(full):
                edge = "%s -> %s" % (rel(p), tgt)
                if original_packet_locator(p, tgt, sources):
                    packet_locators.append(edge)
                elif successor_packet_locator(p, tgt, successor_sources):
                    successor_locators.append(edge)
                else:
                    broken.append(edge)
    check("all repository-relative links resolve", not broken, str(broken))
    if packet_locators:
        print("[INFO] %d original-packet locators (%d unique) have exact external-custody bindings; "
              "public retrieval remains unconfirmed" % (len(packet_locators), len(set(packet_locators))))
    if successor_locators:
        print('[INFO] %d successor original-member references have exact source/custody bindings; '
              'public projection and private custody remain distinct' % len(successor_locators))

    # 9: fences balanced, tables well-formed (column counts)
    bad_struct = []
    for p in files:
        if not p.endswith(".md"):
            continue
        lines = open(p, encoding="utf-8").read().splitlines()
        if sum(1 for ln in lines if ln.strip().startswith("```")) % 2 != 0:
            bad_struct.append(rel(p) + ": unbalanced fences")
    check("markdown structure (balanced code fences)", not bad_struct, str(bad_struct))

    # 10: manifest matches files
    man = os.path.join(ROOT, "docs", "provenance", "RELEASE-MANIFEST.sha256")
    ok10, det = True, []
    if os.path.exists(man):
        for ln in open(man, encoding="utf-8"):
            ln = ln.strip()
            if not ln:
                continue
            h, path = ln.split(None, 1)
            fp = os.path.join(ROOT, path)
            if not os.path.exists(fp):
                ok10 = False; det.append("missing " + path); continue
            actual = hashlib.sha256(open(fp, "rb").read()).hexdigest()
            if actual.lower() != h.lower():
                ok10 = False; det.append("hash mismatch " + path)
    else:
        ok10 = False; det.append("manifest missing")
    check("public SHA-256 manifest matches committed files", ok10, "; ".join(det))

    # 11: verdict-semantic fixtures pass
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "validate_verdict_semantics.py"),
                        "--fixtures", os.path.join(ROOT, "tests", "verdict-fixtures.json")],
                       capture_output=True, text=True)
    check("verdict-semantic fixtures pass", r.returncode == 0, r.stdout[-400:])

    # 12: README/STATUS honesty statements
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read().lower()
    status = open(os.path.join(ROOT, "STATUS.md"), encoding="utf-8").read().lower()
    need_r = ["not peer reviewed", "benchmark", "no empirical", "candidate"]
    need_s = ["not peer reviewed", "no completed empirical validation",
              "terminology not adopted", "not a completed paper", "draft"]
    check("README honesty statements present", all(k in readme for k in need_r),
          str([k for k in need_r if k not in readme]))
    check("STATUS honesty statements present", all(k in status for k in need_s),
          str([k for k in need_s if k not in status]))

    # 13-14 covered by banned patterns (deep-research, zip) above.
    print("TOTAL: %d failures" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()

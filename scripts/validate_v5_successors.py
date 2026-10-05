#!/usr/bin/env python3
"""Fail-closed T07--T15 successor integrity; validation does not adopt research.

Production CLI anchors the frozen predecessor to an accepted Git object and an
independently pinned inventory. Programmatic fixture anchors never affect CLI.
No archive driver, producer-supplied shell command or network request executes.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
from urllib.parse import urlsplit, urlunsplit

_spec = importlib.util.spec_from_file_location(
    '_v5_predecessor_helpers', Path(__file__).with_name('validate_research_continuations.py'))
_legacy = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_legacy)
require = _legacy.require
keys = _legacy.keys
sha = _legacy.sha
digest = _legacy.digest
nonempty = _legacy.nonempty
enum = _legacy.enum
safe_relative = _legacy.safe_relative
path_in = _legacy.path_in
indexed = _legacy.indexed

AREA = 'experiments/orthemology-v5-successors'
PROV = 'docs/provenance/v5-successors'
FROZEN_ROOTS = ['experiments/orthemology-v5-continuations',
                'docs/provenance/v5-research-continuations']
BASE_COMMIT = '19de267cd41d2a5eeeb3eaf0b91562f706e2a916'
BASE_TREE = '08a6452e50e8e4791d02410d1c1732875e520f2e'
BASELINE_ANCHOR = {
    'base_commit': BASE_COMMIT, 'base_tree': BASE_TREE,
    'preservation_sha256': 'cd81d3b80d5183c1c01b637207d0afefd2b143ce4ee346808ca473a15eea6c4a',
    'legacy_registry': {'path': FROZEN_ROOTS[0] + '/registry.json',
                        'sha256': '51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff'},
    'legacy_overlay': {'path': FROZEN_ROOTS[1] + '/SIXTH_FINAL_OVERLAY.json',
                       'sha256': '879879eaffdf04396577d113abb2d224b53e07e20a15f23c3f5b785b2291bd89'},
    'git_required': True,
}
FRESH = {'NOT_RUN', 'BLOCKED_EXTERNAL_INPUT', 'BLOCKED_TOOLCHAIN', 'RESOURCE_INCONCLUSIVE',
         'FAILED', 'FINITE_ONLY', 'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}
INHERITED = {'NONE', 'WRITTEN_MATHEMATICS', 'CONDITIONAL_PHILOSOPHY', 'SOURCE_ASSESSMENT',
             'KERNEL_COMPONENTS', 'KERNEL_DECLARED_SUITE', 'FINITE_REFERENCE_EXECUTION',
             'MIXED_SCOPED', 'STOPPED_UNREVIEWED'}
FORMS = {'FORMAL', 'ORDINARY', 'MIXED', 'CONDITIONAL', 'IMPLEMENTATION', 'PROPOSAL', 'SOURCE_ASSESSMENT'}
CALCULI = {'P01DF', 'P01AC.Has', 'P01AC.Intensional.Plus.HasPlus',
           'P01AC.ExtensionalRepair.HasE', 'OTHER', 'NONE'}
DOMAINS = {'BARE_INPUT', 'SUPPLIED_CERTIFICATE', 'FINITE_MODEL', 'UNBOUNDED_MODEL',
           'SOURCE_TEXT', 'REFERENCE_EXECUTION'}
REACH = {'NONE', 'WRITTEN_ONLY', 'FORMAL_COMPONENT', 'DECLARED_FORMAL_SUITE',
         'FINITE_WITNESS', 'REFERENCE_ONLY', 'RESTRICTED_CHECKER'}
WARRANTS = {'actual_world', 'normative', 'empirical_replication', 'specialist_review',
            'novelty', 'terminology_adoption'}
TERMINALS = {'COMPLETED', 'TIMEOUT', 'SKIPPED', 'INTERRUPTED', 'MISSING'}
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
SUPPLEMENTARY = {'FOUNDATIONAL_FRONTIER', 'SOURCE_USE', 'INTEGRATION_VERIFICATION',
                 'CONTROL_DISPOSITIONS', 'INTERNAL_REVIEW_DISPOSITION', 'TOOLCHAINS'}
BUNDLE_KEYS = {'registry', 'baseline_binding', 'preservation', 'sources', 'reviews', 'results',
               'statuses', 'bindings', 'suites', 'receipts', 'supersession', 'legacy_endpoints',
               'selectors', 'obligations', 'avenues', 'calculus', 'empirical', 'supplementary',
               'projection_reviews', 'public_allowlist'}


def canonical_json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def text_digest(value):
    return hashlib.sha256(nonempty(value).encode('utf-8')).hexdigest()


def check_public_text(text):
    """A public HTTP path is not a local path; queries and secrets still scan.

    Keep the immutable predecessor's credential and locator checks. Only the
    path component of a well-formed HTTP(S) URL gets the filesystem distinction.
    """
    def public_url(match):
        candidate = match.group(0)
        try:
            parsed = urlsplit(candidate)
            if parsed.scheme.lower() not in {'http', 'https'} or not parsed.hostname:
                return candidate
        except ValueError:
            return candidate
        path = re.sub(r'/(?:mnt/(?:data|c/(?:Users|workspace))|home/(?:oai|agent)|tmp)(?=/|$)',
                      '/public-url-path', parsed.path)
        return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))
    inspected = re.sub(r'https?://[^\s<>"\']+', public_url, text, flags=re.IGNORECASE)
    _legacy.check_public_text(inspected)


def _finite(value):
    if isinstance(value, float):
        require(math.isfinite(value), 'Nonfinite JSON number')
    elif isinstance(value, dict):
        for item in value.values():
            _finite(item)
    elif isinstance(value, list):
        for item in value:
            _finite(item)


def _public_values(value):
    """Inspect decoded strings: JSON escaping must not conceal private locators."""
    if isinstance(value, str):
        check_public_text(value)
    elif isinstance(value, dict):
        for key, item in value.items():
            check_public_text(key)
            _public_values(item)
    elif isinstance(value, list):
        for item in value:
            _public_values(item)


def read_json(path):
    value = _legacy.read_json(path)
    _finite(value)  # JSON's 1e999 also overflows; parse_constant alone is insufficient.
    return value


def string_list(value, *, empty=True):
    require(isinstance(value, list), 'Expected string list')
    require(empty or bool(value), 'Empty required collection')
    for item in value:
        nonempty(item)
    require(len(value) == len(set(value)), 'Duplicate collection member')
    return value


def integer(value, minimum=0):
    require(type(value) is int and value >= minimum, 'Invalid integer or exit code')
    return value


def refs(values, owners, label, *, empty=True):
    string_list(values, empty=empty)
    require(set(values) <= set(owners), 'Unknown ' + label + ' reference')


def file_ref(row, root):
    keys(row, {'path', 'sha256'})
    path = path_in(root, row['path'])
    require(sha(path) == digest(row['sha256']), 'Changed referenced file hash: ' + row['path'])
    return path


def _documents(bundle):
    return {
        'BASELINE_BINDING': bundle['baseline_binding'], 'PRESERVATION': bundle['preservation'],
        'SOURCE_MAP': {'sources': bundle['sources'], 'reviews': bundle['reviews']},
        'RESULT_STATUS': {'results': bundle['results'], 'statuses': bundle['statuses']},
        'EVIDENCE_BINDINGS': {'bindings': bundle['bindings'], 'receipts': bundle['receipts']},
        'SUPERSESSION': {'edges': bundle['supersession'], 'selectors': bundle['selectors'],
                        'legacy_endpoints': bundle['legacy_endpoints']},
        'OBLIGATION_CROSSWALK': {'obligations': bundle['obligations']},
        'TWELVE_AVENUES': {'avenues': bundle['avenues']},
        'CALCULUS_MAP': {'results': bundle['calculus']},
        'EMPIRICAL_SCOPE': {'results': bundle['empirical']},
        'PUBLIC_PROJECTION': {'reviews': bundle['projection_reviews'], 'allowlist': bundle['public_allowlist']},
        **bundle['supplementary'],
    }


def _record_files(bundle, root):
    registry = bundle['registry']
    keys(registry, {'schema', 'programme', 'cutoff', 'baseline_commit', 'baseline_tree',
                    'records', 'suite_ids', 'result_ids'})
    require(registry['schema'] == 'orthemology-v5-successors-v1', 'Unknown registry schema')
    require(registry['programme'] == 'Orthemology v5' and registry['cutoff'] == 'fifteenth-final',
            'Wrong programme or cutoff')
    require(isinstance(bundle['supplementary'], dict)
            and set(bundle['supplementary']) <= SUPPLEMENTARY, 'Unknown supplementary record')
    documents = _documents(bundle)
    for suite in bundle['suites']:
        sid = nonempty(suite.get('id'))
        require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', sid), 'Unsafe suite ID')
        documents['suite:' + sid] = suite
    require(isinstance(registry['records'], dict) and set(registry['records']) == set(documents),
            'Missing or unknown indexed record')
    for name, value in documents.items():
        ref = registry['records'][name]
        expected = (AREA + '/suites/' + name[6:] + '.json') if name.startswith('suite:') else PROV + '/' + name + '.json'
        require(isinstance(ref, dict) and ref.get('path') == expected, 'Wrong record owner path')
        path = file_ref(ref, root)
        require(read_json(path) == value, 'Bundle/record mismatch: ' + name)
    for field, rows in [('suite_ids', bundle['suites']), ('result_ids', bundle['results'])]:
        string_list(registry[field])
        require(set(registry[field]) == set(indexed(rows, 'id')), 'Incomplete registry ' + field)


def _git(root, *args):
    try:
        process = subprocess.run(['git', '-C', str(root), *args], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, check=False, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError('Baseline Git objects unavailable') from error
    require(process.returncode == 0, 'Baseline Git object verification failed')
    return process.stdout


def _inventory_paths(root, roots):
    found = set()
    for name in roots:
        safe_relative(name)
        folder = root / name
        require(folder.is_dir() and not folder.is_symlink(), 'Missing Frozen preservation root')
        for path in folder.rglob('*'):
            require(not path.is_symlink(), 'Frozen preservation symlink')
            if path.is_file():
                found.add(path.relative_to(root).as_posix())
    return found


def _preservation(bundle, root, anchor):
    bound, inventory = bundle['baseline_binding'], bundle['preservation']
    keys(bound, {'schema', 'base_commit', 'base_tree', 'preservation_sha256', 'legacy_registry', 'legacy_overlay'})
    require(bound['schema'] == 'orthemology-v5-baseline-binding-v1', 'Unknown baseline schema')
    for name in ['base_commit', 'base_tree', 'preservation_sha256', 'legacy_registry', 'legacy_overlay']:
        require(bound[name] == anchor[name], 'Changed baseline trust anchor: ' + name)
    require(bundle['registry']['records']['PRESERVATION']['sha256'] == bound['preservation_sha256'],
            'Changed preservation inventory binding')
    require(bundle['registry']['baseline_commit'] == bound['base_commit']
            and bundle['registry']['baseline_tree'] == bound['base_tree'], 'Registry baseline mismatch')
    keys(inventory, {'schema', 'base_commit', 'base_tree', 'roots', 'files'})
    require(inventory['schema'] == 'orthemology-v5-preservation-v1', 'Unknown preservation schema')
    require(inventory['base_commit'] == bound['base_commit'] and inventory['base_tree'] == bound['base_tree'],
            'Changed preservation baseline')
    require(inventory['roots'] == FROZEN_ROOTS, 'Changed preservation roots')
    files = indexed(inventory['files'], 'path')
    require(files and set(files) == _inventory_paths(root, FROZEN_ROOTS), 'Frozen preservation file-set changed')
    for name, row in files.items():
        keys(row, {'path', 'bytes', 'sha256', 'git_blob_sha1'})
        integer(row['bytes']); digest(row['sha256'])
        require(re.fullmatch('[0-9a-f]{40}', row['git_blob_sha1']), 'Invalid baseline Git blob identity')
        path = path_in(root, name)
        raw = path.read_bytes()
        require(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
                'Frozen preservation bytes changed: ' + name)
        require(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == row['git_blob_sha1'],
                'Frozen preservation Git blob mismatch')
    for field in ['legacy_registry', 'legacy_overlay']:
        ref = bound[field]
        require(ref['path'] in files and ref['sha256'] == files[ref['path']]['sha256'],
                'Legacy baseline binding missing from preservation')
    if anchor['git_required']:
        actual_tree = _git(root, 'rev-parse', bound['base_commit'] + '^{tree}').decode().strip()
        require(actual_tree == bound['base_tree'], 'Pinned baseline tree mismatch')
        output = _git(root, 'ls-tree', '-rz', '--full-tree', bound['base_commit'], '--', *FROZEN_ROOTS)
        actual = {}
        for record in output.split(b'\0'):
            if record:
                metadata, name = record.split(b'\t', 1)
                mode, kind, blob = metadata.decode().split()
                require(kind == 'blob' and mode in {'100644', '100755'}, 'Unsupported frozen Git object')
                actual[name.decode('utf-8')] = blob
        require(actual == {name: row['git_blob_sha1'] for name, row in files.items()},
                'Preservation inventory does not match pinned Git objects')
    return files


def _sources(bundle, root):
    sources = indexed(bundle['sources'], 'id')
    reviews = indexed(bundle['reviews'], 'id')
    projections = indexed(bundle['projection_reviews'], 'id')
    for row in projections.values():
        keys(row, {'id', 'source_id', 'original_sha256', 'public_sha256', 'diff_sha256',
                   'scope', 'outcome', 'reviewer_kind'})
        require(row['source_id'] in sources, 'Unknown projection source')
        for field in ['original_sha256', 'public_sha256', 'diff_sha256']:
            digest(row[field])
        nonempty(row['scope'])
        enum(row['outcome'], {'CONTENT_REVIEWED', 'PENDING'})
        enum(row['reviewer_kind'], {'INTEGRATOR_CONTENT_REVIEW', 'INDEPENDENT_CONTENT_REVIEW'})
    for row in sources.values():
        keys(row, {'id', 'origin_input_id', 'origin_input_sha256', 'origin_archive_sha256', 'member_chain',
                   'original_sha256', 'original_bytes', 'public_path', 'public_sha256', 'public_bytes',
                   'projection', 'projection_basis', 'review_scope', 'derivation'})
        for field in ['origin_input_id', 'projection_basis', 'review_scope']:
            nonempty(row[field])
        for field in ['origin_input_sha256', 'original_sha256']:
            digest(row[field])
        integer(row['original_bytes'])
        string_list(row['member_chain'])
        for name in row['member_chain']:
            safe_relative(name)
        if row['member_chain']:
            digest(row['origin_archive_sha256'])
        else:
            require(row['origin_archive_sha256'] is None
                    and row['original_sha256'] == row['origin_input_sha256'], 'Direct input/archive identity mismatch')
        enum(row['projection'], {'EXACT', 'DERIVED', 'CUSTODY_ONLY'})
        if row['projection'] == 'CUSTODY_ONLY':
            require(all(row[k] is None for k in ['public_path', 'public_sha256', 'public_bytes', 'derivation']),
                    'CUSTODY_ONLY source has public payload')
            continue
        digest(row['public_sha256']); integer(row['public_bytes'])
        path = path_in(root, row['public_path'])
        prefix = AREA + '/source-store/' + row['public_sha256'] + '/'
        require(row['public_path'].startswith(prefix), 'Wrong public source content-addressed path')
        raw = path.read_bytes()
        require(len(raw) == row['public_bytes'] and hashlib.sha256(raw).hexdigest() == row['public_sha256'],
                'Changed public source hash or bytes')
        require(path.suffix.lower() not in {'.zip', '.7z', '.tar', '.gz'}, 'Private archive payload is not public source')
        try:
            check_public_text(raw.decode('utf-8'))
        except UnicodeDecodeError:
            raise ValueError('Public source must have a reviewed UTF-8 projection') from None
        if path.suffix.lower() == '.json':
            _public_values(read_json(path))
        if row['projection'] == 'EXACT':
            require(row['original_sha256'] == row['public_sha256'] and row['original_bytes'] == row['public_bytes']
                    and row['derivation'] is None, 'EXACT projection differs from original')
        else:
            derivation = row['derivation']
            require(isinstance(derivation, dict), 'Missing DERIVED derivation and review')
            keys(derivation, {'diff_path', 'diff_sha256', 'review_id', 'preserved_scope'})
            digest(derivation['diff_sha256']); nonempty(derivation['preserved_scope'])
            if derivation['diff_path'] is not None:
                diff_path = path_in(root, derivation['diff_path'])
                require(sha(diff_path) == derivation['diff_sha256'], 'Changed DERIVED diff')
                check_public_text(diff_path.read_text(encoding='utf-8'))
            require(derivation['review_id'] in projections, 'Missing DERIVED projection review')
            review = projections[derivation['review_id']]
            require(review['source_id'] == row['id'] and review['original_sha256'] == row['original_sha256']
                    and review['public_sha256'] == row['public_sha256']
                    and review['diff_sha256'] == derivation['diff_sha256']
                    and review['outcome'] == 'CONTENT_REVIEWED', 'DERIVED projection review mismatch or pending')
    for row in reviews.values():
        keys(row, {'id', 'source_id', 'reviewed_source_ids', 'target', 'scope', 'outcome', 'review_sha256'})
        require(row['source_id'] in sources, 'Missing review source')
        refs(row['reviewed_source_ids'], sources, 'reviewed source', empty=False)
        nonempty(row['target']); nonempty(row['scope'])
        enum(row['outcome'], {'REVIEWED_AT_SCOPE', 'LIMITED', 'STOPPED', 'UNREVIEWED'})
        source = sources[row['source_id']]
        require(digest(row['review_sha256']) == (source['public_sha256'] or source['original_sha256']),
                'Changed review document hash')
    return sources, reviews, projections


def _allowlist(bundle, root, sources):
    rows = indexed(bundle['public_allowlist'], 'path')
    for name, row in rows.items():
        keys(row, {'path', 'sha256', 'bytes', 'kind', 'source_ids'})
        enum(row['kind'], {'SOURCE', 'AUTHORED', 'METADATA', 'VALIDATOR', 'TEST'})
        refs(row['source_ids'], sources, 'allowlist source')
        path = path_in(root, name)
        require(sha(path) == digest(row['sha256']) and path.stat().st_size == integer(row['bytes']),
                'Changed public allowlist payload')
        if row['kind'] == 'SOURCE':
            require(bool(row['source_ids']), 'Source allowlist row has no source identity')
            require(all(sources[sid]['public_path'] == name and sources[sid]['public_sha256'] == row['sha256']
                        for sid in row['source_ids']), 'Allowlist source association mismatch')
        if path.suffix.lower() in {'.md', '.json', '.py', '.lean', '.tex', '.txt', '.yaml', '.yml', '.tsv', '.csv'}:
            check_public_text(path.read_text(encoding='utf-8'))
    present = set()
    for relative in [AREA + '/source-store', AREA + '/groups']:
        folder = root / relative
        if folder.exists():
            require(not folder.is_symlink(), 'Public allowlist symlink')
            for path in folder.rglob('*'):
                require(not path.is_symlink(), 'Public allowlist symlink')
                if path.is_file():
                    present.add(path.relative_to(root).as_posix())
    covered = {name for name in rows if any(name.startswith(AREA + '/' + part + '/') for part in ['source-store', 'groups'])}
    require(present == covered, 'Public allowlist inventory is incomplete')
    for source in sources.values():
        if source['public_path'] is not None:
            require(source['public_path'] in rows and source['id'] in rows[source['public_path']]['source_ids'],
                    'Source missing from public allowlist')


def _toolchain(row):
    keys(row, {'kind', 'version', 'platform', 'executable_sha256', 'packages'})
    enum(row['kind'], {'LEAN', 'PYTHON', 'REFERENCE'})
    nonempty(row['version']); nonempty(row['platform']); digest(row['executable_sha256'])
    if row['kind'] == 'LEAN':
        require(row['version'] == '4.19.0', 'Wrong Lean toolchain version')
        if row['platform'] == 'linux-x86_64':
            require(row['executable_sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023',
                    'Wrong official Linux Lean toolchain hash')
    elif row['kind'] == 'PYTHON':
        require(row['version'] == '3.11.9' or re.fullmatch(r'3\.12\.[0-9]+', row['version']),
                'Unsupported source-prescribed Python version')
    for package in indexed(row['packages'], 'name').values():
        keys(package, {'name', 'revision', 'sha256'})
        nonempty(package['revision'])
        require(package['sha256'] == canonical_json_digest({k: package[k] for k in ['name', 'revision']}),
                'Changed package toolchain identity')


def _suite(suite, sources, reviews, root, validator):
    keys(suite, {'id', 'family', 'result_families', 'origin_archive_sha256', 'source_ids', 'review_ids',
                 'targets', 'controls', 'toolchain', 'replay'})
    nonempty(suite['family']); string_list(suite['result_families'], empty=False)
    digest(suite['origin_archive_sha256'])
    refs(suite['source_ids'], sources, 'suite source', empty=False)
    refs(suite['review_ids'], reviews, 'suite review', empty=False)
    require(all(sources[sid]['public_path'] is not None for sid in suite['source_ids']),
            'Suite cannot execute custody-only source')
    targets = indexed(suite['targets'], 'id')
    require(bool(targets), 'Suite has no targets')
    for row in targets.values():
        keys(row, {'id', 'source_id', 'declaration', 'target_sha256', 'domain', 'calculus'})
        require(row['source_id'] in suite['source_ids'], 'Suite target source mismatch')
        enum(row['domain'], DOMAINS); enum(row['calculus'], CALCULI)
        require(row['target_sha256'] == text_digest(row['declaration']), 'Changed expected target hash')
        text = path_in(root, sources[row['source_id']]['public_path']).read_text(encoding='utf-8')
        require(row['declaration'] in text, 'Suite target declaration missing from source')
    for row in indexed(suite['controls'], 'id').values():
        keys(row, {'id', 'source_id', 'target_id', 'role', 'expected_outcome', 'expected_outcome_sha256'})
        require(row['source_id'] in suite['source_ids'] and row['target_id'] in targets,
                'Suite control source/target mismatch')
        enum(row['expected_outcome'], {'ACCEPT', 'REJECT'})
        enum(row['role'], {'POSITIVE', 'MUTATION_REJECTION', 'COUNTEREXAMPLE_PROOF'})
        require(row['expected_outcome'] == ('REJECT' if row['role'] == 'MUTATION_REJECTION' else 'ACCEPT'),
                'Control role/expected outcome mismatch')
        require(row['expected_outcome_sha256'] == text_digest(row['expected_outcome']),
                'Changed expected control outcome hash')
    _toolchain(suite['toolchain'])
    require(callable(validator), 'Missing required replay suite validator')
    validator(suite, sources, root)


def _terminal(row):
    enum(row['terminal'], TERMINALS)
    digest(row['log_sha256'])
    if row['terminal'] == 'COMPLETED':
        integer(row['exit_code'])
    else:
        require(row['exit_code'] is None, 'Noncompleted terminal has a concrete exit code')


def _receipt(receipt, suite, sources, reviews, root, validator):
    keys(receipt, {'id', 'suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes',
                   'toolchain_sha256', 'outcome', 'target_readbacks', 'controls', 'stages', 'invocation',
                   'started_at', 'ended_at', 'exit_code', 'log_sha256', 'axioms', 'proof_scope', 'replay_evidence'})
    require(receipt['suite_id'] == suite['id'] and receipt['family'] == suite['family'], 'Foreign receipt family/suite')
    require(receipt['suite_sha256'] == canonical_json_digest(suite), 'Stale receipt suite digest')
    require(receipt['source_hashes'] == {sid: sources[sid]['public_sha256'] for sid in suite['source_ids']},
            'Receipt source closure mismatch')
    require(receipt['review_hashes'] == {rid: reviews[rid]['review_sha256'] for rid in suite['review_ids']},
            'Receipt review closure mismatch')
    require(receipt['toolchain_sha256'] == canonical_json_digest(suite['toolchain']), 'Receipt toolchain mismatch')
    enum(receipt['outcome'], FRESH)
    enum(receipt['proof_scope'], {'NONE', 'FINITE', 'COMPONENTS', 'DECLARED_SUITE'})
    string_list(receipt['axioms']); require(set(receipt['axioms']) <= AXIOMS, 'Unapproved receipt axiom')
    require(isinstance(receipt['invocation'], list) and receipt['invocation'], 'Missing explicit invocation')
    for argument in receipt['invocation']:
        nonempty(argument)
    digest(receipt['log_sha256'])
    times = []
    for field in ['started_at', 'ended_at']:
        nonempty(receipt[field]); require(receipt[field].endswith('Z'), 'Receipt timestamp is not UTC')
        times.append(datetime.fromisoformat(receipt[field][:-1] + '+00:00'))
    require(times[0] <= times[1], 'Reversed receipt timestamps')
    if receipt['exit_code'] is not None:
        integer(receipt['exit_code'])
    stages = indexed(receipt['stages'], 'id')
    require(bool(stages), 'Missing executed-stage ledger')
    for row in stages.values():
        keys(row, {'id', 'terminal', 'exit_code', 'log_sha256'}); _terminal(row)
    targets = indexed(suite['targets'], 'id')
    readbacks = indexed(receipt['target_readbacks'], 'target_id')
    require(set(readbacks) <= set(targets), 'Foreign target readback')
    for name, row in readbacks.items():
        keys(row, {'target_id', 'source_id', 'target_sha256', 'outcome'})
        expected = targets[name]
        require(row['source_id'] == expected['source_id'] and row['target_sha256'] == expected['target_sha256'],
                'Changed source-bound target readback')
        enum(row['outcome'], {'CHECKED', 'NOT_CHECKED'})
    controls = indexed(suite['controls'], 'id')
    outcomes = indexed(receipt['controls'], 'id')
    require(set(outcomes) <= set(controls), 'Foreign receipt control')
    for name, row in outcomes.items():
        keys(row, {'id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256', 'actual_outcome',
                   'actual_outcome_sha256', 'terminal', 'exit_code', 'log_sha256'})
        expected = controls[name]
        require(all(row[key] == expected[key] for key in ['source_id', 'target_id', 'role', 'expected_outcome_sha256']),
                'Receipt control source/target/role/expected outcome mismatch')
        enum(row['actual_outcome'], {'ACCEPT', 'REJECT', 'UNKNOWN'})
        require(row['actual_outcome_sha256'] == text_digest(row['actual_outcome']), 'Changed control actual outcome hash')
        _terminal(row)
        if row['actual_outcome'] == 'REJECT':
            require(row['terminal'] == 'COMPLETED' and type(row['exit_code']) is int
                    and 0 < row['exit_code'] < 124, 'Receipt control rejection lacks concrete semantic terminal exit')
        elif row['actual_outcome'] == 'ACCEPT':
            require(row['terminal'] == 'COMPLETED' and row['exit_code'] == 0, 'Control acceptance lacks successful exit')
        elif row['terminal'] != 'COMPLETED':
            require(row['actual_outcome'] == 'UNKNOWN', 'Noncompleted control cannot earn semantic credit')
    qualified = receipt['outcome'] == 'QUALIFIED_DECLARED_SUITE'
    successful = receipt['outcome'] in {'FINITE_ONLY', 'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}
    if successful:
        require(receipt['exit_code'] == 0 and type(receipt['exit_code']) is int,
                'Successful receipt lacks zero terminal exit')
        require(all(s['terminal'] == 'COMPLETED' and type(s['exit_code']) is int
                    and 0 <= s['exit_code'] < 124 for s in stages.values()),
                'Successful receipt has incomplete/resource-failed stages')
        # Source-prescribed rejection stages retain their real nonzero exits.
        # D03 binds each exact code, diagnostic and prerequisite to its descriptor.
    if qualified:
        require(receipt['proof_scope'] == 'DECLARED_SUITE', 'Qualified receipt has component-only proof scope')
        require(set(readbacks) == set(targets) and all(r['outcome'] == 'CHECKED' for r in readbacks.values()),
                'Incomplete qualified target coverage')
        roles = {c['role'] for c in controls.values()}
        require(set(outcomes) == set(controls) and 'POSITIVE' in roles
                and bool(roles & {'MUTATION_REJECTION', 'COUNTEREXAMPLE_PROOF'}),
                'Missing qualified positive/negative control')
        require(all(outcomes[name]['actual_outcome'] == expected['expected_outcome']
                    and outcomes[name]['terminal'] == 'COMPLETED' for name, expected in controls.items()),
                'Qualified control outcome is missing or wrong')
        require(all(readbacks[c['target_id']]['outcome'] == 'CHECKED' for c in controls.values()
                    if c['role'] == 'COUNTEREXAMPLE_PROOF'), 'Counterexample control lacks exact checked target')
    elif receipt['outcome'] == 'FRESH_KERNEL_COMPONENTS':
        require(receipt['proof_scope'] == 'COMPONENTS' and any(r['outcome'] == 'CHECKED' for r in readbacks.values()),
                'Kernel components need exact checked target readbacks')
    elif receipt['outcome'] == 'FINITE_ONLY':
        require(receipt['proof_scope'] == 'FINITE', 'Finite receipt has wrong proof scope')
    require(callable(validator), 'Missing required replay receipt validator')
    validator(receipt, suite, sources, root)


def _results(bundle, sources, reviews, projections, suites, receipts):
    results = indexed(bundle['results'], 'id')
    require(bool(results), 'No successor results')
    statuses = indexed(bundle['statuses'], 'id')
    bindings = indexed(bundle['bindings'], 'id')
    require(set(statuses) == set(results), 'Incomplete result status ledger')
    require(set(bindings) == set(results), 'Incomplete evidence binding ledger')
    for rid, row in results.items():
        keys(row, {'id', 'title', 'tranche', 'family', 'original_avenues', 'evidence_keys', 'target', 'input_contract',
                   'assumptions', 'conclusion', 'limitations', 'calculus', 'operational_model', 'math_form',
                   'claim_scope', 'domain', 'source_ids', 'review_ids', 'suite_ids', 'origin_status',
                   'obligation_ids', 'residual_scope'})
        for field in ['title', 'family', 'target', 'input_contract', 'conclusion', 'operational_model',
                      'origin_status', 'residual_scope']:
            nonempty(row[field])
        require(type(row['tranche']) is int and 7 <= row['tranche'] <= 15, 'Out-of-scope tranche')
        require(isinstance(row['original_avenues'], list) and len(row['original_avenues']) == len(set(row['original_avenues']))
                and all(type(n) is int and 1 <= n <= 12 for n in row['original_avenues']), 'Invalid original avenue')
        string_list(row['assumptions']); string_list(row['limitations'], empty=False)
        string_list(row['evidence_keys']); string_list(row['obligation_ids'])
        enum(row['calculus'], CALCULI); enum(row['math_form'], FORMS); enum(row['domain'], DOMAINS)
        enum(row['claim_scope'], {'COMPONENT', 'DECLARED_SUITE', 'WHOLE_RESULT'})
        refs(row['source_ids'], sources, 'result source', empty=False)
        refs(row['review_ids'], reviews, 'result review', empty=False)
        refs(row['suite_ids'], suites, 'result suite')
        coverage = set()
        for review_id in row['review_ids']:
            review = reviews[review_id]
            require(review['target'] == row['target'], 'Result review target mismatch')
            coverage.update(review['reviewed_source_ids'])
        require(set(row['source_ids']) <= coverage, 'Result review coverage is incomplete')
        status = statuses[rid]
        keys(status, {'id', 'custody', 'inherited_evidence', 'fresh_evidence', 'research_disposition',
                      'implementation_reach', 'external_warrants', 'receipt_ids', 'independent_evidence_count'})
        custody = {sources[sid]['projection'] for sid in row['source_ids']}
        require(status['custody'] == (next(iter(custody)) if len(custody) == 1 else 'MIXED'), 'Result custody mismatch')
        enum(status['inherited_evidence'], INHERITED); enum(status['fresh_evidence'], FRESH)
        enum(status['research_disposition'], {'CANDIDATE', 'DEFERRED', 'REJECTED', 'HISTORICAL'})
        enum(status['implementation_reach'], REACH)
        keys(status['external_warrants'], WARRANTS)
        for value in status['external_warrants'].values():
            enum(value, {'NOT_ESTABLISHED', 'OUT_OF_SCOPE'})
        refs(status['receipt_ids'], receipts, 'result receipt')
        require(integer(status['independent_evidence_count']) <= len({sources[sid]['original_sha256'] for sid in row['source_ids']}),
                'Copied source cannot count as independent evidence')
        fresh = status['fresh_evidence']
        kernel = fresh in {'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}
        inherited_kernel = status['inherited_evidence'] in {'KERNEL_COMPONENTS', 'KERNEL_DECLARED_SUITE'}
        if kernel or inherited_kernel:
            require(row['math_form'] in {'FORMAL', 'MIXED'}, 'Written result cannot acquire whole kernel/formal status')
            if row['math_form'] == 'MIXED':
                require(row['claim_scope'] == 'COMPONENT' and fresh != 'QUALIFIED_DECLARED_SUITE'
                        and status['inherited_evidence'] != 'KERNEL_DECLARED_SUITE', 'Mixed written result requires component kernel scope')
        if fresh == 'FINITE_ONLY':
            require(status['implementation_reach'] in {'NONE', 'FINITE_WITNESS', 'REFERENCE_ONLY', 'RESTRICTED_CHECKER'},
                    'Finite evidence cannot confer general formal implementation reach')
        if fresh == 'NOT_RUN':
            require(not status['receipt_ids'], 'NOT_RUN has fresh receipts')
        if fresh in {'FINITE_ONLY', 'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}:
            require(status['receipt_ids'] and 'CUSTODY_ONLY' not in custody, 'Fresh evidence missing public sources or receipts')
            require(all(reviews[rid]['outcome'] in {'REVIEWED_AT_SCOPE', 'LIMITED'} for rid in row['review_ids']),
                    'Stopped/unreviewed scientific scope cannot receive fresh qualified review credit')
        binding = bindings[rid]
        keys(binding, {'id', 'statement_sha256', 'sources', 'reviews', 'suite_targets', 'receipt_ids', 'receipts'})
        require(binding['statement_sha256'] == canonical_json_digest(row), 'Changed result statement binding')
        expected_sources = {}
        for sid in row['source_ids']:
            source = sources[sid]
            review_digest = (canonical_json_digest(projections[source['derivation']['review_id']])
                             if source['projection'] == 'DERIVED' else None)
            expected_sources[sid] = {'original_sha256': source['original_sha256'], 'public_sha256': source['public_sha256'],
                                     'projection_review_sha256': review_digest}
        require(binding['sources'] == expected_sources, 'Changed result source association binding')
        require(binding['reviews'] == {review_id: reviews[review_id]['review_sha256'] for review_id in row['review_ids']},
                'Changed result review binding')
        require(binding['receipt_ids'] == status['receipt_ids'] and binding['receipts'] ==
                {name: canonical_json_digest(receipts[name]) for name in status['receipt_ids']},
                'Changed complete receipt binding digest')
        target_bindings = indexed(binding['suite_targets'], 'suite_id')
        require(set(target_bindings) == set(row['suite_ids']), 'Result suite target coverage mismatch')
        for sid, bound in target_bindings.items():
            keys(bound, {'suite_id', 'target_ids'})
            suite = suites[sid]
            require(row['family'] in suite['result_families'], 'Result suite family mismatch')
            targets = indexed(suite['targets'], 'id')
            refs(bound['target_ids'], targets, 'bound target', empty=False)
            expected = {name for name, target in targets.items() if target['source_id'] in row['source_ids']
                        and target['calculus'] == row['calculus'] and target['domain'] == row['domain']}
            require(set(bound['target_ids']) == expected and bool(expected), 'Result target source/domain/calculus mismatch')
        own_receipts = [receipts[name] for name in status['receipt_ids']]
        require(all(rec['suite_id'] in row['suite_ids'] for rec in own_receipts), 'Cross-family receipt outside result suites')
        if fresh == 'QUALIFIED_DECLARED_SUITE':
            require(set(rec['suite_id'] for rec in own_receipts) == set(row['suite_ids']) and row['suite_ids']
                    and all(rec['outcome'] == fresh for rec in own_receipts), 'Incomplete declared suite qualification')
        elif fresh == 'FRESH_KERNEL_COMPONENTS':
            require(any(rec['outcome'] in {'FRESH_KERNEL_COMPONENTS', 'QUALIFIED_DECLARED_SUITE'}
                        for rec in own_receipts), 'Fresh evidence does not match receipt outcome')
        elif fresh == 'FINITE_ONLY':
            require(any(rec['outcome'] == fresh for rec in own_receipts), 'Fresh evidence does not match receipt outcome')
        if fresh in {'BLOCKED_EXTERNAL_INPUT', 'BLOCKED_TOOLCHAIN', 'RESOURCE_INCONCLUSIVE', 'FAILED'} and own_receipts:
            require(any(rec['outcome'] == fresh for rec in own_receipts), 'Failure/block disposition lacks matching receipt')
    return results, statuses


def _pointer(value, pointer):
    require(isinstance(pointer, str) and (pointer == '' or pointer.startswith('/')), 'Invalid legacy JSON pointer')
    if pointer:
        for encoded in pointer[1:].split('/'):
            require(not re.search(r'~(?![01])', encoded), 'Invalid legacy JSON pointer escape')
            name = encoded.replace('~1', '/').replace('~0', '~')
            if isinstance(value, list):
                require(re.fullmatch(r'0|[1-9][0-9]*', name), 'Invalid legacy list pointer')
                require(int(name) < len(value), 'Missing legacy list member')
                value = value[int(name)]
            else:
                require(isinstance(value, dict) and name in value, 'Missing legacy JSON pointer')
                value = value[name]
    return value


def _graph(bundle, root, results, statuses, sources, preserved):
    legacy = indexed(bundle['legacy_endpoints'], 'id')
    require(not (set(legacy) & set(results)), 'Legacy endpoint shadows new result')
    for row in legacy.values():
        keys(row, {'id', 'owner_path', 'owner_sha256', 'json_pointer', 'statement', 'target', 'domain', 'calculus'})
        require(row['owner_path'] in preserved and row['owner_sha256'] == preserved[row['owner_path']]['sha256'],
                'Legacy endpoint owner is not preserved baseline')
        value = _pointer(read_json(path_in(root, row['owner_path'])), row['json_pointer'])
        literal = value if isinstance(value, str) else json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        require(row['statement'] == literal, 'Legacy endpoint statement changed')
        nonempty(row['target']); enum(row['domain'], DOMAINS); enum(row['calculus'], CALCULI)
    endpoints = {**legacy, **results}
    edges = bundle['supersession']
    require(isinstance(edges, list), 'Expected supersession edges')
    seen, adjacency, superseded = set(), {key: [] for key in endpoints}, set()
    for row in edges:
        keys(row, {'from', 'to', 'relation', 'target', 'basis_source_ids', 'retained_scope'})
        require(row['from'] in endpoints and row['to'] in endpoints, 'Missing supersession endpoint')
        enum(row['relation'], {'REFINES', 'CORRECTS', 'SUPERSEDES'})
        nonempty(row['retained_scope']); refs(row['basis_source_ids'], sources, 'supersession evidence', empty=False)
        signature = (row['from'], row['to'], row['relation'])
        require(signature not in seen, 'Duplicate supersession edge'); seen.add(signature)
        left, right = endpoints[row['from']], endpoints[row['to']]
        require(left['target'] == right['target'] == row['target']
                and left['domain'] == right['domain'] and left['calculus'] == right['calculus'],
                'Supersession target/domain/calculus expansion')
        adjacency[row['from']].append(row['to'])
        if row['relation'] in {'CORRECTS', 'SUPERSEDES'}:
            superseded.add(row['from'])
    active, visited = set(), set()
    def visit(node):
        require(node not in active, 'Supersession cycle')
        if node in visited:
            return
        active.add(node)
        for child in adjacency[node]:
            visit(child)
        active.remove(node); visited.add(node)
    for node in endpoints:
        visit(node)
    selectors = indexed(bundle['selectors'], 'family')
    require(set(selectors) == {row['family'] for row in results.values()}, 'Incomplete current selector families')
    for family, row in selectors.items():
        keys(row, {'family', 'result_id', 'statement_sha256'})
        require(row['result_id'] in results, 'Missing current selector result')
        current = results[row['result_id']]
        require(current['family'] == family and row['statement_sha256'] == canonical_json_digest(current),
                'Stale current selector statement/family')
        require(row['result_id'] not in superseded and statuses[row['result_id']]['research_disposition'] != 'HISTORICAL',
                'Stale current selector points to superseded/historical result')


def _ledgers(bundle, root, results, sources, anchor):
    calculus = indexed(bundle['calculus'], 'id')
    require(set(calculus) == set(results), 'Incomplete calculus map')
    for rid, row in calculus.items():
        keys(row, {'id', 'calculus', 'operational_model', 'canonical_adoption'})
        require(row['calculus'] == results[rid]['calculus'] and row['operational_model'] == results[rid]['operational_model'],
                'Changed calculus/operational model association')
        require(row['canonical_adoption'] == 'NOT_ADOPTED', 'Candidate calculus cannot be adopted by source registration')
    for row in indexed(bundle['empirical'], 'id').values():
        keys(row, {'id', 'activity', 'data_scope', 'limitations'})
        require(row['id'] in results, 'Unknown empirical result')
        enum(row['activity'], {'NONE', 'REANALYSIS', 'REFERENCE_COMPUTATION', 'CANDIDATE_SENSE_REVIEW', 'UNRUN_EXPERIMENT'})
        nonempty(row['data_scope']); string_list(row['limitations'], empty=False)
    obligations = indexed(bundle['obligations'], 'id')
    for row in obligations.values():
        keys(row, {'id', 'owner_path', 'owner_sha256', 'statement', 'result_ids', 'disposition', 'residual'})
        path = path_in(root, row['owner_path'])
        require(sha(path) == digest(row['owner_sha256']), 'Changed obligation owner hash')
        require(nonempty(row['statement']) in path.read_text(encoding='utf-8'), 'Obligation statement missing from owner')
        if anchor['git_required']:
            raw = _git(root, 'show', anchor['base_commit'] + ':' + row['owner_path'])
            require(hashlib.sha256(raw).hexdigest() == row['owner_sha256'], 'Obligation owner differs from accepted base')
        refs(row['result_ids'], results, 'obligation result')
        enum(row['disposition'], {'PRESERVED_OPEN', 'SCOPED_SUCCESSOR', 'PRESERVED_STATUS'})
        nonempty(row['residual'])
    for row in results.values():
        refs(row['obligation_ids'], obligations, 'original obligation')
        require(all(row['id'] in obligations[oid]['result_ids'] for oid in row['obligation_ids']),
                'Missing reciprocal obligation association')
    avenues = bundle['avenues']
    require(isinstance(avenues, list) and len(avenues) == 12, 'Incomplete twelve-avenue map')
    require({row.get('number') for row in avenues} == set(range(1, 13)), 'Wrong avenue identities')
    for row in avenues:
        keys(row, {'number', 'result_ids', 'disposition', 'scope'})
        require(type(row['number']) is int, 'Invalid avenue number')
        refs(row['result_ids'], results, 'avenue result')
        enum(row['disposition'], {'SCOPED_SUCCESSORS', 'NO_NEW_RESULT', 'ADMISSION_STOP'}); nonempty(row['scope'])
        expected = {rid for rid, result in results.items() if row['number'] in result['original_avenues']}
        require(set(row['result_ids']) == expected, 'Avenue/result coverage mismatch')
        if row['disposition'] == 'SCOPED_SUCCESSORS':
            require(bool(expected), 'Empty scoped avenue')
        else:
            require(not expected, 'No-new-result avenue has registered result')
    for document in bundle['supplementary'].values():
        keys(document, {'entries'})
        for row in indexed(document['entries'], 'id').values():
            keys(row, {'id', 'result_ids', 'source_ids', 'disposition', 'scope', 'basis', 'limitations'})
            refs(row['result_ids'], results, 'supplementary result'); refs(row['source_ids'], sources, 'supplementary source')
            for field in ['disposition', 'scope', 'basis']:
                nonempty(row[field])
            string_list(row['limitations'], empty=False)


def _replay_validators(suite_validator, receipt_validator):
    if suite_validator is not None and receipt_validator is not None:
        return suite_validator, receipt_validator
    path = Path(__file__).with_name('replay_v5_successors.py')
    if not path.is_file():
        return suite_validator, receipt_validator
    spec = importlib.util.spec_from_file_location('_v5_successor_replay', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return (suite_validator if suite_validator is not None else getattr(module, 'validate_suite', None),
            receipt_validator if receipt_validator is not None else getattr(module, 'validate_receipt', None))


def validate_bundle(bundle, root, *, baseline_anchor=None, suite_validator=None, receipt_validator=None):
    """Validate a full isolated bundle; explicit anchors/callbacks are test seams."""
    try:
        root = Path(root).resolve()
        keys(bundle, BUNDLE_KEYS)
        _finite(bundle)
        _public_values(bundle)
        _record_files(bundle, root)
        anchor = BASELINE_ANCHOR if baseline_anchor is None else baseline_anchor
        preserved = _preservation(bundle, root, anchor)
        sources, reviews, projections = _sources(bundle, root)
        _allowlist(bundle, root, sources)
        suites = indexed(bundle['suites'], 'id')
        receipts = indexed(bundle['receipts'], 'id')
        if suites:
            suite_validator, receipt_validator = _replay_validators(suite_validator, receipt_validator)
        for suite in suites.values():
            _suite(suite, sources, reviews, root, suite_validator)
        for receipt in receipts.values():
            require(receipt.get('suite_id') in suites, 'Receipt references missing suite')
            _receipt(receipt, suites[receipt['suite_id']], sources, reviews, root, receipt_validator)
        results, statuses = _results(bundle, sources, reviews, projections, suites, receipts)
        _graph(bundle, root, results, statuses, sources, preserved)
        _ledgers(bundle, root, results, sources, anchor)
        return {'results': len(results), 'sources': len(sources), 'suites': len(suites),
                'preserved_files': len(preserved),
                'fresh_qualified_results': sum(row['fresh_evidence'] == 'QUALIFIED_DECLARED_SUITE' for row in statuses.values()),
                'scope': 'INTEGRITY_AND_DECLARED_SCOPE_ONLY'}
    except (KeyError, TypeError, IndexError, AttributeError, OSError, UnicodeError, RecursionError) as error:
        raise ValueError('Malformed or unavailable successor record: ' + str(error)) from error


def load_bundle(root):
    root = Path(root)
    registry = read_json(path_in(root, AREA + '/registry.json'))
    require(isinstance(registry, dict) and isinstance(registry.get('records'), dict), 'Missing registry records')
    docs = {}
    for name, ref in registry['records'].items():
        docs[name] = read_json(file_ref(ref, root))
    mapping = {'sources': ('SOURCE_MAP', 'sources'), 'reviews': ('SOURCE_MAP', 'reviews'),
        'results': ('RESULT_STATUS', 'results'), 'statuses': ('RESULT_STATUS', 'statuses'),
        'bindings': ('EVIDENCE_BINDINGS', 'bindings'), 'receipts': ('EVIDENCE_BINDINGS', 'receipts'),
        'supersession': ('SUPERSESSION', 'edges'), 'legacy_endpoints': ('SUPERSESSION', 'legacy_endpoints'),
        'selectors': ('SUPERSESSION', 'selectors'), 'obligations': ('OBLIGATION_CROSSWALK', 'obligations'),
        'avenues': ('TWELVE_AVENUES', 'avenues'), 'calculus': ('CALCULUS_MAP', 'results'),
        'empirical': ('EMPIRICAL_SCOPE', 'results'), 'projection_reviews': ('PUBLIC_PROJECTION', 'reviews'),
        'public_allowlist': ('PUBLIC_PROJECTION', 'allowlist')}
    try:
        bundle = {key: docs[document][field] for key, (document, field) in mapping.items()}
        bundle.update(registry=registry, baseline_binding=docs['BASELINE_BINDING'], preservation=docs['PRESERVATION'],
                      suites=[docs['suite:' + sid] for sid in registry['suite_ids']],
                      supplementary={name: docs[name] for name in SUPPLEMENTARY if name in docs})
    except (KeyError, TypeError) as error:
        raise ValueError('Missing or malformed linked successor record') from error
    return bundle


def validate(root):
    return validate_bundle(load_bundle(root), root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.root), sort_keys=True))
    except ValueError as error:
        parser.exit(1, 'Successor validation failed: ' + str(error) + '\n')


if __name__ == '__main__':
    main()

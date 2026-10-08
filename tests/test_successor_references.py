"""Successor custody selectors do not waive missing native references."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_repo as repo
import validate_internal_references as refs

PROV = '/'.join(['docs', 'provenance', 'v5-successors'])
AREA = '/'.join(['experiments', 'orthemology-v5-successors', 'source-store'])
MEMBER = 'docs/' + 'original-only.md'


def row(sid, member, content=None):
    digest = hashlib.sha256(content if content is not None else b'private original').hexdigest()
    return {'id': sid, 'origin_input_id': 'INPUT', 'origin_input_sha256': 'a' * 64,
        'origin_archive_sha256': 'b' * 64, 'member_chain': [member],
        'original_sha256': digest, 'original_bytes': len(content if content is not None else b'private original'),
        'public_path': AREA + '/' + digest + '/' + Path(member).name if content is not None else None,
        'public_sha256': digest if content is not None else None,
        'public_bytes': len(content) if content is not None else None,
        'projection': 'EXACT' if content is not None else 'CUSTODY_ONLY',
        'projection_basis': 'Exact synthetic source identity.', 'review_scope': 'Reference fixture only.',
        'derivation': None}


def canonical(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(',', ':')).encode()).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2) + '\n').encode()


class SuccessorReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.content = b'[Original member](original-only.md)\n'
        self.owner = row('owner', ('docs/' + 'reader.md'), self.content)
        self.target = row('target', MEMBER)
        self.source = self.root / self.owner['public_path']
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(self.content)

    def locate(self, target='original-only.md', rows=None, source=None, **kwargs):
        return repo.successor_packet_locator(source or self.source, target,
            rows if rows is not None else [self.owner, self.target], self.root, **kwargs)

    def test_digest_bound_relative_member_is_not_a_native_path_promise(self):
        self.assertTrue(self.locate())
        self.assertTrue(self.locate(MEMBER, from_packet_root=True))
        self.assertFalse(self.locate('missing.md'))
        self.source.write_bytes(self.content + b'changed')
        self.assertFalse(self.locate())

    def test_wrong_archive_ambiguous_identity_and_escape_are_rejected(self):
        changed = copy.deepcopy(self.target); changed['origin_archive_sha256'] = 'c' * 64
        self.assertFalse(self.locate(rows=[self.owner, changed]))
        changed = copy.deepcopy(self.target); changed['original_sha256'] = 'd' * 64
        self.assertFalse(self.locate(rows=[self.owner, self.target, changed]))
        self.assertFalse(self.locate('../../' + MEMBER))
        self.assertFalse(self.locate('/' + MEMBER))
        self.assertTrue(self.locate(rows=[self.owner, self.target, {**self.target, 'id': 'same-bytes-alias'}]))

    def test_native_source_cannot_borrow_a_registered_original_exemption(self):
        native = self.root / 'reader.md'; native.write_bytes(self.content)
        self.assertFalse(self.locate(source=native))
        missing_projected = row('target', MEMBER, b'published original')
        self.assertFalse(self.locate(rows=[self.owner, missing_projected]))

    def test_typed_origin_chain_does_not_hide_a_public_destination(self):
        value = {'sources': [self.target], 'reviews': []}
        found = lambda: [p for p, _ in refs._citation_occurrences(PROV + '/SOURCE_MAP.json', json.dumps(value, indent=2))]
        self.assertNotIn(MEMBER, found())
        value['current_reference'] = MEMBER
        self.assertIn(MEMBER, found())
        del value['current_reference']
        value['sources'][0]['original_bytes'] = True
        self.assertIn(MEMBER, found())

    def test_fragment_metadata_has_same_typed_boundary_only(self):
        doc = {'schema': 'orthemology-v5-successor-fragment-v1', 'cell': 'D15', 'sources': [self.target]}
        paths = lambda source: [p for p, _ in refs._citation_occurrences(source, json.dumps(doc, indent=2))]
        self.assertNotIn(MEMBER, paths(PROV + '/fragments/D15.json'))
        self.assertIn(MEMBER, paths('docs/' + 'ordinary-record.json'))
        doc['cell'] = 'D14'
        self.assertIn(MEMBER, paths(PROV + '/fragments/D15.json'))

    def test_commonmark_angle_url_is_external_but_native_angle_target_still_checked(self):
        external = '[Paper](<https://example.org/docs/paper.md>)'
        self.assertEqual([], list(refs._citation_occurrences(('docs/' + 'reader.md'), external)))
        local = '[Missing](<missing-native.md>)'
        self.assertIn(('docs/' + 'missing-native.md'), [p for p, _ in refs._citation_occurrences(('docs/' + 'reader.md'), local)])

    def test_loader_keeps_successor_and_consolidation_records_separate(self):
        target = self.root / PROV / 'SOURCE_MAP.json'; target.parent.mkdir(parents=True)
        target.write_text(json.dumps({'sources': [self.owner, self.target], 'reviews': []}))
        self.assertEqual([self.owner, self.target], repo.load_successor_source_map(self.root))
        self.assertEqual([], repo.load_source_map(self.root))

    def publish(self, sid, member, value):
        data = encode(value) if isinstance(value, dict) else value
        record = row(sid, member, data)
        path = self.root / record['public_path']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return record

    def occurrences(self, src, document, sources):
        return [name for name, _ in refs._citation_occurrences(src, json.dumps(document, indent=2),
            root=self.root, successor_sources=sources)]

    def suite(self, sources):
        ids = [source['id'] for source in sources]
        replay = {key: [] for key in ['files', 'modules', 'module_order', 'positive_roots', 'audit_roots',
            'negative_roots', 'runtime_roots', 'official_imports', 'target_names', 'packages', 'tools',
            'external_inputs', 'fixtures', 'drivers', 'stages', 'build_roots']}
        replay.update(schema='orthemology-v5-replay-v1', scope='FINITE', package_manifest_source_id=None,
            files=[{'source_id': source['id'], 'path': ('tests/' + 'test_package.py'), 'role': 'DRIVER'} for source in sources])
        return {'id': 'fixture-suite', 'family': 'fixture-family', 'result_families': ['fixture-family'],
            'origin_archive_sha256': 'b' * 64, 'source_ids': ids, 'review_ids': [], 'targets': [], 'controls': [],
            'toolchain': {'kind': 'PYTHON', 'version': '3.12.14', 'platform': 'fixture', 'executable_sha256': 'e' * 64,
                          'packages': []}, 'replay': replay}

    def test_typed_suite_projection_path_binds_existing_public_source(self):
        source = self.publish('tests', 'packet/empirical/tests/test_package.py', b'# source test\n')
        suite = self.suite([source])
        src = AREA.rsplit('/', 1)[0] + '/suites/fixture-suite.json'
        self.assertNotIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [source]))
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(('docs/' + 'ordinary.json'), suite, [source]))
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src.replace('fixture-suite.json', 'foreign-suite.json'), suite, [source]))

    def test_suite_projection_cannot_hide_unknown_field_or_native_field(self):
        source = self.publish('tests', 'packet/empirical/tests/test_package.py', b'# source test\n')
        suite = self.suite([source]); src = AREA.rsplit('/', 1)[0] + '/suites/fixture-suite.json'
        suite['replay']['files'][0]['unreviewed'] = True
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [source]))
        del suite['replay']['files'][0]['unreviewed']
        suite['unrelated_current_reference'] = ('tests/' + 'test_package.py')
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [source]))

    def test_suite_projection_rejects_hash_missing_escape_and_ambiguous_source(self):
        source = self.publish('tests', 'packet/empirical/tests/test_package.py', b'# source test\n')
        suite = self.suite([source]); src = AREA.rsplit('/', 1)[0] + '/suites/fixture-suite.json'
        changed = copy.deepcopy(source); changed['public_sha256'] = 'c' * 64
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [changed]))
        duplicate = copy.deepcopy(source); duplicate['origin_archive_sha256'] = 'c' * 64
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [source, duplicate]))
        suite['replay']['files'][0]['path'] = '../tests/test_package.py'
        with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
            self.occurrences(src, suite, [source])
        suite['replay']['files'][0]['path'] = ('tests/' + 'test_package.py')
        (self.root / source['public_path']).unlink()
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(src, suite, [source]))

    def external_lock(self):
        name = ('docs/' + 'certification-policy.md')
        commit = 'c8b5db593d88311e5a020607dba70ff838ab61c5'
        repository = 'https://github.com/theislampill/fusha'
        return {'format': 'sense-scope-supplemental-source-lock-v1', 'repository': repository,
            'commit': commit, 'tree': 'a5bd2b045bc36c78047b5d3f7e9c2807fbf4153c',
            'scope': 'Synthetic exact external-source identity fixture.',
            'files': [{'path': name, 'blob_sha1': 'd' * 40, 'sha256': 'a' * 64, 'bytes': 123,
                       'url': repository + '/blob/' + commit + '/' + name}]}

    def test_exact_external_lock_path_is_not_a_native_file_promise(self):
        lock = self.external_lock()
        source = self.publish('lock', 'language/sense-source-lock.json', lock)
        self.assertNotIn(('docs/' + 'certification-policy.md'), self.occurrences(source['public_path'], lock, [source]))
        self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(('docs/' + 'ordinary-lock.json'), lock, [source]))

    def test_external_lock_rejects_wrong_repository_commit_url_or_field(self):
        for mutate in [lambda d: d.update(repository='https://github.com/foreign/fusha'),
                       lambda d: d.update(commit='1' * 40),
                       lambda d: d.update(tree='2' * 40),
                       lambda d: d.update(unknown_owner='not an admitted field'),
                       lambda d: d['files'][0].update(url='https://github.com/foreign/fusha/blob/main/docs/certification-policy.md'),
                       lambda d: d['files'][0].update(bytes=True),
                       lambda d: d['files'][0].update(unrecognised=True),
                       lambda d: d['files'].append(copy.deepcopy(d['files'][0]))]:
            with self.subTest(mutate=mutate):
                lock = self.external_lock(); mutate(lock)
                source = self.publish('lock', 'language/sense-source-lock.json', lock)
                self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(source['public_path'], lock, [source]))

    def test_malformed_duplicate_and_nonfinite_json_get_no_selector_exception(self):
        lock = self.external_lock()
        valid = json.dumps(lock, indent=2)
        cases = [valid[:-1], valid.replace('"format":', '"scope":"duplicate", "format":', 1),
                 valid.replace('"bytes": 123', '"bytes": NaN')]
        for content in cases:
            with self.subTest(content=content[:40]):
                source = self.publish('lock', 'language/sense-source-lock.json', content.encode())
                found = [path for path, _ in refs._citation_occurrences(source['public_path'], content,
                    root=self.root, successor_sources=[source])]
                self.assertIn(('docs/' + 'certification-policy.md'), found)

    def test_typed_original_and_external_lock_escapes_fail_explicitly(self):
        malformed = copy.deepcopy(self.target); malformed['member_chain'] = ['../' + MEMBER]
        with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
            self.occurrences(PROV + '/SOURCE_MAP.json', {'sources': [malformed], 'reviews': []}, [])
        lock = self.external_lock()
        lock['files'][0]['path'] = '../docs/certification-policy.md'
        lock['files'][0]['url'] = lock['repository'] + '/blob/' + lock['commit'] + '/' + lock['files'][0]['path']
        source = self.publish('lock', 'language/sense-source-lock.json', lock)
        with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
            self.occurrences(source['public_path'], lock, [source])

    def test_external_lock_requires_original_owner_hash_and_member(self):
        lock = self.external_lock()
        source = self.publish('lock', 'language/sense-source-lock.json', lock)
        changed = copy.deepcopy(source); changed['original_sha256'] = 'e' * 64
        self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(source['public_path'], lock, [changed]))
        changed = copy.deepcopy(source); changed['member_chain'] = ['wrong-owner.json']
        self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(source['public_path'], lock, [changed]))

    def test_external_fixture_path_is_bound_to_its_exact_tree_manifest(self):
        lock = self.external_lock(); source = self.publish('lock', 'language/sense-source-lock.json', lock)
        suite = self.suite([source]); suite['replay']['files'][0].update(path='language/sense-source-lock.json', role='LOCK')
        suite['replay']['external_inputs'] = [{'id': 'fusha-selected', 'source_id': None, 'kind': 'TREE',
            'manifest_source_id': 'lock', 'manifest_key': 'files', 'expected_sha256': None, 'expected_bytes': None, 'role': 'INPUT'}]
        fixture = {'id': 'missing-file', 'input_id': 'fusha-selected', 'operation': 'OMIT', 'path': ('docs/' + 'certification-policy.md')}
        suite['replay']['fixtures'] = [fixture]
        document = {'schema': 'orthemology-v5-successor-fragment-v1', 'cell': 'D17', 'sources': [source], 'suites': [suite]}
        src = PROV + '/fragments/D17.json'
        self.assertNotIn(fixture['path'], self.occurrences(src, document, [source]))
        fixture['input_id'] = 'other-input'
        self.assertIn(fixture['path'], self.occurrences(src, document, [source]))
        fixture['input_id'] = 'fusha-selected'; fixture['operation'] = 'DELETE_NATIVE'
        self.assertIn(fixture['path'], self.occurrences(src, document, [source]))

    def test_external_fixture_cannot_use_wrong_source_or_manifest_key(self):
        lock = self.external_lock(); source = self.publish('lock', 'language/sense-source-lock.json', lock)
        suite = self.suite([source]); suite['replay']['files'][0].update(path='language/sense-source-lock.json', role='LOCK')
        suite['replay']['external_inputs'] = [{'id': 'fusha-selected', 'source_id': None, 'kind': 'TREE',
            'manifest_source_id': 'missing-lock', 'manifest_key': 'files', 'expected_sha256': None, 'expected_bytes': None, 'role': 'INPUT'}]
        suite['replay']['fixtures'] = [{'id': 'missing-file', 'input_id': 'fusha-selected', 'operation': 'OMIT', 'path': ('docs/' + 'certification-policy.md')}]
        src = AREA.rsplit('/', 1)[0] + '/suites/fixture-suite.json'
        self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(src, suite, [source]))
        suite['replay']['external_inputs'][0].update(manifest_source_id='lock', manifest_key='unrelated')
        self.assertIn(('docs/' + 'certification-policy.md'), self.occurrences(src, suite, [source]))

    def test_empirical_binding_uses_exact_original_parent_not_basename(self):
        target = self.publish('tests', 'Outer/empirical/tests/test_package.py', b'# original test\n')
        binding = {'format_version': 1, 'scope': 'Portable software and aggregate verification',
            'runtime': {'python': '3.12.14', 'numpy': '2.3.5', 'scipy': '1.17.0', 'pandas': '2.2.3', 'openpyxl': '3.1.5'},
            'numerical_core_provenance': {'implementation_A_original_sha256': 'a' * 64,
                'implementation_B_original_sha256': 'b' * 64, 'adaptation': 'Synthetic scope.'},
            'synthetic_tests': 'pass', 'aggregate_reference_verification': 'pass', 'source_hash_verification': 'pass',
            'public_files': [{'file': ('tests/' + 'test_package.py'), 'sha256': target['original_sha256'], 'bytes': target['original_bytes']}]}
        owner = self.publish('binding', 'Outer/empirical/BINDING.json', binding)
        self.assertNotIn(('tests/' + 'test_package.py'), self.occurrences(owner['public_path'], binding, [owner, target]))
        foreign = copy.deepcopy(target); foreign['origin_archive_sha256'] = 'c' * 64
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(owner['public_path'], binding, [owner, foreign]))
        foreign = copy.deepcopy(target); foreign['member_chain'] = ['Other/empirical/tests/test_package.py']
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(owner['public_path'], binding, [owner, foreign]))
        (self.root / target['public_path']).unlink()
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(owner['public_path'], binding, [owner, target]))

    def test_empirical_binding_rejects_ambiguous_original_and_bad_hash_field(self):
        target = self.publish('tests', 'Outer/empirical/tests/test_package.py', b'# original test\n')
        binding = {'format_version': 1, 'scope': 'Portable software and aggregate verification',
            'runtime': {'python': '3.12.14', 'numpy': '2.3.5', 'scipy': '1.17.0', 'pandas': '2.2.3', 'openpyxl': '3.1.5'},
            'numerical_core_provenance': {'implementation_A_original_sha256': 'a' * 64,
                'implementation_B_original_sha256': 'b' * 64, 'adaptation': 'Synthetic scope.'},
            'synthetic_tests': 'pass', 'aggregate_reference_verification': 'pass', 'source_hash_verification': 'pass',
            'public_files': [{'file': ('tests/' + 'test_package.py'), 'sha256': target['original_sha256'], 'bytes': target['original_bytes']}]}
        owner = self.publish('binding', 'Outer/empirical/BINDING.json', binding)
        different = self.publish('different-tests', 'Outer/empirical/tests/test_package.py', b'# different source\n')
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(owner['public_path'], binding, [owner, target, different]))
        for change in [{'sha256': 'f' * 64}, {'bytes': True}, {'unexpected': True}]:
            with self.subTest(change=change):
                changed = copy.deepcopy(binding); changed['public_files'][0].update(change)
                changed_owner = self.publish('binding', 'Outer/empirical/BINDING.json', changed)
                self.assertIn(('tests/' + 'test_package.py'), self.occurrences(changed_owner['public_path'], changed, [changed_owner, target]))

    def test_public_source_bytes_and_paths_remain_visible_in_fragment(self):
        source = self.publish('tests', 'packet/empirical/tests/test_package.py', b'# source test\n')
        suite = self.suite([source])
        document = {'schema': 'orthemology-v5-successor-fragment-v1', 'cell': 'D18', 'sources': [source], 'suites': [suite]}
        found = self.occurrences(PROV + '/fragments/D18.json', document, [source])
        self.assertIn(source['public_path'], found)
        self.assertNotIn(('tests/' + 'test_package.py'), found)
        self.assertIn(('tests/' + 'test_package.py'), self.occurrences(PROV + '/fragments/D17.json', document, [source]))

    def test_type_interpretation_does_not_mutate_source_records(self):
        source = self.publish('tests', 'packet/empirical/tests/test_package.py', b'# source test\n')
        sources = [copy.deepcopy(source)]
        suite = self.suite([source])
        document = {'schema': 'orthemology-v5-successor-fragment-v1', 'cell': 'D18', 'sources': [source], 'suites': [suite]}
        self.occurrences(PROV + '/fragments/D18.json', document, sources)
        self.assertEqual(sources, [source])
        self.assertEqual(document['sources'][0]['member_chain'], ['packet/empirical/tests/test_package.py'])

    def test_absent_future_registry_and_group_links_are_still_native(self):
        missing = PROV + '/EVIDENCE_BINDINGS.json'
        text = '[Pending source](../../source-store/' + 'f' * 64 + '/ARTICLE.md)\n[' + missing + '](' + missing + ')'
        found = list(refs._citation_occurrences(AREA.rsplit('/', 1)[0] + '/groups/frontier/README.md', text,
                                             root=self.root, successor_sources=[]))
        self.assertTrue(any('ARTICLE.md' in item[0] for item in found))
        self.assertTrue(any(missing in item[0] for item in found))

    def package_members(self):
        owner = self.publish('package-owner', 'Package/README.md', b'python scripts/' + b'verify.py\n')
        target = self.publish('package-script', 'Package/scripts/verify.py', b'# exact helper\n')
        for record in [owner, target]:
            record['member_chain'].insert(0, 'components/package.zip')
        return owner, target

    def test_packet_root_literal_resolves_exact_leading_package_folder(self):
        owner, target = self.package_members()
        before = copy.deepcopy([owner, target])
        self.assertTrue(self.locate(('scripts/' + 'verify.py'), rows=[owner, target],
            source=self.root / owner['public_path'], from_packet_root=True))
        self.assertEqual([owner, target], before)

    def test_package_member_requires_full_input_archive_chain_and_public_bytes(self):
        owner, target = self.package_members()
        changes = [{'origin_input_id': 'FOREIGN'}, {'origin_input_sha256': 'f' * 64},
                   {'origin_archive_sha256': 'c' * 64}, {'member_chain': ['other.zip', 'Package/scripts/verify.py']},
                   {'member_chain': ['components/package.zip', 'Other/scripts/verify.py']},
                   {'original_sha256': 'd' * 64}, {'unexpected': True}]
        for change in changes:
            with self.subTest(change=change):
                changed = {**target, **change}
                self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[owner, changed],
                    source=self.root / owner['public_path'], from_packet_root=True))
        custody = row('custody', 'Package/scripts/verify.py')
        custody['member_chain'].insert(0, 'components/package.zip')
        self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[owner, custody],
            source=self.root / owner['public_path'], from_packet_root=True))
        (self.root / target['public_path']).write_bytes(b'changed')
        self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[owner, target],
            source=self.root / owner['public_path'], from_packet_root=True))
        (self.root / target['public_path']).unlink()
        self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[owner, target],
            source=self.root / owner['public_path'], from_packet_root=True))

    def test_package_member_rejects_changed_owner_ambiguity_and_escape(self):
        owner, target = self.package_members()
        for changed in [{**owner, 'original_sha256': 'd' * 64}, {**owner, 'unexpected': True}]:
            self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[changed, target],
                source=self.root / owner['public_path'], from_packet_root=True))
        direct = self.publish('direct', ('scripts/' + 'verify.py'), b'# different root helper\n')
        direct['member_chain'].insert(0, 'components/package.zip')
        self.assertFalse(self.locate(('scripts/' + 'verify.py'), rows=[owner, target, direct],
            source=self.root / owner['public_path'], from_packet_root=True))
        for escape in ['../scripts/verify.py', '/scripts/verify.py', ('scripts/' + '../scripts/verify.py')]:
            self.assertFalse(self.locate(escape, rows=[owner, target],
                source=self.root / owner['public_path'], from_packet_root=True))

    def approved_relocation(self, include_environment=False):
        driver = self.publish('driver', 'Package/scripts/verify.py', b'# exact driver\n')
        manifest = self.publish('manifest', 'lean/lake-manifest.json', b'{"packages": []}\n')
        sources = [driver, manifest]
        suite = self.suite(sources)
        suite['id'] = 't11-substitution'
        suite['replay']['files'] = [{'source_id': 'driver', 'path': ('scripts/' + 'verify.py'), 'role': 'DRIVER'},
            {'source_id': 'manifest', 'path': 'configuration/lake-manifest.json', 'role': 'CONFIG'}]
        if include_environment:
            environment = self.publish('identity-src-db1e24bbc42e41ce33ac',
                'Syntactic_Substitution_Admissibility/ENVIRONMENT_AND_DESIGN_INPUTS.json', b'{"scope": "fixture"}\n')
            sources.append(environment)
            suite['source_ids'].append(environment['id'])
            suite['replay']['files'].append({'source_id': environment['id'],
                'path': 'configuration/D10_ENVIRONMENT_AND_DESIGN_INPUTS.json', 'role': 'CONFIG'})
        selected = {source['id']: source for source in sources}
        approval = canonical({'suite': suite, 'sources': {sid: source['public_sha256'] for sid, source in selected.items()}})
        pins = {suite['id']: (approval, canonical(selected))}
        patch = mock.patch.object(repo, '_APPROVED_SUCCESSOR_RELOCATIONS', pins, create=True)
        return patch, suite, sources, AREA.rsplit('/', 1)[0] + '/suites/' + suite['id'] + '.json'

    def test_reviewed_relocation_requires_complete_pinned_suite_and_source_identity(self):
        patch, suite, sources, src = self.approved_relocation()
        with patch:
            self.assertNotIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))
            self.assertNotIn('configuration/lake-manifest.json', self.occurrences(src, suite, sources))
            for change in [{'family': 'unreviewed'}, {'id': 'unreviewed-suite'}, {'unknown': True}]:
                with self.subTest(suite_change=change):
                    self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, {**suite, **change}, sources))
            for change in [{'origin_input_id': 'OTHER'}, {'origin_input_sha256': 'e' * 64},
                           {'member_chain': ['foreign/lake-manifest.json']}, {'review_scope': 'Changed scope.'}]:
                with self.subTest(source_change=change):
                    changed = [sources[0], {**sources[1], **change}]
                    self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, changed))
            (self.root / sources[1]['public_path']).write_bytes(b'changed manifest')
            self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))

    def test_unapproved_relocation_and_escaping_projection_remain_failures(self):
        patch, suite, sources, src = self.approved_relocation()
        self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))
        with patch:
            suite['replay']['files'][1]['path'] = 'elsewhere/lake-manifest.json'
            self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))
            suite['replay']['files'][1]['path'] = '../configuration/lake-manifest.json'
            with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
                self.occurrences(src, suite, sources)

    def test_reviewed_environment_relocation_requires_exact_source_identity(self):
        patch, suite, sources, src = self.approved_relocation(include_environment=True)
        with patch:
            self.assertNotIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))
            changed = copy.deepcopy(sources)
            changed[-1]['id'] = 'unreviewed-environment-source'
            self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, changed))
            suite['replay']['files'][-1]['path'] = 'configuration/other.lean'
            self.assertIn(('scripts/' + 'verify.py'), self.occurrences(src, suite, sources))

    def omitted_inventory(self, native_reference=False):
        omitted = [{'path': ('scripts/' + 'reconstruct.py'), 'sha256': 'd' * 64, 'bytes': 1451, 'reason': 'Preparation only.'},
                   {'path': ('scripts/' + 'package.py'), 'sha256': 'e' * 64, 'bytes': 2172, 'reason': 'Preparation only.'}]
        document = {'omitted': omitted, 'scope': 'Exact negative inventory fixture.'}
        if native_reference:
            document['verification_dependency'] = ('scripts/' + 'reconstruct.py')
        source = self.publish('projection', 'Package/PUBLIC_PROJECTION.json', document)
        pin = {'owner': {key: source[key] for key in ['id', 'origin_input_id', 'origin_input_sha256',
            'origin_archive_sha256', 'member_chain', 'original_sha256', 'original_bytes',
            'public_path', 'public_sha256', 'public_bytes', 'projection']}, 'omitted': copy.deepcopy(omitted)}
        patch = mock.patch.object(repo, '_SUCCESSOR_NEGATIVE_INVENTORY', pin, create=True)
        return patch, document, source

    def test_exact_negative_inventory_does_not_promise_available_helpers(self):
        patch, document, source = self.omitted_inventory()
        before = copy.deepcopy(document)
        with patch:
            self.assertNotIn(('scripts/' + 'reconstruct.py'), self.occurrences(source['public_path'], document, [source]))
            self.assertNotIn(('scripts/' + 'package.py'), self.occurrences(source['public_path'], document, [source]))
        self.assertEqual(document, before)
        patch, document, source = self.omitted_inventory(native_reference=True)
        with patch:
            self.assertEqual(self.occurrences(source['public_path'], document, [source]).count(('scripts/' + 'reconstruct.py')), 1)
            self.assertIn(('scripts/' + 'package.py'), self.occurrences(('docs/' + 'ordinary.json'), document, [source]))

    def test_negative_inventory_rejects_changed_owner_fields_and_hashes(self):
        patch, document, source = self.omitted_inventory()
        with patch:
            for change in [{'id': 'wrong-owner'}, {'origin_input_id': 'OTHER'}, {'origin_input_sha256': 'f' * 64},
                           {'origin_archive_sha256': 'c' * 64}, {'member_chain': ['Wrong/PUBLIC_PROJECTION.json']},
                           {'original_sha256': 'e' * 64}, {'public_sha256': 'f' * 64}, {'unexpected': True}]:
                with self.subTest(owner_change=change):
                    self.assertIn(('scripts/' + 'reconstruct.py'), self.occurrences(source['public_path'], document, [{**source, **change}]))
            for change in [{'sha256': 'f' * 64}, {'bytes': True}, {'reason': 'Available dependency.'}, {'unknown': True}]:
                with self.subTest(record_change=change):
                    changed = copy.deepcopy(document); changed['omitted'][0].update(change)
                    resealed = self.publish('projection', 'Package/PUBLIC_PROJECTION.json', changed)
                    self.assertIn(('scripts/' + 'reconstruct.py'), self.occurrences(resealed['public_path'], changed, [resealed]))
            changed = copy.deepcopy(document); changed['omitted'].reverse()
            resealed = self.publish('projection', 'Package/PUBLIC_PROJECTION.json', changed)
            self.assertIn(('scripts/' + 'reconstruct.py'), self.occurrences(resealed['public_path'], changed, [resealed]))

    def test_negative_inventory_escape_is_rejected_at_pinned_owner_path(self):
        patch, document, source = self.omitted_inventory()
        with patch:
            changed = copy.deepcopy(document)
            changed['omitted'][0]['path'] = '../scripts/reconstruct.py'
            with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
                self.occurrences(source['public_path'], changed, [source])

    def execution_hash_record(self, extra_reference=False):
        key = 'tests/' + 'test_contract.py'
        selected = 'tranche10/research/occurrence-continuation/release-candidate-v1/checker'
        target = self.publish('checker-tests', 'Archive/' + selected + '/' + key, b'# exact selected test\n')
        document = {'candidate_path': 'tranche10/reviews/occurrence-checker/inputs/release-candidate-v1/checker',
            'candidate_file_hashes': {key: target['original_sha256']},
            'public_projection': {'identical_selected_candidate': selected,
                'historical_reviewer_input_copy_distributed': False}}
        if extra_reference:
            document['unrelated_hashes'] = {key: target['original_sha256']}
        owner = self.publish('execution', 'Archive/tranche10/reviews/occurrence-checker/FINAL_EXECUTION_RECORD.json', document)
        pin = {'owner_public_path': owner['public_path'], 'owner_record_sha256': canonical(owner),
            'archive_root': 'Archive', 'selected_candidate': selected, 'key': key,
            'target_id': target['id'], 'target_record_sha256': canonical(target)}
        patch = mock.patch.object(repo, '_SUCCESSOR_EXECUTION_HASH_KEY', pin, create=True)
        return patch, document, owner, target, key

    def test_exact_execution_hash_key_uses_selected_original_and_preserves_bytes(self):
        patch, document, owner, target, key = self.execution_hash_record()
        before = copy.deepcopy([document, owner, target])
        raw = (self.root / owner['public_path']).read_bytes()
        with patch:
            self.assertNotIn(key, self.occurrences(owner['public_path'], document, [owner, target]))
        self.assertEqual([document, owner, target], before)
        self.assertEqual((self.root / owner['public_path']).read_bytes(), raw)

    def test_execution_hash_key_scope_does_not_suppress_other_json_keys(self):
        patch, document, owner, target, key = self.execution_hash_record(extra_reference=True)
        with patch:
            self.assertEqual(self.occurrences(owner['public_path'], document, [owner, target]).count(key), 1)
            self.assertIn(key, self.occurrences(('docs/' + 'ordinary.json'), document, [owner, target]))
            foreign = self.publish('foreign-owner', 'Other/FINAL_EXECUTION_RECORD.json', document)
            self.assertIn(key, self.occurrences(foreign['public_path'], document, [foreign, target]))

    def test_execution_hash_key_rejects_changed_or_foreign_owner_identity(self):
        patch, document, owner, target, key = self.execution_hash_record()
        changes = [{'id': 'foreign'}, {'origin_input_id': 'OTHER'}, {'origin_input_sha256': 'e' * 64},
            {'origin_archive_sha256': 'c' * 64}, {'member_chain': ['Other/FINAL_EXECUTION_RECORD.json']},
            {'original_sha256': 'd' * 64}, {'public_sha256': 'f' * 64}, {'public_bytes': True},
            {'review_scope': 'Altered source scope.'}, {'unknown': True}]
        with patch:
            for change in changes:
                with self.subTest(change=change):
                    changed = {**owner, **change}
                    self.assertIn(key, self.occurrences(owner['public_path'], document, [changed, target]))
            self.assertIn(key, self.occurrences(owner['public_path'], document, [owner, {**owner, 'id': 'alias'}, target]))

    def test_execution_hash_key_rejects_malformed_changed_or_relocated_map(self):
        patch, document, owner, target, key = self.execution_hash_record()
        with patch:
            for value in ['not-a-hash', target['original_sha256'].upper(), 'f' * 64, True, None]:
                with self.subTest(value=value):
                    changed = copy.deepcopy(document); changed['candidate_file_hashes'][key] = value
                    resealed = self.publish('execution', owner['member_chain'][-1], changed)
                    self.assertIn(key, self.occurrences(resealed['public_path'], changed, [resealed, target]))
            changed = copy.deepcopy(document)
            changed['unrelated_hashes'] = changed.pop('candidate_file_hashes')
            resealed = self.publish('execution', owner['member_chain'][-1], changed)
            self.assertIn(key, self.occurrences(resealed['public_path'], changed, [resealed, target]))
            for change in [{'unknown': True}, {'public_projection': {'identical_selected_candidate': 'Other/checker'}},
                           {'candidate_path': 'Other/checker'}]:
                changed = {**document, **change}
                resealed = self.publish('execution', owner['member_chain'][-1], changed)
                self.assertIn(key, self.occurrences(resealed['public_path'], changed, [resealed, target]))

    def test_execution_hash_key_requires_exact_target_identity_not_equal_hash(self):
        patch, document, owner, target, key = self.execution_hash_record()
        changes = [{'id': 'foreign-tests'}, {'origin_input_id': 'OTHER'}, {'origin_input_sha256': 'e' * 64},
            {'origin_archive_sha256': 'c' * 64}, {'member_chain': ['Archive/Other/' + key]},
            {'member_chain': ['nested.zip', target['member_chain'][-1]]}, {'original_sha256': 'd' * 64},
            {'original_bytes': True}, {'public_sha256': 'f' * 64}, {'review_scope': 'Altered source scope.'},
            {'unknown': True}]
        with patch:
            for change in changes:
                with self.subTest(change=change):
                    self.assertIn(key, self.occurrences(owner['public_path'], document, [owner, {**target, **change}]))
            conflicting = {**target, 'member_chain': ['Foreign/' + key]}
            self.assertIn(key, self.occurrences(owner['public_path'], document, [owner, target, conflicting]))
            self.assertIn(key, self.occurrences(owner['public_path'], document, [owner]))

    def test_execution_hash_key_requires_existing_unchanged_public_target(self):
        patch, document, owner, target, key = self.execution_hash_record()
        with patch:
            path = self.root / target['public_path']
            path.write_bytes(b'changed test')
            self.assertIn(key, self.occurrences(owner['public_path'], document, [owner, target]))
            path.unlink()
            self.assertIn(key, self.occurrences(owner['public_path'], document, [owner, target]))

    def test_execution_hash_key_escape_is_rejected_at_pinned_owner_path(self):
        patch, document, owner, target, key = self.execution_hash_record()
        with patch:
            for escape in ['../' + key, '/' + key, 'tests/../' + key, key.replace('/', '\\')]:
                with self.subTest(escape=escape):
                    changed = copy.deepcopy(document)
                    changed['candidate_file_hashes'] = {escape: target['original_sha256']}
                    with self.assertRaisesRegex(ValueError, 'Unsafe.*path'):
                        self.occurrences(owner['public_path'], changed, [owner, target])


if __name__ == '__main__':
    unittest.main(verbosity=2)

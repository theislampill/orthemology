"""Negative controls for the independent T20 v6 public object."""
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from validate_t20_v6_projection import check_object, safe_path, private_locators, private_uuid, origin_reference_text, PREFIX
from validate_decision_dependencies import is_supersession_registry
import validate_decision_dependencies as decisions
import validate_t20_v6_projection as projection
from resolve_t20_v6_source import lean_imports, validate_graph
from validate_repo import preserved_t20_detector_text
from test_repo_validator_corpus import changed_bytes, run_validator


class CompleteValidationTests(unittest.TestCase):
    """Exercise the real inventory and gate, with read-only corrupted overlays."""

    def run_overlay(self, edits):
        read_bytes = pathlib.Path.read_bytes
        replacements = {projection.ROOT / name: body for name, body in edits.items()}

        def read(path):
            if path in replacements:
                if replacements[path] is None:
                    raise FileNotFoundError(path)
                return replacements[path]
            return read_bytes(path)

        with patch.object(pathlib.Path, 'read_bytes', read):
            return projection.validate()[0]

    def manifest(self):
        return json.loads((projection.ROOT / projection.MANIFEST).read_bytes())

    def test_current_public_tree_passes_complete_validation(self):
        self.assertEqual(projection.validate()[0], [])

    def test_standalone_resolver_rejects_retargeted_qualified_suite(self):
        graph_path = projection.ROOT / PREFIX / 'CURRENT_SOURCE_GRAPH.json'
        graph = json.loads(graph_path.read_bytes())
        suite = next(s for s in graph['suites'] if s['id'] == 'PRIOR_C06')
        suite['id'] = 'FamilyComputability'
        identities = set(suite['modules'].values())
        graph['suites'] = [suite]
        graph['nodes'] = [n for n in graph['nodes'] if n['source_sha256'] in identities]
        for key in ('edges', 'official_import_edges'):
            graph[key] = [e for e in graph[key] if e['parent_sha256'] in identities]
        graph['ordinary_proof_dependencies'] = []
        changed = json.dumps(graph).encode()
        read_bytes = pathlib.Path.read_bytes
        objects = {r['source_sha256']: r for r in self.manifest()['objects']}
        with patch.object(pathlib.Path, 'read_bytes', lambda p: changed if p == graph_path else read_bytes(p)):
            errors = validate_graph(projection.ROOT, objects)
        self.assertIn('qualified current source graph differs', errors)

    def test_private_manifest_metadata_is_rejected(self):
        document = self.manifest()
        document['authority'] = '/' + 'home/private-owner/approval'
        errors = self.run_overlay({projection.MANIFEST: json.dumps(document).encode()})
        self.assertTrue(any('private identifier in public metadata' in e for e in errors), errors)

    def test_identity_only_universe_substitution_is_rejected(self):
        document = self.manifest()
        row = next(r for r in document['objects'] if r['disposition'] == 'IDENTITY_ONLY')
        row['source_sha256'] = '0' * 64
        errors = self.run_overlay({projection.MANIFEST: json.dumps(document).encode()})
        self.assertIn('source universe identity differs', errors)

    def test_required_source_withheld_is_rejected(self):
        document = self.manifest()
        source = '54c9b4616f23e904484432cac6f6936b724b42f48621fffa60ad957217b2e4b0'
        row = next(r for r in document['objects'] if r['source_sha256'] == source)
        self.assertIn(row['disposition'], ('ADD_EXACT', 'PROJECT', 'REUSE'))
        errors = self.run_overlay({row['repository_path']: None})
        self.assertTrue(any(source in e and 'missing' in e for e in errors), errors)

    def test_missing_import_declaration_is_rejected_even_with_updated_control_hash(self):
        name = PREFIX + '/CURRENT_SOURCE_GRAPH.json'
        graph = json.loads((projection.ROOT / name).read_bytes())
        graph['edges'].pop(0)
        body = (json.dumps(graph, indent=2) + '\n').encode()
        controls_name = PREFIX + '/PUBLIC_CONTROLS.json'
        controls = json.loads((projection.ROOT / controls_name).read_bytes())
        controls['files'][name] = hashlib.sha256(body).hexdigest()
        errors = self.run_overlay({name: body, controls_name: json.dumps(controls).encode()})
        self.assertTrue(any('actual import declarations differ' in e for e in errors), errors)

    def test_current_register_cannot_be_retargeted_with_a_matching_manifest(self):
        name = PREFIX + '/research-v6/synthesis/CROSS_CONTRIBUTIONS.json'
        document = self.manifest()
        register = json.loads((projection.ROOT / name).read_bytes())
        register['records'][0]['artifact'] = register['records'][1]['artifact']
        register['records'][0]['independent_review'] = register['records'][1]['independent_review']
        body = json.dumps(register).encode()
        row = next(r for r in document['objects'] if r.get('repository_path') == name)
        row.update(disposition='PROJECT', public_sha256=hashlib.sha256(body).hexdigest(), public_bytes=len(body))
        document['counts']['ADD_EXACT'] -= 1
        document['counts']['PROJECT'] += 1
        errors = self.run_overlay({name: body, projection.MANIFEST: json.dumps(document).encode()})
        self.assertIn('qualified current contribution register differs', errors)
        self.assertTrue(any('artifact binding differs' in e for e in errors), errors)


class PublicProjectionTests(unittest.TestCase):
    def test_preserved_detector_crlf_mutation_is_rejected_by_repository_gate(self):
        source = projection.ROOT / PREFIX / 'sources/e56c0aa1a2a0e4045751b6bd0af80f35c02cd4a4075544f44601a49c8b91d988/validate_repo.py'
        original = source.read_bytes()
        self.assertNotIn(b'\r\n', original)
        with changed_bytes(source, original.replace(b'\n', b'\r\n')):
            result = run_validator()
        self.assertEqual(1, result.returncode)
        self.assertIn('[FAIL] no absolute local paths / banned private patterns / secrets', result.stdout)
        self.assertIn('App' + 'Data path', result.stdout)

    def test_preserved_privacy_detector_rule_is_exactly_bound(self):
        name = PREFIX + '/sources/e56c0aa1a2a0e4045751b6bd0af80f35c02cd4a4075544f44601a49c8b91d988/validate_repo.py'
        text = (projection.ROOT / name).read_text()
        self.assertNotIn('App' + 'Data', preserved_t20_detector_text(name, text))
        self.assertEqual(preserved_t20_detector_text(name, text + '\nchanged'), text + '\nchanged')
        self.assertEqual(preserved_t20_detector_text('different.py', text), text)

    def test_actual_import_parser_excludes_comments_and_strings(self):
        text = '/- import Fake /- nested -/ -/\nimport A B -- import C\n"import D"\nimport Mathlib.Data.Nat.Basic\n'
        self.assertEqual(lean_imports(text), [(2, 'A'), (2, 'B'), (4, 'Mathlib.Data.Nat.Basic')])

    def test_archival_registry_exception_is_exact(self):
        relative = PREFIX + '/sources/53d15c2fba0185fdbb3bccdd5b586fd67e7f78824a2fd1e8860860ce36560dad/decision-status.yaml'
        body = (pathlib.Path(__file__).resolve().parents[1] / relative).read_text(encoding='utf-8')
        self.assertTrue(is_supersession_registry(relative, body))
        self.assertFalse(is_supersession_registry(relative, body + '\nnew normative claim'))
        self.assertFalse(is_supersession_registry('/'.join(('theory', 'decision-status.yaml')), body))
        self.assertFalse(is_supersession_registry(PREFIX + '/decision-status.yaml', body))
        with tempfile.TemporaryDirectory() as tmp:
            fixture = pathlib.Path(tmp) / relative
            fixture.parent.mkdir(parents=True)
            fixture.write_bytes(body.replace('\n', '\r\n').encode())
            with patch.object(decisions, 'ROOT', tmp):
                raw_text = decisions.read(relative, newline='')
            self.assertFalse(is_supersession_registry(relative, raw_text))

    def test_original_reference_binding_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            directory = root / PREFIX
            directory.mkdir(parents=True)
            src = PREFIX + '/source.md'
            target = '/'.join(('scripts', 'original.py'))
            text = 'Historical source ' + target
            binding = {'schema':'t20-v6-exact-origin-references-v1','records':[
                {'repository_path':src,'public_sha256':hashlib.sha256(text.encode()).hexdigest(),
                 'origin_context':'preserved_source_document', 'references':[
                     {'components':target.split('/'),'occurrences':1}]}]}
            (directory / 'ORIGIN_REFERENCES.json').write_text(json.dumps(binding))
            self.assertNotIn(target, origin_reference_text(src, text, root))
            self.assertEqual(origin_reference_text(src, text + ' changed', root), text + ' changed')
            self.assertEqual(origin_reference_text(PREFIX + '/other.md', text, root), text)

    def test_traversal(self):
        for value in ('../a', '/a', 'a/../b', 'a\\b', 'C:/a', ''):
            with self.assertRaises(ValueError):
                safe_path(value)

    def test_private_body_regardless_of_extension(self):
        self.assertTrue(private_locators('Evidence at /' + 'home/owner/private.txt'))
        self.assertTrue(private_locators('Evidence at /' + 'tmp/owner/page.png'))
        self.assertTrue(private_locators('unchanged:/' + 'home/owner/source.lean'))
        self.assertTrue(private_locators('LEAN_PATH=public:/' + 'home/owner/lib'))
        self.assertFalse(private_locators('https://example.org/home/article'))
        self.assertFalse(private_locators('https://example.org:443/home/article'))
        self.assertFalse(private_locators(r'pattern: /home/[^/]+/'))

    def test_uuid_in_url_is_not_automatically_public(self):
        identifier = '00000000' + '-0000' * 3 + '-000000000000'
        self.assertTrue(private_uuid('https://example.org/' + identifier, '0' * 64))
        self.assertTrue(private_uuid('https://chatgpt.com/c/' + identifier, '0' * 64))

    def test_tampered_and_missing_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            body = b'bounded source evidence\n'
            (root / 'body').write_bytes(body)
            sha = hashlib.sha256(body).hexdigest()
            row = dict(source_sha256=sha, source_bytes=len(body), disposition='ADD_EXACT',
                       repository_path='body', public_sha256=sha, public_bytes=len(body))
            self.assertEqual(check_object(root, row), [])
            (root / 'body').write_bytes(b'changed')
            self.assertTrue(check_object(root, row))
            (root / 'body').unlink()
            self.assertTrue(check_object(root, row))

    def test_changed_bytes_cannot_claim_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'body').write_bytes(b'projection')
            row = dict(source_sha256='0' * 64, source_bytes=10, disposition='ADD_EXACT',
                       repository_path='body', public_sha256=hashlib.sha256(b'projection').hexdigest(), public_bytes=10)
            self.assertTrue(check_object(root, row))

    def test_held_identity_cannot_have_body(self):
        row = dict(source_sha256='0' * 64, disposition='NOT_PUBLISHED', repository_path='body')
        self.assertTrue(check_object(pathlib.Path('.'), row))

    def test_arbitrary_history_revision_cannot_mask_drift(self):
        row = dict(source_sha256='0' * 64, disposition='REUSE', repository_path='body',
                   repository_revision='HEAD', public_sha256='0' * 64, public_bytes=0)
        self.assertTrue(check_object(pathlib.Path('.'), row))

    def test_symlink_not_a_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'real').write_bytes(b'x')
            (root / 'link').symlink_to(root / 'real')
            row = dict(source_sha256=hashlib.sha256(b'x').hexdigest(), source_bytes=1,
                       disposition='REUSE', repository_path='link', public_sha256=hashlib.sha256(b'x').hexdigest(), public_bytes=1)
            self.assertTrue(check_object(root, row))



class HistoricalProseBindingTests(unittest.TestCase):
    """History must not conceal a wrong present edition or an unsafe path."""

    PATH = 'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md'
    BLOB = 'cf657a78f972b7f98190139b2275a3381d288b66'
    SHA = '52631c602c1c8fede28dbe6da34480094caf6f441c1aec0293229cdfdf28a0be'

    @classmethod
    def setUpClass(cls):
        import subprocess
        cls.original = subprocess.check_output(
            ['git', 'show', projection.BASE + ':' + cls.PATH], cwd=projection.ROOT)
        cls.object_directory = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'objects'], cwd=projection.ROOT,
            text=True).strip())
        if not cls.object_directory.is_absolute():
            cls.object_directory = projection.ROOT / cls.object_directory

    def setUp(self):
        import subprocess
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        # Read-only access to the real pinned Git objects; no fabricated history.
        (self.root / '.git/objects/info/alternates').write_text(
            str(self.object_directory.resolve()) + '\n')
        self.target = self.root / self.PATH
        self.target.parent.mkdir(parents=True)
        self.target.write_bytes(self.original)
        self.row = dict(source_sha256=self.SHA, source_bytes=15839,
                        disposition='REUSE', repository_path=self.PATH,
                        public_sha256=self.SHA, public_bytes=15839,
                        repository_revision=projection.BASE, git_blob=self.BLOB)

    def resolve(self, row=None):
        from resolve_t20_v6_source import source_bytes
        return source_bytes(self.root, self.row if row is None else row)

    def rejected_by_both(self, row=None):
        import subprocess
        selected = self.row if row is None else row
        self.assertTrue(check_object(self.root, selected))
        with self.assertRaises((ValueError, OSError, subprocess.CalledProcessError)):
            self.resolve(selected)

    def test_exact_present_and_missing_historical_prose_authenticate_same_bytes(self):
        self.assertEqual(check_object(self.root, self.row), [])
        self.assertEqual(self.resolve(), self.original)
        self.target.unlink()
        self.assertEqual(check_object(self.root, self.row), [])
        self.assertEqual(self.resolve(), self.original)
        self.assertFalse(self.target.exists(), 'verification must not recreate a predecessor')

    def test_present_wrong_edition_cannot_hide_behind_correct_history(self):
        self.target.write_bytes(self.original + b'\nwrong edition\n')
        self.rejected_by_both()

    def test_present_executable_mode_cannot_hide_behind_history(self):
        self.target.chmod(0o755)
        self.rejected_by_both()

    def test_leaf_symlink_is_rejected_even_when_it_names_exact_bytes(self):
        actual = self.target.with_name('exact-copy')
        self.target.rename(actual)
        self.target.symlink_to(actual)
        self.rejected_by_both()

    def test_ancestor_symlink_inside_root_is_still_rejected(self):
        directory = self.target.parent
        actual = directory.with_name(directory.name + '-exact')
        directory.rename(actual)
        directory.symlink_to(actual, target_is_directory=True)
        self.rejected_by_both()

    def test_dangling_symlink_is_not_an_absent_historical_source(self):
        self.target.unlink()
        self.target.symlink_to(self.target.with_name('unavailable'))
        self.rejected_by_both()

    def test_directory_cannot_replace_historical_prose(self):
        self.target.unlink()
        self.target.mkdir()
        self.rejected_by_both()

    def test_binding_requires_exact_revision_blob_path_and_size(self):
        for field, value in (
                ('repository_revision', 'HEAD'),
                ('repository_revision', '8fab6133d72d76fe714f84b36716eb418892c7be'),
                ('repository_revision', '0' * 40),
                ('git_blob', '0' * 40),
                ('repository_path', self.PATH.replace('CP20/compound-ground-necessity',
                                                     'CP19/necessary-truth-operative-basing')),
                ('source_bytes', 15840), ('public_bytes', 15840),
                ('source_sha256', '0' * 64)):
            with self.subTest(field=field, value=value):
                row = dict(self.row, **{field: value})
                self.rejected_by_both(row)

    def test_present_copy_does_not_substitute_for_missing_pinned_git_objects(self):
        (self.root / '.git/objects/info/alternates').unlink()
        self.rejected_by_both()

    def test_existing_distinct_current_history_rows_keep_original_semantics(self):
        document = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        old_paths = {'scripts/validate_repo.py', 'CONTRIBUTING.md',
                     'scripts/validate_internal_references.py',
                     'scripts/validate_decision_dependencies.py',
                     'docs/project-closure/HISTORICAL-STATUS-INDEX.yaml'}
        selected = [r for r in document['objects'] if r.get('repository_path') in old_paths]
        self.assertEqual(len(selected), 5)
        from resolve_t20_v6_source import source_bytes
        for row in selected:
            with self.subTest(path=row['repository_path']):
                self.assertEqual(check_object(projection.ROOT, row), [])
                self.assertEqual(hashlib.sha256(source_bytes(projection.ROOT, row)).hexdigest(),
                                 row['public_sha256'])


    def test_original_or_deleted_index_is_accepted_with_exact_or_absent_worktree(self):
        import subprocess
        for indexed in (True, False):
            for present in (True, False):
                with self.subTest(indexed=indexed, present=present):
                    subprocess.run(['git', 'update-index', '--force-remove', '--', self.PATH],
                                   cwd=self.root, check=True)
                    if indexed:
                        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                        '100644,' + self.BLOB + ',' + self.PATH],
                                       cwd=self.root, check=True)
                    if present:
                        self.target.write_bytes(self.original)
                    elif self.target.exists():
                        self.target.unlink()
                    self.assertEqual(check_object(self.root, self.row), [])
                    self.assertEqual(self.resolve(), self.original)
                    self.assertEqual(self.target.exists(), present)

    def test_wrong_or_unmerged_index_is_rejected_with_exact_or_absent_worktree(self):
        import subprocess
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                        cwd=self.root, input=b'wrong staged edition\n').decode().strip()
        link = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                       cwd=self.root, input=b'exact-copy').decode().strip()
        for kind, mode, blob in (('blob', '100644', wrong), ('mode', '100755', self.BLOB),
                                 ('symlink', '120000', link), ('unmerged', None, None)):
            for present in (True, False):
                with self.subTest(kind=kind, present=present):
                    subprocess.run(['git', 'update-index', '--force-remove', '--', self.PATH],
                                   cwd=self.root, check=True)
                    if mode:
                        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                        mode + ',' + blob + ',' + self.PATH], cwd=self.root, check=True)
                    else:
                        entries = ''.join(mode_ + ' ' + oid + ' ' + stage + '\t' + self.PATH + '\n'
                                          for mode_, oid, stage in (('100644', self.BLOB, '1'),
                                                                   ('100644', wrong, '2'),
                                                                   ('100644', self.BLOB, '3')))
                        subprocess.run(['git', 'update-index', '--index-info'], cwd=self.root,
                                       input=entries.encode(), check=True)
                    if present:
                        self.target.write_bytes(self.original)
                    elif self.target.exists():
                        self.target.unlink()
                    self.rejected_by_both()
                    self.assertEqual(self.target.exists(), present)




class HistoricalProseRootTests(unittest.TestCase):
    """Only exact declared deletions may cross the preserved-root boundary."""

    PATHS = (
        'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/REPORT.md',
        'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md',
        'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md',
        'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/VARIABLE_SHARING_REDUCTION.md',
        'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md',
    )
    EXTRA = 'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/CHECK_RESULTS.json'

    def setUp(self):
        import subprocess
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        self.objects = {r['source_sha256']: r for r in manifest['objects']}
        for path in self.PATHS:
            for row in self.objects.values():
                if row.get('repository_path') == path:
                    row.update(repository_revision=projection.BASE, git_blob=subprocess.check_output(
                        ['git', 'rev-parse', projection.BASE + ':' + path],
                        cwd=projection.ROOT, text=True).strip())
        self.saved, self.created_directories = {}, set()
        for path in (*self.PATHS, self.EXTRA):
            node = projection.ROOT
            for part in path.split('/'):
                node = node / part
                self.assertFalse(node.is_symlink(), "unsafe initial historical path")
            self.saved[path] = ((node.read_bytes(), node.stat().st_mode & 0o777)
                                if node.exists() else (None, None))
            if self.saved[path][0] is not None:
                self.assertEqual(self.saved[path][0], subprocess.check_output(
                    ['git', 'show', projection.BASE + ':' + path], cwd=projection.ROOT))
                self.assertFalse(self.saved[path][1] & 0o111, "wrong initial historical Git mode")
        self.addCleanup(self.restore)
        for path, (body, mode) in self.saved.items():
            if body is not None:
                continue
            self.assertIn(path, self.PATHS, "unqualified fixture input is absent")
            node = projection.ROOT / path
            parent = node.parent
            while not parent.exists():
                self.created_directories.add(parent)
                parent = parent.parent
            node.parent.mkdir(parents=True, exist_ok=True)
            # Mutation fixtures need a present copy even after actual retirement.
            # Seed the exact original solely for this test, then restore absence.
            node.write_bytes(subprocess.check_output(
                ['git', 'show', projection.BASE + ':' + path], cwd=projection.ROOT))
            node.chmod(0o644)

    def restore(self):
        for path, (body, mode) in self.saved.items():
            node = projection.ROOT / path
            if body is None:
                if node.exists() or node.is_symlink():
                    node.unlink()
            else:
                node.write_bytes(body)
                node.chmod(mode)
        for directory in sorted(self.created_directories, key=lambda p: len(p.parts), reverse=True):
            directory.rmdir()

    def errors(self):
        gate = getattr(projection, 'check_preserved_roots', None)
        self.assertTrue(callable(gate), 'finite protected-root owner is not implemented')
        return gate(projection.ROOT, self.objects)

    def test_all_five_absences_keep_original_object_and_occurrence_coverage(self):
        for path in self.PATHS:
            (projection.ROOT / path).unlink()
        self.assertEqual(self.errors(), [])
        self.assertTrue(all(not (projection.ROOT / path).exists() for path in self.PATHS),
                        'verification must not recreate original paths')
        self.assertEqual(len(self.objects), 28478)

    def test_one_undeclared_extra_deletion_still_fails(self):
        (projection.ROOT / self.EXTRA).unlink()
        self.assertTrue(any('preserved v5 or prior T20 baseline changed' in e for e in self.errors()))

    def test_selected_modified_file_is_not_treated_as_a_deletion(self):
        path = projection.ROOT / self.PATHS[0]
        path.write_bytes(path.read_bytes() + b'\nwrong edition\n')
        errors = self.errors()
        self.assertTrue(any('preserved v5 or prior T20 baseline changed' in e for e in errors))

    def test_inherited_duplicate_proof_is_checked_without_an_extra_manifest_row(self):
        path = projection.ROOT / self.PATHS[2]
        path.write_bytes(path.read_bytes() + b'\nwrong inherited proof\n')
        self.assertTrue(any(self.PATHS[2] in e for e in self.errors()))

    def test_selected_rename_does_not_become_an_admitted_deletion(self):
        import subprocess
        root = projection.ROOT
        index = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'index'], cwd=root, text=True).strip())
        if not index.is_absolute():
            index = root / index
        saved_index = index.read_bytes()
        source = root / self.PATHS[0]
        renamed = source.with_name('unqualified-renamed-report.md')
        try:
            # In a thin checkout this mutation fixture starts untracked. Admit
            # its exact original temporarily; restore the byte-exact index below.
            subprocess.run(['git', 'add', '--', self.PATHS[0]], cwd=root, check=True)
            subprocess.run(['git', 'mv', '--', str(source), str(renamed)], cwd=root, check=True)
            self.assertTrue(any('preserved v5 or prior T20 baseline changed' in e for e in self.errors()))
        finally:
            if renamed.exists():
                renamed.rename(source)
            index.write_bytes(saved_index)

    def test_missing_or_wrong_public_history_binding_rejects_root_admission(self):
        identity = '4bd8f0e5bcac178bf9eb890544fcba9fd60f6a1d08cdf2e0cc12bb6d2c4b4c1c'
        self.objects[identity]['repository_revision'] = 'HEAD'
        self.assertTrue(self.errors())


    def test_wrong_staged_selected_blob_mode_symlink_or_conflict_cannot_hide_in_absence(self):
        import subprocess
        root, path = projection.ROOT, self.PATHS[0]
        node = root / path
        body = node.read_bytes()
        index = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'index'], cwd=root, text=True).strip())
        if not index.is_absolute():
            index = root / index
        saved = index.read_bytes()
        original = subprocess.check_output(['git', 'rev-parse', projection.BASE + ':' + path],
                                           cwd=root, text=True).strip()
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                        cwd=root, input=b'wrong staged original\n').decode().strip()
        link = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                       cwd=root, input=b'REPORT.md').decode().strip()
        try:
            for kind, mode, blob in (('blob', '100644', wrong), ('mode', '100755', original),
                                     ('symlink', '120000', link), ('unmerged', None, None)):
                with self.subTest(kind=kind):
                    index.write_bytes(saved)
                    subprocess.run(['git', 'update-index', '--force-remove', '--', path], cwd=root, check=True)
                    if mode:
                        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                        mode + ',' + blob + ',' + path], cwd=root, check=True)
                    else:
                        entries = ''.join('100644 ' + oid + ' ' + stage + '\t' + path + '\n'
                                          for oid, stage in ((original, '1'), (wrong, '2'), (original, '3')))
                        subprocess.run(['git', 'update-index', '--index-info'], cwd=root,
                                       input=entries.encode(), check=True)
                    if node.exists():
                        node.unlink()
                    errors = self.errors()
                    self.assertTrue(any(path in e for e in errors), errors)
                    self.assertFalse(node.exists(), 'index verification must not recreate the original')
        finally:
            index.write_bytes(saved)
            node.write_bytes(body)
            node.chmod(0o644)
        self.assertEqual(index.read_bytes(), saved)

    def test_staged_unqualified_protected_changes_cannot_hide_under_original_worktree(self):
        import subprocess
        root = projection.ROOT
        index = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'index'], cwd=root, text=True).strip())
        if not index.is_absolute():
            index = root / index
        saved = index.read_bytes()
        original = subprocess.check_output(['git', 'rev-parse', projection.BASE + ':' + self.EXTRA],
                                           cwd=root, text=True).strip()
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                        cwd=root, input=b'wrong staged protected source\n').decode().strip()
        link = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                       cwd=root, input=b'CHECK_RESULTS.json').decode().strip()
        added = self.EXTRA.rsplit('/', 1)[0] + '/unqualified-index-only.md'
        self.assertFalse((root / added).exists())
        try:
            for kind, path, mode, blob in (
                    ('blob', self.EXTRA, '100644', wrong), ('mode', self.EXTRA, '100755', original),
                    ('symlink', self.EXTRA, '120000', link), ('addition', added, '100644', wrong)):
                with self.subTest(kind=kind):
                    index.write_bytes(saved)
                    subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                    mode + ',' + blob + ',' + path], cwd=root, check=True)
                    errors = self.errors()
                    self.assertIn('preserved v5 or prior T20 baseline changed', errors)
        finally:
            index.write_bytes(saved)
        self.assertEqual(index.read_bytes(), saved)




class MediatorOwnerMigrationTests(unittest.TestCase):
    """Two exact prose admissions cannot weaken current or historical owners."""

    REV = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
    COORD = 'experiments/orthemology-v5-successors/source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/BOUNDED_COORDINATION_INFORMATION_v1.md'
    APPROX = 'research/t20-v6-20261012/research-v6/type_collective/ROBUST_FINITE_MEDIATOR_BOUND.md'
    GUIDE = 'experiments/orthemology-v5-successors/groups/t12-written/README.md'
    CHAPTER = 'mathematics/collective-inquiry-and-strategic-coordination.md'
    REVIEW = 'docs/scientific-consolidation-review.md'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    BLOBS = {COORD: 'a949e7e8fdb1fcf386d3580a034d9cb14f34e7d5',
             APPROX: '8c8b327bb642570307e50ddaef35850b508a80e6'}

    @classmethod
    def setUpClass(cls):
        import importlib.util
        import subprocess
        import check_reader_pilot
        import resolve_t20_v6_source
        cls.reader = check_reader_pilot
        cls.resolver = resolve_t20_v6_source
        spec = importlib.util.spec_from_file_location(
            'mediator_v5_owner', projection.ROOT / 'scripts/validate_v5_successors.py')
        cls.v5 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.v5)
        cls.objects = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'objects'], cwd=projection.ROOT,
            text=True).strip())
        if not cls.objects.is_absolute():
            cls.objects = projection.ROOT / cls.objects
        cls.original = {p: subprocess.check_output(
            ['git', 'show', cls.REV + ':' + p], cwd=projection.ROOT)
            for p in (cls.COORD, cls.APPROX, cls.GUIDE)}
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        cls.manifest_rows = {p: next(r for r in manifest['objects']
                                    if r.get('repository_path') == p)
                             for p in (cls.COORD, cls.APPROX)}
        cls.source_row = next(r for r in json.loads((projection.ROOT /
            'docs/provenance/v5-successors/SOURCE_MAP.json').read_bytes())['sources']
                              if r.get('id') == 'T12-SOURCE-COORDINATION')
        projection_rows = json.loads((projection.ROOT /
            'docs/provenance/v5-successors/PUBLIC_PROJECTION.json').read_bytes())['allowlist']
        cls.allowlist = [r for r in projection_rows if r['path'] in (cls.COORD, cls.GUIDE)]
        cls.indexed = {r['path']: r for r in cls.reader.entries_at(projection.ROOT, cls.REV)}

    def setUp(self):
        from copy import deepcopy
        import subprocess
        self.tmp = tempfile.TemporaryDirectory(prefix='mediator-owner-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.git/objects/info/alternates').write_text(str(self.objects.resolve()) + '\n')
        for name in (self.CHAPTER, self.REVIEW, self.OWNER, self.CROSS,
                     'epistemology/recognition-warrant-and-restoration.md'):
            self.put(name, (projection.ROOT / name).read_bytes())
        for name in (self.COORD, self.APPROX):
            self.put(name, self.original[name])
        old = ('../../source-store/c77bb25b5b3072294a16fb8678441c30a62ec917cad59957193350af80973ff7/'
               'BOUNDED_COORDINATION_INFORMATION_v1.md').encode()
        new = ('https://github.com/theislampill/orthemology/blob/' + self.REV + '/' + self.COORD).encode()
        self.assertEqual(self.original[self.GUIDE].count(old), 3)
        self.guide = self.original[self.GUIDE].replace(old, new)
        self.put(self.GUIDE, self.guide)
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                        '100644,7c6a9bfdeaf8372d3ea73ff8a06f4aefb17ef838,' + self.GUIDE],
                       cwd=self.root, check=True)
        self.owners = json.loads((self.root / self.OWNER).read_bytes())
        for name in (self.COORD, self.APPROX):
            self.owners['historical_source_bindings'] = [r for r in self.owners['historical_source_bindings']
                                                        if r['path'] != name]
            self.owners['historical_source_bindings'].append(dict(
                path=name, repository_revision=self.REV, git_blob=self.BLOBS[name],
                role='historical-source', reading_source='consolidated-collective-inquiry',
                basis='scientific-consolidation-review'))
        self.put(self.OWNER, (json.dumps(self.owners) + '\n').encode())
        self.cross = json.loads((self.root / self.CROSS).read_bytes())
        self.additions = {r['path']: r for r in self.owners['source_additions']}
        self.rows = {p: dict(deepcopy(self.manifest_rows[p]), repository_revision=self.REV,
                             git_blob=self.BLOBS[p]) for p in (self.COORD, self.APPROX)}
        self.bundle = dict(sources=[deepcopy(self.source_row)], reviews=[], projection_reviews=[],
                           public_allowlist=deepcopy(self.allowlist))

    def put(self, name, data):
        node = self.root / name
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(data)
        node.chmod(0o644)

    def resolve(self, path, row=None):
        return self.resolver.source_bytes(self.root, self.rows[path] if row is None else row)

    def reject(self, path, row=None):
        selected = self.rows[path] if row is None else row
        self.assertTrue(check_object(self.root, selected))
        import subprocess
        with self.assertRaises((ValueError, OSError, subprocess.CalledProcessError)):
            self.resolve(path, selected)

    def v5_check(self):
        sources, _, _ = self.v5._sources(self.bundle, self.root)
        self.v5._allowlist(self.bundle, self.root, sources)

    def test_two_distinct_dispositions_authenticate_exact_present_and_absent_bodies(self):
        for path in (self.COORD, self.APPROX):
            with self.subTest(path=path):
                self.assertEqual(check_object(self.root, self.rows[path]), [])
                self.assertEqual(self.resolve(path), self.original[path])
                (self.root / path).unlink()
                self.assertEqual(check_object(self.root, self.rows[path]), [])
                self.assertEqual(self.resolve(path), self.original[path])
                self.assertFalse((self.root / path).exists(), 'a check must not restore prose')

    def test_reader_authenticates_seven_bound_paths_and_the_same_current_science(self):
        admitted, errors = self.reader.check_historical_sources(
            self.root, self.indexed, self.owners, self.cross, self.additions)
        self.assertEqual(errors, [])
        self.assertEqual(len(admitted), 7)
        self.assertEqual(admitted[self.COORD], self.original[self.COORD])
        self.assertEqual(admitted[self.APPROX], self.original[self.APPROX])

    def test_v5_exact_source_and_full_allowlist_keep_rows_when_one_body_is_absent(self):
        from copy import deepcopy
        saved = deepcopy(self.bundle)
        try:
            self.v5_check()
            (self.root / self.COORD).unlink()
            self.v5_check()
        except (ValueError, OSError) as error:
            self.fail('finite source-owned admission missing: ' + str(error))
        self.assertEqual(self.bundle, saved)
        self.assertFalse((self.root / self.COORD).exists())

    def test_changed_current_chapter_or_review_rejects_all_new_history(self):
        for path in (self.CHAPTER, self.REVIEW):
            with self.subTest(path=path):
                original = (self.root / path).read_bytes()
                try:
                    self.put(path, original + b'\nwrong current edition\n')
                    for source in (self.COORD, self.APPROX):
                        self.reject(source)
                    with self.assertRaises((ValueError, OSError)):
                        self.v5_check()
                    self.assertTrue(self.reader.check_historical_sources(
                        self.root, self.indexed, self.owners, self.cross, self.additions)[1])
                finally:
                    self.put(path, original)

    def test_wrong_original_bytes_modes_or_symlinks_cannot_hide_behind_history(self):
        for path in (self.COORD, self.APPROX):
            target = self.root / path
            for kind in ('bytes', 'executable', 'symlink'):
                with self.subTest(path=path, kind=kind):
                    try:
                        if kind == 'bytes':
                            target.write_bytes(self.original[path] + b'changed\n')
                        elif kind == 'executable':
                            target.chmod(0o755)
                        else:
                            target.unlink()
                            target.symlink_to('missing-original')
                        self.reject(path)
                    finally:
                        if target.is_symlink(): target.unlink()
                        self.put(path, self.original[path])

    def test_exact_revision_blob_role_and_lengths_are_required(self):
        for path in (self.COORD, self.APPROX):
            for field, value in (
                    ('repository_revision', projection.BASE), ('repository_revision', 'HEAD'),
                    ('git_blob', '0' * 40), ('source_sha256', '0' * 64),
                    ('public_sha256', '0' * 64), ('source_bytes', 1), ('public_bytes', 1),
                    ('disposition', 'ADD_EXACT' if path == self.COORD else 'REUSE')):
                with self.subTest(path=path, field=field):
                    self.reject(path, dict(self.rows[path], **{field: value}))

    def test_missing_pinned_objects_reject_even_when_bodies_are_present(self):
        (self.root / '.git/objects/info/alternates').unlink()
        for path in (self.COORD, self.APPROX): self.reject(path)

    def test_undeclared_similar_absence_receives_no_history_fallback(self):
        row = dict(self.rows[self.COORD], repository_path=self.COORD.replace('v1.md', 'v2.md'))
        self.reject(self.COORD, row)

    def test_staged_tampering_cannot_hide_behind_absent_new_prose(self):
        import subprocess
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
            cwd=self.root, input=b'wrong staged source\n').decode().strip()
        for path in (self.COORD, self.APPROX):
            target = self.root / path
            target.unlink()
            try:
                for kind, mode, blob in [('blob', '100644', wrong),
                                         ('mode', '100755', self.BLOBS[path]),
                                         ('link', '120000', wrong), ('conflict', None, None)]:
                    with self.subTest(path=path, kind=kind):
                        subprocess.run(['git', 'update-index', '--force-remove', '--', path],
                                       cwd=self.root, check=True)
                        if mode:
                            subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                            mode + ',' + blob + ',' + path], cwd=self.root, check=True)
                        else:
                            rows = ''.join('100644 ' + oid + ' ' + stage + '\t' + path + '\n'
                                for oid, stage in [(self.BLOBS[path], '1'), (wrong, '2'),
                                                   (self.BLOBS[path], '3')])
                            subprocess.run(['git', 'update-index', '--index-info'], cwd=self.root,
                                           input=rows.encode(), check=True)
                        self.reject(path)
                        self.assertFalse(target.exists())
            finally:
                subprocess.run(['git', 'update-index', '--force-remove', '--', path],
                               cwd=self.root, check=True)
                self.put(path, self.original[path])

    def test_guide_missing_or_nonliteral_navigation_change_rejects_new_admission(self):
        for variant in (None, self.original[self.GUIDE], self.guide + b'changed prose\n',
                        self.guide.replace(self.REV.encode(), b'HEAD', 1)):
            with self.subTest(variant='missing' if variant is None else len(variant)):
                try:
                    if variant is None: (self.root / self.GUIDE).unlink()
                    else: self.put(self.GUIDE, variant)
                    for path in (self.COORD, self.APPROX): self.reject(path)
                    with self.assertRaises((ValueError, OSError)): self.v5_check()
                finally:
                    self.put(self.GUIDE, self.guide)

    def test_guide_wrong_staged_mode_cannot_hide_behind_valid_navigation(self):
        import subprocess
        blob = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                                       cwd=self.root, input=self.guide).decode().strip()
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                        '100755,' + blob + ',' + self.GUIDE], cwd=self.root, check=True)
        for path in (self.COORD, self.APPROX): self.reject(path)
        with self.assertRaises((ValueError, OSError)): self.v5_check()

    def test_v5_allowlist_still_rejects_an_undeclared_extra_file(self):
        self.put('/'.join(('experiments', 'orthemology-v5-successors', 'source-store', 'unlisted', 'extra.md')), b'extra\n')
        with self.assertRaises((ValueError, OSError)): self.v5_check()

    def test_v5_missing_unqualified_source_is_not_a_qualified_absence(self):
        from copy import deepcopy
        row = deepcopy(self.source_row)
        row['id'] = 'UNQUALIFIED-COPY'
        row['public_path'] = row['public_path'].replace('v1.md', 'v2.md')
        self.bundle['sources'].append(row)
        entry = next(x for x in self.bundle['public_allowlist'] if x['path'] == self.COORD)
        self.bundle['public_allowlist'].append(dict(entry, path=row['public_path'], source_ids=[row['id']]))
        with self.assertRaises((ValueError, OSError)): self.v5_check()

    def test_add_exact_inventory_authenticates_only_the_one_declared_absence(self):
        from copy import deepcopy
        rows = [deepcopy(self.rows[p]) for p in (self.COORD, self.APPROX)]
        controls = {'files': {}}
        saved = deepcopy(rows)
        self.put(projection.MANIFEST, b'{}\n')
        self.put(projection.PREFIX + '/PUBLIC_CONTROLS.json', b'{}\n')
        self.assertEqual(projection.check_public_inventory(self.root, rows, controls), [])
        (self.root / self.APPROX).unlink()
        self.assertEqual(projection.check_public_inventory(self.root, rows, controls), [])
        self.assertEqual(rows, saved)
        self.assertFalse((self.root / self.APPROX).exists())
        wrong = deepcopy(rows)
        wrong[1]['git_blob'] = '0' * 40
        self.assertTrue(projection.check_public_inventory(self.root, wrong, controls))
        extra = self.APPROX.replace('.md', '_extra.md')
        self.put(extra, b'undeclared extra file\n')
        self.assertTrue(projection.check_public_inventory(self.root, rows, controls))
        (self.root / extra).unlink()
        declared_missing = dict(rows[1], repository_path=extra)
        self.assertTrue(projection.check_public_inventory(self.root, rows + [declared_missing], controls))



class ReadOnlyPreservedRootDiffTests(unittest.TestCase):
    """Isolate real Git diffs; no original source or public manifest is opened."""

    def setUp(self):
        import os
        from unittest.mock import patch
        self.env = patch.dict(os.environ, {"GIT_OPTIONAL_LOCKS": "0",
                              "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        self.env.start()
        self.addCleanup(self.env.stop)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = pathlib.Path(self.tmp.name)
        self.relative = "/".join(("experiments", "orthemology-v5", "fixture-source.txt"))
        self.node = self.repo / self.relative
        self.node.parent.mkdir(parents=True)
        self.original = b"synthetic unchanged source\n"
        self.node.write_bytes(self.original)
        self._git("init", "-q")
        self._git("config", "diff.autoRefreshIndex", "true")
        self._git("add", "--", self.relative)
        self._git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                  "commit", "-qm", "synthetic baseline")
        self.baseline = self._git("rev-parse", "HEAD").decode().strip()
        self.initial = self._snapshot()

        self.rejection = ["preserved v5 or prior T20 baseline changed"]

    def _gate(self):
        with patch.object(projection, "BASE", self.baseline), \
             patch.object(projection, "HISTORICAL_PROSE", {}), \
             patch.object(projection, "mediator_guide_source_bytes",
                          side_effect=ValueError("no synthetic guide admission")):
            return projection.check_preserved_roots(self.repo, {})

    def _git(self, *args):
        import subprocess
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, check=True).stdout

    def _snapshot(self):
        raw = (self.repo / ".git" / "index").read_bytes()
        info = self.node.stat()
        return {
            "raw_index_sha256": hashlib.sha256(raw).hexdigest(), "raw_index_bytes": len(raw),
            "logical_entries": self._git("ls-files", "--stage", "-z").decode(),
            "flags": self._git("ls-files", "-v", "-z").decode(),
            "debug_metadata": self._git("ls-files", "--debug", "-z").decode(),
            "source_sha256": hashlib.sha256(self.node.read_bytes()).hexdigest(),
            "physical_stat": {"mode": info.st_mode & 0o777, "inode": info.st_ino,
                              "device": info.st_dev, "size": info.st_size,
                              "ctime_ns": info.st_ctime_ns, "mtime_ns": info.st_mtime_ns},
        }

    def _require_read_only(self, expected):
        before = self._snapshot()
        result = self._gate()
        after = self._snapshot()
        self._diff_observation = {"initial": self.initial, "before": before,
                                  "after": after, "result": result}
        self.assertEqual(result, expected)
        for key in ("logical_entries", "flags", "source_sha256", "physical_stat"):
            self.assertEqual(before[key], after[key], key)
        self.assertEqual(before["raw_index_sha256"], after["raw_index_sha256"],
                         "read-only diff refreshed the raw index")
        self.assertEqual(before["debug_metadata"], after["debug_metadata"])

    def test_stat_only_replacement_preserves_exact_index(self):
        import os
        info = self.node.stat()
        replacement = self.node.with_name("replacement.tmp")
        replacement.write_bytes(self.original)
        replacement.chmod(info.st_mode & 0o777)
        os.utime(replacement, ns=(info.st_atime_ns, info.st_mtime_ns - 2_000_000_000))
        replacement.replace(self.node)
        self.assertEqual(self.node.read_bytes(), self.original)
        self.assertEqual(self._snapshot()["logical_entries"], self.initial["logical_entries"])
        self._require_read_only([])

    def test_staged_tamper_cannot_hide_behind_original_worktree(self):
        self.node.write_bytes(b"synthetic staged tampering\n")
        self._git("add", "--", self.relative)
        self.node.write_bytes(self.original)
        self.assertNotEqual(self._snapshot()["logical_entries"], self.initial["logical_entries"])
        self._require_read_only(self.rejection)


    def test_racy_content_preserves_index_mtime_and_cleans_private_copies(self):
        import os
        import subprocess
        self._git("config", "core.trustctime", "false")
        self._git("config", "core.checkStat", "minimal")
        index = self.repo / ".git" / "index"
        stamp = self.node.stat().st_mtime_ns
        self.node.write_bytes(b"X" + self.original[1:])
        os.utime(self.node, ns=(stamp, stamp))
        os.utime(index, ns=(stamp, stamp))
        original_run = subprocess.run
        copies = []

        def observe(command, *args, **kwargs):
            if "diff" in command:
                self.assertIn("GIT_INDEX_FILE", kwargs.get("env", {}))
                shadow = pathlib.Path(kwargs["env"]["GIT_INDEX_FILE"])
                self.assertNotEqual(shadow, index)
                self.assertEqual(shadow.read_bytes(), index.read_bytes())
                self.assertEqual(shadow.stat().st_mtime_ns, index.stat().st_mtime_ns)
                copies.append(shadow)
            return original_run(command, *args, **kwargs)

        with patch.object(subprocess, "run", side_effect=observe):
            self._require_read_only(self.rejection)
        self.assertEqual(len(copies), 2)
        self.assertTrue(all(not p.parent.exists() for p in copies))

    def test_exception_cleans_private_copy_without_real_index_write(self):
        import subprocess
        import resolve_t20_v6_source as source
        helper = getattr(source, "readonly_git_diff", None)
        self.assertTrue(callable(helper), "disposable-index comparison is not implemented")
        before = self._snapshot()
        original_run = subprocess.run
        copies = []

        def interrupt(command, *args, **kwargs):
            if "diff" in command:
                shadow = pathlib.Path(kwargs["env"]["GIT_INDEX_FILE"])
                self.assertTrue(shadow.exists())
                copies.append(shadow)
                raise RuntimeError("synthetic interrupted diff")
            return original_run(command, *args, **kwargs)

        with patch.object(subprocess, "run", side_effect=interrupt):
            with self.assertRaisesRegex(RuntimeError, "synthetic interrupted diff"):
                helper(self.repo, ["git", "diff", "--name-status", "-z", self.baseline, "--"])
        after = self._snapshot()
        self._diff_observation = {"before": before, "after": after,
                                  "result": "expected synthetic interruption"}
        self.assertEqual(before, after)
        self.assertEqual(len(copies), 1)
        self.assertFalse(copies[0].parent.exists())

    def test_unsupported_index_dependencies_fail_before_diff(self):
        import struct
        import subprocess
        import resolve_t20_v6_source as source
        helper = getattr(source, "readonly_git_diff", None)
        self.assertTrue(callable(helper), "disposable-index comparison is not implemented")
        index = self.repo / ".git" / "index"
        original = index.read_bytes()
        linked = original[:-20] + b"link" + struct.pack(">I", 20) + b"\0" * 20
        versioned = original[:4] + struct.pack(">I", 3) + original[8:-20]
        cases = (("split-extension", linked + hashlib.sha1(linked).digest(), False),
                 ("unsupported-version", versioned + hashlib.sha1(versioned).digest(), False),
                 ("enabled-split-config", original, True))
        original_run = subprocess.run
        observed = []

        def no_diff(command, *args, **kwargs):
            self.assertNotIn("diff", command, "unsupported index reached comparison")
            return original_run(command, *args, **kwargs)

        try:
            for label, data, split in cases:
                with self.subTest(kind=label):
                    index.write_bytes(data)
                    self._git("config", "core.splitIndex", "true" if split else "false")
                    with patch.object(subprocess, "run", side_effect=no_diff):
                        result = helper(self.repo, ["git", "diff", "--name-status",
                                                   "-z", self.baseline, "--"])
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(result.stdout, b"")
                    self.assertEqual(index.read_bytes(), data)
                    observed.append({"kind": label, "returncode": result.returncode,
                                     "before_sha256": hashlib.sha256(data).hexdigest(),
                                     "after_sha256": hashlib.sha256(index.read_bytes()).hexdigest()})
        finally:
            index.write_bytes(original)
            self._git("config", "core.splitIndex", "false")
        self._diff_observation = {"unsupported_cases": observed,
                                  "restored_fixture_index": index.read_bytes() == original}


if __name__ == '__main__':
    unittest.main()

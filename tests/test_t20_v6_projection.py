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



if __name__ == '__main__':
    unittest.main()

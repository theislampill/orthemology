"""Negative controls for the independent T20 v6 public object."""
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
import ast
import collections
import io
from pathlib import Path, PurePosixPath
import os
import re
import shutil
import stat
import subprocess
import types
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from validate_t20_v6_projection import check_object, safe_path, private_locators, private_uuid, origin_reference_text, PREFIX
from validate_decision_dependencies import is_supersession_registry
import validate_decision_dependencies as decisions
import validate_t20_v6_projection as projection
from resolve_t20_v6_source import lean_imports, validate_graph
from validate_repo import preserved_t20_detector_text
from test_repo_validator_corpus import changed_bytes, run_validator

def _reader_fixture_entries(repo, revision, paths):
    """Read only the real historical blobs consumed by this reader fixture.

    The production whole-tree census is unchanged. Missing objects and wrong
    native identities remain errors; no size or entry is synthesized.
    """
    import subprocess
    if (not isinstance(revision, str) or len(revision) != 40
            or any(char not in '0123456789abcdef' for char in revision)):
        raise ValueError('fixture requires an exact commit identity')
    selected = sorted(paths)
    if (not selected or len(selected) != len(set(selected))
            or any(not isinstance(path, str) or not path or path.startswith('/')
                   or '\\' in path or '\0' in path
                   or any(part in ('', '.', '..') for part in path.split('/'))
                   for path in selected)):
        raise ValueError('fixture requires finite ordinary relative paths')
    def git(*args):
        result = subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=repo, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required pinned fixture Git objects are unavailable')
        return result.stdout
    if git('rev-parse', '--verify', revision + '^{commit}').decode().strip() != revision:
        raise ValueError('fixture requires the exact native commit')
    rows = []
    for path in selected:
        body = git('ls-tree', '-l', '-z', revision, '--', path)
        if not body.endswith(b'\0') or body.count(b'\0') != 1:
            raise ValueError('fixture requires one native entry for each selected path')
        metadata, actual_path = body[:-1].split(b'\t', 1)
        mode, kind, oid, size = metadata.decode('ascii').split()
        if actual_path.decode('utf-8') != path or mode != '100644' or kind != 'blob':
            raise ValueError('fixture historical path, kind or mode differs')
        rows.append({'path': path, 'mode': mode, 'kind': kind,
                     'git_oid': oid, 'bytes': int(size)})
    return rows



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
        cls.indexed = {r['path']: r for r in _reader_fixture_entries(
            projection.ROOT, cls.REV,
            set(cls.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS) | set(cls.BLOBS))}

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
        # Keep this fixture at its independently qualified seven-path scope.
        self.owners['historical_source_bindings'] = [
            r for r in self.owners['historical_source_bindings']
            if r['path'] in set(self.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS) | set(self.BLOBS)]
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



class FisherOwnerMigrationTests(unittest.TestCase):
    """One authentic ADD_EXACT original; no broader missing-file fallback."""

    REV = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
    PATH = 'research/t20-v6-20261012/sources/178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b/finite-audit-gradient-classification.md'
    BLOB = '4dd0bce99ab60c34752bda1e4102341b67350c79'
    SHA = '178adaf0d9c8f19f2d0eaf5b8118b157e582b356fa9dddfee6ba8ebe6e5da71b'
    CHAPTER = 'mathematics/information-and-inquiry.md'
    REVIEW = 'docs/scientific-consolidation-review.md'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'

    @classmethod
    def setUpClass(cls):
        import subprocess
        import check_reader_pilot
        import resolve_t20_v6_source
        cls.reader, cls.resolver = check_reader_pilot, resolve_t20_v6_source
        cls.objects = pathlib.Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'objects'], cwd=projection.ROOT,
            text=True).strip())
        if not cls.objects.is_absolute():
            cls.objects = projection.ROOT / cls.objects
        cls.original = subprocess.check_output(
            ['git', 'show', cls.REV + ':' + cls.PATH], cwd=projection.ROOT)
        cls.indexed = {r['path']: r for r in _reader_fixture_entries(
            projection.ROOT, cls.REV, set(cls.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS)
            | set(MediatorOwnerMigrationTests.BLOBS) | {cls.PATH})}

    def setUp(self):
        import subprocess
        self.tmp = tempfile.TemporaryDirectory(prefix='fisher-owner-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.git/objects/info/alternates').write_text(str(self.objects.resolve()) + '\n')
        # Public current owners and chapters are copied as data, not executed.
        # The other seven original prose paths stay absent in this fixture.
        for name in (self.CHAPTER, self.REVIEW, self.OWNER, self.CROSS,
                     'epistemology/recognition-warrant-and-restoration.md',
                     MediatorOwnerMigrationTests.CHAPTER, MediatorOwnerMigrationTests.GUIDE):
            self.put(name, (projection.ROOT / name).read_bytes())
        self.put(self.PATH, self.original)
        self.assertEqual((len(self.original), hashlib.sha256(self.original).hexdigest()),
                         (29666, self.SHA))
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                        '100644,' + self.BLOB + ',' + self.PATH], cwd=self.root, check=True)
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                        '100644,7c6a9bfdeaf8372d3ea73ff8a06f4aefb17ef838,' +
                        MediatorOwnerMigrationTests.GUIDE], cwd=self.root, check=True)
        self.owners = json.loads((self.root / self.OWNER).read_bytes())
        # This pre-existing fixture retains its independently qualified eight paths.
        self.owners['historical_source_bindings'] = [r for r in self.owners['historical_source_bindings']
            if r['path'] in set(self.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS)
            | set(MediatorOwnerMigrationTests.BLOBS) | {self.PATH}]
        self.put(self.OWNER, json.dumps(self.owners).encode())
        self.cross = json.loads((self.root / self.CROSS).read_bytes())
        self.additions = {r['path']: r for r in self.owners['source_additions']}
        self.row = dict(source_sha256=self.SHA, source_bytes=29666,
                        disposition='ADD_EXACT', repository_path=self.PATH,
                        public_sha256=self.SHA, public_bytes=29666,
                        repository_revision=self.REV, git_blob=self.BLOB)

    def put(self, path, body):
        node = self.root / path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(body)
        node.chmod(0o644)

    def resolve(self, row=None):
        return self.resolver.source_bytes(self.root, self.row if row is None else row)

    def reject(self, row=None):
        import subprocess
        selected = self.row if row is None else row
        self.assertTrue(check_object(self.root, selected))
        with self.assertRaises((ValueError, OSError, subprocess.CalledProcessError)):
            self.resolve(selected)

    def test_authentic_present_absent_and_staged_absent_states_preserve_evidence(self):
        from copy import deepcopy
        import subprocess
        saved = deepcopy(self.row)
        for staged in (True, False):
            if not staged:
                subprocess.run(['git', 'update-index', '--force-remove', '--', self.PATH],
                               cwd=self.root, check=True)
            for present in (True, False):
                with self.subTest(staged=staged, present=present):
                    if present: self.put(self.PATH, self.original)
                    else: (self.root / self.PATH).unlink()
                    index = (self.root / '.git/index').read_bytes()
                    self.assertEqual(check_object(self.root, self.row), [])
                    self.assertEqual(self.resolve(), self.original)
                    self.assertEqual((self.root / self.PATH).exists(), present)
                    self.assertEqual((self.root / '.git/index').read_bytes(), index)
                    self.assertEqual(self.row, saved)

    def test_original_five_mediator_seven_and_fisher_eight_remain_distinct(self):
        from copy import deepcopy
        bindings = deepcopy(self.owners['historical_source_bindings'])
        five = [r for r in bindings if r['repository_revision'] == projection.BASE]
        seven = [r for r in bindings if r['path'] != self.PATH]
        self.assertEqual((len(five), len(seven), len(bindings)), (5, 7, 8))
        for selected in (five, seven, bindings):
            with self.subTest(population=len(selected)):
                self.owners['historical_source_bindings'] = deepcopy(selected)
                self.put(self.OWNER, json.dumps(self.owners).encode())
                admitted, errors = self.reader.check_historical_sources(
                    self.root, self.indexed, self.owners, self.cross, self.additions)
                self.assertEqual(errors, [])
                self.assertEqual(set(admitted), {r['path'] for r in selected})
                if len(selected) == 8:
                    self.assertEqual(admitted[self.PATH], self.original)
        fisher = next(r for r in bindings if r['path'] == self.PATH)
        variants = (five + [fisher], bindings[:-2] + [fisher],
                    bindings + [deepcopy(fisher)],
                    [dict(fisher, path=self.PATH.replace('.md', '_unqualified.md'))] + seven)
        for selected in variants:
            with self.subTest(invalid_population=len(selected)):
                self.owners['historical_source_bindings'] = deepcopy(selected)
                self.put(self.OWNER, json.dumps(self.owners).encode())
                self.assertTrue(self.reader.check_historical_sources(
                    self.root, self.indexed, self.owners, self.cross, self.additions)[1])

    def test_add_exact_revision_blob_path_hash_and_size_are_exact(self):
        for field, value in (
                ('repository_revision', projection.BASE), ('repository_revision', 'HEAD'),
                ('repository_revision', '0' * 40), ('git_blob', '0' * 40),
                ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                ('source_bytes', 29667), ('public_bytes', 29667), ('disposition', 'REUSE'),
                ('repository_path', self.PATH.replace('.md', '_unqualified.md'))):
            with self.subTest(field=field, value=value):
                self.reject(dict(self.row, **{field: value}))

    def test_present_bytes_do_not_replace_missing_authentic_git_objects(self):
        (self.root / '.git/objects/info/alternates').unlink()
        self.reject()

    def test_wrong_physical_bytes_mode_directory_or_symlink_are_rejected(self):
        target = self.root / self.PATH
        for kind in ('bytes', 'executable', 'directory', 'symlink'):
            with self.subTest(kind=kind):
                try:
                    if kind == 'bytes': target.write_bytes(self.original + b'changed\n')
                    elif kind == 'executable': target.chmod(0o755)
                    else:
                        target.unlink()
                        if kind == 'directory': target.mkdir()
                        else: target.symlink_to('missing-original')
                    self.reject()
                finally:
                    if target.is_symlink(): target.unlink()
                    elif target.is_dir(): target.rmdir()
                    self.put(self.PATH, self.original)
        parent = target.parent
        alternate = parent.with_name(parent.name + '-copy')
        parent.rename(alternate)
        try:
            parent.symlink_to(alternate, target_is_directory=True)
            self.reject()
        finally:
            parent.unlink()
            alternate.rename(parent)

    def test_wrong_staged_blob_mode_link_and_conflict_cannot_hide(self):
        import subprocess
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'],
                    cwd=self.root, input=b'wrong staged Fisher source\n').decode().strip()
        for present in (True, False):
            if not present: (self.root / self.PATH).unlink()
            for mode, blob in (('100644', wrong), ('100755', self.BLOB),
                               ('120000', wrong), (None, None)):
                with self.subTest(present=present, mode=mode):
                    subprocess.run(['git', 'update-index', '--force-remove', '--', self.PATH],
                                   cwd=self.root, check=True)
                    if mode:
                        subprocess.run(['git', 'update-index', '--add', '--cacheinfo',
                                        mode + ',' + blob + ',' + self.PATH],
                                       cwd=self.root, check=True)
                    else:
                        entries = ''.join('100644 ' + oid + ' ' + stage + '\t' + self.PATH + '\n'
                            for oid, stage in ((self.BLOB, '1'), (wrong, '2'), (self.BLOB, '3')))
                        subprocess.run(['git', 'update-index', '--index-info'],
                                       cwd=self.root, input=entries.encode(), check=True)
                    self.reject()
                    self.assertEqual((self.root / self.PATH).exists(), present)

    def test_changed_or_missing_current_chapter_and_review_reject_history(self):
        for path in (self.CHAPTER, self.REVIEW):
            original = (self.root / path).read_bytes()
            for variant in ('changed', 'missing', 'executable', 'symlink'):
                with self.subTest(path=path, variant=variant):
                    try:
                        if variant == 'changed': self.put(path, original + b'changed current prose\n')
                        elif variant == 'executable': (self.root / path).chmod(0o755)
                        else:
                            (self.root / path).unlink()
                            if variant == 'symlink': (self.root / path).symlink_to('missing-current')
                        self.reject()
                    finally:
                        if (self.root / path).is_symlink(): (self.root / path).unlink()
                        self.put(path, original)

    def test_wrong_owner_source_form_relation_and_journey_reject_history(self):
        from copy import deepcopy
        for change in ('owner', 'binding', 'source', 'form', 'relation', 'journey', 'route'):
            with self.subTest(change=change):
                owners, cross = deepcopy(self.owners), deepcopy(self.cross)
                if change == 'owner':
                    next(r for r in owners['source_additions']
                         if r['key'] == 'consolidated-information-and-inquiry')['git_oid'] = '0' * 40
                elif change == 'binding':
                    next(r for r in owners['historical_source_bindings']
                         if r['path'] == self.PATH)['repository_revision'] = projection.BASE
                elif change == 'source':
                    cross['sources']['fisher']['sha256'] = '0' * 64
                elif change == 'form':
                    for work in cross['works']:
                        for form in work.get('reading_forms', []):
                            if form.get('source') == 'fisher': form['relationship'] = 'authored-source'
                elif change == 'relation':
                    cross['relations'] = [r for r in cross['relations']
                        if not (r.get('from') == 'fisher' and r.get('kind') ==
                                'logical-content-incorporated-historical-source-retained')]
                elif change == 'journey':
                    cross['reader_journeys'][0]['source_keys'].append('fisher')
                else:
                    next(j for j in cross['reader_journeys'] if j['id'] == 'J06')['source_keys'].remove(
                        'consolidated-information-and-inquiry')
                self.put(self.OWNER, json.dumps(owners).encode())
                self.put(self.CROSS, json.dumps(cross).encode())
                self.reject()
        self.put(self.OWNER, json.dumps(self.owners).encode())
        self.put(self.CROSS, json.dumps(self.cross).encode())

    def test_inventory_admits_only_the_exact_authenticated_fisher_absence(self):
        from copy import deepcopy
        rows = [deepcopy(self.row)]
        saved = deepcopy(rows)
        self.put(projection.MANIFEST, b'{}\n')
        self.put(projection.PREFIX + '/PUBLIC_CONTROLS.json', b'{}\n')
        self.assertEqual(projection.check_public_inventory(self.root, rows, {'files': {}}), [])
        (self.root / self.PATH).unlink()
        self.assertEqual(projection.check_public_inventory(self.root, rows, {'files': {}}), [])
        self.assertEqual(rows, saved)
        self.assertFalse((self.root / self.PATH).exists())
        wrong = [dict(self.row, repository_revision=projection.BASE)]
        self.assertTrue(projection.check_public_inventory(self.root, wrong, {'files': {}}))
        other = self.PATH.replace('.md', '_unqualified.md')
        self.assertTrue(projection.check_public_inventory(
            self.root, rows + [dict(self.row, repository_path=other)], {'files': {}}))
        self.put(other, b'undeclared fixture source\n')
        self.assertTrue(projection.check_public_inventory(self.root, rows, {'files': {}}))

    def test_reader_pages_link_current_proof_and_keep_exact_original_section(self):
        local = '../../mathematics/information-and-inquiry.md#'
        expected = {
            'RESEARCH-ATLAS.md': '6-the-categorical-fisher-dynamics-of-the-full-source',
            'PAPER-CATALOGUE.md': '5-fixed-audits-and-the-value-of-inquiry',
            'RESULT-INDEX.md': '6-the-categorical-fisher-dynamics-of-the-full-source',
            'CURRENT-FRONTIERS.md': '8-preserving-one-objective-versus-preserving-an-entire-metric',
        }
        current = self.reader.markdown_index((self.root / self.CHAPTER).read_text())
        original = 'https://github.com/theislampill/orthemology/blob/' + self.REV + '/' + self.PATH
        for name, anchor in expected.items():
            text = (projection.ROOT / 'docs/reader' / name).read_text()
            links = [href for _, href in self.reader.markdown_index(text)['links']]
            self.assertIn(local + anchor, links)
            self.assertIn(anchor, current['anchors'])
            self.assertIn(original, links)
            self.assertNotIn('../../' + self.PATH, links)
        text = (projection.ROOT / 'docs/reader/RESULT-INDEX.md').read_text()
        self.assertIn(original + '#9-decisive-controls-and-the-connection-to-inquiry-value',
                      [href for _, href in self.reader.markdown_index(text)['links']])


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



class TypedProseOwnerMigrationTests(unittest.TestCase):
    """Four prose identities migrate; original proofs, reviews and roles survive."""

    REV = 'a7ff0e33d1a299db640041c46b1af81ca70851f6'
    OWNER = 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json'
    CROSS = 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json'
    CHAPTER = 'logic/encodings-and-witnesses.md'
    REVIEW = 'docs/scientific-consolidation-review.md'
    WORK = 'consolidated-encodings-and-witnesses'
    ITEMS = {
        't13-opaque': ('b99fb16058f99ce5db66dd7a02e7515ede5157a002a6e76fc29d0f1bd8d65236',
            'OPAQUE_ATOM_COMPLETENESS_PROOF_v3.md', 'ab7ccee9a98d5a88b8b79a6f0d6a010298bf3204',
            26969, 'identity-src-18324561d5a479234e08', '103-equal-evaluation-need-not-preserve-a-supplied-typing'),
        't13-residual': ('7ff286710275b8873e2847ef21b9a30e70c20f465b6bb680569b8f107b484f3e',
            'RESIDUAL_IDENTITY_COMPLETENESS_FEASIBILITY_v1.md', '0692dd6d775e0391498c97c5b77e8c83cf32eb41',
            11482, 'identity-src-36405a21fb515a544d13', '105-the-identity-question-that-packing-leaves-open'),
        't13-bridge': ('02f2ba85547a0798288ec5d307f06fa5b239b8cb9e0faa4b7c7a6ba303097bbe',
            'HYPOTHETICAL_ATOM_APPLICATION_BRIDGE_v2.md', 'a4d90c7d566d79394ca4755bf1d792e810d66880',
            19906, 'identity-src-210a260c6b65330bbabb', '104-what-the-bridge-repairs'),
        't14-separation': ('5d58087eab7e247235ec159abc17f6dc6d5779dc7722518f06d5040b25414e3a',
            'Intensional_Identity_Separation_and_Closed_Identity_Conversion.md', '4920e71de4ac0c17fa8a93f02cd891d65ea8ad74',
            48239, 'identity-src-ae495071a75fcc65a509', '107-full-rule-separation-and-the-exact-closed-criterion'),
    }
    GUIDES = {
        'experiments/orthemology-v5-successors/groups/t13-identity/README.md':
            {'t13-opaque': 1, 't13-residual': 2, 't13-bridge': 1},
        'experiments/orthemology-v5-successors/groups/t14-identity/README.md':
            {'t14-separation': 5},
    }

    @classmethod
    def setUpClass(cls):
        import importlib.util
        import subprocess
        import check_reader_pilot
        import resolve_t20_v6_source
        cls.reader, cls.resolver = check_reader_pilot, resolve_t20_v6_source
        cls.project = projection.ROOT
        spec = importlib.util.spec_from_file_location('typed_v5_owner',
            pathlib.Path(cls.resolver.__file__).with_name('validate_v5_successors.py'))
        cls.v5 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.v5)
        cls.paths = {k: 'experiments/orthemology-v5-successors/source-store/' + row[0] + '/' + row[1]
                     for k, row in cls.ITEMS.items()}
        cls.owners_original = json.loads((cls.project / cls.OWNER).read_bytes())
        cls.cross_original = json.loads((cls.project / cls.CROSS).read_bytes())
        cls.earlier = [r for r in cls.owners_original['historical_source_bindings']
                       if r['path'] in set(cls.resolver.ORIGINAL_HISTORICAL_PROSE_PATHS)
                       | set(MediatorOwnerMigrationTests.BLOBS) | {FisherOwnerMigrationTests.PATH}]
        if len(cls.earlier) != 8:
            raise ValueError('This fixture requires the eight preserved earlier bindings')
        cls.bindings = cls.earlier + [dict(path=cls.paths[key], repository_revision=cls.REV,
            git_blob=row[2], role='historical-source', reading_source=cls.WORK,
            basis='scientific-consolidation-review') for key, row in cls.ITEMS.items()]
        cls.original = {}
        cls.object_data = {}

        def acquire(oid, kind):
            if oid not in cls.object_data:
                body = subprocess.check_output(['git', '--no-replace-objects', 'cat-file', kind, oid],
                                               cwd=cls.project)
                cls.object_data[oid] = (kind, body)
            return cls.object_data[oid][1]

        def acquire_path(revision, path):
            attributes = subprocess.check_output(['git', '--no-replace-objects', 'ls-tree', '-z',
                revision, '--', '.gitattributes'], cwd=cls.project)
            if attributes:
                metadata, name = attributes.rstrip(b'\0').split(b'\t')
                mode, kind, oid = metadata.decode().split()
                if mode != '100644' or kind != 'blob' or name != b'.gitattributes':
                    raise ValueError('unsafe fixture Git attributes dependency')
                acquire(oid, kind)
            acquire(revision, 'commit')
            tree = subprocess.check_output(['git', '--no-replace-objects', 'rev-parse', revision + '^{tree}'],
                                           cwd=cls.project).decode().strip()
            parts = path.split('/')
            for index, part in enumerate(parts):
                acquire(tree, 'tree')
                entry = subprocess.check_output(['git', '--no-replace-objects', '--literal-pathspecs',
                    'ls-tree', '-z', tree, '--', part], cwd=cls.project)
                metadata, actual = entry.rstrip(b'\0').split(b'\t')
                mode, kind, oid = metadata.decode().split()
                if actual.decode() != part:
                    raise ValueError('wrong fixture Git path')
                if index == len(parts) - 1:
                    if mode != '100644' or kind != 'blob':
                        raise ValueError('fixture original must be regular data')
                    return acquire(oid, kind), oid
                if kind != 'tree':
                    raise ValueError('fixture path ancestor is not a tree')
                tree = oid

        for row in cls.bindings:
            body, oid = acquire_path(row['repository_revision'], row['path'])
            if oid != row['git_blob']:
                raise ValueError('fixture source blob differs')
            cls.original[row['path']] = body
        cls.guide_original = {}
        cls.guide_blobs = {}
        for path in [*cls.GUIDES, cls.resolver.MEDIATOR_GUIDE]:
            cls.guide_original[path], cls.guide_blobs[path] = acquire_path(cls.REV, path)
        # The shared t14 guide also authenticates the finite administrative
        # catalogue. Supply its exact native traversal trees, not record bodies.
        def acquire_tree_path(revision, relative):
            acquire(revision, 'commit')
            tree = subprocess.check_output(['git', '--no-replace-objects', 'rev-parse',
                revision + '^{tree}'], cwd=cls.project).decode().strip()
            for part in relative.rstrip('/').split('/'):
                acquire(tree, 'tree')
                raw = subprocess.check_output(['git', '--no-replace-objects', '--literal-pathspecs',
                    'ls-tree', '-z', tree, '--', part], cwd=cls.project)
                metadata, actual = raw.rstrip(b'\0').split(b'\t')
                mode, kind, oid = metadata.decode().split()
                if actual.decode() != part or mode != '040000' or kind != 'tree':
                    raise ValueError('unsafe administrative fixture tree dependency')
                tree = oid
            acquire(tree, 'tree')
            descendants = subprocess.check_output(['git', '--no-replace-objects',
                'ls-tree', '-d', '-r', '-z', tree], cwd=cls.project)
            for entry in descendants.split(b'\0'):
                if not entry:
                    continue
                metadata, _ = entry.split(b'\t', 1)
                mode, kind, oid = metadata.decode().split()
                if mode != '040000' or kind != 'tree':
                    raise ValueError('administrative fixture descendant is not a tree')
                acquire(oid, kind)

        catalogue_revision = cls.resolver.ADMIN_RECORD_BASE
        for directory in sorted(cls.resolver.ADMIN_RECORD_NAMES):
            acquire_tree_path(catalogue_revision, directory)
        catalogue = subprocess.check_output(['git', '--no-replace-objects', 'ls-tree',
            '-rz', '--full-tree', catalogue_revision, '--', *sorted(cls.resolver.ADMIN_RECORD_NAMES)],
            cwd=cls.project)
        if (len(catalogue.rstrip(b'\0').split(b'\0')) != 236
                or hashlib.sha256(catalogue).hexdigest() != cls.resolver.ADMIN_RECORD_TREE_SHA256):
            raise ValueError('administrative fixture catalogue differs')
        for path in sorted(set(cls.GUIDES) & set(cls.resolver.ADMIN_GUIDES)):
            body, oid = acquire_path(catalogue_revision, path)
            if body != cls.guide_original[path] or oid != cls.guide_blobs[path]:
                raise ValueError('shared typed/administrative guide identity differs')
        cls.old_manifest, cls.old_manifest_blob = acquire_path(cls.REV, projection.MANIFEST)
        # This isolated fixture owns the twelve prose bindings above. Pin its
        # manifest form before later snapshot migrations, whose independent
        # source objects and snapshot owners are intentionally outside it.
        cls.current_manifest = json.loads(subprocess.check_output(
            ['git', '--no-replace-objects', 'show',
             '1beacf590a4f11079039582b42d98d63c563378b:' + projection.MANIFEST], cwd=cls.project))
        for key, item in cls.ITEMS.items():
            row = next(r for r in cls.current_manifest['objects'] if r['source_sha256'] == item[0])
            if (row.get('repository_path'), row.get('repository_revision'), row.get('git_blob')) != (
                    cls.paths[key], cls.REV, item[2]):
                raise ValueError('typed fixture predecessor binding differs')
            # The positive test must actually add all four bindings.
            del row['repository_revision']
            del row['git_blob']
        cls.source_map = json.loads((cls.project / 'docs/provenance/v5-successors/SOURCE_MAP.json').read_bytes())
        cls.projection_map = json.loads((cls.project / 'docs/provenance/v5-successors/PUBLIC_PROJECTION.json').read_bytes())
        cls.current_bodies = {p: (cls.project / p).read_bytes() for p in (
            cls.CHAPTER, cls.REVIEW, 'epistemology/recognition-warrant-and-restoration.md',
            'mathematics/information-and-inquiry.md', 'mathematics/collective-inquiry-and-strategic-coordination.md')}

    def setUp(self):
        from copy import deepcopy
        import subprocess
        self.tmp = tempfile.TemporaryDirectory(prefix='typed-owner-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        for oid, (kind, body) in self.object_data.items():
            got = subprocess.check_output(['git', 'hash-object', '-t', kind, '-w', '--stdin'],
                                          cwd=self.root, input=body).decode().strip()
            self.assertEqual(got, oid)
        for path, body in {**self.current_bodies, **self.original}.items():
            self.put(path, body)
        self.owners = deepcopy(self.owners_original)
        self.cross = deepcopy(self.cross_original)
        self.owners['historical_source_bindings'] = deepcopy(self.bindings)
        for key in self.ITEMS:
            work = next(w for w in self.cross['works'] if w['key'] == key)
            form = next(f for f in work['reading_forms'] if f['source'] == key)
            form['relationship'] = 'historical-source'
            relation = {'from': key, 'to': self.WORK,
                        'kind': 'logical-content-incorporated-historical-source-retained',
                        'basis': 'scientific-consolidation-review'}
            self.cross['relations'] = [r for r in self.cross['relations']
                if not (r.get('from') == key and r.get('kind') == relation['kind'])] + [relation]
        self.write_context()
        self.guides = {}
        for path, members in self.GUIDES.items():
            body = self.guide_original[path]
            for key, count in members.items():
                old = ('../../source-store/' + self.paths[key].split('/source-store/', 1)[1]).encode()
                self.assertEqual(body.count(old), count)
                body = body.replace(old, self.original_url(key).encode())
            self.guides[path] = body
        path = self.resolver.MEDIATOR_GUIDE
        old = ('../../source-store/' + self.resolver.MEDIATOR_COORDINATION.split('/source-store/', 1)[1]).encode()
        url = ('https://github.com/theislampill/orthemology/blob/' + self.REV + '/' +
               self.resolver.MEDIATOR_COORDINATION).encode()
        self.guides[path] = self.guide_original[path].replace(old, url)
        for path, body in self.guides.items():
            self.put(path, body)
        for row in self.bindings:
            self.stage(row['path'], row['git_blob'])
        for path, blob in self.guide_blobs.items():
            self.stage(path, blob)
        self.rows = {key: dict(source_sha256=row[0], source_bytes=row[3], disposition='REUSE',
            repository_path=self.paths[key], public_sha256=row[0], public_bytes=row[3],
            repository_revision=self.REV, git_blob=row[2]) for key, row in self.ITEMS.items()}
        public = set(self.paths.values()) | {self.resolver.MEDIATOR_COORDINATION}
        self.bundle = dict(sources=[deepcopy(r) for r in self.source_map['sources'] if r.get('public_path') in public],
            reviews=[], projection_reviews=[], public_allowlist=[deepcopy(r) for r in self.projection_map['allowlist']
                if r['path'] in public | set(self.guides)])

    def put(self, path, body):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        target.chmod(0o644)

    def stage(self, path, blob, mode='100644'):
        import subprocess
        subprocess.run(['git', 'update-index', '--add', '--cacheinfo', mode + ',' + blob + ',' + path],
                       cwd=self.root, check=True)

    def write_context(self):
        self.put(self.OWNER, (json.dumps(self.owners) + '\n').encode())
        self.put(self.CROSS, (json.dumps(self.cross) + '\n').encode())

    def original_url(self, key):
        return 'https://github.com/theislampill/orthemology/blob/' + self.REV + '/' + self.paths[key]

    def reject(self, key, row=None):
        selected = self.rows[key] if row is None else row
        self.assertTrue(projection.check_object(self.root, selected))
        with self.assertRaises((ValueError, OSError)):
            self.resolver.source_bytes(self.root, selected)

    def test_exact_four_public_sources_authenticate_present(self):
        for key, spec in self.ITEMS.items():
            with self.subTest(source=key):
                body = self.original[self.paths[key]]
                self.assertEqual((len(body), hashlib.sha256(body).hexdigest()), (spec[3], spec[0]))
                try:
                    actual = self.resolver.source_bytes(self.root, self.rows[key])
                except (ValueError, OSError) as error:
                    self.fail('exact typed source owner route rejected: ' + str(error))
                self.assertEqual(actual, body)
                self.assertEqual(projection.check_object(self.root, self.rows[key]), [])
        # Physical bytes never substitute for the required exact history object.
        key = 't13-opaque'
        blob = self.ITEMS[key][2]
        (self.root / '.git/objects' / blob[:2] / blob[2:]).unlink()
        self.assertTrue((self.root / self.paths[key]).is_file())
        self.reject(key)

    def test_only_four_typed_absences_use_exact_objects_without_writes(self):
        for key in self.ITEMS:
            (self.root / self.paths[key]).unlink()
        before = (self.root / '.git/index').read_bytes()
        for key in self.ITEMS:
            self.assertEqual(self.resolver.source_bytes(self.root, self.rows[key]), self.original[self.paths[key]])
            self.assertEqual(projection.check_object(self.root, self.rows[key]), [])
            self.assertFalse((self.root / self.paths[key]).exists())
        self.assertEqual((self.root / '.git/index').read_bytes(), before)
        self.assertTrue(all((self.root / r['path']).is_file() for r in self.earlier))

    def test_wrong_typed_identity_revision_role_and_alias_are_rejected(self):
        for key in self.ITEMS:
            for field, wrong in [('repository_revision', 'HEAD'), ('repository_revision', projection.BASE),
                    ('git_blob', '0' * 40), ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                    ('source_bytes', 1), ('public_bytes', 1), ('disposition', 'ADD_EXACT'),
                    ('repository_path', self.paths[key].replace('.md', '_alias.md'))]:
                with self.subTest(source=key, field=field):
                    self.reject(key, dict(self.rows[key], **{field: wrong}))

    def test_present_typed_corruption_symlink_and_executable_cannot_fall_back(self):
        for key in self.ITEMS:
            path = self.paths[key]
            target = self.root / path
            for kind in ('bytes', 'symlink', 'executable', 'directory'):
                with self.subTest(source=key, kind=kind):
                    try:
                        if kind == 'bytes': target.write_bytes(self.original[path] + b'wrong\n')
                        elif kind == 'executable': target.chmod(0o755)
                        else:
                            target.unlink()
                            if kind == 'symlink': target.symlink_to('absent-original')
                            else: target.mkdir()
                        self.reject(key)
                    finally:
                        if target.is_symlink(): target.unlink()
                        elif target.is_dir(): target.rmdir()
                        self.put(path, self.original[path])

    def test_staged_wrong_blob_mode_and_conflict_reject_present_typed_prose(self):
        import subprocess
        wrong = subprocess.check_output(['git', 'hash-object', '-w', '--stdin'], cwd=self.root,
                                        input=b'wrong typed staged body\n').decode().strip()
        for key, spec in self.ITEMS.items():
            path = self.paths[key]
            for mode, blob in [('100644', wrong), ('100755', spec[2]), ('120000', wrong)]:
                with self.subTest(source=key, mode=mode):
                    self.stage(path, blob, mode)
                    self.reject(key)
            subprocess.run(['git', 'update-index', '--force-remove', '--', path], cwd=self.root, check=True)
            entries = ''.join('100644 ' + oid + ' ' + stage + '\t' + path + '\n'
                for oid, stage in [(spec[2], '1'), (wrong, '2'), (spec[2], '3')])
            subprocess.run(['git', 'update-index', '--index-info'], cwd=self.root,
                           input=entries.encode(), check=True)
            self.reject(key)
            subprocess.run(['git', 'update-index', '--force-remove', '--', path], cwd=self.root, check=True)
            self.stage(path, spec[2])

    def test_changed_current_logic_or_review_rejects_the_typed_family(self):
        for path in (self.CHAPTER, self.REVIEW):
            try:
                self.put(path, self.current_bodies[path] + b'changed edition\n')
                for key in self.ITEMS: self.reject(key)
            finally:
                self.put(path, self.current_bodies[path])

    def test_incomplete_family_formal_role_and_support_loss_reject_history(self):
        from copy import deepcopy
        original_owners, original_cross = deepcopy(self.owners), deepcopy(self.cross)
        for fault in ('missing-source', 'duplicate-source', 'authored-form', 'formal-role', 'support', 'support-identity'):
            self.owners, self.cross = deepcopy(original_owners), deepcopy(original_cross)
            work = next(w for w in self.cross['works'] if w['key'] == 't14-separation')
            if fault == 'missing-source': self.owners['historical_source_bindings'].pop()
            elif fault == 'duplicate-source': self.owners['historical_source_bindings'].append(deepcopy(self.bindings[-1]))
            elif fault == 'authored-form': work['reading_forms'][0]['relationship'] = 'authored-source'
            elif fault == 'formal-role': work['reading_forms'][1]['relationship'] = 'historical-source'
            elif fault == 'support': work['supporting_source_keys'].remove('t14-suite')
            else: self.cross['sources']['t14-separation-lean']['sha256'] = '0' * 64
            self.write_context()
            with self.subTest(fault=fault):
                for key in self.ITEMS: self.reject(key)
        self.owners, self.cross = original_owners, original_cross
        self.write_context()

    def test_only_literal_typed_guide_adaptations_preserve_original_evidence(self):
        for path in self.GUIDES:
            self.assertEqual(self.resolver.typed_guide_source_bytes(self.root, path), self.guide_original[path])
            for body in (self.guide_original[path], self.guides[path] + b'changed prose\n',
                         self.guides[path].replace(self.REV.encode(), b'HEAD', 1)):
                try:
                    self.put(path, body)
                    for key in self.ITEMS: self.reject(key)
                finally:
                    self.put(path, self.guides[path])
            self.stage(path, self.guide_blobs[path], '100755')
            for key in self.ITEMS: self.reject(key)
            self.stage(path, self.guide_blobs[path])

    def test_v5_keeps_exact_source_and_allowlist_rows_for_typed_absence(self):
        from copy import deepcopy
        original = deepcopy(self.bundle)
        sources, _, _ = self.v5._sources(self.bundle, self.root)
        self.v5._allowlist(self.bundle, self.root, sources)
        for key in self.ITEMS: (self.root / self.paths[key]).unlink()
        sources, _, _ = self.v5._sources(self.bundle, self.root)
        self.v5._allowlist(self.bundle, self.root, sources)
        self.assertEqual(self.bundle, original)
        self.assertTrue(all(not (self.root / self.paths[k]).exists() for k in self.ITEMS))
        row = next(r for r in self.bundle['sources'] if r['id'] == self.ITEMS['t13-opaque'][4])
        row['id'] = 'wrong-source-identity'
        with self.assertRaises(ValueError): self.v5._sources(self.bundle, self.root)
        self.bundle = deepcopy(original)
        sources, _, _ = self.v5._sources(self.bundle, self.root)
        allowed = next(r for r in self.bundle['public_allowlist'] if r['path'] == self.paths['t13-opaque'])
        allowed['kind'] = 'AUTHORED'
        with self.assertRaises(ValueError): self.v5._allowlist(self.bundle, self.root, sources)

    def test_reader_admits_exact_twelve_present_sources_and_rejects_partial_or_extra(self):
        from copy import deepcopy
        indexed = {r['path']: dict(kind='blob', mode='100644', git_oid=r['git_blob'],
                                  bytes=len(self.original[r['path']])) for r in self.bindings}
        additions = {r['path']: r for r in self.owners['source_additions']}
        admitted, errors = self.reader.check_historical_sources(self.root, indexed, self.owners, self.cross, additions)
        self.assertEqual(errors, [])
        self.assertEqual(set(admitted), {r['path'] for r in self.bindings})
        self.assertTrue(all((self.root / path).is_file() for path in admitted))
        for variant in (self.bindings[:-1], self.earlier + self.bindings[-1:],
                        self.bindings + [deepcopy(self.bindings[-1])]):
            altered = dict(self.owners, historical_source_bindings=variant)
            self.assertTrue(self.reader.check_historical_sources(self.root, indexed, altered, self.cross, additions)[1])

    def test_manifest_accepts_only_complete_four_exact_revision_blob_additions(self):
        from copy import deepcopy
        manifest = deepcopy(self.current_manifest)
        for key, spec in self.ITEMS.items():
            row = next(r for r in manifest['objects'] if r['source_sha256'] == spec[0])
            row.update(repository_revision=self.REV, git_blob=spec[2])
        baseline = dict(path=projection.MANIFEST, git_oid=self.old_manifest_blob)
        self.assertTrue(self.reader.permitted_historical_status_pin(self.root, baseline, json.dumps(manifest).encode()))
        for fault in ('partial', 'identity', 'role', 'count'):
            changed = deepcopy(manifest)
            row = next(r for r in changed['objects'] if r['source_sha256'] == self.ITEMS['t13-opaque'][0])
            if fault == 'partial': del row['repository_revision']
            elif fault == 'identity': row['public_sha256'] = '0' * 64
            elif fault == 'role': row['role'] = 'formal_component'
            else: changed['counts']['objects'] = -1
            with self.subTest(fault=fault):
                self.assertFalse(self.reader.permitted_historical_status_pin(self.root, baseline, json.dumps(changed).encode()))

    def test_reader_pages_reach_current_logic_and_exact_historical_witnesses(self):
        pages = {'APPLICATIONS.md': ['t13-bridge'],
                 'CURRENT-FRONTIERS.md': ['t13-residual', 't14-separation'],
                 'PAPER-CATALOGUE.md': list(self.ITEMS), 'RESEARCH-ATLAS.md': list(self.ITEMS),
                 'RESULT-INDEX.md': list(self.ITEMS)}
        anchors = self.reader.markdown_index(self.current_bodies[self.CHAPTER].decode())['anchors']
        for page, keys in pages.items():
            text = (self.project / 'docs/reader' / page).read_text()
            links = [href for _, href in self.reader.markdown_index(text)['links']]
            for key in keys:
                with self.subTest(page=page, source=key):
                    self.assertIn(self.ITEMS[key][5], anchors)
                    self.assertTrue('../../' + self.CHAPTER + '#' + self.ITEMS[key][5] in links,
                                    'missing current logic route: ' + page + ': ' + key)
                    self.assertTrue(self.original_url(key) in links,
                                    'missing exact historical witness: ' + page + ': ' + key)
                    self.assertFalse('../../' + self.paths[key] in links,
                                     'physical original still required by reader page: ' + page + ': ' + key)

    def test_canonical_reference_resolution_requires_exact_typed_history(self):
        import validate_internal_references as references
        previous = references.ROOT
        references.ROOT = str(self.root)
        try:
            for key in self.ITEMS:
                path = self.paths[key]
                with self.subTest(source=key):
                    self.assertTrue(references._resolves('docs/reader/PAPER-CATALOGUE.md', path))
                    (self.root / path).unlink()
                    self.assertTrue(references._resolves('docs/reader/PAPER-CATALOGUE.md', path),
                                    'canonical typed source reference still requires the physical body')
                    self.put(path, self.original[path] + b'changed source\n')
                    self.assertFalse(references._resolves('docs/reader/PAPER-CATALOGUE.md', path))
                    self.put(path, self.original[path])
                    self.assertFalse(references._resolves('docs/reader/PAPER-CATALOGUE.md',
                        path.replace('.md', '_unqualified.md')))
            self.put(self.CHAPTER, self.current_bodies[self.CHAPTER] + b'changed current edition\n')
            for key in self.ITEMS:
                self.assertFalse(references._resolves('docs/reader/PAPER-CATALOGUE.md', self.paths[key]))
        finally:
            references.ROOT = previous

    def test_retained_companion_link_uses_the_exact_original_typed_source(self):
        import validate_repo as repository
        from copy import deepcopy
        companion = ('experiments/orthemology-v5-successors/source-store/'
            '2c16dbf40f6a945785b51ddc230a0e1f78004fe716a0412492b4345be8c95734/'
            'Finite_Certificates_and_Inhabitation_Limits_for_P01AC_and_HasPlus_v1.md')
        self.put(companion, (self.project / companion).read_bytes())
        target = self.ITEMS['t14-separation'][1]
        sources = self.source_map['sources']
        self.assertTrue(repository.successor_packet_locator(self.root / companion, target, sources, self.root))
        path = self.paths['t14-separation']
        (self.root / path).unlink()
        self.assertTrue(repository.successor_packet_locator(self.root / companion, target, sources, self.root),
                        'retained companion reference still requires the physical typed prose')
        selected = next(r for r in sources if r.get('public_path') == path)
        self.assertEqual(repository._public_successor_bytes(selected, self.root), self.original[path])
        wrong = deepcopy(selected)
        wrong['id'] = 'wrong-typed-origin-source'
        self.assertIsNone(repository._public_successor_bytes(wrong, self.root))
        self.assertFalse(repository.successor_packet_locator(self.root / companion,
            target.replace('.md', '_unqualified.md'), sources, self.root))
        self.put(path, self.original[path] + b'changed original\n')
        self.assertFalse(repository.successor_packet_locator(self.root / companion, target, sources, self.root))


class ContinuationOwnerRootMigrationTests(unittest.TestCase):
    """Exercise the real protected-root gate with exact four-owner editions.

    The synthetic Git baseline contains authentic public historical owners.
    Only unrelated historical-prose and guide populations are excluded from
    this fixture; the owner primitive, index and both diff calls remain real.
    """

    @classmethod
    def setUpClass(cls):
        import validate_v5_successors as owners
        cls.owners = owners
        cls.paths = tuple(owners.PRESERVATION_OWNER_PATHS)
        cls.current = {
            name: owners._preservation_owner_body(
                projection.ROOT, name, owners.PRESERVATION_OWNER_SPARSE_PRIOR[name])
            for name in cls.paths
        }
        # All current ordinary bodies authenticate before any historical read.
        cls.original = {}
        for name in cls.paths:
            blob, sha, size = owners.PRESERVATION_OWNER_ORIGINAL[name]
            body = owners._preservation_owner_git(projection.ROOT, 'cat-file', 'blob', blob)
            actual_blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
            if (actual_blob, hashlib.sha256(body).hexdigest(), len(body)) != (blob, sha, size):
                raise ValueError('fixture historical owner identity differs')
            cls.original[name] = body

    def setUp(self):
        import os
        self.tmp = tempfile.TemporaryDirectory(prefix='continuation-root-owner-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = pathlib.Path(self.tmp.name)
        self.git_env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.git_env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                            GIT_CONFIG_SYSTEM=os.devnull, GIT_OPTIONAL_LOCKS='0',
                            GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='')
        self._git('init', '-q')
        self.extra = '/'.join(('docs', 'provenance', 'v5-research-continuations', 'unqualified-owner-control.md'))
        for name, body in self.original.items():
            self._put(name, body)
        self._put(self.extra, b'unrelated protected fixture\n')
        self._git('add', '--', *self.paths, self.extra)
        self._git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                  'commit', '-qm', 'exact historical owners in isolated fixture')
        self.baseline = self._git('rev-parse', 'HEAD').decode().strip()

    def _git(self, *args):
        import subprocess
        return subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs',
             '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
             '-c', 'core.untrackedCache=false', '-c', 'gc.auto=0',
             '-c', 'maintenance.auto=false', '-c', 'protocol.allow=never',
             '-c', 'init.templateDir=', *args],
            cwd=self.repo, env=self.git_env, capture_output=True, check=True).stdout

    def _put(self, name, body):
        node = self.repo / name
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(body)
        node.chmod(0o644)

    def _use_current(self):
        for name, body in self.current.items():
            self._put(name, body)
        self._git('add', '--', *self.paths)

    def _snapshot(self):
        return {
            'raw_index': (self.repo / '.git/index').read_bytes(),
            'logical_entries': self._git('ls-files', '--stage', '-z'),
            'bodies': {name: (self.repo / name).read_bytes() for name in (*self.paths, self.extra)},
        }

    def _gate(self, expected):
        before = self._snapshot()
        with patch.object(projection, 'BASE', self.baseline), \
             patch.object(projection, 'HISTORICAL_PROSE', {}), \
             patch.object(projection, 'TYPED_GUIDES', {}), \
             patch.object(projection, 'mediator_guide_source_bytes',
                          side_effect=ValueError('no mediator population in this fixture')):
            result = projection.check_preserved_roots(self.repo, {})
        self.assertEqual(result, expected)
        self.assertEqual(self._snapshot(), before, 'protected-root check changed the fixture or index')

    def test_original_owner_edition_needs_no_modification_allowance(self):
        self._gate([])

    def test_complete_current_owner_edition_is_accepted(self):
        self._use_current()
        self._gate([])

    def test_mixed_original_current_owner_edition_is_rejected(self):
        self._use_current()
        name = self.paths[0]
        self._put(name, self.original[name])
        self._git('add', '--', name)
        self._gate(['preserved v5 or prior T20 baseline changed'])

    def test_current_owner_worktree_tamper_is_rejected(self):
        self._use_current()
        name = self.paths[0]
        self._put(name, self.current[name] + b'\nunqualified worktree edit\n')
        self._gate(['preserved v5 or prior T20 baseline changed'])

    def test_unrelated_protected_modification_is_not_an_owner_allowance(self):
        self._use_current()
        self._put(self.extra, b'unqualified protected change\n')
        self._git('add', '--', self.extra)
        self._gate(['preserved v5 or prior T20 baseline changed'])

    def test_staged_owner_tamper_cannot_hide_behind_current_worktree(self):
        self._use_current()
        name = self.paths[0]
        self._put(name, self.current[name] + b'\nunqualified staged edit\n')
        self._git('add', '--', name)
        self._put(name, self.current[name])
        self._gate(['preserved v5 or prior T20 baseline changed'])


    def _public_registry_row(self):
        return dict(source_sha256='51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff',
                    source_bytes=192971, disposition='REUSE',
                    repository_path='experiments/orthemology-v5-continuations/registry.json',
                    public_sha256='51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff',
                    public_bytes=192971, repository_revision=self.baseline,
                    git_blob='d90b5647de1cf290d3b7dbe20a805983c75f0fcf')

    def _registry_projection(self, expected):
        import resolve_t20_v6_source as source
        row = self._public_registry_row()
        before = (self.repo / '.git/index').read_bytes()
        with patch.object(source, 'CONTINUATION_REGISTRY_REVISION', self.baseline, create=True), \
             patch.object(source, 'HISTORICAL_PROSE_REVISION', self.baseline), \
             patch.object(projection, 'BASE', self.baseline):
            errors = check_object(self.repo, row)
            if expected:
                self.assertEqual(errors, [])
                self.assertEqual(source.source_bytes(self.repo, row), self.original[row['repository_path']])
            else:
                self.assertTrue(errors)
                with self.assertRaises((ValueError, OSError)):
                    source.source_bytes(self.repo, row)
        self.assertEqual((self.repo / '.git/index').read_bytes(), before)

    def test_public_registry_original_and_current_owner_editions_resolve_original_identity(self):
        self._registry_projection(True)
        self._use_current()
        self._registry_projection(True)

    def test_public_registry_history_does_not_hide_missing_or_changed_current_owner(self):
        self._use_current()
        name = self.paths[0]
        self._put(name, self.current[name] + b'changed owner\n')
        self._registry_projection(False)
        (self.repo / name).unlink()
        self._registry_projection(False)

    def test_public_registry_history_does_not_hide_staged_owner_tampering(self):
        self._use_current()
        name = self.paths[0]
        self._put(name, self.current[name] + b'changed staged owner\n')
        self._git('add', '--', name)
        self._put(name, self.current[name])
        self._registry_projection(False)




def _checkpoint_binding_fixture_inputs(case):
    """Give record-shaped checkpoint fixtures a nonempty administrative history.

    Checkpoint aliases can share MANIFEST/INPUT_BINDINGS/SOURCE_BINDINGS names
    without belonging to the unique-body binding class. The real consumer still
    qualifies that class before admitting a deletion, so its history must exist
    in this isolated repository too. These two bodies are inert fixture data.
    """
    if not any(case.source.binding_record_candidate(path) for path in case.catalog):
        return {}
    case.binding_record = (case.source.CHECKPOINT_COPY_ROOT
                           + 'CP99/binding-record-fixture/INPUT_BINDINGS.json')
    case.binding_owner = 'docs/' 'checkpoint-binding-fixture-owner.json'
    result = {
        case.binding_record: b'{"fixture":"historical binding record","active":false}\n',
        case.binding_owner: b'{"fixture":"current binding role owner","active_inputs":[]}\n',
    }
    case.assertTrue(set(result).isdisjoint(case.bodies))
    return result


def _checkpoint_binding_fixture_history(case):
    """Rebind only synthetic coordinates; execute the unchanged native catalogue.

    Existing copied bodies are duplicated in this tree and must not become
    unique binding records. The expected class is the one literal fixture row,
    not a census obtained by accepting the production qualifier's output.
    Complete public/successor row pins and the eight active-record pins stay
    unchanged; no real public row is manufactured for the synthetic record.
    """
    if not case.binding_fixture:
        return
    blob = lambda body: hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
    known = {**case.bodies, case.extra: b'unrelated protected fixture\n', **case.binding_fixture}
    entries = case._git('ls-tree', '-rz', '--full-tree', case.baseline).split(b'\0')[:-1]
    expected = {('100644 blob ' + blob(body) + '\t' + path).encode()
                for path, body in known.items()}
    case.assertEqual(len(entries), len(known))
    case.assertEqual(set(entries), expected)
    record_blob = blob(case.binding_fixture[case.binding_record])
    owner_body = case.binding_fixture[case.binding_owner]
    vector = ('100644 blob ' + record_blob + '\t' + case.binding_record + '\0').encode()
    pins = {
        'BINDING_RECORD_BASE': case.baseline,
        'BINDING_RECORD_TREE': case._git('rev-parse', case.baseline + '^{tree}').decode().strip(),
        'BINDING_RECORD_ORIGINAL_COUNT': len(known),
        'BINDING_RECORD_COUNT': 1,
        'BINDING_RECORD_CLASS_SHA256': hashlib.sha256(vector).hexdigest(),
        'BINDING_RECORD_PATH_HASHES': frozenset((hashlib.sha256(case.binding_record.encode()).hexdigest(),)),
        'BINDING_RECORD_ROLE_OWNERS': {case.binding_owner: (
            blob(owner_body), hashlib.sha256(owner_body).hexdigest(), len(owner_body))},
    }
    for name, value in pins.items():
        binding_patch = patch.object(case.source, name, value)
        binding_patch.start()
        case.addCleanup(binding_patch.stop)
    case.assertNotIn(case.binding_record, case.source.BINDING_RECORD_CURRENT_REQUIRED)
    case.assertEqual(case.source._binding_record_catalog(case.repo), {case.binding_record: record_blob})


class CheckpointCopyMigrationTests(unittest.TestCase):
    """Real finite public bodies in isolated Git/index and reference fixtures.

    The original a7ff identities authenticate read-only before fixture creation.
    Each synthetic commit then carries exactly those same 172 public objects.
    No historical Python wrapper is executed or treated as currently qualified.
    """

    @classmethod
    def setUpClass(cls):
        import resolve_t20_v6_source as source
        cls.source = source
        if not callable(getattr(source, '_checkpoint_copy_catalog', None)):
            raise AssertionError('finite checkpoint copy route is not implemented')
        cls.catalog = source._checkpoint_copy_catalog()
        if len(cls.catalog) != 87:
            raise AssertionError('checkpoint fixture population differs')
        cls.bodies = {}
        for alias, binding in cls.catalog.items():
            body = source.checkpoint_copy_bytes(projection.ROOT, alias)
            cls.bodies[alias] = body
            previous = cls.bodies.setdefault(binding['canonical'], body)
            if previous != body:
                raise AssertionError('retained fixture body conflicts')
            if 'prior_canonical' in binding:
                former = binding['prior_canonical']
                if cls.bodies.setdefault(former, body) != body:
                    raise AssertionError('former provider fixture body conflicts')

    def setUp(self):
        import os
        self.tmp = tempfile.TemporaryDirectory(prefix='checkpoint-copy-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = pathlib.Path(self.tmp.name)
        self.git_env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        self.git_env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                            GIT_CONFIG_SYSTEM=os.devnull, GIT_OPTIONAL_LOCKS='0',
                            GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1',
                            GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='')
        self.environment = patch.dict(os.environ, self.git_env, clear=True)
        self.environment.start(); self.addCleanup(self.environment.stop)
        self._git('init', '-q')
        for name, body in self.bodies.items():
            self._put(name, body)
        self.extra = self.source.CHECKPOINT_COPY_ROOT + 'CP99/unqualified-fixture.md'
        self._put(self.extra, b'unrelated protected fixture\n')
        self.binding_fixture = _checkpoint_binding_fixture_inputs(self)
        for name, body in self.binding_fixture.items():
            self._put(name, body)
        self._git('add', '--', *self.bodies, self.extra, *self.binding_fixture)
        self._git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                  'commit', '-qm', 'authentic public checkpoint objects in isolated fixture')
        self.baseline = self._git('rev-parse', 'HEAD').decode().strip()
        self.base_patch = patch.object(self.source, 'CHECKPOINT_COPY_BASE', self.baseline)
        self.base_patch.start(); self.addCleanup(self.base_patch.stop)
        _checkpoint_binding_fixture_history(self)
        self.alias = next(iter(self.catalog))
        self.canonical = self.catalog[self.alias]['canonical']

    def _git(self, *args, input=None):
        import subprocess
        return subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs',
             '-c', 'core.hooksPath=/dev/null', '-c', 'core.fsmonitor=false',
             '-c', 'core.untrackedCache=false', '-c', 'gc.auto=0',
             '-c', 'maintenance.auto=false', '-c', 'protocol.allow=never',
             '-c', 'init.templateDir=', *args], cwd=self.repo, env=self.git_env,
            input=input, capture_output=True, check=True).stdout

    def _put(self, name, body):
        target=self.repo/name; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body); target.chmod(0o644)

    def _gate(self):
        before=(self.repo/'.git/index').read_bytes()
        with patch.object(projection, 'BASE', self.baseline), \
             patch.object(projection, 'HISTORICAL_PROSE', {}), \
             patch.object(projection, 'TYPED_GUIDES', {}), \
             patch.object(projection, 'mediator_guide_source_bytes',
                          side_effect=ValueError('no unrelated guide population in fixture')):
            result=projection.check_preserved_roots(self.repo,{})
        self.assertEqual((self.repo/'.git/index').read_bytes(),before,
                         'checkpoint check wrote the active fixture index')
        return result

    def _reject(self, alias=None):
        with self.assertRaises((ValueError,OSError)):
            self.source.checkpoint_copy_bytes(self.repo,alias or self.alias)

    def _row(self, alias):
        binding=self.catalog[alias]
        return {'repository_path':alias,'repository_revision':None,'disposition':'REUSE',
                'git_blob':binding['blob'],'source_sha256':binding['sha256'],
                'public_sha256':binding['sha256'],'source_bytes':binding['bytes'],
                'public_bytes':binding['bytes']}

    def test_all_87_present_absent_and_staged_absent_keep_exact_bytes(self):
        self.assertEqual(self._gate(),[])
        for alias in self.catalog:
            self.assertEqual(self.source.source_bytes(self.repo,self._row(alias)),self.bodies[alias])
            (self.repo/alias).unlink()
        self.assertEqual(self.source.checkpoint_duplicate_paths(self.repo),set(self.catalog))
        self.assertEqual(self._gate(),[])
        self._git('add','-u','--',*self.catalog)
        self.assertEqual(self._gate(),[])
        for alias in self.catalog:
            self.assertEqual(self.source.source_bytes(self.repo,self._row(alias)),self.bodies[alias])

    def test_present_corruption_cannot_fall_back_to_a_correct_retained_copy(self):
        self._put(self.alias,b'X'+self.bodies[self.alias][1:]); self._reject()
        self.assertTrue(self._gate())

    def test_wrong_missing_or_executable_counterpart_rejects_absent_alias(self):
        (self.repo/self.alias).unlink()
        target=self.repo/self.canonical
        self._put(self.canonical,b'X'+self.bodies[self.canonical][1:]);self._reject()
        self._put(self.canonical,self.bodies[self.canonical]);target.chmod(0o755);self._reject()
        target.unlink();self._reject();self.assertTrue(self._gate())

    def test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence(self):
        target=self.repo/self.alias;target.unlink()
        target.symlink_to(self.repo/self.canonical);self._reject();target.unlink()
        target.symlink_to(self.repo/'missing-fixture');self._reject();target.unlink()
        parent=target.parent; moved=parent.with_name(parent.name+'-moved-fixture')
        parent.rename(moved);parent.symlink_to(moved,target_is_directory=True)
        self._reject()

    def test_staged_alias_tamper_cannot_hide_under_worktree_absence(self):
        self._put(self.alias,b'X'+self.bodies[self.alias][1:]);self._git('add','--',self.alias)
        (self.repo/self.alias).unlink();self._reject();self.assertTrue(self._gate())

    def test_staged_retained_tamper_cannot_hide_under_exact_worktree(self):
        self._put(self.canonical,b'X'+self.bodies[self.canonical][1:]);self._git('add','--',self.canonical)
        self._put(self.canonical,self.bodies[self.canonical]);(self.repo/self.alias).unlink()
        self._reject();self.assertTrue(self._gate())

    def test_unmerged_or_wrong_mode_index_is_rejected(self):
        binding=self.catalog[self.alias];(self.repo/self.alias).unlink()
        self._git('update-index','--cacheinfo','100755',binding['blob'],self.alias);self._reject()
        self._git('update-index','--force-remove','--',self.alias)
        records=''.join('100644 '+binding['blob']+' '+str(stage)+'\t'+self.alias+'\n'
                        for stage in (1,2,3)).encode()
        self._git('update-index','--index-info',input=records);self._reject();self.assertTrue(self._gate())

    def test_unknown_paths_and_changed_population_fail_before_git(self):
        with patch.object(self.source,'_continuation_git',side_effect=AssertionError('unlisted path reached Git')):
            for name in (self.extra,self.alias+'.other','../'+self.alias,'/'+self.alias,self.alias.replace('/','\\'),None):
                with self.subTest(path=name):self._reject(name) if name else self.assertRaises(
                    ValueError,self.source.checkpoint_copy_bytes,self.repo,name)
            with patch.object(self.source,'CHECKPOINT_COPY_MEMBERS',self.source.CHECKPOINT_COPY_MEMBERS[:-1]):
                self._reject()

    def test_source_row_requires_exact_current_copy_identity_and_role(self):
        for field,value in [('git_blob','0'*40),('source_sha256','0'*64),('public_sha256','0'*64),
                            ('source_bytes',0),('public_bytes',0),('disposition','ADD_EXACT'),
                            ('repository_revision',self.baseline),
                            ('repository_path','./'+self.alias),
                            ('repository_path',self.alias.replace('/','//',1))]:
            with self.subTest(field=field):
                row=self._row(self.alias);row[field]=value
                with self.assertRaises(ValueError):self.source.source_bytes(self.repo,row)

    def test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances(self):
        (self.repo/self.alias).unlink()
        self._put(self.extra,b'changed unrelated source\n');self._git('add','--',self.extra)
        self._put(self.extra,b'unrelated protected fixture\n')
        self.assertTrue(self._gate())

    def test_missing_pinned_commit_rejects_even_present_exact_bodies(self):
        with patch.object(self.source,'CHECKPOINT_COPY_BASE','0'*40):self._reject()

    def test_root_and_relative_references_authenticate_before_exists(self):
        import validate_internal_references as references
        local=self.alias.rsplit('/',1)[0]+'/citation.md'
        relative=self.alias.rsplit('/',1)[1]
        with patch.object(references,'ROOT',str(self.repo)):
            for absent in (False,True):
                if absent:(self.repo/self.alias).unlink()
                self.assertTrue(references._resolves('docs/reader/PAPER-CATALOGUE.md',self.alias))
                self.assertTrue(references._resolves(local,relative))
            self._put(self.alias,b'X'+self.bodies[self.alias][1:])
            self.assertFalse(references._resolves('docs/reader/PAPER-CATALOGUE.md',self.alias))
            self.assertFalse(references._resolves(local,relative))

    def test_replacement_restores_exact_fixture_identity_vector(self):
        before=self._git('ls-files','--stage','-z')
        for alias in self.catalog:(self.repo/alias).unlink()
        self._git('add','-u','--',*self.catalog);self.assertEqual(self._gate(),[])
        for alias in self.catalog:self._put(alias,self.bodies[alias])
        self._git('add','--',*self.catalog)
        self.assertEqual(self._git('ls-files','--stage','-z'),before)
        self.assertEqual(self._gate(),[])

    def test_all_twelve_retargets_keep_bytes_with_both_original_coordinates_absent(self):
        import os
        import validate_internal_references as references
        chains = [(alias, row) for alias, row in self.catalog.items() if 'prior_canonical' in row]
        self.assertEqual(len(chains), 12)
        original_index = (self.repo / '.git/index').read_bytes()
        with patch.object(references, 'ROOT', str(self.repo)):
            for alias, row in chains:
                former = row['prior_canonical']
                with self.subTest(alias=alias):
                    try:
                        for name in (alias, former):
                            (self.repo / name).unlink()
                            self.assertFalse(os.path.lexists(self.repo / name))
                        for staged in (False, True):
                            if staged:
                                self._git('update-index', '--force-remove', '--', alias, former)
                            before = (self.repo / '.git/index').read_bytes()
                            self.assertEqual(self.source.checkpoint_copy_bytes(self.repo, alias), self.bodies[alias])
                            self.assertTrue(references._resolves(alias, alias))
                            self.assertTrue(references._resolves(alias, pathlib.PurePosixPath(alias).name))
                            self.assertFalse(os.path.lexists(self.repo / alias))
                            self.assertFalse(os.path.lexists(self.repo / former))
                            self.assertEqual((self.repo / '.git/index').read_bytes(), before)
                    finally:
                        for name in (alias, former):
                            self._put(name, self.bodies[name])
                        (self.repo / '.git/index').write_bytes(original_index)

    def test_all_twelve_former_provider_corruptions_are_rejected(self):
        import os
        import validate_internal_references as references
        chains = [(alias, row) for alias, row in self.catalog.items() if 'prior_canonical' in row]
        self.assertEqual(len(chains), 12)
        original_index = (self.repo / '.git/index').read_bytes()
        with patch.object(references, 'ROOT', str(self.repo)):
            for alias, row in chains:
                former = row['prior_canonical']
                for fault in ('body', 'mode', 'staged-body-under-absence'):
                    with self.subTest(alias=alias, fault=fault):
                        try:
                            if fault == 'mode':
                                (self.repo / former).chmod(0o755)
                            else:
                                self._put(former, self.bodies[former] + b'wrong former provider\n')
                            if fault == 'staged-body-under-absence':
                                self._git('add', '--', former)
                                for name in (alias, former):
                                    (self.repo / name).unlink()
                                    self.assertFalse(os.path.lexists(self.repo / name))
                            before = (self.repo / '.git/index').read_bytes()
                            self._reject(alias)
                            self.assertFalse(references._resolves(alias, alias))
                            self.assertFalse(references._resolves(alias, pathlib.PurePosixPath(alias).name))
                            self.assertEqual((self.repo / '.git/index').read_bytes(), before)
                            if fault == 'staged-body-under-absence':
                                for name in (alias, former):
                                    self.assertFalse(os.path.lexists(self.repo / name))
                        finally:
                            for name in (alias, former):
                                self._put(name, self.bodies[name])
                            (self.repo / '.git/index').write_bytes(original_index)

    def test_retarget_catalog_binds_each_former_and_final_coordinate_before_git(self):
        import hashlib
        members = self.source.CHECKPOINT_COPY_RETARGETS
        self.assertEqual(len(members), 12)
        alternative = next(row[2] for row in members if row[2] != members[0][2])
        variants = (
            members[:-1],
            ((members[0][0], members[1][1], *members[0][2:]), *members[1:]),
            ((members[0][0], members[0][1], alternative, *members[0][3:]), *members[1:]),
            ((members[0][0], members[0][1], members[0][1], *members[0][3:]), *members[1:]),
            ((*members[0][:3], '0' * 40, *members[0][4:]), *members[1:]),
        )
        with patch.object(self.source, '_continuation_git', side_effect=AssertionError('bad retarget reached Git')):
            for changed in variants:
                self.assertNotEqual(changed, members)
                digest = hashlib.sha256(json.dumps(changed, separators=(',', ':')).encode()).hexdigest()
                with patch.object(self.source, 'CHECKPOINT_COPY_RETARGETS', changed), \
                     patch.object(self.source, 'CHECKPOINT_COPY_RETARGETS_SHA256', digest):
                    with self.assertRaises(ValueError):
                        self.source._checkpoint_copy_catalog()

    def _reader_currentness(self):
        import check_reader_pilot as reader
        before = (self.repo / '.git/index').read_bytes()
        result = reader.check_corpus_currentness(self.repo, self.baseline)
        self.assertEqual((self.repo / '.git/index').read_bytes(), before,
                         'reader currentness changed the raw fixture index')
        return result

    def test_reader_currentness_authenticates_present_and_both_absence_states(self):
        self.assertEqual(self._reader_currentness(), [])
        for path in self.catalog:
            (self.repo / path).unlink()
        self.assertEqual(self._reader_currentness(), [])
        self._git('add', '-u', '--', *self.catalog)
        self.assertEqual(self._reader_currentness(), [])

    def test_reader_currentness_rejects_retained_body_and_index_tampering(self):
        (self.repo / self.alias).unlink()
        self._put(self.canonical, b'X' + self.bodies[self.canonical][1:])
        self.assertTrue(self._reader_currentness())
        self._git('add', '--', self.canonical)
        self._put(self.canonical, self.bodies[self.canonical])
        self.assertTrue(self._reader_currentness())

    def test_reader_currentness_rejects_present_alias_and_unrelated_changes(self):
        self._put(self.alias, b'X' + self.bodies[self.alias][1:])
        self.assertTrue(self._reader_currentness())
        self._git('add', '--', self.alias)
        (self.repo / self.alias).unlink()
        self.assertTrue(self._reader_currentness())
        self._put(self.alias, self.bodies[self.alias])
        self._git('add', '--', self.alias)
        (self.repo / self.extra).unlink()
        self.assertTrue(self._reader_currentness())

    def test_binding_fixture_keeps_native_history_and_complete_public_row_guards(self):
        body = self.binding_fixture[self.binding_record]
        identity = hashlib.sha256(body).hexdigest()
        self.assertEqual(self.source.binding_record_bytes(
            self.repo, self.binding_record, identity, len(body)), body)
        self.assertEqual(self.source.binding_record_absences(self.repo), set())
        row = {'repository_path': self.binding_record, 'public_sha256': identity,
               'public_bytes': len(body)}
        with self.assertRaisesRegex(ValueError, 'complete public source row differs'):
            self.source.binding_record_public_bytes(self.repo, row)

    def test_binding_fixture_rejects_missing_or_wrong_native_catalogue(self):
        body = self.binding_fixture[self.binding_record]
        body_oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        changes = (
            ('BINDING_RECORD_BASE', '0' * 40),
            ('BINDING_RECORD_BASE', body_oid),
            ('BINDING_RECORD_TREE', '0' * 40),
            ('BINDING_RECORD_ORIGINAL_COUNT', self.source.BINDING_RECORD_ORIGINAL_COUNT + 1),
            ('BINDING_RECORD_COUNT', 2),
            ('BINDING_RECORD_CLASS_SHA256', '0' * 64),
            ('BINDING_RECORD_PATH_HASHES', frozenset(('0' * 64,))),
        )
        for name, value in changes:
            with self.subTest(coordinate=name, value=value), patch.object(self.source, name, value):
                with self.assertRaises(ValueError):
                    self.source._binding_record_catalog(self.repo)
        alias = next(path for path in self.catalog if self.source.binding_record_candidate(path))
        (self.repo / alias).unlink()
        with patch.object(self.source, 'BINDING_RECORD_BASE', '0' * 40):
            self.assertIn('preserved v5 or prior T20 baseline comparison unavailable', self._gate())
            self.assertIn('corpus-currentness: source binding record: frozen administrative Git input is unavailable',
                          self._reader_currentness())

    def test_binding_fixture_qualifies_absence_only_with_unchanged_current_owner(self):
        (self.repo / self.binding_record).unlink()
        self.assertEqual(self.source.binding_record_absences(self.repo), {self.binding_record})
        self.assertEqual(self._gate(), [])
        self.assertEqual(self._reader_currentness(), [])
        self._git('add', '-u', '--', self.binding_record)
        self.assertEqual(self._gate(), [])
        self.assertEqual(self._reader_currentness(), [])
        owner = self.binding_fixture[self.binding_owner]
        for condition in ('changed', 'absent', 'executable', 'staged'):
            with self.subTest(owner=condition):
                self._put(self.binding_owner, owner)
                if condition == 'changed':
                    self._put(self.binding_owner, b'changed current fixture owner\n')
                elif condition == 'absent':
                    (self.repo / self.binding_owner).unlink()
                elif condition == 'executable':
                    (self.repo / self.binding_owner).chmod(0o755)
                else:
                    self._put(self.binding_owner, b'changed staged fixture owner\n')
                    self._git('add', '--', self.binding_owner)
                    self._put(self.binding_owner, owner)
                with self.assertRaises(ValueError):
                    self.source.binding_record_absences(self.repo)
                self.assertTrue(self._gate())
                self.assertTrue(self._reader_currentness())
                self._put(self.binding_owner, owner)
                self._git('add', '--', self.binding_owner)
        self.assertEqual(self.source.binding_record_absences(self.repo), {self.binding_record})

    def test_binding_fixture_rejects_changed_or_missing_original_input(self):
        body = self.binding_fixture[self.binding_record]
        self._put(self.binding_record, b'changed current fixture binding\n')
        with self.assertRaises(ValueError):
            self.source.binding_record_bytes(self.repo, self.binding_record)
        self._put(self.binding_record, body)
        oid = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        native = self.repo / '.git' / 'objects' / oid[:2] / oid[2:]
        self.assertTrue(native.is_file())
        native.unlink()  # Only this test-owned synthetic loose object.
        try:
            with self.assertRaisesRegex(ValueError, 'frozen administrative Git input is unavailable'):
                self.source.binding_record_bytes(self.repo, self.binding_record)
        finally:
            self.assertEqual(self._git('hash-object', '-w', '--stdin', input=body).decode().strip(), oid)
        self.assertEqual(self.source.binding_record_bytes(self.repo, self.binding_record), body)

    def test_binding_fixture_rejects_staged_or_active_record_disappearance(self):
        body = self.binding_fixture[self.binding_record]
        self._put(self.binding_record, b'changed staged fixture binding\n')
        self._git('add', '--', self.binding_record)
        self._put(self.binding_record, body)
        with self.assertRaisesRegex(ValueError, 'staged identity differs'):
            self.source.binding_record_absences(self.repo)
        self.assertTrue(self._gate())
        self.assertTrue(self._reader_currentness())
        self._git('add', '--', self.binding_record)
        active = self.source.BINDING_RECORD_CURRENT_REQUIRED | {self.binding_record}
        with patch.object(self.source, 'BINDING_RECORD_CURRENT_REQUIRED', active):
            (self.repo / self.binding_record).unlink()
            with self.assertRaisesRegex(ValueError, 'must remain present'):
                self.source.binding_record_absences(self.repo)
            self.assertTrue(self._gate())
            self.assertTrue(self._reader_currentness())
            self._put(self.binding_record, body)
            self._git('rm', '--cached', '--', self.binding_record)
            with self.assertRaisesRegex(ValueError, 'must remain indexed'):
                self.source.binding_record_bytes(self.repo, self.binding_record)




class PublicReaderNoteProjectionTests(unittest.TestCase):
    """Resolve six already-public notes through exact native historical owners."""

    ITEMS = (
        ('002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e',
         '2804e7b196437dd437f0099b15aa45a76249e63b', 6680,
         'a7ff0e33d1a299db640041c46b1af81ca70851f6'),
        ('4878fd0a4cf6c952af7cdbcb7e8a386c2730ff9986b74b8e39bf9b5077815b0f',
         'f419024deb2a40bf50f7315cdf2dfdde9ede77f6', 15286,
         'a7ff0e33d1a299db640041c46b1af81ca70851f6'),
        ('7d3cbeb8bcacdb5d28cb457801ba41de9b21f91542866fe5c5f13a4a632dadd9',
         '07a1df58ff170334e07261c93af8345093b0f160', 14328,
         'b4d58482ae00f138782276ee5c4034c48bb2df19'),
        ('b092780b29dd9fa00ac276142b090a5b8b88da79da9c278268264669e08f3d8c',
         '4e69862256f3014f8e94d528b13ff0f63dd7f3eb', 29013,
         'b4d58482ae00f138782276ee5c4034c48bb2df19'),
        ('34c1f25cd1144b386ff4c70a2fbfacc7da2a0fc87f5cd78b430badf260ab49f6',
         '6bcd9f7c0faea3fe3037c1f188288555312517b1', 1017,
         'b4d58482ae00f138782276ee5c4034c48bb2df19'),
        ('9438fdcbea8747c7e5599483096eca9541cfdf673d6a96866c019c5ced06519a',
         '80e45c60c8f4e71a8191f906d04afd4ab0384b06', 11145,
         'b4d58482ae00f138782276ee5c4034c48bb2df19'),
    )

    @classmethod
    def setUpClass(cls):
        import subprocess
        import resolve_t20_v6_source as source
        cls.source = source
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        by_hash = {row['source_sha256']: row for row in manifest['objects']}
        cls.rows, cls.bodies = {}, {}
        for identity, blob, size, revision in cls.ITEMS:
            path = 'docs/provenance/v5-research-continuations/notes/' + identity + '.md'
            recorded = by_hash[identity]
            if (('repository_revision' in recorded or 'git_blob' in recorded)
                    and (recorded.get('repository_revision'), recorded.get('git_blob')) != (revision, blob)):
                raise ValueError('public reader-note manifest coordinate differs')
            row = dict(by_hash[identity], repository_revision=revision, git_blob=blob)
            if (row['repository_path'], row['disposition'], row['source_bytes'],
                    row['public_sha256'], row['public_bytes']) != (path, 'REUSE', size, identity, size):
                raise ValueError('public reader-note fixture owner differs')
            body = source.historical_source_bytes(projection.ROOT, path, revision, blob)
            if hashlib.sha256(body).hexdigest() != identity or len(body) != size:
                raise ValueError('public reader-note fixture body differs')
            cls.rows[path], cls.bodies[path] = row, body
        cls.context = {
            path: (projection.ROOT / path).read_bytes() for path in (
                'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json',
                'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json',
                'mathematics/common-repair-and-geometric-obstructions.md',
                'mathematics/information-and-inquiry.md',
                'mathematics/collective-inquiry-and-strategic-coordination.md',
                'docs/scientific-consolidation-review.md')}
        objects = subprocess.check_output(['git', 'rev-parse', '--git-path', 'objects'],
                                          cwd=projection.ROOT, text=True).strip()
        cls.objects = pathlib.Path(objects)
        if not cls.objects.is_absolute():
            cls.objects = projection.ROOT / cls.objects

    def setUp(self):
        import os
        import subprocess
        self.tmp = tempfile.TemporaryDirectory(prefix='public-note-projection-')
        self.addCleanup(self.tmp.cleanup)
        self.repo = pathlib.Path(self.tmp.name)
        self.env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_CONFIG_SYSTEM=os.devnull, GIT_OPTIONAL_LOCKS='0',
                        GIT_TERMINAL_PROMPT='0', GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='')
        subprocess.run(['git', '-c', 'init.templateDir=', 'init', '-q', str(self.repo)],
                       env=self.env, check=True)
        (self.repo / '.git/objects/info/alternates').write_text(str(self.objects.resolve()) + '\n')
        for path, body in {**self.context, **self.bodies}.items():
            target = self.repo / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)
            target.chmod(0o644)
        self._git('add', '--', *self.bodies)

    def _git(self, *args):
        import subprocess
        return subprocess.run(['git', '--no-replace-objects', '--literal-pathspecs',
                               '-c', 'core.hooksPath=/dev/null', *args],
                              cwd=self.repo, env=self.env, capture_output=True, check=True).stdout

    def _reject(self, row):
        self.assertTrue(check_object(self.repo, row))
        with self.assertRaises((ValueError, OSError)):
            self.source.source_bytes(self.repo, row)

    def test_six_exact_pins_resolve_present_and_absent_without_index_writes(self):
        before = (self.repo / '.git/index').read_bytes()
        for present in (True, False):
            for path, row in self.rows.items():
                if not present:
                    (self.repo / path).unlink()
                with self.subTest(path=path, present=present):
                    self.assertEqual(check_object(self.repo, row), [])
                    self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[path])
        self.assertEqual((self.repo / '.git/index').read_bytes(), before)

    def test_public_note_history_requires_exact_coordinate_role_and_identity(self):
        row = next(iter(self.rows.values()))
        for field, value in (('repository_revision', 'HEAD'), ('git_blob', '0' * 40),
                             ('disposition', 'ADD_EXACT'), ('source_sha256', '0' * 64),
                             ('public_sha256', '0' * 64), ('source_bytes', 1), ('public_bytes', 1)):
            with self.subTest(field=field):
                self._reject(dict(row, **{field: value}))
        for field in ('repository_revision', 'git_blob'):
            changed = dict(row); del changed[field]
            with self.subTest(missing=field):
                self._reject(changed)

    def test_public_note_present_or_staged_corruption_cannot_hide_in_history(self):
        path, row = next(iter(self.rows.items()))
        target = self.repo / path
        target.write_bytes(self.bodies[path] + b'changed current source\n')
        self._reject(row)
        self._git('add', '--', path)
        target.unlink()
        self._reject(row)

    def test_reader_only_notes_do_not_acquire_public_source_admission(self):
        admitted = set(self.rows)
        other_paths = set(self.source.CONTINUATION_READER_PROSE) | set(self.source.T4_READER_PROSE)
        with patch.object(self.source, 'historical_source_bytes',
                          side_effect=AssertionError('reader-only source reached a body read')):
            for path in sorted(other_paths - admitted):
                blob, identity, size = self.source.HISTORICAL_PROSE[path]
                row = dict(repository_path=path, disposition='REUSE', source_sha256=identity,
                           public_sha256=identity, source_bytes=size, public_bytes=size,
                           repository_revision=self.source.HISTORICAL_PROSE_REVISIONS[path],
                           git_blob=blob)
                with self.subTest(path=path):
                    self._reject(row)


class PublicProjectionConsumerManifestTests(unittest.TestCase):
    """Seven coordinate additions cannot alter any source or publication identity."""

    @classmethod
    def setUpClass(cls):
        import check_reader_pilot as reader
        cls.reader = reader
        cls.original = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        rows = {row['source_sha256']: row for row in cls.original['objects']}
        coordinates = [(identity, revision, blob)
                       for identity, blob, size, revision in PublicReaderNoteProjectionTests.ITEMS]
        coordinates.append(('51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff',
                            '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
                            'd90b5647de1cf290d3b7dbe20a805983c75f0fcf'))
        for identity, revision, blob in coordinates:
            row = rows[identity]
            if (('repository_revision' in row or 'git_blob' in row)
                    and (row.get('repository_revision'), row.get('git_blob')) != (revision, blob)):
                raise ValueError('public consumer manifest fixture coordinate differs')
            row.pop('repository_revision', None)
            row.pop('git_blob', None)

    def candidate(self):
        from copy import deepcopy
        result = deepcopy(self.original)
        rows = {row['source_sha256']: row for row in result['objects']}
        for identity, blob, size, revision in PublicReaderNoteProjectionTests.ITEMS:
            rows[identity].update(repository_revision=revision, git_blob=blob)
        rows['51e2cea236dd0a880c7243b2f9ccbd558c6c70f16f03ec0efa274f19d3d105ff'].update(
            repository_revision='7efc6217c090b92d65f2c4cb8b011c18eb96bf7c',
            git_blob='d90b5647de1cf290d3b7dbe20a805983c75f0fcf')
        return result

    def permitted(self, candidate):
        gate = getattr(self.reader, '_permitted_projection_consumer_pins', None)
        return bool(gate and gate(self.original, candidate))

    def test_complete_seven_coordinates_preserve_original_manifest_identities(self):
        self.assertTrue(self.permitted(self.candidate()))

    def test_partial_or_changed_publication_cannot_claim_consumer_pin_extension(self):
        for fault in ('partial', 'revision', 'role', 'identity', 'size', 'dependency', 'count', 'unrelated'):
            candidate = self.candidate()
            row = next(r for r in candidate['objects'] if r['source_sha256'] ==
                       '002eab67237670bc990e3762cb0cce1f0de465987ba5aa48a5ccbd27d4ac302e')
            if fault == 'partial': del row['git_blob']
            elif fault == 'revision': row['repository_revision'] = 'HEAD'
            elif fault == 'role': row['role'] = 'formal_component'
            elif fault == 'identity': row['public_sha256'] = '0' * 64
            elif fault == 'size': row['public_bytes'] += 1
            elif fault == 'dependency': row['required_dependencies'] = ['0' * 64]
            elif fault == 'count': candidate['counts']['REUSE'] += 1
            else: candidate['objects'][-1]['unrelated'] = True
            with self.subTest(fault=fault):
                self.assertFalse(self.permitted(candidate))



class CheckpointRecordCopyMigrationTests(unittest.TestCase):
    """Keep original coordinates for76 dated records and their five original-context dependencies with exact retained bytes.

    The shared fixture helpers and contrary methods below are unchanged from
    the earlier87 class. Their byte reader and rows are bound to this separate
    finite record class. Twelve former providers have separately authenticated routes.
    """

    CONTEXT_SOURCE = 'research/t20-live-20261009/checkpoints/CP23/warranted-discrimination-kernel-20261009/MANIFEST.json'
    CONTEXT_MEMBERS = (
        ('independent-review/CertificateFrontier.lean', '208cf6e6250c6ff50d0b03575a6ae7926b70d1ed', '5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0', 12278),
        ('independent-review/Controls.lean', '1c6b8900e600c63e30f0aa83f49f7db8211a7cdf', '7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132', 2410),
        ('independent-review/mutations/CostBlind.lean', '01cef9257fc16b90c16ae14ca9e65aef41cdd787', 'c05bf6d3207aeeaa7dddc222092c73d44f73ecc5eab5c8d465485a9a540d5776', 227),
        ('independent-review/mutations/CurrentCost.lean', '9ad7316c3906603cd262cb781736078b18cd14a5', '876039d480a1415531f1f099679c5094327caf35c7933a36550e09692de1e83d', 249),
        ('independent-review/mutations/InfinitePrice.lean', 'ffa13821c157cd943b1bcb5f6aa514c917f198b1', '0b2d8b2584f48d343d753a373161e28f93c397982ce9ab4c098b8daf16db31fe', 293),
    )

    setUp = CheckpointCopyMigrationTests.setUp
    _git = CheckpointCopyMigrationTests._git
    _put = CheckpointCopyMigrationTests._put
    _gate = CheckpointCopyMigrationTests._gate

    @classmethod
    def setUpClass(cls):
        import resolve_t20_v6_source as source
        cls.source = source
        cls.catalog = source._checkpoint_record_copy_catalog()
        if len(cls.catalog) != 76:
            raise AssertionError('record fixture population differs')
        cls.bodies = {}
        for alias, binding in cls.catalog.items():
            body = source.checkpoint_record_copy_bytes(projection.ROOT, alias)
            cls.bodies[alias] = body
            if cls.bodies.setdefault(binding['canonical'], body) != body:
                raise AssertionError('retained record body conflicts')
        formal = source._formal_copy_catalog()
        for relative, blob, identity, size in cls.CONTEXT_MEMBERS:
            path = str(pathlib.PurePosixPath(cls.CONTEXT_SOURCE).parent / relative)
            binding = dict(canonical=path, blob=blob, sha256=identity, bytes=size, mode='100644')
            body = source._checkpoint_bound_bytes(projection.ROOT, path, binding)
            if cls.bodies.setdefault(path, body) != body:
                raise AssertionError('original-context fixture body conflicts')
            # These five original-context dependencies now authenticate their
            # exact retained formal counterparts before reference resolution.
            retained = formal[path]
            if (retained['blob'], retained['sha256'], retained['bytes'], retained['mode']) != (
                    blob, identity, size, '100644'):
                raise AssertionError('original-context retained identity differs')
            if cls.bodies.setdefault(retained['canonical'], body) != body:
                raise AssertionError('original-context retained body conflicts')
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        cls.public_rows = [r for r in manifest['objects'] if r.get('repository_path') in cls.catalog]
        if len(cls.public_rows) != 14:
            raise AssertionError('existing public record population differs')

    def _reject(self, alias=None):
        with self.assertRaises((ValueError, OSError)):
            self.source.checkpoint_record_copy_bytes(self.repo, alias or self.alias)

    def _row(self, alias):
        binding = self.catalog[alias]
        return dict(repository_path=alias, disposition='REUSE',
                    source_sha256=binding['sha256'], public_sha256=binding['sha256'],
                    source_bytes=binding['bytes'], public_bytes=binding['bytes'])

    def test_all_76_present_absent_and_staged_absent_keep_exact_bytes(self):
        self.assertEqual(self._gate(), [])
        for alias in self.catalog:
            self.assertEqual(self.source.source_bytes(self.repo, self._row(alias)), self.bodies[alias])
            (self.repo / alias).unlink()
        self.assertEqual(self.source.checkpoint_record_duplicate_paths(self.repo), set(self.catalog))
        self.assertEqual(self._gate(), [])
        self._git('add', '-u', '--', *self.catalog)
        self.assertEqual(self._gate(), [])
        for alias in self.catalog:
            self.assertEqual(self.source.source_bytes(self.repo, self._row(alias)), self.bodies[alias])

    def test_fourteen_existing_projection_rows_resolve_their_original_identities(self):
        before = (self.repo / '.git/index').read_bytes()
        for row in self.public_rows:
            with self.subTest(path=row['repository_path']):
                self.assertEqual(check_object(self.repo, row), [])
                (self.repo / row['repository_path']).unlink()
                self.assertEqual(check_object(self.repo, row), [])
                self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[row['repository_path']])
        self.assertEqual((self.repo / '.git/index').read_bytes(), before)
        self._git('add', '-u', '--', *(r['repository_path'] for r in self.public_rows))
        self.assertEqual(self._gate(), [])

    def test_unknown_paths_and_changed_record_population_fail_before_git(self):
        with patch.object(self.source, '_continuation_git', side_effect=AssertionError('unlisted record reached Git')):
            for name in (self.extra, self.alias+'.other', '../'+self.alias, '/'+self.alias,
                         self.alias.replace('/', '\\')):
                with self.subTest(path=name): self._reject(name)
            with self.assertRaises(ValueError):
                self.source.checkpoint_record_copy_bytes(self.repo, None)
            with patch.object(self.source, 'CHECKPOINT_RECORD_COPY_MEMBERS',
                              self.source.CHECKPOINT_RECORD_COPY_MEMBERS[:-1]):
                self._reject()

    test_present_corruption_cannot_fall_back_to_a_correct_retained_copy = CheckpointCopyMigrationTests.test_present_corruption_cannot_fall_back_to_a_correct_retained_copy
    test_wrong_missing_or_executable_counterpart_rejects_absent_alias = CheckpointCopyMigrationTests.test_wrong_missing_or_executable_counterpart_rejects_absent_alias
    test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence = CheckpointCopyMigrationTests.test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence
    test_staged_alias_tamper_cannot_hide_under_worktree_absence = CheckpointCopyMigrationTests.test_staged_alias_tamper_cannot_hide_under_worktree_absence
    test_staged_retained_tamper_cannot_hide_under_exact_worktree = CheckpointCopyMigrationTests.test_staged_retained_tamper_cannot_hide_under_exact_worktree
    test_unmerged_or_wrong_mode_index_is_rejected = CheckpointCopyMigrationTests.test_unmerged_or_wrong_mode_index_is_rejected
    test_source_row_requires_exact_current_copy_identity_and_role = CheckpointCopyMigrationTests.test_source_row_requires_exact_current_copy_identity_and_role
    test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances = CheckpointCopyMigrationTests.test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances
    test_missing_pinned_commit_rejects_even_present_exact_bodies = CheckpointCopyMigrationTests.test_missing_pinned_commit_rejects_even_present_exact_bodies
    test_root_and_relative_references_authenticate_before_exists = CheckpointCopyMigrationTests.test_root_and_relative_references_authenticate_before_exists
    test_replacement_restores_exact_fixture_identity_vector = CheckpointCopyMigrationTests.test_replacement_restores_exact_fixture_identity_vector


    def test_five_manifest_dependencies_keep_the_original_source_context(self):
        import os
        import validate_internal_references as references
        source = self.CONTEXT_SOURCE
        canonical = self.catalog[source]['canonical']
        with patch.object(references, 'ROOT', str(self.repo)):
            for state in ('present', 'unstaged-absence', 'staged-absence'):
                if state == 'unstaged-absence':
                    (self.repo / source).unlink()
                elif state == 'staged-absence':
                    self._git('update-index', '--force-remove', '--', source)
                self.assertEqual(os.path.lexists(self.repo / source), state == 'present')
                self.assertEqual(self.source.checkpoint_record_copy_bytes(self.repo, source), self.bodies[source])
                for relative, blob, identity, size in self.CONTEXT_MEMBERS:
                    original = str(pathlib.PurePosixPath(source).parent / relative)
                    body = (self.repo / original).read_bytes()
                    self.assertEqual((self.source.digest(body), len(body)), (identity, size))
                    self.assertTrue(references._resolves(source, relative))
                    self.assertFalse(references._resolves(canonical, relative))
                self.assertEqual(self._gate(), [])

    _reader_currentness = CheckpointCopyMigrationTests._reader_currentness
    test_reader_currentness_authenticates_present_and_both_absence_states = CheckpointCopyMigrationTests.test_reader_currentness_authenticates_present_and_both_absence_states
    test_reader_currentness_rejects_retained_body_and_index_tampering = CheckpointCopyMigrationTests.test_reader_currentness_rejects_retained_body_and_index_tampering
    test_reader_currentness_rejects_present_alias_and_unrelated_changes = CheckpointCopyMigrationTests.test_reader_currentness_rejects_present_alias_and_unrelated_changes




class CheckpointPackageCopyMigrationTests(unittest.TestCase):
    """Preserve exact inert sources for26 reviewed obsolete package locations."""

    setUp = CheckpointCopyMigrationTests.setUp
    _git = CheckpointCopyMigrationTests._git
    _put = CheckpointCopyMigrationTests._put
    _gate = CheckpointCopyMigrationTests._gate

    @classmethod
    def setUpClass(cls):
        import resolve_t20_v6_source as source
        cls.source = source
        cls.catalog = source._checkpoint_package_copy_catalog()
        if len(cls.catalog) != 26:
            raise AssertionError('package fixture population differs')
        cls.bodies = {}
        for alias, binding in cls.catalog.items():
            body = source.checkpoint_package_copy_bytes(projection.ROOT, alias)
            cls.bodies[alias] = body
            if cls.bodies.setdefault(binding['canonical'], body) != body:
                raise AssertionError('retained package body conflicts')
            if 'prior_canonical' in binding:
                if cls.bodies.setdefault(binding['prior_canonical'], body) != body:
                    raise AssertionError('former package provider body conflicts')
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        if any(r.get('repository_path') in cls.catalog for r in manifest['objects']):
            raise AssertionError('package aliases acquired a public projection role')
        providers = {r['canonical'] for r in cls.catalog.values()} | {r['prior_canonical'] for r in cls.catalog.values() if 'prior_canonical' in r}
        cls.public_rows = [r for r in manifest['objects'] if r.get('repository_path') in providers]
        if len(cls.public_rows) != 13:
            raise AssertionError('existing public provider population differs')

    def _reject(self, alias=None):
        with self.assertRaises((ValueError, OSError)):
            self.source.checkpoint_package_copy_bytes(self.repo, alias or self.alias)

    def _row(self, alias):
        binding = self.catalog[alias]
        return dict(repository_path=alias, disposition='REUSE',
                    source_sha256=binding['sha256'], public_sha256=binding['sha256'],
                    source_bytes=binding['bytes'], public_bytes=binding['bytes'])

    def test_all_26_present_absent_and_staged_absent_keep_exact_inert_bytes(self):
        self.assertEqual(self._gate(), [])
        for alias in self.catalog:
            self.assertEqual(self.source.checkpoint_package_copy_bytes(self.repo, alias), self.bodies[alias])
            (self.repo / alias).unlink()
        self.assertEqual(self.source.checkpoint_package_duplicate_paths(self.repo), set(self.catalog))
        self.assertEqual(self._gate(), [])
        self._git('add', '-u', '--', *self.catalog)
        self.assertEqual(self._gate(), [])
        for alias in self.catalog:
            self.assertEqual(self.source.checkpoint_package_copy_bytes(self.repo, alias), self.bodies[alias])

    def test_thirteen_existing_provider_rows_remain_exact_when_all_aliases_are_absent(self):
        before = (self.repo / '.git/index').read_bytes()
        for alias in self.catalog:
            (self.repo / alias).unlink()
        for row in self.public_rows:
            with self.subTest(path=row['repository_path']):
                self.assertEqual(check_object(self.repo, row), [])
                self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[row['repository_path']])
        self.assertEqual((self.repo / '.git/index').read_bytes(), before)
        self._git('add', '-u', '--', *self.catalog)
        self.assertEqual(self._gate(), [])

    def test_unknown_paths_and_changed_package_population_fail_before_git(self):
        with patch.object(self.source, '_continuation_git', side_effect=AssertionError('unlisted package reached Git')):
            for name in (self.extra, self.alias + '.other', '../' + self.alias,
                         '/' + self.alias, self.alias.replace('/', '\\')):
                with self.subTest(path=name):
                    self._reject(name)
            with self.assertRaises(ValueError):
                self.source.checkpoint_package_copy_bytes(self.repo, None)
            with patch.object(self.source, 'CHECKPOINT_PACKAGE_COPY_MEMBERS',
                              self.source.CHECKPOINT_PACKAGE_COPY_MEMBERS[:-1]):
                self._reject()

    def test_historical_byte_route_does_not_admit_new_public_projection_rows(self):
        for alias in self.catalog:
            (self.repo / alias).unlink()
            row = self._row(alias)
            with self.subTest(path=alias):
                self.assertEqual(self.source.checkpoint_package_copy_bytes(self.repo, alias), self.bodies[alias])
                self.assertEqual(check_object(self.repo, row), ['missing or unsafe public source'])
                with self.assertRaises((ValueError, OSError)):
                    self.source.source_bytes(self.repo, row)

    def test_historical_python_bodies_are_never_compiled_or_executed(self):
        historical = [p for p in self.catalog if p.endswith('.py')]
        self.assertEqual(len(historical), 21)
        with patch('builtins.compile', side_effect=AssertionError('historical source compiled')), \
             patch('builtins.exec', side_effect=AssertionError('historical source executed')):
            for alias in historical:
                with self.subTest(path=alias):
                    self.assertEqual(self.source.checkpoint_package_copy_bytes(self.repo, alias), self.bodies[alias])

    test_present_corruption_cannot_fall_back_to_a_correct_retained_copy = CheckpointCopyMigrationTests.test_present_corruption_cannot_fall_back_to_a_correct_retained_copy
    test_wrong_missing_or_executable_counterpart_rejects_absent_alias = CheckpointCopyMigrationTests.test_wrong_missing_or_executable_counterpart_rejects_absent_alias
    test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence = CheckpointCopyMigrationTests.test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence
    test_staged_alias_tamper_cannot_hide_under_worktree_absence = CheckpointCopyMigrationTests.test_staged_alias_tamper_cannot_hide_under_worktree_absence
    test_staged_retained_tamper_cannot_hide_under_exact_worktree = CheckpointCopyMigrationTests.test_staged_retained_tamper_cannot_hide_under_exact_worktree
    test_unmerged_or_wrong_mode_index_is_rejected = CheckpointCopyMigrationTests.test_unmerged_or_wrong_mode_index_is_rejected
    test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances = CheckpointCopyMigrationTests.test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances
    test_missing_pinned_commit_rejects_even_present_exact_bodies = CheckpointCopyMigrationTests.test_missing_pinned_commit_rejects_even_present_exact_bodies
    test_root_and_relative_references_authenticate_before_exists = CheckpointCopyMigrationTests.test_root_and_relative_references_authenticate_before_exists
    test_replacement_restores_exact_fixture_identity_vector = CheckpointCopyMigrationTests.test_replacement_restores_exact_fixture_identity_vector

    _reader_currentness = CheckpointCopyMigrationTests._reader_currentness
    test_reader_currentness_authenticates_present_and_both_absence_states = CheckpointCopyMigrationTests.test_reader_currentness_authenticates_present_and_both_absence_states
    test_reader_currentness_rejects_retained_body_and_index_tampering = CheckpointCopyMigrationTests.test_reader_currentness_rejects_retained_body_and_index_tampering
    test_reader_currentness_rejects_present_alias_and_unrelated_changes = CheckpointCopyMigrationTests.test_reader_currentness_rejects_present_alias_and_unrelated_changes



    def test_all_ten_retargets_keep_bytes_with_both_original_coordinates_absent(self):
        import os
        import validate_internal_references as references
        chains = [(alias, row) for alias, row in self.catalog.items() if 'prior_canonical' in row]
        self.assertEqual(len(chains), 10)
        original_index = (self.repo / '.git/index').read_bytes()
        with patch.object(references, 'ROOT', str(self.repo)):
            for alias, row in chains:
                former = row['prior_canonical']
                with self.subTest(alias=alias):
                    try:
                        for name in (alias, former):
                            (self.repo / name).unlink()
                            self.assertFalse(os.path.lexists(self.repo / name))
                        for staged in (False, True):
                            if staged:
                                self._git('update-index', '--force-remove', '--', alias, former)
                            before = (self.repo / '.git/index').read_bytes()
                            self.assertEqual(self.source.checkpoint_package_copy_bytes(self.repo, alias), self.bodies[alias])
                            self.assertTrue(references._resolves(alias, alias))
                            self.assertTrue(references._resolves(alias, pathlib.PurePosixPath(alias).name))
                            self.assertFalse(os.path.lexists(self.repo / alias))
                            self.assertFalse(os.path.lexists(self.repo / former))
                            self.assertEqual((self.repo / '.git/index').read_bytes(), before)
                    finally:
                        for name in (alias, former):
                            self._put(name, self.bodies[name])
                        (self.repo / '.git/index').write_bytes(original_index)

    def test_all_ten_former_provider_corruptions_are_rejected(self):
        import os
        import validate_internal_references as references
        chains = [(alias, row) for alias, row in self.catalog.items() if 'prior_canonical' in row]
        self.assertEqual(len(chains), 10)
        original_index = (self.repo / '.git/index').read_bytes()
        with patch.object(references, 'ROOT', str(self.repo)):
            for alias, row in chains:
                former = row['prior_canonical']
                for fault in ('body', 'mode', 'staged-body-under-absence'):
                    with self.subTest(alias=alias, fault=fault):
                        try:
                            if fault == 'mode':
                                (self.repo / former).chmod(0o755)
                            else:
                                self._put(former, self.bodies[former] + b'wrong former provider\n')
                            if fault == 'staged-body-under-absence':
                                self._git('add', '--', former)
                                for name in (alias, former):
                                    (self.repo / name).unlink()
                                    self.assertFalse(os.path.lexists(self.repo / name))
                            before = (self.repo / '.git/index').read_bytes()
                            self._reject(alias)
                            self.assertFalse(references._resolves(alias, alias))
                            self.assertFalse(references._resolves(alias, pathlib.PurePosixPath(alias).name))
                            self.assertEqual((self.repo / '.git/index').read_bytes(), before)
                            if fault == 'staged-body-under-absence':
                                for name in (alias, former):
                                    self.assertFalse(os.path.lexists(self.repo / name))
                        finally:
                            for name in (alias, former):
                                self._put(name, self.bodies[name])
                            (self.repo / '.git/index').write_bytes(original_index)

    def test_retarget_catalog_binds_each_former_and_final_coordinate_before_git(self):
        import hashlib
        members = self.source.CHECKPOINT_PACKAGE_RETARGETS
        self.assertEqual(len(members), 10)
        alternative = next(row[2] for row in members if row[2] != members[0][2])
        variants = (
            members[:-1],
            ((members[0][0], members[1][1], *members[0][2:]), *members[1:]),
            ((members[0][0], members[0][1], alternative, *members[0][3:]), *members[1:]),
            ((members[0][0], members[0][1], members[0][1], *members[0][3:]), *members[1:]),
            ((*members[0][:3], '0' * 40, *members[0][4:]), *members[1:]),
        )
        with patch.object(self.source, '_continuation_git', side_effect=AssertionError('bad retarget reached Git')):
            for changed in variants:
                self.assertNotEqual(changed, members)
                digest = hashlib.sha256(json.dumps(changed, separators=(',', ':')).encode()).hexdigest()
                with patch.object(self.source, 'CHECKPOINT_PACKAGE_RETARGETS', changed), \
                     patch.object(self.source, 'CHECKPOINT_PACKAGE_RETARGETS_SHA256', digest):
                    with self.assertRaises(ValueError):
                        self.source._checkpoint_package_copy_catalog()


class CheckpointCodeCopyMigrationTests(unittest.TestCase):
    """Authenticate archived source bytes without executing historical programs."""

    CONTEXT_RELATIONS = (
        ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/general-roots/src/test_design_rank.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-general-v1/test_design_rank.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/general-roots/src/design_rank.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-general-v1/design_rank.py', '24ec8da899ff548dcbadab483dc32a58962bf456', '37cf8f723bf3813ea2fecbe04185297eae30b4d2de8618f83715329bc8c9284a', 5995),
        ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/identifiability.py', 'd3a3fb5d457e047adb67e29d495d9955f698d569', 'c35e212dbc24066ec3f1baf6e4fe753d5eb16e71b1318f5d307de6c805d33c3d', 7578),
        ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/provision-identity/src/provision_semantics.py', 'research/t20-live-20261009/checkpoints/CP01/recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/provision-identity/src/provision_semantics.py', '1a1fd82dc9b75be5de778fc3436550865b991543', '6b06c7cec417a961052971d605b54570c34e44d3e0f0ddfc1a2021e384038268', 14477),
        ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/identification-review/frozen-v2/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/productive-identifiability/src/test_identifiability.py', 'research/t20-live-20261009/checkpoints/CP01/recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py', 'research/t20-live-20261009/checkpoints/CP01/recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-frontier-continuation/sovereignty-choice-semantics/reactive-context-extension/src/reactive_context.py', '14f8836f0c8b8a7e64a7943db200311204d8a88d', 'f73cee9c0271dd2a80843a3994534e1119fca33386e59a483f3175d69880a6cc', 6736),
        ('research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-review/frozen/test_crt_calibration.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-design/src/test_crt_calibration.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-review/frozen/crt_calibration.py', 'research/t20-live-20261009/checkpoints/CP01/t20-next-frontier-20261008/single-calibration-design/src/crt_calibration.py', '894119aece108e7fc93e6edd979e59edbcd44198', '8aa9f0b05291efdd876e9e9c2e4f04eeb09959b7b3d96adb1d6a4ee149faecec', 5074),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/countable_support.py', '0d09017120146576d7d58d6760747efff05a7712', 'e6e928ce4894770b671e1b74b4c7cf2f88e5a3b767bdbd28c0dd03a6b923e2f6', 8119),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/countable_support.py', '0d09017120146576d7d58d6760747efff05a7712', 'e6e928ce4894770b671e1b74b4c7cf2f88e5a3b767bdbd28c0dd03a6b923e2f6', 8119),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/gcd_decoder.py', '8ec47140335456b7cb1bced055f80aa86f22ba92', '3450a5cf943da435984a48bbb8e04a5c4cdb13ad7fa89bed48f18738ba70d827', 4257),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/countable_support.py', '0d09017120146576d7d58d6760747efff05a7712', 'e6e928ce4894770b671e1b74b4c7cf2f88e5a3b767bdbd28c0dd03a6b923e2f6', 8119),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/gcd_decoder.py', '8ec47140335456b7cb1bced055f80aa86f22ba92', '3450a5cf943da435984a48bbb8e04a5c4cdb13ad7fa89bed48f18738ba70d827', 4257),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_gcd_decoder.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/countable_support.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/countable_support.py', '0d09017120146576d7d58d6760747efff05a7712', 'e6e928ce4894770b671e1b74b4c7cf2f88e5a3b767bdbd28c0dd03a6b923e2f6', 8119),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/test_oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/test_oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-identification/src/oracle_boundaries.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/countable-signature-review/frozen/oracle_boundaries.py', '041fb80e6a60a25ddef3eaf67260661737fee6cf', 'f39ed4839663137b7c7863211de97fd6c33cf5b75486b5f96fd02cbc181cc060', 4206),
        ('research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/test_robust_masks.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-review/frozen/test_robust_masks.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-calibration/src/robust_masks.py', 'research/t20-live-20261009/checkpoints/CP02/t20-next-frontier-20261008/noise-aware-review/frozen/robust_masks.py', '8431f617edbe9d2429c9f3705bd26c1525c67bce', '1c818590a66e5e6b7af39d46c2db849bb2bb99e758a90771218c4b2cb148efd3', 9511),
        ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_appendix_controls/efficiency_controls.py', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/efficiency_controls.py', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_appendix_controls/POLYNOMIAL_EFFICIENCY_APPENDIX.md', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/POLYNOMIAL_EFFICIENCY_APPENDIX.md', '323b35e3a4827ab25416d551c84372cf88b11ed7', '4242d8cbcc9fd576266e2ee01f902b45c93e6701b5c01d07a5a0c3909f97f0f4', 7854),
        ('research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_author_controls/exact_controls.py', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/exact_controls.py', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity-review/replayed_author_controls/RESULT.md', 'research/t20-live-20261009/checkpoints/CP04/t20-next-frontier-20261008/global-calibration-ambiguity/RESULT.md', 'fd1c39b4bed42c37d997c95be9fb64b4b7d1a33b', 'ec620e491fd1c58cdc9dc0bcc8700784b79b4b399247ca1e2a235438138cf827', 12746),
        ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py', 'research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/compiler.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/compiler.py', '694261f36e31caf66ec6c2e79c1bf501e45d778c', '5da2762fe31720e898165751bf53636f66a5267719e0b3687587628c48ac4714', 6557),
        ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py', 'research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/compiler.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/compiler.py', '694261f36e31caf66ec6c2e79c1bf501e45d778c', '5da2762fe31720e898165751bf53636f66a5267719e0b3687587628c48ac4714', 6557),
        ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py', 'research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py', 'd8c2bd9d095b83b557982f27620bc4a830bedb13', 'ba6b947c758b0541ce4dc489c116c87cc6000ebc221ff23f8b5f3efd5de94f70', 10995),
        ('research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/verify.py', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/verify.py', 'research/t20-live-20261009/checkpoints/CP23/root-resumed-research-20261009/compilation-replay/RESULT.md', 'research/t20-live-20261009/checkpoints/CP23/certificate-compilation-boundary-20261009/RESULT.md', '44931a48d2fdf8c8e521928f60103dedad49dd9b', '3d8d11d73055b62913cf36138cc0b3b273d032f8f927a885ee2af11bd8eaf459', 22505),
    )

    setUp = CheckpointCopyMigrationTests.setUp
    _git = CheckpointCopyMigrationTests._git
    _put = CheckpointCopyMigrationTests._put
    _gate = CheckpointCopyMigrationTests._gate

    @classmethod
    def setUpClass(cls):
        import resolve_t20_v6_source as source
        cls.source = source
        cls.catalog = source._checkpoint_code_copy_catalog()
        if len(cls.catalog) != 52:
            raise AssertionError('code fixture population differs')
        cls.bodies = {}
        for alias, binding in cls.catalog.items():
            body = source.checkpoint_code_copy_bytes(projection.ROOT, alias)
            cls.bodies[alias] = body
            if cls.bodies.setdefault(binding['canonical'], body) != body:
                raise AssertionError('retained code body conflicts')
        for original_source, retained_source, original, retained, blob, identity, size in cls.CONTEXT_RELATIONS:
            for path in (original, retained):
                if path in cls.bodies:
                    if (source.digest(cls.bodies[path]), len(cls.bodies[path])) != (identity, size):
                        raise AssertionError('context overlaps a different code identity')
                    continue
                binding = dict(canonical=path, blob=blob, sha256=identity, bytes=size, mode='100644')
                cls.bodies[path] = source._checkpoint_bound_bytes(projection.ROOT, path, binding)
        manifest = json.loads((projection.ROOT / projection.MANIFEST).read_bytes())
        cls.public_rows = [r for r in manifest['objects'] if r.get('repository_path') in cls.catalog]
        if len(cls.public_rows) != 34 or {r['repository_path'] for r in cls.public_rows} != source.CHECKPOINT_CODE_PUBLIC_PATHS:
            raise AssertionError('existing public code population differs')
        cls.public_by_path = {r['repository_path']: r for r in cls.public_rows}

    def _reject(self, alias=None):
        with self.assertRaises((ValueError, OSError)):
            self.source.checkpoint_code_copy_bytes(self.repo, alias or self.alias)

    def _row(self, alias):
        if alias in self.public_by_path:
            return dict(self.public_by_path[alias])
        binding = self.catalog[alias]
        return dict(repository_path=alias, disposition='REUSE', role='authored_code', source_action='include',
                    source_sha256=binding['sha256'], public_sha256=binding['sha256'],
                    source_bytes=binding['bytes'], public_bytes=binding['bytes'])

    def test_all_52_sources_keep_exact_bytes_and_references_in_three_states(self):
        import os
        import validate_internal_references as references
        with patch.object(references, 'ROOT', str(self.repo)):
            for state in ('present', 'unstaged-absence', 'staged-absence'):
                if state == 'unstaged-absence':
                    for alias in self.catalog:
                        (self.repo / alias).unlink()
                elif state == 'staged-absence':
                    self._git('update-index', '--force-remove', '--', *self.catalog)
                before = (self.repo / '.git/index').read_bytes()
                expected_absent = set() if state == 'present' else set(self.catalog)
                self.assertEqual({p for p in self.catalog if not os.path.lexists(self.repo / p)}, expected_absent)
                for alias in self.catalog:
                    self.assertEqual(self.source.checkpoint_code_copy_bytes(self.repo, alias), self.bodies[alias])
                    self.assertTrue(references._resolves(alias, alias))
                    self.assertTrue(references._resolves(alias, pathlib.PurePosixPath(alias).name))
                self.assertEqual(self.source.checkpoint_code_duplicate_paths(self.repo), expected_absent)
                self.assertEqual(self._gate(), [])
                self.assertEqual({p for p in self.catalog if not os.path.lexists(self.repo / p)}, expected_absent)
                self.assertEqual((self.repo / '.git/index').read_bytes(), before)

    def test_34_actual_rows_preserve_identity_and_18_nonpublic_routes_stay_nonpublic(self):
        import os
        nonpublic = set(self.catalog) - set(self.public_by_path)
        self.assertEqual(len(nonpublic), 18)
        for absent in (False, True):
            if absent:
                for alias in self.catalog:
                    (self.repo / alias).unlink()
            before = (self.repo / '.git/index').read_bytes()
            for row in self.public_rows:
                with self.subTest(path=row['repository_path'], absent=absent):
                    self.assertEqual(check_object(self.repo, row), [])
                    self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[row['repository_path']])
            for alias in nonpublic:
                with self.subTest(nonpublic=alias, absent=absent):
                    self.assertEqual(self.source.checkpoint_code_copy_bytes(self.repo, alias), self.bodies[alias])
                    self.assertEqual(check_object(self.repo, self._row(alias)), ['missing or unsafe public source'])
                    with self.assertRaises(ValueError):
                        self.source.source_bytes(self.repo, self._row(alias))
            self.assertEqual((self.repo / '.git/index').read_bytes(), before)
            self.assertEqual({p for p in self.catalog if not os.path.lexists(self.repo / p)}, set(self.catalog) if absent else set())

    def test_each_public_code_row_requires_exact_identity_role_action_and_native_policy(self):
        faults = (('disposition', 'ADD_EXACT'), ('source_sha256', '0' * 64), ('public_sha256', '0' * 64),
                  ('source_bytes', 1), ('public_bytes', 1), ('repository_revision', self.baseline),
                  ('git_blob', '0' * 40), ('role', 'recorded_output'), ('source_action', 'exclude'),
                  ('repository_path', '../outside.py'))
        for actual in self.public_rows:
            for field, value in faults:
                with self.subTest(path=actual['repository_path'], field=field):
                    row = dict(actual); row[field] = value
                    self.assertTrue(check_object(self.repo, row))
                    with self.assertRaises(ValueError):
                        self.source.source_bytes(self.repo, row)

    def test_unknown_or_changed_code_and_public_populations_fail_before_git(self):
        with patch.object(self.source, '_continuation_git', side_effect=AssertionError('unlisted code reached Git')):
            for name in (self.extra, self.alias + '.other', '../' + self.alias, '/' + self.alias,
                         self.alias.replace('/', '\\'), None):
                with self.subTest(path=name):
                    with self.assertRaises(ValueError):
                        self.source.checkpoint_code_copy_bytes(self.repo, name)
            for name in ('CHECKPOINT_CODE_COPY_MEMBERS', 'CHECKPOINT_CODE_PUBLIC_MEMBERS'):
                with patch.object(self.source, name, getattr(self.source, name)[:-1]):
                    self._reject()

    def test_all_code_bodies_remain_inert(self):
        with patch('builtins.compile', side_effect=AssertionError('historical source compiled')), \
             patch('builtins.exec', side_effect=AssertionError('historical source executed')):
            for alias in self.catalog:
                self.assertEqual(self.source.checkpoint_code_copy_bytes(self.repo, alias), self.bodies[alias])

    def test_19_original_module_and_input_contexts_preserve_exact_source_access(self):
        import os
        import validate_internal_references as references
        self.assertEqual(len(self.CONTEXT_RELATIONS), 19)
        with patch.object(references, 'ROOT', str(self.repo)):
            for state in ('present', 'unstaged-absence', 'staged-absence'):
                if state == 'unstaged-absence':
                    for alias in self.catalog:
                        (self.repo / alias).unlink()
                elif state == 'staged-absence':
                    self._git('update-index', '--force-remove', '--', *self.catalog)
                before = (self.repo / '.git/index').read_bytes()
                for original_source, retained_source, original, retained, blob, identity, size in self.CONTEXT_RELATIONS:
                    for source, path in ((original_source, original), (retained_source, retained)):
                        with self.subTest(source=source, target=path, state=state):
                            if path in self.catalog:
                                body = self.source.checkpoint_code_copy_bytes(self.repo, path)
                            else:
                                binding = dict(canonical=path, blob=blob, sha256=identity, bytes=size, mode='100644')
                                body = self.source._checkpoint_bound_bytes(self.repo, path, binding)
                            self.assertEqual((self.source.digest(body), len(body)), (identity, size))
                            relative = os.path.relpath(path, os.path.dirname(source))
                            self.assertTrue(references._resolves(source, path))
                            self.assertTrue(references._resolves(source, relative))
                self.assertEqual((self.repo / '.git/index').read_bytes(), before)
                self.assertEqual({p for p in self.catalog if not os.path.lexists(self.repo / p)},
                                 set() if state == 'present' else set(self.catalog))

    test_present_corruption_cannot_fall_back_to_a_correct_retained_copy = CheckpointCopyMigrationTests.test_present_corruption_cannot_fall_back_to_a_correct_retained_copy
    test_wrong_missing_or_executable_counterpart_rejects_absent_alias = CheckpointCopyMigrationTests.test_wrong_missing_or_executable_counterpart_rejects_absent_alias
    test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence = CheckpointCopyMigrationTests.test_leaf_ancestor_and_dangling_alias_symlinks_never_mean_absence
    test_staged_alias_tamper_cannot_hide_under_worktree_absence = CheckpointCopyMigrationTests.test_staged_alias_tamper_cannot_hide_under_worktree_absence
    test_staged_retained_tamper_cannot_hide_under_exact_worktree = CheckpointCopyMigrationTests.test_staged_retained_tamper_cannot_hide_under_exact_worktree
    test_unmerged_or_wrong_mode_index_is_rejected = CheckpointCopyMigrationTests.test_unmerged_or_wrong_mode_index_is_rejected
    test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances = CheckpointCopyMigrationTests.test_unrelated_staged_changes_are_not_checkpoint_deletion_allowances
    test_missing_pinned_commit_rejects_even_present_exact_bodies = CheckpointCopyMigrationTests.test_missing_pinned_commit_rejects_even_present_exact_bodies
    test_root_and_relative_references_authenticate_before_exists = CheckpointCopyMigrationTests.test_root_and_relative_references_authenticate_before_exists
    test_replacement_restores_exact_fixture_identity_vector = CheckpointCopyMigrationTests.test_replacement_restores_exact_fixture_identity_vector

    _reader_currentness = CheckpointCopyMigrationTests._reader_currentness
    test_reader_currentness_authenticates_present_and_both_absence_states = CheckpointCopyMigrationTests.test_reader_currentness_authenticates_present_and_both_absence_states
    test_reader_currentness_rejects_retained_body_and_index_tampering = CheckpointCopyMigrationTests.test_reader_currentness_rejects_retained_body_and_index_tampering
    test_reader_currentness_rejects_present_alias_and_unrelated_changes = CheckpointCopyMigrationTests.test_reader_currentness_rejects_present_alias_and_unrelated_changes



class HistoricalSuccessorFixtureRouteTests(unittest.TestCase):
    SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1] / 'scripts'
    FIXTURE_PATH = pathlib.Path(__file__).resolve().parents[1] / 'tests/v5_successor_fixtures.py'
    RESOURCE_ROOT = None
    ROW = {
        'source_sha256': '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
        'source_action': 'include', 'source_bytes': 13030, 'role': 'authored_code',
        'declared_eligibility_basis': 'reviewed_owner_authored', 'required_dependencies': [],
        'disposition': 'REUSE', 'repository_path': 'tests/v5_successor_fixtures.py',
        'repository_revision': '69f3f9284f2cb94433958c0669fc9b06a9760fe7',
        'git_blob': 'ccf0bd64f34b10f65ed8bd1bdd8a88adcaf03c7f',
        'public_sha256': '283ea7d698a5bf6a208e45260ee9078f819ecdb25a42c6dd2252d794d2dd3233',
        'public_bytes': 13030, 'publication_basis': 'exact_existing_public_repository_object',
    }
    CURRENT = ('350c192a7c912232889673110d326e4242bde8cf',
               'd1b092a7deb91b71812f838d87d4af8de37fc72184b84eff8e8348d743ac0fb7', 12785)

    @staticmethod
    def _identity(body):
        return (hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                hashlib.sha256(body).hexdigest(), len(body))

    def _load_interfaces(self):
        # Compile only these operational definitions, never the fixture body or
        # either complete production module. Unrelated dispatch populations are
        # empty synthetic inputs; the actual target route is left intact.
        resolver = self.SOURCE_ROOT / 'resolve_t20_v6_source.py'
        functions = {'digest', 'source_bytes', '_successor_input_path',
                     '_successor_input_regular', 'successor_fixture_source_bytes'}
        constants = {'HISTORICAL_PROSE_REVISION', 'SUCCESSOR_FIXTURE_PATH',
                     'SUCCESSOR_FIXTURE_PUBLIC_ROW', 'SUCCESSOR_FIXTURE_CURRENT'}
        nodes = []
        for node in ast.parse(resolver.read_bytes(), filename=str(resolver)).body:
            if isinstance(node, ast.FunctionDef) and node.name in functions: nodes.append(node)
            elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                  and isinstance(node.targets[0], ast.Name) and node.targets[0].id in constants): nodes.append(node)
        namespace = {'pathlib': pathlib, 'hashlib': hashlib, 'os': os, 'stat': stat,
                     'subprocess': types.SimpleNamespace(run=self._native, check_output=self._legacy,
                                                         CalledProcessError=subprocess.CalledProcessError),
                     'is_binding_record': lambda root, path: False,
                     'SUCCESSOR_INPUT_PATHS': (), 'GENERATED_FIXTURE_PATHS': (),
                     'DIGEST_RECORD_PATHS': (), 'FORMAL_COPY_PATHS': (),
                     'CONTINUATION_FORMAL_RETARGET_PATHS': (),
                     'CONTINUATION_REGISTRY_PATH': 'synthetic/other-registry.json',
                     'ADMIN_PUBLIC_GUIDE_PATHS': (), 'HISTORICAL_PROSE': {},
                     'CHECKPOINT_CODE_COPY_PATHS': (), 'CHECKPOINT_RECORD_COPY_PATHS': (),
                     'CHECKPOINT_COPY_PATHS': (), 'CONTINUATION_COPY_ROOT': 'synthetic/other-continuation/'}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(resolver), 'exec'), namespace)
        self.resolver = namespace
        projection = self.SOURCE_ROOT / 'validate_t20_v6_projection.py'
        nodes = [node for node in ast.parse(projection.read_bytes(), filename=str(projection)).body
                 if isinstance(node, ast.FunctionDef) and node.name in {'check_object', 'safe_path', 'sha256'}]
        projection_namespace = dict(namespace, re=re, SHA=re.compile(r'[0-9a-f]{64}\Z'),
                                    BASE=namespace['HISTORICAL_PROSE_REVISION'],
                                    binding_record_candidate=lambda path: False,
                                    source_bytes=namespace['source_bytes'])
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(projection), 'exec'), projection_namespace)
        self.projection = projection_namespace

    def setUp(self):
        if self.RESOURCE_ROOT is None:
            self.area = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory(prefix='t20-fixture-route-')))
        else:
            self.area = pathlib.Path(self.RESOURCE_ROOT) / self.id()
            self.area.mkdir()
            self.addCleanup(shutil.rmtree, self.area)
        self.current = self.FIXTURE_PATH.read_bytes()
        self.assertEqual(self._identity(self.current), self.CURRENT)
        # Invert only the three reviewed calculus-fixture removals. This yields
        # exact inert historical bytes without invoking Git or importing code.
        anchor = b"            'EMPIRICAL_SCOPE': {'results': bundle['empirical']},\n"
        original = b"            'CALCULUS_MAP': {'results': bundle['calculus']},\n" + anchor
        self.assertEqual(self.current.count(anchor), 1)
        self.historical = self.current.replace(anchor, original)
        anchor = b"              'empirical': [], 'supplementary': {}, 'projection_reviews': [],\n"
        original = (b"              'calculus': [{'id': result['id'], 'calculus': 'NONE', 'operational_model': result['operational_model'],\n"
                    b"                           'canonical_adoption': 'NOT_ADOPTED'}],\n" + anchor)
        self.assertEqual(self.historical.count(anchor), 1)
        self.historical = self.historical.replace(anchor, original)
        self.assertEqual(self._identity(self.historical),
                         (self.ROW['git_blob'], self.ROW['public_sha256'], self.ROW['public_bytes']))
        self.case_number = 0
        self._load_interfaces()
        self._case()

    def _case(self):
        self.repo = self.area / ('case-' + str(self.case_number)); self.case_number += 1
        self.repo.mkdir()
        self.target = self.repo / self.ROW['repository_path']
        self.target.parent.mkdir(); self.target.write_bytes(self.current); self.target.chmod(0o644)
        self.current_oid = self.CURRENT[0]
        self.native_commands, self.legacy_commands = [], []
        self.overrides = {}
        self.after_blob = None
        self.after_repeated_index = None

    def _native(self, argv, *, cwd, capture_output, check, env):
        self.assertEqual(argv[:3], ['git', '--no-replace-objects', '--literal-pathspecs'])
        self.assertEqual(pathlib.Path(cwd), self.repo)
        self.assertTrue(capture_output); self.assertFalse(check)
        self.assertEqual({name: env[name] for name in ('GIT_NO_LAZY_FETCH', 'GIT_NO_REPLACE_OBJECTS',
                                                     'GIT_ALLOW_PROTOCOL', 'GIT_TERMINAL_PROMPT')},
                         {'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1',
                          'GIT_ALLOW_PROTOCOL': '', 'GIT_TERMINAL_PROMPT': '0'})
        command = tuple(argv[3:]); self.native_commands.append(command)
        revision, path, blob = self.ROW['repository_revision'], self.ROW['repository_path'], self.ROW['git_blob']
        replies = {
            ('cat-file', '-t', revision): b'commit\n',
            ('ls-tree', '-z', revision, '--', path): ('100644 blob ' + blob + '\t' + path + '\0').encode(),
            ('cat-file', 'blob', blob): self.historical,
            ('ls-files', '--stage', '-z', '--', path): ('100644 ' + self.current_oid + ' 0\t' + path + '\0').encode(),
        }
        self.assertIn(command, replies, 'No unbounded or unrelated native request is permitted')
        result = self.overrides.get(command, (0, replies[command]))
        if command == ('cat-file', 'blob', blob) and self.after_blob is not None:
            callback, self.after_blob = self.after_blob, None
            callback()
        if (command == ('ls-files', '--stage', '-z', '--', path)
                and self.native_commands.count(command) == 2 and self.after_repeated_index is not None):
            callback, self.after_repeated_index = self.after_repeated_index, None
            callback()
        return subprocess.CompletedProcess(argv, result[0], result[1], b'')

    def _legacy(self, argv, *, cwd):
        self.legacy_commands.append(argv)
        self.assertEqual(pathlib.Path(cwd), self.repo)
        self.assertEqual(argv, ['git', 'show', self.resolver['HISTORICAL_PROSE_REVISION'] + ':docs/' 'synthetic_legacy.txt'])
        return b'inert legacy baseline body\n'

    def _source(self, row=None):
        return self.resolver['source_bytes'](self.repo, dict(self.ROW) if row is None else row)

    def _projection(self, row=None):
        return self.projection['check_object'](self.repo, dict(self.ROW) if row is None else row)

    def _rejected(self, row=None):
        with self.assertRaises((ValueError, KeyError, OSError)): self._source(row)
        self.assertTrue(self._projection(row))

    def test_exact_full_row_resolves_inert_historical_body(self):
        self.assertEqual(self._source(), self.historical)
        self.assertNotEqual(self.historical, self.current)
        self.assertEqual(self.legacy_commands, [])

    def test_exact_full_row_passes_projection_dispatch(self):
        self.assertEqual(self._projection(), [])
        self.assertEqual(self.legacy_commands, [])

    def test_production_pins_equal_exact_reviewed_coordinates(self):
        self.assertEqual(self.resolver['SUCCESSOR_FIXTURE_PUBLIC_ROW'], self.ROW)
        self.assertEqual(len(self.resolver['SUCCESSOR_FIXTURE_PUBLIC_ROW']), 13)
        self.assertEqual(self.resolver['SUCCESSOR_FIXTURE_PATH'], self.ROW['repository_path'])
        self.assertEqual(self.resolver['SUCCESSOR_FIXTURE_CURRENT'], self.CURRENT)

    def test_every_row_field_tamper_and_omission_refuses(self):
        for name, original in self.ROW.items():
            with self.subTest(field=name, change='value'):
                row = dict(self.ROW)
                row[name] = original + 1 if type(original) is int else ['unreviewed-dependency'] if isinstance(original, list) else original + '-changed'
                self._rejected(row)
            with self.subTest(field=name, change='omitted'):
                row = dict(self.ROW); del row[name]
                self._rejected(row)
        self.assertEqual(self.native_commands, [])
        self.assertEqual(self.legacy_commands, [])

    def test_extra_field_float_size_and_lexical_alias_refuse(self):
        for change in ({'extra': 'unreviewed'}, {'source_bytes': 13030.0}, {'public_bytes': 13030.0},
                       {'repository_path': 'tests/./v5_successor_fixtures.py'},
                       {'repository_path': 'tests//v5_successor_fixtures.py'},
                       {'repository_path': './tests/v5_successor_fixtures.py'}):
            with self.subTest(change=change): self._rejected(dict(self.ROW, **change))
        self.assertEqual(self.native_commands, [])

    def test_unrelated_path_or_revision_has_no_new_exception(self):
        for change in ({'repository_path': 'tests/' 'nearby_successor_fixtures.py'},
                       {'repository_revision': self.resolver['HISTORICAL_PROSE_REVISION']},
                       {'repository_revision': None}, {'git_blob': '0' * 40}):
            with self.subTest(change=change): self._rejected(dict(self.ROW, **change))
        self.assertEqual(self.native_commands, [])
        self.assertEqual(self.legacy_commands, [])

    def test_existing_generic_baseline_route_is_unchanged(self):
        body = b'inert legacy baseline body\n'
        row = dict(self.ROW, repository_path='docs/' 'synthetic_legacy.txt',
                   repository_revision=self.resolver['HISTORICAL_PROSE_REVISION'],
                   source_sha256=hashlib.sha256(body).hexdigest(), public_sha256=hashlib.sha256(body).hexdigest(),
                   source_bytes=len(body), public_bytes=len(body), git_blob=self._identity(body)[0])
        self.assertEqual(self._source(row), body)
        self.assertEqual(self._projection(row), [])
        self.assertEqual(len(self.legacy_commands), 2)
        self.assertEqual(self.native_commands, [])

    def test_exact_original_current_alias_is_also_qualified(self):
        self.target.write_bytes(self.historical); self.current_oid = self.ROW['git_blob']
        self.assertEqual(self._source(), self.historical)
        self.assertEqual(self._projection(), [])

    def test_current_missing_corrupt_executable_or_directory_refuses(self):
        for corruption in ('missing', 'bytes', 'short', 'executable', 'directory'):
            with self.subTest(corruption=corruption):
                self._case()
                if corruption == 'missing': self.target.unlink()
                elif corruption == 'bytes': self.target.write_bytes(b'X' * len(self.current))
                elif corruption == 'short': self.target.write_bytes(self.current[:-1])
                elif corruption == 'executable': self.target.chmod(0o755)
                else: self.target.unlink(); self.target.mkdir()
                self._rejected()
                self.assertEqual(self.native_commands, [])

    def test_current_symlink_parent_symlink_and_hardlink_refuse(self):
        for alias in ('final-symlink', 'parent-symlink', 'hardlink'):
            with self.subTest(alias=alias):
                self._case()
                if alias == 'final-symlink':
                    other = self.repo / 'synthetic-target'; other.write_bytes(self.current)
                    self.target.unlink(); self.target.symlink_to(other)
                elif alias == 'parent-symlink':
                    parent = self.target.parent; moved = parent.with_name('synthetic-tests-target')
                    parent.rename(moved); parent.symlink_to(moved, target_is_directory=True)
                else: os.link(self.target, self.repo / 'synthetic-hardlink')
                self._rejected()
                self.assertEqual(self.native_commands, [])

    def test_root_and_root_ancestor_symlinks_refuse(self):
        for alias in ('root', 'ancestor'):
            with self.subTest(alias=alias):
                self._case()
                if alias == 'root':
                    link = self.area / ('linked-root-' + str(self.case_number)); link.symlink_to(self.repo, target_is_directory=True)
                    self.repo = link
                else:
                    link = self.area / ('linked-parent-' + str(self.case_number)); link.symlink_to(self.area, target_is_directory=True)
                    self.repo = link / self.repo.name
                self._rejected()
                self.assertEqual(self.native_commands, [])

    def test_native_commit_type_and_missing_commit_refuse(self):
        command = ('cat-file', '-t', self.ROW['repository_revision'])
        for result in ((0, b'blob\n'), (0, b'tag\n'), (1, b'')):
            with self.subTest(result=result):
                self._case(); self.overrides[command] = result; self._rejected()

    def test_native_path_mode_type_blob_and_extra_entries_refuse(self):
        row = self.ROW
        good = ('100644 blob ' + row['git_blob'] + '\t' + row['repository_path'] + '\0').encode()
        for bad in (b'', good.replace(b'100644', b'100755'), good.replace(b' blob ', b' tree '),
                    good.replace(row['git_blob'].encode(), b'0' * 40), good.replace(b'v5_successor', b'nearby_successor'), good + good):
            with self.subTest(reply=bad):
                self._case(); self.overrides[('ls-tree', '-z', row['repository_revision'], '--', row['repository_path'])] = (0, bad)
                self._rejected()

    def test_native_object_missing_truncated_extra_or_corrupt_refuses(self):
        command = ('cat-file', 'blob', self.ROW['git_blob'])
        for result in ((1, b''), (0, self.historical[:-1]), (0, self.historical + b'\n'), (0, b'X' * len(self.historical))):
            with self.subTest(returncode=result[0], length=len(result[1])):
                self._case(); self.overrides[command] = result; self._rejected()

    def test_current_index_identity_mode_stage_and_absence_refuse(self):
        row = self.ROW
        good = ('100644 ' + self.current_oid + ' 0\t' + row['repository_path'] + '\0').encode()
        for bad in (b'', good.replace(self.current_oid.encode(), row['git_blob'].encode()),
                    good.replace(b'100644', b'100755'), good.replace(b' 0\t', b' 1\t'), good + good):
            with self.subTest(reply=bad):
                self._case(); self.overrides[('ls-files', '--stage', '-z', '--', row['repository_path'])] = (0, bad)
                self._rejected()

    def test_current_disappearance_or_replacement_during_native_read_refuses(self):
        for interface in ('source', 'projection'):
            for mutation in ('disappearance', 'same-byte-replacement', 'corruption'):
                with self.subTest(interface=interface, mutation=mutation):
                    self._case()
                    def change():
                        if mutation == 'disappearance': self.target.unlink()
                        elif mutation == 'same-byte-replacement':
                            replacement = self.repo / 'synthetic-replacement'; replacement.write_bytes(self.current)
                            replacement.replace(self.target)
                        else: self.target.write_bytes(b'X' * len(self.current))
                    self.after_blob = change
                    if interface == 'source':
                        with self.assertRaises((ValueError, OSError)): self._source()
                    else: self.assertTrue(self._projection())

    def test_current_index_changed_during_native_read_refuses(self):
        for interface in ('source', 'projection'):
            with self.subTest(interface=interface):
                self._case()
                def change():
                    self.current_oid = self.ROW['git_blob']
                self.after_blob = change
                if interface == 'source':
                    with self.assertRaises(ValueError): self._source()
                else: self.assertTrue(self._projection())

    def test_current_disappearance_during_final_native_read_refuses(self):
        for interface in ('source', 'projection'):
            with self.subTest(interface=interface):
                self._case()
                self.after_repeated_index = self.target.unlink
                if interface == 'source':
                    with self.assertRaises((ValueError, OSError)): self._source()
                else: self.assertTrue(self._projection())





class FormalCopyMigrationTests(unittest.TestCase):
    """Native finite-copy guards; no Lean or historical replay is executed."""

    @classmethod
    def setUpClass(cls):
        import resolve_t20_v6_source as source
        cls.source = source
        cls.catalog = source._formal_copy_catalog()
        if len(cls.catalog) != 71:
            raise AssertionError('formal fixture population differs')
        cls.bodies = {}
        for alias, binding in cls.catalog.items():
            body = source.formal_copy_bytes(projection.ROOT, alias)
            cls.bodies[alias] = body
            if cls.bodies.setdefault(binding['canonical'], body) != body:
                raise AssertionError('retained formal body conflicts')
        cls.public = [r for r in json.loads((projection.ROOT / projection.MANIFEST).read_bytes())['objects']
                      if r.get('repository_path') in source.FORMAL_COPY_PATHS]
        cls.continuations = [r for r in json.loads((projection.ROOT /
            'docs/provenance/v5-research-continuations/SOURCE_MAP.json').read_bytes())['sources']
            if r.get('path') in source.FORMAL_CONTINUATION_PATHS]
        cls.successors = [r for r in json.loads((projection.ROOT /
            'docs/provenance/v5-successors/SOURCE_MAP.json').read_bytes())['sources']
            if r.get('public_path') in source.FORMAL_SUCCESSOR_PATHS]
        cls.allowlist = [r for r in json.loads((projection.ROOT /
            'docs/provenance/v5-successors/PUBLIC_PROJECTION.json').read_bytes())['allowlist']
            if r.get('path') in source.FORMAL_SUCCESSOR_PATHS]
        if tuple(map(len, (cls.public, cls.continuations, cls.successors, cls.allowlist))) != (26, 12, 9, 3):
            raise AssertionError('actual formal source-role rows differ')

    setUp = CheckpointCopyMigrationTests.setUp
    _git = CheckpointCopyMigrationTests._git
    _put = CheckpointCopyMigrationTests._put
    _gate = CheckpointCopyMigrationTests._gate

    def _reject(self, path=None):
        with self.assertRaises((ValueError, OSError)):
            self.source.formal_copy_bytes(self.repo, path or self.alias)

    def test_native_formal_copies_survive_absence_and_staged_absence(self):
        for path in self.catalog:
            (self.repo / path).unlink()
        self.assertEqual(self.source.formal_duplicate_paths(self.repo), set(self.catalog))
        for path in self.catalog:
            self.assertEqual(self.source.formal_copy_bytes(self.repo, path), self.bodies[path])
        self._git('add', '-u')
        self.assertEqual(self.source.formal_duplicate_paths(self.repo), set(self.catalog))
        for row in self.public:
            self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[row['repository_path']])

    def test_changed_alias_and_retained_body_are_rejected(self):
        for path in (self.alias, self.canonical):
            with self.subTest(path=path):
                self._put(path, self.bodies[path] + b'\n-- changed inert source\n')
                self._reject()
                self._put(path, self.bodies[path])

    def test_executable_formal_alias_and_retained_source_are_rejected(self):
        for path in (self.alias, self.canonical):
            with self.subTest(path=path):
                (self.repo / path).chmod(0o755)
                self._reject()
                (self.repo / path).chmod(0o644)

    def test_symlink_formal_alias_and_retained_source_are_rejected(self):
        for path in (self.alias, self.canonical):
            with self.subTest(path=path):
                target = self.repo / path
                target.unlink()
                target.symlink_to(self.repo / (self.canonical if path == self.alias else self.alias))
                self._reject()
                target.unlink()
                self._put(path, self.bodies[path])

    def test_staged_mode_and_blob_substitutions_are_rejected(self):
        blob = self.catalog[self.alias]['blob']
        wrong = self._git('hash-object', '-w', '--stdin', input=b'unrelated public fixture\n').decode().strip()
        for path in (self.alias, self.canonical):
            for mode, identity in (('100755', blob), ('100644', wrong)):
                with self.subTest(path=path, mode=mode, blob=identity):
                    self._git('update-index', '--cacheinfo', mode + ',' + identity + ',' + path)
                    self._reject()
                    self._git('update-index', '--cacheinfo', '100644,' + blob + ',' + path)

    def test_unavailable_history_and_wrong_requested_identity_are_rejected(self):
        with patch.object(self.source, 'CHECKPOINT_COPY_BASE', '0' * 40):
            self._reject()
        for values in ({'identity': '0' * 64}, {'size': -1}):
            with self.assertRaises(ValueError):
                self.source.formal_copy_bytes(self.repo, self.alias, **values)
        for value in (None, '../unknown.lean', self.extra):
            with self.assertRaises(ValueError):
                self.source.formal_copy_bytes(self.repo, value)

    def test_all_existing_public_fields_remain_bound(self):
        import copy
        for row in self.public:
            self.assertEqual(self.source.source_bytes(self.repo, row), self.bodies[row['repository_path']])
            for key, value in row.items():
                changed = copy.deepcopy(row)
                changed[key] = (value + '-changed' if isinstance(value, str) else
                                value + 1 if type(value) is int else ['unadmitted-field-value'])
                with self.subTest(path=row['repository_path'], field=key), self.assertRaises(ValueError):
                    self.source._formal_public_source_bytes(self.repo, changed)

    def test_nonpublic_formal_aliases_gain_no_public_admission(self):
        published = {r['repository_path'] for r in self.public}
        for path in set(self.catalog) - published:
            binding = self.catalog[path]
            row = dict(repository_path=path, disposition='REUSE', source_sha256=binding['sha256'],
                       public_sha256=binding['sha256'], source_bytes=binding['bytes'], public_bytes=binding['bytes'])
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.source.source_bytes(self.repo, row)

    def test_full_continuation_origin_member_and_module_source_rows_remain_bound(self):
        import copy
        for row in self.continuations:
            self.assertEqual(self.source.continuation_formal_source_bytes(self.repo, row), self.bodies[row['path']])
            for key in row:
                changed = copy.deepcopy(row)
                changed[key] = 'changed-field-value'
                with self.subTest(source=row['id'], field=key), self.assertRaises(ValueError):
                    self.source.continuation_formal_source_bytes(self.repo, changed)

    def test_full_successor_origins_and_allowlist_associations_remain_bound(self):
        import copy
        for row in self.successors:
            self.assertEqual(self.source.successor_formal_source_bytes(self.repo, row), self.bodies[row['public_path']])
            for key in row:
                changed = copy.deepcopy(row)
                changed[key] = 'changed-field-value'
                with self.subTest(source=row['id'], field=key), self.assertRaises(ValueError):
                    self.source.successor_formal_source_bytes(self.repo, changed)
        for row in self.allowlist:
            self.assertEqual(self.source.successor_formal_allowlist_bytes(self.repo, row), self.bodies[row['path']])
            for key in row:
                changed = copy.deepcopy(row)
                changed[key] = 'changed-field-value'
                with self.subTest(path=row['path'], field=key), self.assertRaises(ValueError):
                    self.source.successor_formal_allowlist_bytes(self.repo, changed)

    def test_preservation_accepts_only_checkpoint_D_not_staged_M_or_T(self):
        path = next(p for p in self.catalog if p.startswith(self.source.CHECKPOINT_COPY_ROOT))
        (self.repo / path).unlink()
        self.assertEqual(self._gate(), [])
        self._git('add', '-u')
        self.assertEqual(self._gate(), [])
        self._put(path, self.bodies[path] + b'\n-- changed\n')
        self._git('add', '--', path)
        (self.repo / path).unlink()
        self.assertTrue(self._gate())
        self._put(path, self.bodies[path])
        self._git('add', '--', path)
        (self.repo / path).unlink()
        (self.repo / path).symlink_to(self.repo / self.catalog[path]['canonical'])
        self._git('add', '--', path)
        (self.repo / path).unlink()
        self.assertTrue(self._gate())


class FormalCurrentCompositionControls(unittest.TestCase):
    """Finite operational interfaces; no original formal/replay program runs."""

    @classmethod
    def _module(cls, name, functions, *, source_constants=False):
        import collections
        filename = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / name
        tree = ast.parse(filename.read_text(encoding='utf-8'))
        nodes = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in functions:
                nodes.append(node)
            elif source_constants and isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and (target.id.startswith(
                        ('FORMAL_', 'CONTINUATION_FORMAL_', 'CHECKPOINT_', 'BINDING_RECORD_'))
                        or target.id in {'CONTINUATION_COPY_ROOT', 'STATUS_RECORD_PATH_HASHES', 'STATUS_RECORD_OWNERS'})
                    for target in node.targets):
                nodes.append(node)
        found = {node.name for node in nodes if isinstance(node, ast.FunctionDef)}
        if found != set(functions):
            raise AssertionError('operational fixture function population differs')
        module = types.ModuleType('formal_current_' + name.replace('.', '_'))
        module.__dict__.update(hashlib=hashlib, json=json, pathlib=pathlib, os=os, re=re,
                               stat=stat, collections=collections, subprocess=subprocess,
                               Path=pathlib.Path)
        future = ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0)
        code = ast.fix_missing_locations(ast.Module(body=[future, *nodes], type_ignores=[]))
        exec(compile(code, str(filename), 'exec'), module.__dict__)
        return module

    def setUp(self):
        self.source = self._module('resolve_t20_v6_source.py', {
            'digest', '_formal_tuple_binding', '_formal_copy_catalog', '_formal_row_digest',
            '_formal_public_source_bytes', '_continuation_formal_bound_bytes', 'source_bytes',
            'binding_record_candidate', 'is_binding_record',
            'status_record_candidate'}, source_constants=True)
        self.source.DIGEST_RECORD_PATHS = frozenset()
        self.source.SUCCESSOR_FIXTURE_PATH = 'synthetic-unused-fixture-coordinate'
        self.source.SUCCESSOR_INPUT_PATHS = frozenset()
        self.source.GENERATED_FIXTURE_PATHS = frozenset()
        self.source.CONTINUATION_REGISTRY_PATH = 'synthetic-unused-registry-coordinate'
        manifest = pathlib.Path(__file__).resolve().parents[1] / 'research/t20-v6-20261012/PUBLIC_PROJECTION_MANIFEST.json'
        public = dict(self.source.FORMAL_PUBLIC_MEMBERS)
        self.rows = {row['repository_path']: row for row in json.loads(manifest.read_text())['objects']
                     if row.get('repository_path') in public}
        self.assertEqual(len(self.rows), 27)
        self.assertEqual({path: self.source._formal_row_digest(row) for path, row in self.rows.items()}, public)
        self.prior_path, = self.source.CONTINUATION_FORMAL_RETARGET_PATHS

    def _prior_field(self, field):
        import copy
        original = self.rows[self.prior_path]
        self.assertIn(field, original)
        for mode in ('changed', 'missing'):
            changed = copy.deepcopy(original)
            if mode == 'missing':
                del changed[field]
            else:
                value = changed[field]
                changed[field] = (value + '-changed' if isinstance(value, str) else
                                  value + 1 if type(value) is int else ['unadmitted-fixture-value'])
            with self.subTest(field=field, mode=mode), patch.object(
                    self.source, 'continuation_copy_bytes', create=True,
                    side_effect=AssertionError('changed complete row reached a body getter')) as getter:
                with self.assertRaisesRegex(ValueError, 'formal existing public role or complete identity differs'):
                    self.source._formal_public_source_bytes(pathlib.Path('unused-synthetic-root'), changed)
                getter.assert_not_called()

    def test_prior_declared_eligibility_basis_is_bound(self):
        self._prior_field('declared_eligibility_basis')

    def test_prior_required_dependencies_are_bound(self):
        self._prior_field('required_dependencies')

    def test_prior_disposition_is_bound(self):
        self._prior_field('disposition')

    def test_prior_repository_path_is_bound(self):
        self._prior_field('repository_path')

    def test_prior_public_sha256_is_bound(self):
        self._prior_field('public_sha256')

    def test_prior_public_bytes_are_bound(self):
        self._prior_field('public_bytes')

    def test_prior_publication_basis_is_bound(self):
        self._prior_field('publication_basis')

    def test_current_public_entry_dispatch_and_returned_identity(self):
        body = b'inert synthetic public interface body\n'
        identity = hashlib.sha256(body).hexdigest()
        direct = next(path for path in self.rows if path in self.source.FORMAL_COPY_PATHS)
        for path in (direct, self.prior_path):
            row = dict(self.rows[path], public_sha256=identity, source_sha256=identity,
                       public_bytes=len(body), source_bytes=len(body))
            members = tuple((name, self.source._formal_row_digest(row) if name == path else digest)
                            for name, digest in self.source.FORMAL_PUBLIC_MEMBERS)
            checksum = hashlib.sha256(json.dumps(members, separators=(',', ':')).encode()).hexdigest()
            with self.subTest(path=path), \
                 patch.object(self.source, 'FORMAL_PUBLIC_MEMBERS', members), \
                 patch.object(self.source, 'FORMAL_PUBLIC_MEMBERS_SHA256', checksum), \
                 patch.object(self.source, 'formal_copy_bytes', create=True, return_value=body) as direct_getter, \
                 patch.object(self.source, 'continuation_copy_bytes', create=True, return_value=body) as prior_getter:
                self.assertEqual(self.source.source_bytes(pathlib.Path('unused-synthetic-root'), row), body)
                used, unused = (prior_getter, direct_getter) if path == self.prior_path else (direct_getter, prior_getter)
                used.assert_called_once_with(pathlib.Path('unused-synthetic-root'), path, identity, len(body))
                unused.assert_not_called()
                used.return_value = b'wrong returned identity\n'
                with self.assertRaisesRegex(ValueError, 'source identity differs'):
                    self.source.source_bytes(pathlib.Path('unused-synthetic-root'), row)

    def test_prior_chain_checks_former_provider_before_final_endpoint(self):
        alias, former, canonical, blob, identity, size = self.source.CONTINUATION_FORMAL_RETARGETS[0]
        binding = dict(canonical=former, blob=blob, sha256=identity, bytes=size, sources=[])
        calls = []
        def checkpoint(root, path, value):
            calls.append(('former', path, value['canonical']))
            return b'inert-provider-interface'
        def continuation(root, path, value):
            calls.append(('prior', path, value['canonical']))
            return b'inert-endpoint-interface'
        with patch.object(self.source, '_checkpoint_bound_bytes', create=True, side_effect=checkpoint) as original, \
             patch.object(self.source, '_continuation_bound_bytes', create=True, side_effect=continuation) as endpoint:
            self.assertEqual(self.source._continuation_formal_bound_bytes('unused', alias, binding),
                             b'inert-endpoint-interface')
            self.assertEqual(calls, [('former', former, canonical), ('prior', alias, canonical)])
            endpoint.reset_mock()
            original.side_effect = ValueError('corrupt former provider')
            with self.assertRaisesRegex(ValueError, 'corrupt former provider'):
                self.source._continuation_formal_bound_bytes('unused', alias, binding)
            endpoint.assert_not_called()

    def _consumer(self, filename, function):
        module = self._module(filename, {function})
        def unrelated(*args, **kwargs):
            raise ValueError('unrelated population is absent from this finite interface fixture')
        module.__dict__.update(self.source.__dict__)
        # Bind the exact function back after supplying only its finite inputs.
        compiled = self._module(filename, {function})
        module.__dict__.update({function: getattr(compiled, function)})
        namespace = getattr(module, function).__globals__
        namespace.update(self.source.__dict__)
        namespace.update(BASE='unused-synthetic-baseline', REFACTOR_EDIT_PATHS=set(),
            HISTORICAL_PROSE={}, HISTORICAL_PROSE_PUBLIC_PATHS=set(), HISTORICAL_PROSE_REVISIONS={},
            TYPED_GUIDES={}, ADMIN_GUIDES={}, ADMIN_RECORD_PATHS=set(),
            SUCCESSOR_CALCULUS_GUIDES={}, SUCCESSOR_CALCULUS_MAP='unused-calculus',
            SUCCESSOR_INPUT_REGISTRY='unused-registry', MEDIATOR_GUIDE='unused-guide',
            CONTINUATION_OWNER_PATHS=set(), FIXTURE_CONSUMER_ORIGINAL={},
            PMR007_DEEP_PREFIX='unused-deep', PMR007_ROUNDS_PREFIX='unused-rounds',
            PMR007_ROUNDS_FORMALIZATION='unused-formalization',
            continuation_owners=types.SimpleNamespace(PRESERVATION_OWNER_PATHS=set()))
        for name in ('pmr007_deep_duplicate_paths', 'pmr007_rounds_duplicate_paths',
                     'checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths',
                     'checkpoint_package_duplicate_paths', 'checkpoint_code_duplicate_paths',
                     'digest_record_absences', 'mediator_guide_source_bytes',
                     'status_record_absences'):
            namespace[name] = unrelated
        return getattr(module, function), namespace

    def _deletion_gate(self, filename, function, reader):
        call, namespace = self._consumer(filename, function)
        path = next(path for path in self.source.FORMAL_COPY_PATHS
                    if path.startswith(self.source.CHECKPOINT_COPY_ROOT))
        for status, qualified, permitted in (('D', {path}, True), ('M', {path}, False),
                                             ('T', {path}, False), ('D', set(), False)):
            with self.subTest(status=status, qualified=bool(qualified)), patch.dict(namespace):
                namespace['readonly_git_diff'] = lambda *a, **k: subprocess.CompletedProcess(
                    ['synthetic-name-status'], 0, (status + '\0' + path + '\0').encode(), b'')
                with patch.dict(namespace, formal_duplicate_paths=unittest.mock.Mock(return_value=qualified)):
                    result = call(pathlib.Path('unused-root'), 'unused-baseline') if reader else call(pathlib.Path('unused-root'), {})
                    self.assertEqual(result == [], permitted)
                    self.assertEqual(namespace['formal_duplicate_paths'].call_count, 1 if status == 'D' else 0)
        with patch.dict(namespace):
            namespace['readonly_git_diff'] = lambda *a, **k: subprocess.CompletedProcess(
                ['synthetic-name-status'], 0, ('D\0' + path + '\0').encode(), b'')
            namespace['formal_duplicate_paths'] = unittest.mock.Mock(side_effect=ValueError('unavailable formal evidence'))
            result = call(pathlib.Path('unused-root'), 'unused-baseline') if reader else call(pathlib.Path('unused-root'), {})
            self.assertTrue(result)

    def test_current_reader_requires_qualified_D_only_formal_absence(self):
        self._deletion_gate('check_reader_pilot.py', 'check_corpus_currentness', True)

    def test_current_projection_requires_qualified_D_only_formal_absence(self):
        self._deletion_gate('validate_t20_v6_projection.py', 'check_preserved_roots', False)

    def test_continuation_adapter_preserves_formal_prior_and_sparse_routes(self):
        module = self._module('validate_research_continuations.py', {'source_bytes'})
        module._source = self.source
        module.path_in = lambda root, name, exists: pathlib.Path(name)
        self.source.SPARSE_PRIOR_PROSE = {'synthetic-sparse.md'}
        for path, getter in ((next(iter(self.source.FORMAL_CONTINUATION_PATHS)), 'continuation_formal_source_bytes'),
                             (self.prior_path, 'continuation_copy_bytes'),
                             ('synthetic-sparse.md', 'sparse_prior_source_bytes')):
            row = dict(path=path, sha256='1' * 64, bytes=7)
            with self.subTest(route=getter), patch.object(self.source, getter, create=True, return_value=b'inert') as selected:
                self.assertEqual(module.source_bytes('unused-root', row), b'inert')
                if getter == 'continuation_copy_bytes':
                    selected.assert_called_once_with('unused-root', path, row['sha256'], row['bytes'], source=row)
                else:
                    selected.assert_called_once_with('unused-root', row)

    def test_replay_byte_getter_preserves_digest_input_and_formal_routes(self):
        module = self._module('replay_v5_successors.py', {'public_bytes', 'require', 'digest', 'relative', 'sha'})
        body = b'inert synthetic replay-getter interface\n'
        identity = hashlib.sha256(body).hexdigest()
        prefix = 'experiments/orthemology-v5-successors/source-store/' + identity + '/'
        fake = types.ModuleType('resolve_t20_v6_source')
        fake.FORMAL_SUCCESSOR_PATHS = {prefix + 'Synthetic.lean'}
        fake.SUCCESSOR_INPUT_PATHS = {prefix + 'INPUT.json'}
        fake.successor_input_source_bytes = unittest.mock.Mock(return_value=body)
        fake.successor_formal_source_bytes = unittest.mock.Mock(return_value=body)
        module._formal_sources = fake
        module.DIGEST_RECORD_PATHS = {prefix + 'DIGEST.md'}
        module.digest_record_successor_bytes = unittest.mock.Mock(return_value=body)
        with patch.dict(sys.modules, resolve_t20_v6_source=fake):
            for path, getter in ((prefix + 'Synthetic.lean', fake.successor_formal_source_bytes),
                                 (prefix + 'INPUT.json', fake.successor_input_source_bytes),
                                 (prefix + 'DIGEST.md', module.digest_record_successor_bytes)):
                row = dict(public_path=path, public_sha256=identity, public_bytes=len(body))
                with self.subTest(path=path):
                    self.assertEqual(module.public_bytes('unused-root', row), body)
                    getter.assert_called_once_with('unused-root', row)
                    getter.return_value = b'wrong-returned-body'
                    with self.assertRaisesRegex(ValueError, 'Source bytes/hash changed'):
                        module.public_bytes('unused-root', row)
class _StatusMemory:
    """Wholly in-memory files/index/native responses; no external resources."""
    ROOT = '/status-interface-fixture'

    def __init__(self):
        self.entries = {}
        self.objects = {}
        self.object_types = {}
        self.index = {}
        self.tree = {}
        self.events = []
        self.fd_paths = {}
        self.on_event = None
        self.next_inode = 1
        self.put('/', None)
        self.put(self.ROOT, None)
        owner = self

        class MemoryPath:
            def __init__(self, value):
                self.value = str(value)
            def __str__(self):
                return self.value
            def __fspath__(self):
                return self.value
            def __truediv__(self, part):
                return type(self)(str(PurePosixPath(self.value) / str(part)))
            def is_absolute(self):
                return self.value.startswith('/')
            @property
            def parents(self):
                return tuple(type(self)(str(p)) for p in PurePosixPath(self.value).parents)
            @classmethod
            def cwd(cls):
                return cls(owner.ROOT)
            def lstat(self):
                owner.event(('lstat', self.value))
                if self.value not in owner.entries:
                    raise FileNotFoundError(self.value)
                entry = owner.entries[self.value]
                return types.SimpleNamespace(st_dev=1, st_ino=entry['inode'], st_mode=entry['mode'],
                    st_nlink=1, st_size=len(entry['body']), st_mtime_ns=entry['stamp'],
                    st_ctime_ns=entry['stamp'])
            def stat(self):
                return self.lstat()
            def is_symlink(self):
                try:
                    return stat.S_ISLNK(self.lstat().st_mode)
                except FileNotFoundError:
                    return False
            def is_dir(self):
                try:
                    return stat.S_ISDIR(self.lstat().st_mode)
                except FileNotFoundError:
                    return False
            def read_bytes(self):
                owner.event(('read', self.value))
                if self.value not in owner.entries:
                    raise FileNotFoundError(self.value)
                return owner.entries[self.value]['body']

        self.Path = MemoryPath
        self.root = MemoryPath(self.ROOT)
        self.pathlib = types.SimpleNamespace(Path=MemoryPath)
        self.os = types.SimpleNamespace(
            O_RDONLY=os.O_RDONLY, O_NOFOLLOW=os.O_NOFOLLOW, O_NONBLOCK=os.O_NONBLOCK,
            O_NOATIME=getattr(os, 'O_NOATIME', 0), open=self.open, fdopen=self.fdopen,
            fstat=self.fstat, path=types.SimpleNamespace(lexists=lambda p: str(p) in self.entries))

    def event(self, event):
        self.events.append(event)
        if self.on_event is not None:
            self.on_event(event)

    @staticmethod
    def blob(body, kind='blob'):
        return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

    def put(self, path, body, mode=None):
        name = str(path)
        for parent in reversed(PurePosixPath(name).parents):
            if str(parent) not in self.entries:
                self.put(str(parent), None)
        self.entries[name] = {'body': b'' if body is None else body,
                             'mode': (stat.S_IFDIR | 0o755 if body is None else stat.S_IFREG | 0o644)
                                     if mode is None else mode,
                             'inode': self.next_inode, 'stamp': self.next_inode}
        self.next_inode += 1

    def remove(self, relative):
        self.entries.pop(self.ROOT + '/' + relative, None)

    def set_file(self, relative, body, mode=None):
        self.put(self.ROOT + '/' + relative, body, mode)

    def add_object(self, body, kind='blob'):
        oid = self.blob(body, kind)
        self.objects[oid] = body
        self.object_types[oid] = kind
        return oid

    def open(self, path, flags):
        name = str(path)
        self.event(('open', name, flags))
        if name not in self.entries:
            raise FileNotFoundError(name)
        if stat.S_ISLNK(self.entries[name]['mode']):
            raise OSError('in-memory O_NOFOLLOW refusal')
        fd = len(self.fd_paths) + 100
        self.fd_paths[fd] = name
        return fd

    def fstat(self, fd):
        return self.Path(self.fd_paths[fd]).lstat()

    def fdopen(self, fd, mode):
        owner = self
        path = self.fd_paths[fd]
        class Stream(io.BytesIO):
            def fileno(self):
                return fd
            def read(self, size=-1):
                owner.event(('stream-read', path))
                return super().read(size)
        return Stream(self.entries[path]['body'])

    def git(self, root, *args):
        self.event(('git', *args))
        if args[:1] == ('cat-file',) and len(args) == 3:
            kind, oid = args[1:]
            if oid not in self.objects or self.object_types.get(oid) != kind:
                raise ValueError('declared synthetic native object missing or wrong type')
            return self.objects[oid]
        if args[:4] == ('ls-files', '--stage', '-z', '--'):
            return b''.join((row + '\t' + path + '\0').encode()
                            for path in args[4:] for row in self.index.get(path, []))
        if args[:2] == ('ls-tree', '-z') and len(args) == 5 and args[3] == '--':
            return self.tree.get(args[4], b'')
        raise AssertionError('undeclared synthetic native request: ' + repr(args))

class StatusSourceViewMigrationTests(unittest.TestCase):
    STATUS = 'research/t20-live-20261009/checkpoints/CP01/COMPONENT_STATUS.json'
    PROVIDER = ('research/t20-live-20261009/checkpoints/CP01/'
                't20-next-frontier-20261008/identification-review/results/INDEPENDENT_METRICS.json')
    ALIAS = ('research/t20-live-20261009/checkpoints/CP01/'
             't20-next-frontier-20261008/identification-review/results/INDEPENDENT_METRICS_V2.json')
    BODY = b'{"inert": "software interface fixture", "status": "ACTIVE"}\n'

    def selected(self, filename, names, namespace):
        root = globals().get('_STATUS_TEST_SOURCE_ROOT', Path(__file__).resolve().parents[1])
        source = (root / 'scripts' / filename).read_text()
        nodes = [node for node in ast.parse(source).body
                 if (isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names)
                 or (isinstance(node, ast.Assign) and len(node.targets) == 1
                     and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names)]
        exec(compile(ast.Module(body=nodes, type_ignores=[]), filename + ':operational-interface', 'exec'), namespace)
        return namespace


    def currentness(self, *, changes=None, refuse=False, qualified=None):
        def unexpected(*args, **kwargs):
            raise AssertionError('unrelated history or original-body qualifier invoked')
        requests = []
        namespace = {'Path': Path, 'REFACTOR_EDIT_PATHS': set(), 'HISTORICAL_PROSE': {},
                     'FIXTURE_CONSUMER_ORIGINAL': {}, 'binding_record_candidate': lambda path: False,
                     'status_record_candidate': lambda path: path == self.STATUS}
        for name in ('CHECKPOINT_COPY_PATHS', 'CHECKPOINT_RECORD_COPY_PATHS',
                     'CHECKPOINT_PACKAGE_COPY_PATHS', 'FORMAL_COPY_PATHS',
                     'CHECKPOINT_CODE_COPY_PATHS', 'DIGEST_RECORD_PATHS', 'SUCCESSOR_INPUT_PATHS',
                     'GENERATED_FIXTURE_PATHS', 'ADMIN_RECORD_PATHS', 'ADMIN_GUIDES',
                     'CONTINUATION_OWNER_PATHS', 'TYPED_GUIDES', 'SUCCESSOR_CALCULUS_GUIDES'):
            namespace[name] = set()
        for name in ('PMR007_DEEP_PREFIX', 'PMR007_ROUNDS_PREFIX', 'PMR007_ROUNDS_FORMALIZATION',
                     'CONTINUATION_COPY_ROOT', 'SUCCESSOR_INPUT_REGISTRY',
                     'SUCCESSOR_CALCULUS_MAP', 'MEDIATOR_GUIDE'):
            namespace[name] = 'unrelated/' + name
        for name in ('pmr007_deep_duplicate_paths', 'pmr007_rounds_duplicate_paths',
                     'checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths',
                     'checkpoint_package_duplicate_paths', 'formal_duplicate_paths',
                     'checkpoint_code_duplicate_paths', 'digest_record_absences',
                     'pmr007_rounds_formalization_navigation', 'continuation_duplicate_paths',
                     'successor_input_absences', 'successor_calculus_map_absences',
                     'generated_fixture_absences', 'binding_record_absences',
                     'administrative_record_absences', 'administrative_guide_source_bytes'):
            namespace[name] = unexpected
        def qualify(root, paths):
            requests.append(set(paths))
            if refuse:
                raise ValueError('synthetic current role owner or original coordinate refusal')
            return set(paths) if qualified is None else set(qualified)
        namespace['status_record_absences'] = qualify
        changes = [('D', self.STATUS)] if changes is None else changes
        raw = b''.join((status + '\0' + path + '\0').encode() for status, path in changes)
        namespace['readonly_git_diff'] = lambda root, args: subprocess.CompletedProcess(args, 0, raw)
        self.selected('resolve_t20_v6_source.py', {'STATUS_RECORD_OWNERS'}, namespace)
        self.selected('check_reader_pilot.py', {'check_corpus_currentness'}, namespace)
        return namespace['check_corpus_currentness'](Path('in-memory-root'), 'synthetic-baseline'), requests

    def provider(self, *, absent=True, selected=True, corrupt=False, refused=False):
        body = self.BODY
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        binding = {'canonical': self.PROVIDER, 'blob': blob,
                   'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body)}
        class MemoryPath:
            def __init__(self, name='in-memory-root'):
                self.name = str(name)
            def __truediv__(self, value):
                return type(self)(self.name + '/' + str(value))
            def is_symlink(self):
                return False
            def is_dir(self):
                return True
            def __str__(self):
                return self.name
        def git(root, *args):
            if args == ('ls-tree', '-z', 'synthetic-baseline', '--', self.ALIAS, self.PROVIDER):
                return b''.join(('100644 blob ' + blob + '\t' + p + '\0').encode()
                                for p in (self.ALIAS, self.PROVIDER))
            if args == ('ls-files', '--stage', '-z', '--', self.ALIAS, self.PROVIDER):
                return ('100644 ' + blob + ' 0\t' + self.PROVIDER + '\0').encode()
            raise AssertionError('unexpected native command: ' + repr(args))
        def current(root, path):
            if absent:
                raise FileNotFoundError('declared absent inert provider')
            return body + (b'corruption' if corrupt else b'')
        requests = []
        def historical(root, path, identity=None, size=None):
            requests.append((path, identity, size))
            if refused:
                raise ValueError('synthetic source-owner refusal')
            return body
        namespace = {'pathlib': types.SimpleNamespace(Path=lambda value: value),
                     'CHECKPOINT_COPY_BASE': 'synthetic-baseline',
                     '_continuation_object': lambda root, kind, oid: body if kind == 'blob' else b'inert commit',
                     '_continuation_git': git, '_regular_current_bytes': current,
                     'collections': collections, 'digest': lambda value: hashlib.sha256(value).hexdigest(),
                     'os': types.SimpleNamespace(path=types.SimpleNamespace(lexists=lambda path: False)),
                     'status_record_candidate': lambda path: selected and path == self.PROVIDER,
                     'status_record_provider': lambda path: selected and path == self.PROVIDER,
                     '_binding_record_present': lambda root, path: not absent,
                     'status_record_bytes': historical}
        self.selected('resolve_t20_v6_source.py', {'_checkpoint_bound_bytes'}, namespace)
        return lambda: namespace['_checkpoint_bound_bytes'](MemoryPath(), self.ALIAS, binding), requests


    def test_currentness_uses_only_qualified_actual_status_absence(self):
        errors, requests = self.currentness()
        self.assertEqual(errors, [])
        self.assertEqual(requests, [{self.STATUS}, {self.STATUS}])

    def test_selected_absent_provider_uses_exact_source_view(self):
        read, requests = self.provider()
        self.assertEqual(read(), self.BODY)
        self.assertEqual(requests, [(self.PROVIDER, hashlib.sha256(self.BODY).hexdigest(), len(self.BODY))])

    def runtime(self):
        namespace = {'__name__': 'inert_status_runtime', 'json': json, 'hashlib': hashlib, 're': re,
                     'stat': stat, 'digest': lambda body: hashlib.sha256(body).hexdigest()}
        names = {
            '_StatusJsonNumber', '_status_json_loads', '_status_integer', '_status_identity',
            '_status_render', '_status_decode_body', 'status_record_candidate', 'status_record_provider',
            '_status_record_owner_bytes', '_status_record_catalog', '_status_record_original_base',
            '_status_record_bound_bytes', 'status_record_bytes', 'status_record_absences',
            '_binding_record_root', '_binding_record_present', '_binding_record_current_state',
            '_binding_record_role_context', '_administrative_bound_bytes',
        }
        self.selected('resolve_t20_v6_source.py', names, namespace)
        self.assertEqual(names - set(namespace), set(), 'actual operational definition absent')
        return namespace

    def raw_source(self, namespace, raw, *, tree=None, values=None, style=None, edits=None, base=None):
        value = namespace['_status_json_loads'](raw)
        source = {'identity': {'git_blob': _StatusMemory.blob(raw),
                              'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)},
                  'aliases': [self.STATUS], 'root': tree or {'value_id': 'V000001'},
                  'raw_byte_reconstruction': {
                      'schema': 'typed-json-original-byte-recipe-v1',
                      'style': style or {'indent': None, 'compact': False,
                                        'ensure_ascii': False, 'trailing': '\n'},
                      'base_render_sha256': hashlib.sha256(raw if base is None else base).hexdigest(),
                      'format_edits': [] if edits is None else edits}}
        return source, {'V000001': value} if values is None else values

    def memory_runtime(self, *, present=False):
        ns, memory = self.runtime(), _StatusMemory()
        source, values = self.raw_source(ns, self.BODY)
        # Fixture metadata are plain JSON and are reparsed by the actual strict
        # loader. No original source data, owner row or catalogue is substituted.
        document = {'schema': 'scientific-status-owner-v3',
                    'sources': {'S0001': source}, 'values': values}
        raw = json.dumps(document, ensure_ascii=False, separators=(',', ':')).encode()
        index_path = 'research/t20-live-20261009/INDEX.json'
        readme_path = 'research/t20-live-20261009/README.md'
        role_path = 'docs/provenance/v5-successors/SOURCE_MAP.json'
        owners = {}
        for path, body in ((index_path, raw), (readme_path, b'# Inert current owner\n'),
                           (role_path, b'{"sources": []}\n')):
            oid = memory.add_object(body)
            memory.set_file(path, body)
            memory.index[path] = ['100644 ' + oid + ' 0']
            pin = (oid, hashlib.sha256(body).hexdigest(), len(body))
            if path != role_path:
                owners[path] = pin
            else:
                role_pin = pin
        blob = memory.add_object(self.BODY)
        if present:
            memory.set_file(self.STATUS, self.BODY)
        memory.index[self.STATUS] = ['100644 ' + blob + ' 0']
        memory.tree[self.STATUS] = ('100644 blob ' + blob + '\t' + self.STATUS + '\0').encode()
        tree = '0123456789abcdef0123456789abcdef01234567'
        commit = memory.add_object(('tree ' + tree + '\n\ninert synthetic commit\n').encode(), 'commit')
        vector = (self.STATUS + '\0S0001\0' + blob + '\0' + hashlib.sha256(self.BODY).hexdigest()
                  + '\0' + str(len(self.BODY)) + '\n').encode()
        ns.update(pathlib=memory.pathlib, os=memory.os, _administrative_git=memory.git,
                  STATUS_RECORD_INDEX=index_path, STATUS_RECORD_OWNERS=owners,
                  STATUS_RECORD_PATH_HASHES={hashlib.sha256(self.STATUS.encode()).hexdigest()},
                  STATUS_RECORD_PROVIDER_HASHES=set(), STATUS_RECORD_ALIAS_COUNT=1,
                  STATUS_RECORD_SOURCE_COUNT=1, STATUS_RECORD_CLASS_SHA256=hashlib.sha256(vector).hexdigest(),
                  STATUS_RECORD_BASE=commit, STATUS_RECORD_TREE=tree,
                  BINDING_RECORD_ROLE_OWNERS={role_path: role_pin})
        memory.status_blob, memory.owner_index, memory.role_path = blob, index_path, role_path
        return ns, memory

    def test_actual_getter_authenticates_native_owner_and_preserved_active_value(self):
        ns, memory = self.memory_runtime()
        self.assertEqual(ns['status_record_bytes'](memory.root, self.STATUS), self.BODY)
        self.assertIn(('git', 'cat-file', 'commit', ns['STATUS_RECORD_BASE']), memory.events)
        self.assertIn(('git', 'cat-file', 'blob', memory.status_blob), memory.events)
        self.assertIn(('git', 'ls-tree', '-z', ns['STATUS_RECORD_BASE'], '--', self.STATUS), memory.events)
        self.assertTrue(any(event[:2] == ('open', memory.ROOT + '/' + memory.role_path)
                            for event in memory.events))
        self.assertEqual(ns['_status_json_loads'](self.BODY)['status'], 'ACTIVE')

    def test_getter_rejects_present_corruption_modes_and_lexical_aliases(self):
        for mutation in ('bytes', 'executable', 'directory', 'symlink', 'ancestor-symlink', 'root-symlink'):
            with self.subTest(mutation=mutation):
                ns, memory = self.memory_runtime(present=True)
                if mutation == 'bytes':
                    memory.set_file(self.STATUS, self.BODY + b'corrupt')
                elif mutation == 'executable':
                    memory.set_file(self.STATUS, self.BODY, stat.S_IFREG | 0o755)
                elif mutation == 'directory':
                    memory.set_file(self.STATUS, None)
                elif mutation == 'symlink':
                    memory.set_file(self.STATUS, b'declared-target', stat.S_IFLNK | 0o777)
                elif mutation == 'ancestor-symlink':
                    memory.set_file('research/t20-live-20261009/checkpoints', b'target', stat.S_IFLNK | 0o777)
                else:
                    memory.put(memory.ROOT, b'target', stat.S_IFLNK | 0o777)
                with self.assertRaises((ValueError, OSError)):
                    ns['status_record_bytes'](memory.root, self.STATUS)

    def test_getter_refuses_native_original_corruption_and_coordinate_changes(self):
        for mutation in ('commit-bytes', 'commit-type', 'commit-missing', 'tree-coordinate',
                         'blob-bytes', 'blob-type', 'blob-missing', 'mode', 'path-missing', 'path-blob'):
            with self.subTest(mutation=mutation):
                ns, memory = self.memory_runtime()
                if mutation == 'commit-bytes':
                    memory.objects[ns['STATUS_RECORD_BASE']] += b'changed'
                elif mutation == 'commit-type':
                    memory.object_types[ns['STATUS_RECORD_BASE']] = 'blob'
                elif mutation == 'commit-missing':
                    del memory.objects[ns['STATUS_RECORD_BASE']]
                elif mutation == 'tree-coordinate':
                    ns['STATUS_RECORD_TREE'] = 'f' * 40
                elif mutation == 'blob-bytes':
                    memory.objects[memory.status_blob] += b'changed'
                elif mutation == 'blob-type':
                    memory.object_types[memory.status_blob] = 'tree'
                elif mutation == 'blob-missing':
                    del memory.objects[memory.status_blob]
                elif mutation == 'mode':
                    memory.tree[self.STATUS] = memory.tree[self.STATUS].replace(b'100644', b'100755')
                elif mutation == 'path-missing':
                    del memory.tree[self.STATUS]
                else:
                    memory.tree[self.STATUS] = memory.tree[self.STATUS].replace(memory.status_blob.encode(), b'f' * 40)
                with self.assertRaises(ValueError):
                    ns['status_record_bytes'](memory.root, self.STATUS)

    def test_getter_refuses_missing_changed_or_unindexed_current_owners(self):
        for mutation in ('owner-absent', 'owner-corrupt', 'owner-unindexed', 'owner-symlink',
                         'role-absent', 'role-corrupt', 'role-unindexed', 'source-index-conflict'):
            with self.subTest(mutation=mutation):
                ns, memory = self.memory_runtime()
                if mutation == 'owner-absent':
                    memory.remove(memory.owner_index)
                elif mutation == 'owner-corrupt':
                    memory.set_file(memory.owner_index, b'{}')
                elif mutation == 'owner-unindexed':
                    memory.index[memory.owner_index] = []
                elif mutation == 'owner-symlink':
                    memory.set_file(memory.owner_index, b'target', stat.S_IFLNK | 0o777)
                elif mutation == 'role-absent':
                    memory.remove(memory.role_path)
                elif mutation == 'role-corrupt':
                    memory.set_file(memory.role_path, b'{}')
                elif mutation == 'role-unindexed':
                    memory.index[memory.role_path] = []
                else:
                    memory.index[self.STATUS] = ['100644 ' + memory.status_blob + ' 1']
                with self.assertRaises((ValueError, OSError)):
                    ns['status_record_bytes'](memory.root, self.STATUS)

    def test_getter_refuses_source_owner_and_role_changes_during_original_lookup(self):
        for mutation in ('present-to-absent', 'absent-to-present', 'owner-disappears', 'role-disappears'):
            with self.subTest(mutation=mutation):
                ns, memory = self.memory_runtime(present=mutation == 'present-to-absent')
                def race(event):
                    if event == ('git', 'cat-file', 'blob', memory.status_blob):
                        memory.on_event = None
                        if mutation == 'present-to-absent':
                            memory.remove(self.STATUS)
                        elif mutation == 'absent-to-present':
                            memory.set_file(self.STATUS, self.BODY + b'corrupt')
                        elif mutation == 'owner-disappears':
                            memory.remove(memory.owner_index)
                        else:
                            memory.remove(memory.role_path)
                memory.on_event = race
                with self.assertRaises((ValueError, OSError)):
                    ns['status_record_bytes'](memory.root, self.STATUS)
                self.assertIsNone(memory.on_event, 'the intended race discriminator must execute')

    def test_actual_absence_qualifier_rejects_unrelated_and_present_inputs(self):
        ns, memory = self.memory_runtime()
        memory.index[self.STATUS] = []
        self.assertEqual(ns['status_record_absences'](memory.root, {self.STATUS}), {self.STATUS})
        for paths in (set(), {self.STATUS, 'research/t20-live-20261009/unselected.json'},
                      {'experiments/current-required-source.json'}):
            with self.subTest(paths=sorted(paths)):
                with self.assertRaises(ValueError):
                    ns['status_record_absences'](memory.root, paths)
        memory.set_file(self.STATUS, self.BODY)
        with self.assertRaisesRegex(ValueError, 'present'):
            ns['status_record_absences'](memory.root, {self.STATUS})

    def test_exact_request_identity_and_finite_catalogue_are_enforced(self):
        ns, memory = self.memory_runtime(present=True)
        self.assertEqual(ns['status_record_bytes'](memory.root, self.STATUS,
                         hashlib.sha256(self.BODY).hexdigest(), len(self.BODY)), self.BODY)
        for identity, size in (('0' * 64, len(self.BODY)), (None, len(self.BODY) + 1),
                               (None, True), (123, None)):
            with self.subTest(identity=identity, size=size):
                with self.assertRaises(ValueError):
                    ns['status_record_bytes'](memory.root, self.STATUS, identity, size)
        ns['STATUS_RECORD_CLASS_SHA256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'finite'):
            ns['status_record_bytes'](memory.root, self.STATUS)

    def test_provider_migration_preserves_present_and_unselected_refusals(self):
        read, requests = self.provider(absent=False)
        self.assertEqual(read(), self.BODY)
        self.assertEqual(requests, [])
        for options in ({'selected': False}, {'absent': False, 'corrupt': True}, {'refused': True}):
            with self.subTest(options=options):
                read, requests = self.provider(**options)
                with self.assertRaises(ValueError):
                    read()


    def test_currentness_preserves_modification_unrelated_and_refusal_failures(self):
        for changes in ([('M', self.STATUS)], [('D', 'research/t20-live-20261009/unselected.json')]):
            with self.subTest(changes=changes):
                errors, requests = self.currentness(changes=changes)
                self.assertTrue(errors)
                self.assertEqual(requests, [])
        errors, requests = self.currentness(refuse=True)
        self.assertTrue(any('synthetic current role owner' in error for error in errors))
        self.assertTrue(any('requires source-baseline' in error for error in errors))
        errors, requests = self.currentness(qualified=set())
        self.assertTrue(any('requires source-baseline' in error for error in errors))

    def test_decoder_preserves_number_lexemes_order_and_literal_value_id_data(self):
        ns = self.runtime()
        raw = b'{"z": [1.2300e+04, -0, 9007199254740993], "value_id": "literal-data"}\n'
        source, values = self.raw_source(ns, raw)
        self.assertEqual(ns['_status_decode_body'](source, values), raw)
        self.assertEqual(ns['_status_json_loads'](raw)['z'][0], '1.2300e+04')
        self.assertIsInstance(ns['_status_json_loads'](raw)['z'][0], ns['_StatusJsonNumber'])
        source['root'] = {'object': [['a', {'value_id': 'V000002'}],
                                     ['b', {'array': [{'value_id': 'V000003'}]}]]}
        expected = b'{"a": "1", "b": [1]}\n'
        source['identity'] = {'bytes': len(expected), 'sha256': hashlib.sha256(expected).hexdigest(),
                              'git_blob': _StatusMemory.blob(expected)}
        source['raw_byte_reconstruction']['base_render_sha256'] = hashlib.sha256(expected).hexdigest()
        self.assertEqual(ns['_status_decode_body'](source,
                         {'V000002': '1', 'V000003': ns['_StatusJsonNumber']('1')}), expected)

    def test_decoder_uses_one_base_offset_vector_and_equivalent_string_escapes(self):
        ns = self.runtime()
        base = '{"x": "é", "n": 1.00}\n'.encode()
        original = b'{ "x": "\\u00e9", "n": 1.00}\r\n'
        token_start, token_end = base.index('"é"'.encode()), base.index('"é"'.encode()) + len('"é"'.encode())
        edits = [[1, 1, ' '], [token_start, token_end, '"\\u00e9"'], [len(base)-1, len(base), '\r\n']]
        source, values = self.raw_source(ns, original, base=base, edits=edits)
        self.assertEqual(ns['_status_decode_body'](source, values), original)

    def test_decoder_preserves_indented_unicode_and_empty_container_styles(self):
        ns = self.runtime()
        value = {'name': 'é', 'empty': [], 'nested': {'empty': {}, 'truth': True}}
        for indent, ascii_only, compact in ((1, False, False), (2, True, False),
                                             (4, False, False), (None, False, True)):
            with self.subTest(indent=indent, ascii_only=ascii_only, compact=compact):
                options = {'ensure_ascii': ascii_only, 'indent': indent}
                if compact:
                    options['separators'] = (',', ':')
                raw = (json.dumps(value, **options) + '\n').encode()
                style = {'indent': indent, 'ensure_ascii': ascii_only,
                         'compact': compact, 'trailing': '\n'}
                source, values = self.raw_source(ns, raw, style=style)
                self.assertEqual(ns['_status_decode_body'](source, values), raw)

    def test_unpatched_production_selector_excludes_existing_routes_and_active_source_store(self):
        root = globals().get('_STATUS_TEST_SOURCE_ROOT', Path(__file__).resolve().parents[1])
        source = (root / 'scripts/resolve_t20_v6_source.py').read_text()
        names = {'STATUS_RECORD_PATH_HASHES', 'STATUS_RECORD_PROVIDER_HASHES',
                 'STATUS_RECORD_SOURCE_COUNT', 'STATUS_RECORD_ALIAS_COUNT',
                 'STATUS_RECORD_BASE', 'STATUS_RECORD_TREE'}
        selected = []
        for node in ast.parse(source).body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
                selected.append(node)
            elif isinstance(node, ast.FunctionDef) and node.name in ('status_record_candidate', 'status_record_provider'):
                selected.append(node)
        ns = {'digest': lambda body: hashlib.sha256(body).hexdigest()}
        exec(compile(ast.Module(body=selected, type_ignores=[]), 'actual-status-selectors', 'exec'), ns)
        self.assertEqual(len(ns['STATUS_RECORD_PATH_HASHES']), 574)
        self.assertEqual(len(ns['STATUS_RECORD_PROVIDER_HASHES']), 87)
        self.assertEqual((ns['STATUS_RECORD_ALIAS_COUNT'], ns['STATUS_RECORD_SOURCE_COUNT']), (811, 749))
        self.assertEqual(ns['STATUS_RECORD_BASE'], 'f97b01417de9d95a44cae4d3a3ac71d1e29f984b')
        self.assertEqual(ns['STATUS_RECORD_TREE'], 'c8ec5b28d65fccc5a2f38c6564384fcd682089e3')
        self.assertTrue(ns['status_record_candidate'](self.STATUS))
        self.assertTrue(ns['status_record_provider'](self.PROVIDER))
        for path in ('research/t20-live-20261009/checkpoints/CP01/MANIFEST.json', self.ALIAS,
                     'research/t20-live-20261009/unselected.json',
                     'experiments/orthemology-v5-successors/source-store/'
                     '5c6421b650bc87a2427a892a39e5522dc44543ca4ac1bd6e9f08d536c044a752/mathlib-lake-manifest.json'):
            with self.subTest(path=path):
                self.assertFalse(ns['status_record_candidate'](path))

    def test_decoder_rejects_malformed_graph_keys_cycles_and_unknown_values(self):
        ns = self.runtime()
        bad_nodes = ({'value_id': 'V999999'}, {'other': []}, {'value_id': 'V000001', 'array': []},
                     {'object': [['same', {'value_id': 'V000001'}], ['same', {'value_id': 'V000001'}]]},
                     {'array': 'not-an-array'}, {'object': [['key']]})
        for node in bad_nodes:
            with self.subTest(node=node):
                source, values = self.raw_source(ns, self.BODY)
                source['root'] = node
                with self.assertRaises(ValueError):
                    ns['_status_decode_body'](source, values)
        source, values = self.raw_source(ns, self.BODY)
        node = {'array': []}
        node['array'].append(node)
        source['root'] = node
        with self.assertRaisesRegex(ValueError, 'cyclic'):
            ns['_status_decode_body'](source, values)
        for raw in (b'{"x": 1, "x": 2}', b'{"x": NaN}'):
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    ns['_status_json_loads'](raw)

    def test_decoder_rejects_recipe_style_edit_and_native_identity_tampering(self):
        ns = self.runtime()
        mutations = (
            lambda s: s['raw_byte_reconstruction'].__setitem__('schema', 'unqualified'),
            lambda s: s['raw_byte_reconstruction'].__setitem__('base_render_sha256', '0' * 64),
            lambda s: s['raw_byte_reconstruction']['style'].__setitem__('indent', True),
            lambda s: s['raw_byte_reconstruction']['style'].__setitem__('indent', -1),
            lambda s: s['raw_byte_reconstruction']['style'].__setitem__('ensure_ascii', 'false'),
            lambda s: s['raw_byte_reconstruction']['style'].__setitem__('trailing', 'execute'),
            lambda s: s['raw_byte_reconstruction'].__setitem__('format_edits', [[1, 3, ''], [2, 4, '']]),
            lambda s: s['raw_byte_reconstruction'].__setitem__('format_edits', [[0, len(self.BODY)+1, '']]),
            lambda s: s['raw_byte_reconstruction'].__setitem__('format_edits', [[False, 0, '']]),
            lambda s: s['identity'].__setitem__('bytes', len(self.BODY)+1),
            lambda s: s['identity'].__setitem__('sha256', '0' * 64),
            lambda s: s['identity'].__setitem__('git_blob', '0' * 40),
        )
        for i, mutate in enumerate(mutations):
            with self.subTest(mutation=i):
                source, values = self.raw_source(ns, self.BODY)
                mutate(source)
                with self.assertRaises(ValueError):
                    ns['_status_decode_body'](source, values)

    def test_recipe_cannot_change_typed_content_even_with_new_matching_hashes(self):
        ns = self.runtime()
        source, values = self.raw_source(ns, self.BODY)
        changed = self.BODY.replace(b'ACTIVE', b'CLOSED')
        start = self.BODY.index(b'ACTIVE')
        source['raw_byte_reconstruction']['format_edits'] = [[start, start + 6, 'CLOSED']]
        source['identity'] = {'bytes': len(changed), 'sha256': hashlib.sha256(changed).hexdigest(),
                              'git_blob': _StatusMemory.blob(changed)}
        with self.assertRaisesRegex(ValueError, 'typed source content'):
            ns['_status_decode_body'](source, values)


class StatusOwnerEditionResponseTests(unittest.TestCase):
    """Actual operational interfaces with new, wholly in-memory metadata."""

    INDEX = 'research/t20-live-20261009/INDEX.json'
    README = 'research/t20-live-20261009/README.md'
    ALIAS = 'research/t20-live-20261009/checkpoints/CP01/INERT_ALIAS.json'

    def base(self):
        return StatusSourceViewMigrationTests(
            'test_actual_getter_authenticates_native_owner_and_preserved_active_value')

    def observe(self, row):
        sink = globals().get('_STATUS_RESPONSE_OBSERVATIONS')
        if sink is not None:
            sink.append(dict(test=self.id(), **row))

    def owner_runtime(self, *, edition='current', changes=None):
        helper = self.base()
        ns, memory = helper.memory_runtime()
        original = {}
        for path, body in ((self.INDEX, b'{"inert_original_index": true}\n'),
                           (self.README, b'# Inert original discovery owner\n')):
            blob = memory.add_object(body)
            original[path] = (blob, hashlib.sha256(body).hexdigest(), len(body))
            memory.tree[path] = ('100644 blob ' + blob + '\t' + path + '\0').encode()
            if edition == 'original':
                memory.set_file(path, body)
                memory.index[path] = ['100644 ' + blob + ' 0']
        tree = '76543210fedcba9876543210fedcba9876543210'
        commit = memory.add_object(('tree ' + tree + '\n\ninert owner baseline\n').encode(), 'commit')
        ns.update(STATUS_RECORD_OWNER_ORIGINAL=original, STATUS_RECORD_OWNER_BASE=commit,
                  STATUS_RECORD_OWNER_TREE=tree)
        helper.selected('resolve_t20_v6_source.py', {'status_owner_edition'}, ns)
        rows = {path: {'path': path, 'mode': '100644', 'kind': 'blob',
                       'git_oid': pin[0], 'bytes': pin[2]}
                for path, pin in original.items()}
        owners = {'schema': 'orthemology-reader-owner-map-v1',
                  'baseline': {'commit': commit, 'tree': tree}, 'external_body_admissions': [],
                  'collections': [{'key': 't20-live', 'include': ['research/t20-live-20261009/'],
                                   'exclude': [], 'owners': [self.README, self.INDEX],
                                   'candidate_paths': 2}]}
        cross = {'schema': 'orthemology-reader-crosswalk-v1', 'coverage_stage': 'reader-candidate'}
        # Only unrelated collection populations are empty. The two owner rows,
        # native objects, files and stage rows pass the actual admission helper.
        for name in ('CHECKPOINT_COPY_PATHS', 'CHECKPOINT_RECORD_COPY_PATHS',
                     'CHECKPOINT_PACKAGE_COPY_PATHS', 'FORMAL_COPY_PATHS',
                     'CHECKPOINT_CODE_COPY_PATHS', 'DIGEST_RECORD_PATHS', 'SUCCESSOR_INPUT_PATHS',
                     'GENERATED_FIXTURE_PATHS', 'ADMIN_RECORD_PATHS', 'ADMIN_GUIDES',
                     'CONTINUATION_OWNER_PATHS', 'TYPED_GUIDES', 'SUCCESSOR_CALCULUS_GUIDES'):
            ns[name] = set()
        for name in ('PMR007_DEEP_PREFIX', 'PMR007_ROUNDS_PREFIX', 'PMR007_ROUNDS_FORMALIZATION',
                     'CONTINUATION_COPY_ROOT', 'SUCCESSOR_INPUT_REGISTRY',
                     'SUCCESSOR_CALCULUS_MAP', 'MEDIATOR_GUIDE', 'PMR007_ROUNDS_PARENT',
                     'FIXTURE_STATUS_PATH'):
            ns[name] = 'unrelated/' + name
        ns.update(REFACTOR_EDIT_PATHS=set(), HISTORICAL_PROSE={}, FIXTURE_CONSUMER_ORIGINAL={},
                  binding_record_candidate=lambda path: False, Path=memory.Path,
                  Counter=collections.Counter)
        def unexpected(*args, **kwargs):
            raise AssertionError('unrelated source qualification must not run')
        for name in ('pmr007_deep_duplicate_paths', 'pmr007_rounds_duplicate_paths',
                     'checkpoint_duplicate_paths', 'checkpoint_record_duplicate_paths',
                     'checkpoint_package_duplicate_paths', 'formal_duplicate_paths',
                     'checkpoint_code_duplicate_paths', 'digest_record_absences',
                     'pmr007_rounds_formalization_navigation', 'continuation_duplicate_paths',
                     'successor_input_absences', 'successor_calculus_map_absences',
                     'generated_fixture_absences', 'binding_record_absences',
                     'administrative_record_absences', 'administrative_guide_source_bytes'):
            ns[name] = unexpected
        ns.update(check_continuation_owner_edition=lambda *a: ({}, []),
                  check_fixture_consumer_edition=lambda *a: ({}, None, []),
                  check_source_additions=lambda *a: ({}, []),
                  check_historical_sources=lambda *a: ({}, []),
                  check_collection_dispositions=lambda *a: [],
                  check_collection_result_routes=lambda *a: [],
                  entries_at=lambda *a: list(rows.values()),
                  permitted_reader_ci_addition=lambda *a: False,
                  permitted_historical_status_pin=lambda *a: False,
                  permitted_contributor_navigation=lambda *a: False)
        selected_changes = ([('M', self.INDEX), ('M', self.README)] if changes is None else changes)
        def differences(root, args):
            raw = b''.join((status + '\0' + path + '\0').encode() for status, path in selected_changes)
            return subprocess.CompletedProcess(args, 0, raw)
        ns['readonly_git_diff'] = differences
        def native_tree(args, **kwargs):
            if args != ['git', 'rev-parse', commit + '^{tree}']:
                raise AssertionError('undeclared native request: ' + repr(args))
            return subprocess.CompletedProcess(args, 0, tree + '\n')
        ns['subprocess'] = types.SimpleNamespace(run=native_tree)
        memory.Path.is_file = lambda path: stat.S_ISREG(path.lstat().st_mode)
        helper.selected('check_reader_pilot.py',
                        {'check_corpus_currentness', 'corpus_currentness_context', 'safe_path', 'matches'}, ns)
        root = globals().get('_STATUS_TEST_SOURCE_ROOT', Path(__file__).resolve().parents[1])
        reader = (root / 'scripts/check_reader_pilot.py').read_text()
        node = next(n for n in ast.parse(reader).body if isinstance(n, ast.FunctionDef) and n.name == 'check')
        # Execute the exact check() prefix through discovery. Later publication,
        # scientific crosswalk and original-body loops are outside this fixture.
        prefix = []
        for statement in node.body:
            if isinstance(statement, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == 'sources' for target in statement.targets):
                break
            prefix.append(statement)
        node.body = prefix + [ast.Return(value=ast.Name(id='errors', ctx=ast.Load()))]
        exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])),
                     'reader-check-through-discovery:actual-prefix', 'exec'), ns)
        return ns, memory, rows, owners, cross

    def test_current_pair_modifications_use_authenticated_edition(self):
        ns, memory, rows, owners, cross = self.owner_runtime()
        context, context_errors = ns['corpus_currentness_context'](memory.root, rows, owners, cross)
        errors = ns['check_corpus_currentness'](memory.root, owners['baseline']['commit'], *context)
        self.observe({'case': 'two-owner-M', 'context_errors': context_errors, 'errors': errors,
                      'edition_paths': sorted(context[3])})
        self.assertEqual(context_errors, [])
        self.assertEqual(errors, [])
        self.assertEqual(set(context[3]), {self.INDEX, self.README})

    def test_discovery_uses_current_rows_without_rebasing_original_population(self):
        ns, memory, rows, owners, cross = self.owner_runtime(changes=[])
        original_rows = json.loads(json.dumps(rows))
        errors = ns['check'](memory.root, owners, cross)
        self.observe({'case': 'two-owner-discovery', 'errors': errors, 'baseline_rows_unchanged': rows == original_rows})
        self.assertEqual(errors, [])
        self.assertEqual(rows, original_rows)
        self.assertEqual(owners['collections'][0]['candidate_paths'], 2)

    def test_original_pair_retains_original_discovery_and_existing_context_mapping(self):
        ns, memory, rows, owners, cross = self.owner_runtime(edition='original', changes=[])
        self.assertEqual(ns['status_owner_edition'](memory.root, rows, owners['baseline']), {})
        self.assertEqual(ns['check'](memory.root, owners, cross), [])
        sentinel = {'unrelated/prior-owner.md': {'git_oid': 'a' * 40}}
        ns['check_continuation_owner_edition'] = lambda *a: (dict(sentinel), [])
        context, errors = ns['corpus_currentness_context'](memory.root, rows, owners, cross)
        self.assertEqual(errors, [])
        self.assertEqual(context[3], sentinel)
        self.assertEqual(len(context), 5)

    def test_owner_edition_refuses_wrong_baseline_or_incomplete_original_pair(self):
        for mutation in ('baseline-commit', 'baseline-tree', 'missing-pair', 'path', 'kind', 'mode', 'git_oid', 'bytes'):
            with self.subTest(mutation=mutation):
                ns, memory, rows, owners, cross = self.owner_runtime()
                if mutation.startswith('baseline-'):
                    owners['baseline'][mutation.split('-')[1]] = 'f' * 40
                elif mutation == 'missing-pair':
                    del rows[self.README]
                else:
                    rows[self.INDEX][mutation] = 0 if mutation == 'bytes' else 'wrong'
                context, errors = ns['corpus_currentness_context'](memory.root, rows, owners, cross)
                self.assertTrue(any(error.startswith('status-owner: ') for error in errors), errors)
                self.assertFalse({self.INDEX, self.README} & set(context[3]))
        ns, memory, _, _, _ = self.owner_runtime()
        self.assertEqual(ns['status_owner_edition'](memory.root, {}, {}), {})

    def test_owner_edition_refuses_native_original_identity_and_coordinate_changes(self):
        mutations = ('commit-bytes', 'commit-type', 'commit-missing', 'tree-pin',
                     'native-mode', 'native-path-missing', 'native-blob',
                     'original-bytes', 'original-type', 'original-missing', 'original-size', 'original-sha256')
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                ns, memory, rows, owners, _ = self.owner_runtime()
                commit = ns['STATUS_RECORD_OWNER_BASE']
                blob, identity, size = ns['STATUS_RECORD_OWNER_ORIGINAL'][self.INDEX]
                if mutation == 'commit-bytes': memory.objects[commit] += b'corrupt'
                elif mutation == 'commit-type': memory.object_types[commit] = 'blob'
                elif mutation == 'commit-missing': del memory.objects[commit]
                elif mutation == 'tree-pin':
                    ns['STATUS_RECORD_OWNER_TREE'] = 'f' * 40
                    owners['baseline']['tree'] = 'f' * 40
                elif mutation == 'native-mode': memory.tree[self.INDEX] = memory.tree[self.INDEX].replace(b'100644', b'100755')
                elif mutation == 'native-path-missing': del memory.tree[self.INDEX]
                elif mutation == 'native-blob': memory.tree[self.INDEX] = memory.tree[self.INDEX].replace(blob.encode(), b'f' * 40)
                elif mutation == 'original-bytes': memory.objects[blob] += b'corrupt'
                elif mutation == 'original-type': memory.object_types[blob] = 'tree'
                elif mutation == 'original-missing': del memory.objects[blob]
                elif mutation == 'original-size':
                    ns['STATUS_RECORD_OWNER_ORIGINAL'][self.INDEX] = (blob, identity, size + 1)
                    rows[self.INDEX]['bytes'] = size + 1
                else: ns['STATUS_RECORD_OWNER_ORIGINAL'][self.INDEX] = (blob, 'f' * 64, size)
                with self.assertRaises((ValueError, OSError)):
                    ns['status_owner_edition'](memory.root, rows, owners['baseline'])

    def test_both_current_owners_require_one_exact_present_indexed_edition(self):
        mutations = ('unindexed', 'conflict', 'wrong-index', 'mixed-edition', 'absent',
                     'corrupt', 'executable', 'directory', 'symlink',
                     'native-bytes', 'native-type', 'native-missing')
        for path in (self.INDEX, self.README):
            for mutation in mutations:
                with self.subTest(path=path, mutation=mutation):
                    ns, memory, rows, owners, _ = self.owner_runtime()
                    blob = ns['STATUS_RECORD_OWNERS'][path][0]
                    if mutation == 'unindexed': memory.index[path] = []
                    elif mutation == 'conflict': memory.index[path] = ['100644 ' + blob + ' 1']
                    elif mutation == 'wrong-index': memory.index[path] = ['100644 ' + 'f' * 40 + ' 0']
                    elif mutation == 'mixed-edition':
                        old_blob = ns['STATUS_RECORD_OWNER_ORIGINAL'][path][0]
                        memory.index[path] = ['100644 ' + old_blob + ' 0']
                        memory.set_file(path, memory.objects[old_blob])
                    elif mutation == 'absent': memory.remove(path)
                    elif mutation == 'corrupt': memory.set_file(path, b'corrupt')
                    elif mutation == 'executable': memory.set_file(path, memory.objects[blob], stat.S_IFREG | 0o755)
                    elif mutation == 'directory': memory.set_file(path, None)
                    elif mutation == 'symlink': memory.set_file(path, b'target', stat.S_IFLNK | 0o777)
                    elif mutation == 'native-bytes': memory.objects[blob] += b'corrupt'
                    elif mutation == 'native-type': memory.object_types[blob] = 'tree'
                    else: del memory.objects[blob]
                    with self.assertRaises((ValueError, OSError)):
                        ns['status_owner_edition'](memory.root, rows, owners['baseline'])

    def test_owner_ancestry_and_late_pair_changes_refuse(self):
        for mutation in ('root-symlink', 'ancestor-symlink', 'late-index', 'late-body', 'late-absence'):
            with self.subTest(mutation=mutation):
                ns, memory, rows, owners, _ = self.owner_runtime()
                fired = []
                if mutation == 'root-symlink': memory.put(memory.ROOT, b'target', stat.S_IFLNK | 0o777)
                elif mutation == 'ancestor-symlink': memory.set_file('research', b'target', stat.S_IFLNK | 0o777)
                else:
                    def drift(event):
                        if event == ('git', 'cat-file', 'blob', ns['STATUS_RECORD_OWNERS'][self.README][0]):
                            memory.on_event = None
                            fired.append(len(memory.events) - 1)
                            if mutation == 'late-index': memory.index[self.INDEX] = ['100644 ' + ns['STATUS_RECORD_OWNERS'][self.INDEX][0] + ' 1']
                            elif mutation == 'late-body': memory.set_file(self.INDEX, b'corrupt')
                            else: memory.remove(self.INDEX)
                    memory.on_event = drift
                with self.assertRaises((ValueError, OSError)):
                    ns['status_owner_edition'](memory.root, rows, owners['baseline'])
                if mutation.startswith('late-'):
                    self.assertTrue(fired)

    def test_status_edition_never_admits_owner_deletion_addition_or_nearby_edit(self):
        for changes, authenticated in (([('M', self.INDEX)], False),
                                       ([('D', self.INDEX)], True),
                                       ([('A', self.README)], True),
                                       ([('T', self.INDEX)], True),
                                       ([('M', 'research/t20-live-20261009/nearby.json')], True)):
            with self.subTest(changes=changes, authenticated=authenticated):
                ns, memory, rows, owners, cross = self.owner_runtime(changes=changes)
                context, context_errors = ns['corpus_currentness_context'](memory.root, rows, owners, cross)
                self.assertEqual(context_errors, [])
                if not authenticated:
                    context = (*context[:3], {}, context[4])
                self.assertTrue(ns['check_corpus_currentness'](memory.root, owners['baseline']['commit'], *context))

    def test_production_owner_pins_and_editable_paths_remain_exact(self):
        root = globals().get('_STATUS_TEST_SOURCE_ROOT', Path(__file__).resolve().parents[1])
        source = (root / 'scripts/resolve_t20_v6_source.py').read_text()
        names = {'STATUS_RECORD_OWNER_BASE', 'STATUS_RECORD_OWNER_TREE',
                 'STATUS_RECORD_OWNER_ORIGINAL', 'STATUS_RECORD_OWNERS'}
        pins = {node.targets[0].id: ast.literal_eval(node.value) for node in ast.parse(source).body
                if isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name) and node.targets[0].id in names}
        self.assertEqual(pins['STATUS_RECORD_OWNER_BASE'], '0784acddd4770f1190f758f264ba52b2b110bd27')
        self.assertEqual(pins['STATUS_RECORD_OWNER_TREE'], '38b18f38db2e38dabe1ec391c07c0b0f2b20d574')
        self.assertEqual(pins['STATUS_RECORD_OWNER_ORIGINAL'], {
            self.INDEX: ('533205328be61d4ef00734ec5ab1726af056ce24', '578b2f63c3038627a68c1d4cd816ca9f9a3cd973ee35864a5c22e3860f2f7483', 15728),
            self.README: ('0d225b8cf2973d28c9ff2bcfd215e364bb18ca42', '543cc8ea246fdc3f1fb03e0b41bb539dde2f23a7eeaa2ddf9178826840b5f139', 10196)})
        self.assertEqual(pins['STATUS_RECORD_OWNERS'], {
            self.INDEX: ('08341bfd44725c42af1048aec08fcad5b51aadfd', '9cf4bca6f4162f3a0426dba75949cb13482544ba35876d6e3a4dc1d2e699241f', 5956771),
            self.README: ('3a93bf5c75cbbd0796e3edef91a7571da4eb2771', '1bea43d34528443aedec67f7a58a92d04b173e87c4d068f018499f9c4651d49d', 107789)})
        reader = (root / 'scripts/check_reader_pilot.py').read_text()
        editable = next(node for node in ast.parse(reader).body
                        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'REFACTOR_EDIT_PATHS' for t in node.targets))
        namespace = {}
        exec(compile(ast.Module(body=[editable], type_ignores=[]),
                     'reader-exact-editable-constant', 'exec'), namespace)
        self.assertFalse({self.INDEX, self.README} & namespace['REFACTOR_EDIT_PATHS'])

    def late_source_index(self, interface, present):
        helper = self.base()
        ns, memory = helper.memory_runtime(present=present)
        reads, fired = [], []
        owner_blob = ns['STATUS_RECORD_OWNERS'][memory.owner_index][0]
        def drift(event):
            if event == ('git', 'cat-file', 'blob', owner_blob):
                reads.append(len(memory.events) - 1)
                if len(reads) == 2:
                    memory.on_event = None
                    fired.append(len(memory.events) - 1)
                    memory.index[helper.STATUS] = ['100644 ' + memory.status_blob + ' 1']
        memory.on_event = drift
        argument = helper.STATUS if interface == 'status_record_bytes' else {helper.STATUS}
        error = None
        try: ns[interface](memory.root, argument)
        except (ValueError, OSError) as exc: error = str(exc)
        index_reads = [i for i, event in enumerate(memory.events)
                       if event == ('git', 'ls-files', '--stage', '-z', '--', helper.STATUS)]
        self.observe({'case': 'SCR-002', 'interface': interface, 'present': present,
                      'fired': fired, 'index_reads': index_reads, 'error': error,
                      'events': [list(event) for event in memory.events]})
        self.assertTrue(fired)
        self.assertIsNotNone(error, 'late selected-source index conflict was accepted')
        self.assertTrue(any(i > fired[0] for i in index_reads))

    def test_absent_getter_refuses_index_drift_during_final_owner_read(self):
        self.late_source_index('status_record_bytes', False)

    def test_present_getter_refuses_index_drift_during_final_owner_read(self):
        self.late_source_index('status_record_bytes', True)

    def test_absence_set_refuses_index_drift_during_final_owner_read(self):
        self.late_source_index('status_record_absences', False)

    def test_source_entry_conflicts_refuse_and_stable_empty_indexes_remain_allowed(self):
        helper = self.base()
        for interface, present in (('status_record_bytes', False), ('status_record_bytes', True), ('status_record_absences', False)):
            for index in ('exact', 'empty', 'conflict'):
                with self.subTest(interface=interface, present=present, index=index):
                    ns, memory = helper.memory_runtime(present=present)
                    if index == 'empty': memory.index[helper.STATUS] = []
                    elif index == 'conflict': memory.index[helper.STATUS] = ['100644 ' + memory.status_blob + ' 1']
                    argument = helper.STATUS if interface == 'status_record_bytes' else {helper.STATUS}
                    if index == 'conflict':
                        with self.assertRaises(ValueError): ns[interface](memory.root, argument)
                    else:
                        expected = helper.BODY if interface == 'status_record_bytes' else {helper.STATUS}
                        self.assertEqual(ns[interface](memory.root, argument), expected)

    def test_absence_bracket_checks_every_requested_source(self):
        helper = self.base()
        other = 'research/t20-live-20261009/checkpoints/CP01/SECOND_INERT_STATUS.json'
        for changed in (helper.STATUS, other):
            with self.subTest(changed=changed):
                ns, memory = helper.memory_runtime()
                source, values = helper.raw_source(ns, helper.BODY)
                source['aliases'].append(other)
                document = {'schema': 'scientific-status-owner-v3', 'sources': {'S0001': source}, 'values': values}
                raw = json.dumps(document, ensure_ascii=False, separators=(',', ':')).encode()
                blob = memory.add_object(raw)
                memory.set_file(self.INDEX, raw)
                memory.index[self.INDEX] = ['100644 ' + blob + ' 0']
                ns['STATUS_RECORD_OWNERS'][self.INDEX] = (blob, hashlib.sha256(raw).hexdigest(), len(raw))
                paths = {helper.STATUS, other}
                for path in paths:
                    memory.index[path] = ['100644 ' + memory.status_blob + ' 0']
                    memory.tree[path] = ('100644 blob ' + memory.status_blob + '\t' + path + '\0').encode()
                vector = b''.join((path + '\0S0001\0' + memory.status_blob + '\0' + hashlib.sha256(helper.BODY).hexdigest() + '\0' + str(len(helper.BODY)) + '\n').encode() for path in sorted(paths))
                ns.update(STATUS_RECORD_PATH_HASHES={hashlib.sha256(path.encode()).hexdigest() for path in paths},
                          STATUS_RECORD_ALIAS_COUNT=2, STATUS_RECORD_CLASS_SHA256=hashlib.sha256(vector).hexdigest())
                count, fired = [], []
                def drift(event):
                    if event == ('git', 'cat-file', 'blob', blob):
                        count.append(1)
                        if len(count) == 2:
                            memory.on_event = None
                            fired.append(1)
                            memory.index[changed] = ['100644 ' + memory.status_blob + ' 1']
                memory.on_event = drift
                with self.assertRaises(ValueError): ns['status_record_absences'](memory.root, paths)
                self.assertTrue(fired)

    def provider_runtime(self):
        helper = self.base()
        ns, memory = helper.memory_runtime()
        memory.tree[self.ALIAS] = ('100644 blob ' + memory.status_blob + '\t' + self.ALIAS + '\0').encode()
        memory.index[self.ALIAS] = ['100644 ' + memory.status_blob + ' 0']
        ns.update(STATUS_RECORD_PROVIDER_HASHES={hashlib.sha256(helper.STATUS.encode()).hexdigest()},
                  CHECKPOINT_COPY_BASE=ns['STATUS_RECORD_BASE'], collections=collections)
        def native(root, *args):
            if args[:2] == ('ls-tree', '-z') and len(args) == 6 and args[3] == '--':
                memory.event(('checkpoint-native', *args))
                return b''.join(memory.tree.get(path, b'') for path in args[4:])
            return memory.git(root, *args)
        ns['_continuation_git'] = native
        helper.selected('resolve_t20_v6_source.py',
                        {'_checkpoint_bound_bytes', '_continuation_object', '_regular_current_bytes'}, ns)
        binding = {'canonical': helper.STATUS, 'blob': memory.status_blob,
                   'sha256': hashlib.sha256(helper.BODY).hexdigest(), 'bytes': len(helper.BODY)}
        return ns, memory, binding

    def late_alias(self, mutation):
        helper = self.base()
        ns, memory, binding = self.provider_runtime()
        initial_index = list(memory.index[self.ALIAS])
        fired = []
        def drift(event):
            if event == ('git', 'cat-file', 'blob', ns['STATUS_RECORD_OWNERS'][self.INDEX][0]):
                memory.on_event = None
                fired.append(len(memory.events) - 1)
                if mutation == 'index': memory.index[self.ALIAS] = ['100644 ' + memory.status_blob + ' 1']
                else: memory.set_file(self.ALIAS, helper.BODY + b'corrupt')
        memory.on_event = drift
        error = None
        try: ns['_checkpoint_bound_bytes'](memory.root, self.ALIAS, binding)
        except (ValueError, OSError) as exc: error = str(exc)
        self.observe({'case': 'SCR-003', 'mutation': mutation, 'fired': fired, 'error': error,
                      'alias_index_before': initial_index, 'alias_index_after': memory.index[self.ALIAS],
                      'events': [list(event) for event in memory.events]})
        self.assertTrue(fired)
        self.assertIsNotNone(error, 'late requested-alias change was accepted')

    def test_provider_read_cannot_hide_late_alias_index_conflict(self):
        self.late_alias('index')

    def test_provider_read_cannot_hide_late_corrupt_alias_appearance(self):
        self.late_alias('bytes')

    def test_provider_entry_guards_and_final_provider_absence_remain_required(self):
        helper = self.base()
        for mutation in ('unchanged', 'entry-index', 'entry-bytes', 'late-provider-present'):
            with self.subTest(mutation=mutation):
                ns, memory, binding = self.provider_runtime()
                fired = []
                if mutation == 'entry-index': memory.index[self.ALIAS] = ['100644 ' + memory.status_blob + ' 1']
                elif mutation == 'entry-bytes': memory.set_file(self.ALIAS, helper.BODY + b'corrupt')
                elif mutation == 'late-provider-present':
                    def appear(event):
                        if event == ('git', 'ls-files', '--stage', '-z', '--', self.ALIAS, helper.STATUS):
                            memory.on_event = None
                            fired.append(1)
                            memory.set_file(helper.STATUS, helper.BODY)
                    memory.on_event = appear
                if mutation == 'unchanged':
                    self.assertEqual(ns['_checkpoint_bound_bytes'](memory.root, self.ALIAS, binding), helper.BODY)
                else:
                    with self.assertRaises(ValueError): ns['_checkpoint_bound_bytes'](memory.root, self.ALIAS, binding)
                if mutation == 'late-provider-present': self.assertTrue(fired)


class StatusProjectionCompositionControls(unittest.TestCase):
    """Actual protected-root logic with inert interfaces; no source-body replay."""

    SOURCE = pathlib.Path(__file__).resolve().parents[1] / 'scripts/validate_t20_v6_projection.py'
    OWNERS = ('research/t20-live-20261009/INDEX.json',
              'research/t20-live-20261009/README.md')
    RECORDS = ('research/t20-live-20261009/synthetic-selected-a.json',
               'research/t20-live-20261009/synthetic-selected-b.json')

    def _gate(self, cached=(), worktree=None, *, owners='qualified', absences='qualified',
              diff_status=0):
        # Only the actual operational function is compiled. Every dependency is
        # finite in-memory input, never an import or a native/filesystem probe.
        nodes = [n for n in ast.parse(self.SOURCE.read_bytes()).body
                 if isinstance(n, ast.FunctionDef) and n.name == 'check_preserved_roots']
        self.assertEqual(len(nodes), 1)
        calls = []
        worktree = cached if worktree is None else worktree
        original = {p: (str(i + 1) * 40, str(i + 1) * 64, i + 100)
                    for i, p in enumerate(self.OWNERS)}
        expected_rows = {p: dict(path=p, kind='blob', mode='100644', git_oid=b, bytes=z)
                         for p, (b, h, z) in original.items()}
        baseline = dict(commit='a' * 40, tree='b' * 40)
        def owner_edition(root, rows, base):
            self.assertEqual(rows, expected_rows)
            self.assertEqual(base, baseline)
            calls.append(('owner', None))
            if owners == 'ioerror': raise OSError('unavailable owner evidence')
            if owners == 'valueerror': raise ValueError('wrong owner edition')
            return expected_rows if owners == 'qualified' else {}
        def record_absences(root, requested):
            requested = set(requested)
            calls.append(('absence', requested))
            self.assertTrue(requested)
            self.assertTrue(requested <= set(self.RECORDS))
            if absences == 'ioerror': raise OSError('unavailable record evidence')
            if absences == 'valueerror': raise ValueError('present or corrupt record')
            return requested if absences == 'qualified' else set()
        def diff(root, command):
            selected = cached if '--cached' in command else worktree
            raw = ''.join(status + '\0' + path + '\0' for status, path in selected).encode()
            return subprocess.CompletedProcess(command, diff_status, raw, b'')
        def unavailable(*args, **kwargs):
            raise ValueError('unrelated population absent from inert fixture')
        namespace = dict(subprocess=subprocess, readonly_git_diff=diff,
            HISTORICAL_PROSE={}, HISTORICAL_PROSE_PUBLIC_PATHS=set(),
            HISTORICAL_PROSE_REVISIONS={}, TYPED_GUIDES={}, ADMIN_GUIDES={},
            BASE='inert-baseline', CONTINUATION_COPY_ROOT='unrelated-continuation/',
            CHECKPOINT_COPY_PATHS=set(), CHECKPOINT_RECORD_COPY_PATHS=set(),
            CHECKPOINT_PACKAGE_COPY_PATHS=set(), FORMAL_COPY_PATHS=set(),
            CHECKPOINT_CODE_COPY_PATHS=set(), DIGEST_RECORD_PATHS=set(),
            SUCCESSOR_INPUT_REGISTRY='unrelated-input-registry', SUCCESSOR_INPUT_PATHS=set(),
            SUCCESSOR_CALCULUS_MAP='unrelated-calculus-map', SUCCESSOR_CALCULUS_GUIDES={},
            MEDIATOR_GUIDE='unrelated-guide', binding_record_candidate=lambda p: False,
            continuation_owners=types.SimpleNamespace(PRESERVATION_OWNER_PATHS=set()),
            mediator_guide_source_bytes=unavailable,
            STATUS_RECORD_OWNERS={p: () for p in self.OWNERS},
            STATUS_RECORD_OWNER_ORIGINAL=original,
            STATUS_RECORD_OWNER_BASE=baseline['commit'], STATUS_RECORD_OWNER_TREE=baseline['tree'],
            status_owner_edition=owner_edition,
            status_record_candidate=lambda p: p in self.RECORDS,
            status_record_absences=record_absences)
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(self.SOURCE), 'exec'), namespace)
        return namespace['check_preserved_roots'](pathlib.Path('unused-inert-root'), {}), calls

    def test_unchanged_scope_is_live_without_status_qualification(self):
        result, calls = self._gate()
        self.assertEqual(result, [])
        self.assertEqual(calls, [])

    def test_complete_qualified_status_owner_modifications_are_admitted(self):
        result, calls = self._gate(tuple(('M', p) for p in self.OWNERS))
        self.assertEqual(result, [])
        self.assertEqual(calls, [('owner', None), ('owner', None)])

    def test_original_or_unavailable_owner_does_not_waive_modification(self):
        for state in ('original', 'valueerror', 'ioerror'):
            with self.subTest(state=state):
                result, calls = self._gate((('M', self.OWNERS[0]),), owners=state)
                self.assertTrue(result)
                self.assertEqual(len(calls), 2)

    def test_owner_deletion_type_addition_and_unselected_modification_refuse(self):
        for status, path in (('D', self.OWNERS[0]), ('T', self.OWNERS[0]),
                             ('A', self.OWNERS[0]), ('M', 'research/t20-live-20261009/unselected.md')):
            with self.subTest(status=status, path=path):
                result, calls = self._gate(((status, path),))
                self.assertTrue(result)
                self.assertEqual(calls, [])

    def test_selected_qualified_D_only_status_absence_is_admitted(self):
        result, calls = self._gate((('D', self.RECORDS[0]),))
        self.assertEqual(result, [])
        self.assertEqual(calls, [('absence', {self.RECORDS[0]})] * 2)

    def test_each_boundary_qualifies_its_complete_requested_absence_set(self):
        result, calls = self._gate((('D', self.RECORDS[0]),),
                                  tuple(('D', p) for p in self.RECORDS))
        self.assertEqual(result, [])
        self.assertEqual(calls, [('absence', {self.RECORDS[0]}),
                                 ('absence', set(self.RECORDS))])

    def test_empty_unavailable_present_or_corrupt_absence_refuses(self):
        for state in ('empty', 'valueerror', 'ioerror'):
            with self.subTest(state=state):
                result, calls = self._gate((('D', self.RECORDS[0]),), absences=state)
                self.assertTrue(result)
                self.assertEqual(len(calls), 2)

    def test_selected_M_T_A_and_unselected_D_are_not_absence_allowances(self):
        for status, path in (('M', self.RECORDS[0]), ('T', self.RECORDS[0]),
                             ('A', self.RECORDS[0]), ('D', 'research/t20-live-20261009/unselected.json')):
            with self.subTest(status=status, path=path):
                result, calls = self._gate(((status, path),))
                self.assertTrue(result)
                self.assertEqual(calls, [])

    def test_staged_M_cannot_hide_behind_worktree_D(self):
        result, calls = self._gate((('M', self.RECORDS[0]),), (('D', self.RECORDS[0]),))
        self.assertTrue(result)
        self.assertEqual(calls, [('absence', {self.RECORDS[0]})])

    def test_owner_and_absence_admission_compose_without_widening_scope(self):
        changes = tuple(('M', p) for p in self.OWNERS) + (('D', self.RECORDS[0]),)
        result, calls = self._gate(changes)
        self.assertEqual(result, [])
        self.assertEqual(len(calls), 4)
        result, _ = self._gate(changes + (('D', 'research/t20-live-20261009/unselected.json'),))
        self.assertTrue(result)

    def test_failed_diff_is_not_empty_success(self):
        result, calls = self._gate(diff_status=1)
        self.assertTrue(result)
        self.assertEqual(calls, [])

if __name__ == '__main__':
    unittest.main()

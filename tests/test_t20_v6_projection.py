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


if __name__ == '__main__':
    unittest.main()

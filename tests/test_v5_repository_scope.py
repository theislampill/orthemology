"""Regression controls for separate research locks and mathematical link text."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_dependency_lock as dependencies
import validate_repo as repository
import validate_internal_references as references


class ResearchDependencyScopeTests(unittest.TestCase):
    def fixture(self, root):
        lock = b'numpy==2.3.5\n'
        code = b'import numpy\nimport os\n'
        lh, ch = hashlib.sha256(lock).hexdigest(), hashlib.sha256(code).hexdigest()
        prefix = 'experiments/orthemology-v5-successors/source-store/'
        for rel, raw in [(prefix + lh + '/requirements.txt', lock), (prefix + ch + '/research.py', code)]:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(raw)
        return {lh: {'research.py': ch}}, root / (prefix + lh + '/requirements.txt'), root / (prefix + ch + '/research.py')

    def test_exact_research_lock_does_not_upgrade_ci_environment(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            packages, _, _ = self.fixture(root)
            with patch.object(dependencies, 'RESEARCH_SOURCE_LOCKS', packages, create=True):
                self.assertEqual({'os'}, dependencies.scan_repository_imports(root))

    def test_same_import_outside_exact_research_owner_remains_unmapped(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            packages, _, _ = self.fixture(root)
            (root / 'scripts').mkdir()
            (root / 'scripts' / 'unbound.py').write_text('import numpy\n')
            with patch.object(dependencies, 'RESEARCH_SOURCE_LOCKS', packages, create=True):
                self.assertIn('numpy', dependencies.scan_repository_imports(root))

    def test_changed_lock_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            packages, lock, _ = self.fixture(root)
            lock.write_bytes(b'numpy>=2\n')
            with patch.object(dependencies, 'RESEARCH_SOURCE_LOCKS', packages, create=True):
                with self.assertRaises(ValueError):
                    dependencies.scan_repository_imports(root)

    def test_changed_source_cannot_borrow_research_scope(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            packages, _, source = self.fixture(root)
            source.write_bytes(b'import numpy\nimport unpinned_extra\n')
            with patch.object(dependencies, 'RESEARCH_SOURCE_LOCKS', packages, create=True):
                with self.assertRaises(ValueError):
                    dependencies.scan_repository_imports(root)


class MathematicalLinkTests(unittest.TestCase):
    def test_equations_are_not_links_and_real_missing_links_remain(self):
        text = '$$\n[\\![f]\\!](n,e)=0\n$$\n[missing](missing.md)\n'
        self.assertEqual(['missing.md'], list(repository.markdown_link_targets(text)))

    def test_angle_url_with_fragment_and_parenthesized_filename(self):
        text = '[paper](<https://example.org/paper.pdf#page=66>) [local](a(b).md#x)'
        self.assertEqual(['https://example.org/paper.pdf#page=66', 'a(b).md#x'],
                         list(repository.markdown_link_targets(text)))


class MathlibLocatorTests(unittest.TestCase):
    def source(self):
        rows = json.loads((ROOT / 'docs/provenance/v5-successors/SOURCE_MAP.json').read_bytes())['sources']
        owner = next(row for row in rows if row['public_sha256'] == '1c4d1fa63acf416d7b965ed519d16faea965022cb8eb8d74725d59d801db16f0')
        return owner, json.loads((ROOT / owner['public_path']).read_bytes())

    def test_exact_mathlib_inventory_is_external_not_local_docs(self):
        owner, document = self.source()
        self.assertIn('docs/' + '100.yaml', repository._locked_external_files(document, owner) or {})

    def test_changed_inventory_cannot_borrow_a_known_lock(self):
        owner, document = self.source()
        document['files'][0]['path'] = '../missing.py'
        self.assertIsNone(repository._locked_external_files(document, owner))


class OriginalDriverLocatorTests(unittest.TestCase):
    def test_exact_adapter_members_are_not_repository_files(self):
        path = 'scripts/replay_v5_successors.py'
        text = (ROOT / path).read_text(encoding='utf-8')
        citations = {cited for cited, _ in references._citation_occurrences(path, text)}
        self.assertNotIn('scripts/' + 'verify-inputs.py', citations)
        self.assertNotIn('scripts/' + 'verify-sources.py', citations)

    def test_changed_adapter_cannot_borrow_original_member_scope(self):
        path = 'scripts/replay_v5_successors.py'
        text = (ROOT / path).read_text(encoding='utf-8') + '\n# changed adapter\n'
        citations = {cited for cited, _ in references._citation_occurrences(path, text)}
        self.assertIn('scripts/' + 'verify-inputs.py', citations)

    def test_same_locator_outside_adapter_is_still_checked(self):
        target = 'scripts/' + 'verify-inputs.py'
        citations = {cited for cited, _ in references._citation_occurrences('docs/' + 'new.md', target)}
        self.assertIn(target, citations)


if __name__ == '__main__':
    unittest.main()

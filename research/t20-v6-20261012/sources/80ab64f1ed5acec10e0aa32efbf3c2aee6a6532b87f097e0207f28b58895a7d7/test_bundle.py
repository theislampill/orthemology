"""Negative and positive controls for the compact preservation checker."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

CHECKER = Path(__file__).with_name('verify_bundle.py')


class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CHECKER.exists(), 'Compact preservation checker not implemented')
        spec = importlib.util.spec_from_file_location('compact_checker', CHECKER)
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def fixture(self, root):
        (root / 'data.txt').write_bytes(b'bound source\n')
        manifest = {'files': {'data.txt': {'bytes': 13, 'sha256': hashlib.sha256(b'bound source\n').hexdigest()}}}
        (root / 'MANIFEST.json').write_text(json.dumps(manifest))

    def test_matching_manifest_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            self.assertEqual(self.module.verify_integrity(root), 1)

    def test_uninventoried_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'extra.txt').write_text('unbound')
            with self.assertRaisesRegex(ValueError, 'uninventoried'):
                self.module.verify_integrity(root)

    def test_dependency_hash_is_enforced(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'script.py').write_text('pass\n')
            (root / 'source.txt').write_text('source\n')
            script = {'path': 'script.py', **self.module.digest(root / 'script.py')}
            source = {'path': 'source.txt', **self.module.digest(root / 'source.txt')}
            records = [{'script': script, 'dependencies': [source]}]
            self.assertEqual(self.module.verify_script_dependencies(root, records),
                             {'scripts': 1, 'dependency_bindings': 1})
            (root / 'source.txt').write_text('changed\n')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                self.module.verify_script_dependencies(root, records)

    def test_only_runtime_metadata_is_ignored(self):
        a = {'assertion_groups': 1, 'python': 'old', 'sympy': '1', 'platform': 'a'}
        b = {'assertion_groups': 1, 'python': 'new', 'sympy': '2', 'platform': 'b'}
        self.assertEqual(self.module.computational_content(a), self.module.computational_content(b))
        b['assertion_groups'] = 2
        self.assertNotEqual(self.module.computational_content(a), self.module.computational_content(b))

    def test_corruption_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'data.txt').write_bytes(b'wrong source\n')
            with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                self.module.verify_integrity(root)

    def test_missing_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); self.fixture(root)
            (root / 'data.txt').unlink()
            with self.assertRaisesRegex(ValueError, 'missing bound file'):
                self.module.verify_integrity(root)

    def test_parent_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'unsafe relative path'):
                self.module.resolve(Path(tmp), '../outside')

    def test_existing_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'already exists'):
                self.module.new_output(Path(tmp))

    def test_new_output_is_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'new'
            self.module.new_output(root)
            self.assertTrue(root.is_dir())


if __name__ == '__main__':
    unittest.main()

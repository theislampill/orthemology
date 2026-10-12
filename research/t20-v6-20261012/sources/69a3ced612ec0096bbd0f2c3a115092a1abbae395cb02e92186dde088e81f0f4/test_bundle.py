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

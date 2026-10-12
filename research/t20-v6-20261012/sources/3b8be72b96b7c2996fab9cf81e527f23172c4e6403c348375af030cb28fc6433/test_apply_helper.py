"""Apply authorization guards, using inert Git responses (no branch is written)."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

HELPER = Path(__file__).with_name('apply_checked_patch.py')
spec = importlib.util.spec_from_file_location('patch_helper', HELPER)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class ApplyBranchGuardTests(unittest.TestCase):
    def invoke(self, branch, apply, patch_filename='test.patch'):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name) / 'package'
            folder.mkdir()
            raw = b'test-only inert patch\n'
            (folder / 'test.patch').write_bytes(raw)
            (folder.parent / 'outside.patch').write_bytes(raw)
            (folder / 'PATCH_MANIFEST.json').write_text(json.dumps({
                'schema': 'through-twentieth-exact-base-patch-v1',
                'base_commit': 'a' * 40, 'base_tree': 'b' * 40,
                'candidate_tree': 'c' * 40, 'changed_files': [],
                'patch': {'filename': patch_filename, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)},
            }))
            writes = []
            def inert_git(root, *args):
                if args == ('rev-parse', 'HEAD'): return 'a' * 40
                if args == ('rev-parse', 'HEAD^{tree}'): return 'b' * 40
                if args == ('branch', '--show-current'): return branch
                if args == ('write-tree',): return 'c' * 40
                if args[:2] == ('apply', '--index'): writes.append(args)
                return ''
            argv = ['apply_checked_patch.py', '--repository', str(folder)] + (['--apply'] if apply else [])
            with patch.object(helper, '__file__', str(folder / 'apply_checked_patch.py')), patch.object(helper, 'git', inert_git), patch.object(sys, 'argv', argv), contextlib.redirect_stdout(io.StringIO()):
                try:
                    helper.main()
                finally:
                    self.writes = writes
            return writes

    def test_apply_refuses_main_before_mutation(self):
        with self.assertRaisesRegex(ValueError, 'feature branch|main|master'):
            self.invoke('main', True)
        self.assertEqual(self.writes, [])

    def test_apply_refuses_master_before_mutation(self):
        with self.assertRaisesRegex(ValueError, 'feature branch|main|master'):
            self.invoke('master', True)
        self.assertEqual(self.writes, [])

    def test_apply_refuses_detached_head(self):
        with self.assertRaisesRegex(ValueError, 'feature branch|detached'):
            self.invoke('', True)
        self.assertEqual(self.writes, [])

    def test_read_only_check_is_allowed_on_main(self):
        self.assertEqual(self.invoke('main', False), [])

    def test_manifest_patch_filename_cannot_escape_package(self):
        with self.assertRaisesRegex(ValueError, 'Unsafe manifest path'):
            self.invoke('main', False, '../outside.patch')
        self.assertEqual(self.writes, [])

    def test_repository_metadata_paths_are_refused(self):
        with tempfile.TemporaryDirectory() as name:
            for relative in ('.git', '.git/config', 'nested/.git/objects/x', '.GIT/config'):
                with self.subTest(relative=relative), self.assertRaisesRegex(ValueError, 'metadata'):
                    helper.safe(Path(name), relative)

    def test_apply_is_allowed_on_named_feature_branch(self):
        self.assertEqual(len(self.invoke('integration/t20-review', True)), 1)


if __name__ == '__main__':
    unittest.main()

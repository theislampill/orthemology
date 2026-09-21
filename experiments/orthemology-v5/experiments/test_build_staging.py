"""Real filesystem orchestration tests; no Lean compiler is mocked or certified."""
from pathlib import Path
import importlib.util
import sys
import tempfile
import unittest
sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1] / 'formal_project'
sys.path.insert(0, str(PROJECT))
spec = importlib.util.spec_from_file_location('formal_build_driver', PROJECT / 'build.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)

class BuildStaging(unittest.TestCase):
    def stage(self, source, dest):
        fn = getattr(driver, 'stage_build', None)
        self.assertTrue(callable(fn), 'real build driver needs an isolated staging operation')
        return fn(source, dest)

    def test_real_build_tree_is_isolated_and_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / 'source'; source.mkdir()
            (source/'A.lean').write_text('theorem t : True := True.intro\n')
            target = self.stage(source, root/'work')
            self.assertEqual((target/'A.lean').read_bytes(), (source/'A.lean').read_bytes())
            (target/'.lake').mkdir(); (target/'.lake'/'probe').write_text('compiled output')
            self.assertFalse((source/'.lake').exists())
            self.assertEqual([p.name for p in source.iterdir()], ['A.lean'])

    def test_staging_refuses_source_descendant_or_reused_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'source'; source.mkdir()
            (source/'A.lean').write_text('import Init\n')
            fn = getattr(driver, 'stage_build', None)
            self.assertTrue(callable(fn), 'isolation guard must exist')
            with self.assertRaises(driver.gate.GateError): fn(source, source/'build')
            (root/'work').mkdir()
            with self.assertRaises(driver.gate.GateError): fn(source, root/'work')

    def test_staging_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'source'; source.mkdir()
            (root/'outside').write_text('not project source')
            (source/'link').symlink_to(root/'outside')
            fn = getattr(driver, 'stage_build', None)
            self.assertTrue(callable(fn), 'staging validation must exist')
            with self.assertRaises(driver.gate.GateError): fn(source, root/'work')

if __name__ == '__main__': unittest.main()

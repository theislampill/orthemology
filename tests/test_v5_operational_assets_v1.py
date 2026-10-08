"""Pure adapter packaging checks; no source-owned driver or compiler runs."""
import ast
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
CATALOG = 'v5_operational_recipes_v1.json'
ASSETS = 'v5_operational_assets_v1'


def load(path):
    spec = importlib.util.spec_from_file_location('operational_packaging_fixture', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OperationalAssetPackagingTests(unittest.TestCase):
    def test_exact_catalog_and_helpers_load(self):
        adapter = load(SCRIPTS / 'replay_v5_successors.py')
        self.assertEqual(adapter._OPERATIONAL_DATA, json.loads((SCRIPTS / CATALOG).read_text()))
        self.assertEqual(len(adapter.OPERATIONAL_RECIPES), 6)
        self.assertEqual(adapter.operational_execute_suite.__globals__['__file__'], str(SCRIPTS / 'replay_v5_successors.py'))
        self.assertEqual(adapter.operational_validate_package.__globals__, adapter.__dict__)

    def test_catalog_is_json_without_executable_literal_loader(self):
        data = json.loads((SCRIPTS / CATALOG).read_text())
        self.assertEqual(len(data['suites']), 6)
        tree = ast.parse((SCRIPTS / 'replay_v5_successors.py').read_text())
        assignments = [node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == '_OPERATIONAL_DATA' for target in node.targets)]
        self.assertEqual(len(assignments), 1)
        self.assertFalse(isinstance(assignments[0].value.args[0], ast.Constant))

    def corrupted_copy(self, change):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'scripts'; shutil.copytree(SCRIPTS, target)
            change(target)
            with self.assertRaisesRegex(ValueError, 'operational asset'):
                load(target / 'replay_v5_successors.py')

    def test_changed_catalog_is_rejected(self):
        def change(target):
            with (target / CATALOG).open('ab') as stream: stream.write(b' ')
        self.corrupted_copy(change)

    def test_missing_helper_is_rejected(self):
        self.corrupted_copy(lambda target: (target / ASSETS / 'collection.py').unlink())

    def test_changed_helper_is_rejected_before_code_execution(self):
        def change(target):
            with (target / ASSETS / 'execution.py').open('ab') as stream:
                stream.write(b'\nraise RuntimeError("unverified code executed")\n')
        self.corrupted_copy(change)

    def test_symlinked_helper_is_rejected(self):
        def change(target):
            path = target / ASSETS / 'runtime.py'; payload = path.read_bytes()
            actual = target / 'other.py'; actual.write_bytes(payload); path.unlink(); path.symlink_to(actual)
        self.corrupted_copy(change)

    def test_no_asset_compilation_until_every_hash_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'scripts'; shutil.copytree(SCRIPTS, target)
            (target / ASSETS / 'execution.py').write_text('raise RuntimeError("unverified code executed")\n')
            spec = importlib.util.spec_from_file_location('partial_packaging_fixture', target / 'replay_v5_successors.py')
            module = importlib.util.module_from_spec(spec)
            with self.assertRaisesRegex(ValueError, 'operational asset'):
                spec.loader.exec_module(module)
            self.assertFalse(hasattr(module, 'operational_precheck'))


if __name__ == '__main__': unittest.main(verbosity=2)

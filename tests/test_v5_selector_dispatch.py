"""Public-shaped loader/receipt/CLI routing controls; no execution."""
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MAIN_PATH = ROOT / 'scripts/replay_v5_successors.py'
MAIN = None
if MAIN_PATH.exists():
    spec = importlib.util.spec_from_file_location('selector_dispatch_candidate', MAIN_PATH)
    MAIN = importlib.util.module_from_spec(spec); exec(compile(MAIN_PATH.read_bytes(), str(MAIN_PATH), 'exec'), MAIN.__dict__)


class DispatchTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(MAIN, 'Verified public-shaped selector dispatch proposal is absent')

    def test_exact_assets_load_with_main_owned_registry(self):
        helper, executor = MAIN.selector_continuation_load()
        self.assertEqual(helper.SC_SCHEMA, 'orthemology-v5-selector-audit-continuation-v1')
        self.assertEqual(helper.SC_REVIEWED_EXECUTORS, MAIN.SELECTOR_CONTINUATION_REVIEWED_EXECUTORS)
        self.assertTrue(callable(executor.execute))

    def test_changed_missing_and_linked_assets_fail_before_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for name in ('v5_selector_continuation.py', 'v5_selector_executor.py'):
                (root / name).write_bytes((MAIN_PATH.parent / name).read_bytes())
            with mock.patch.object(MAIN, '__file__', str(root / 'replay_v5_successors.py')):
                target = root / 'v5_selector_executor.py'; raw = target.read_bytes()
                target.write_bytes(raw + b'\nraise AssertionError("unreviewed code ran")\n')
                with self.assertRaises(ValueError): MAIN.selector_continuation_load()
                target.unlink()
                with self.assertRaises((ValueError, OSError)): MAIN.selector_continuation_load()
                outside = root / 'outside.py'; outside.write_bytes(raw); target.symlink_to(outside)
                with self.assertRaises(ValueError): MAIN.selector_continuation_load()

    def test_new_receipt_dispatch_precedes_ordinary_selector_gate(self):
        validator = mock.Mock(return_value={'checked': True}); helper = SimpleNamespace(validate_selector_continuation=validator)
        receipt = {'replay_evidence': {'schema': 'orthemology-v5-selector-audit-continuation-v1'}}
        with mock.patch.object(MAIN, 'selector_continuation_load', return_value=(helper, None)), \
                mock.patch.object(MAIN, 'selector_g1_handles', side_effect=AssertionError('ordinary gate reached')):
            self.assertEqual(MAIN.validate_receipt(receipt, {}, {}, ROOT), {'checked': True})
        validator.assert_called_once()

    def test_ordinary_selector_receipt_keeps_existing_dispatch(self):
        family = SimpleNamespace(selector_g1_adapter_view=lambda values: None, selector_g1_validate_receipt=mock.Mock(return_value={'ordinary': True}))
        with mock.patch.object(MAIN, 'selector_continuation_load', side_effect=AssertionError('continuation hijacked v2')), \
                mock.patch.object(MAIN, 'selector_g1_handles', return_value=True), mock.patch.object(MAIN, 'selector_g1_load_family', return_value=family):
            self.assertEqual(MAIN.validate_receipt({'replay_evidence': {'schema': 'orthemology-v5-replay-evidence-v2'}}, {}, {}, ROOT), {'ordinary': True})

    def test_cli_requires_prior_and_routes_only_explicit_selector_mode(self):
        bundle = {'suites': [{'id': 'd06-selector'}], 'sources': [], 'reviews': []}
        records = SimpleNamespace(load_bundle=lambda root: bundle)
        args = ['replay_v5_successors.py', '--selector-audit-continuation', '--suite', 'd06-selector', '--out', str(ROOT / 'NEVER_CREATED')]
        with mock.patch.dict(sys.modules, {'validate_v5_successors': records}), \
                mock.patch.object(MAIN, 'execute_selector_audit_continuation', return_value={'suite_id': 'd06-selector', 'outcome': 'FAILED', 'proof_scope': 'NONE', 'exit_code': 1}) as run, \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            with mock.patch.object(sys, 'argv', args): self.assertEqual(MAIN.main(), 1)
            run.assert_not_called()
            with mock.patch.object(sys, 'argv', args + ['--prior', str(ROOT / 'RETAINED')]): self.assertEqual(MAIN.main(), 1)
            run.assert_called_once()
            with mock.patch.object(sys, 'argv', args + ['--execute']), self.assertRaises(SystemExit): MAIN.main()
        self.assertFalse((ROOT / 'NEVER_CREATED').exists())


if __name__ == '__main__':
    if sys.version_info[:3] != (3, 11, 9) or not sys.dont_write_bytecode: raise ValueError('Pinned Python3.11.9 -B required')
    print(sys.version, 'optimized=' + str(sys.flags.optimize), flush=True)
    unittest.main(verbosity=2)

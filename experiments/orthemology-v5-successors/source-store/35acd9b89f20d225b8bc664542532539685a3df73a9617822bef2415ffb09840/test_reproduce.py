"""Offline fail-closed contract tests. No Lean process or network is started."""
import sys
sys.dont_write_bytecode = True
import importlib.util
import pathlib
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parents[1]


class HarnessContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = HERE / 'reproduce.py'
        if not path.is_file():
            cls.runner = None
            return
        spec = importlib.util.spec_from_file_location('joint_reproduce', path)
        cls.runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.runner)

    def runner_required(self):
        self.assertIsNotNone(self.runner, 'Missing bounded joint verification runner')
        return self.runner

    def test_readback_exact_type_and_allowed_axioms(self):
        r = self.runner_required()
        text = "CONTINUATION_BEGIN JointFinite.claim\nJointFinite.claim : True\n'JointFinite.claim' depends on axioms: [propext, Quot.sound]\nCONTINUATION_END JointFinite.claim\n"
        got = r.parse_readback(text, ['JointFinite.claim'], ['JointFinite.claim'])
        self.assertEqual(got['JointFinite.claim']['type'], 'JointFinite.claim : True')
        self.assertEqual(got['JointFinite.claim']['axioms'], ['Quot.sound', 'propext'])
        self.assertEqual(len(got['JointFinite.claim']['type_sha256']), 64)

    def test_readback_rejects_missing_axiom_audit(self):
        r = self.runner_required()
        with self.assertRaisesRegex(RuntimeError, 'axiom'):
            r.parse_readback('CONTINUATION_BEGIN JointFinite.claim\nJointFinite.claim : True\nCONTINUATION_END JointFinite.claim\n', ['JointFinite.claim'], ['JointFinite.claim'])

    def test_readback_rejects_custom_axiom(self):
        r = self.runner_required()
        with self.assertRaisesRegex(RuntimeError, 'Unexpected axiom'):
            r.parse_readback("CONTINUATION_BEGIN JointFinite.claim\nJointFinite.claim : True\n'JointFinite.claim' depends on axioms: [sorryAx]\nCONTINUATION_END JointFinite.claim\n", ['JointFinite.claim'], ['JointFinite.claim'])

    def test_readback_rejects_duplicate_or_out_of_order_markers(self):
        r = self.runner_required()
        with self.assertRaises(RuntimeError):
            r.parse_readback('CONTINUATION_BEGIN A\nA : Prop\nCONTINUATION_END A\nCONTINUATION_BEGIN A\nA : Prop\nCONTINUATION_END A\n', ['A'], [])

    def test_false_claims_require_exactly_four_semantic_failures(self):
        r = self.runner_required()
        diagnostic = "tests/RejectedClaims.lean:1:1: error: tactic 'decide' proved that the proposition\n False\nis false\n"
        self.assertEqual(len(r.validate_rejections(1, diagnostic * 4)), 4)
        for code, text in [(0, diagnostic * 4), (1, diagnostic * 3), (1, diagnostic * 4 + 'x:1:1: error: unknown identifier\n')]:
            with self.assertRaises(RuntimeError):
                r.validate_rejections(code, text)

    def test_source_binding_detects_mutation(self):
        r = self.runner_required()
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            source = root / 'Core.lean'
            source.write_text('import Init\n')
            entries = [{'path': 'Core.lean', 'sha256': r.sha(source), 'bytes': source.stat().st_size}]
            self.assertEqual(r.verify_bindings(root, entries)[0]['sha256'], entries[0]['sha256'])
            source.write_text('import Mathlib\n')
            with self.assertRaisesRegex(RuntimeError, 'binding'):
                r.verify_bindings(root, entries)

    def test_import_closure_rejects_ambiguous_object(self):
        r = self.runner_required()
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            one, two = root / 'one', root / 'two'
            one.mkdir(); two.mkdir()
            (one / 'Init.olean').write_bytes(b'one')
            (two / 'Init.olean').write_bytes(b'two')
            with self.assertRaisesRegex(RuntimeError, 'ambiguous'):
                r.bind_imports('KERNEL_IMPORT Init\n', [one, two], one)

    def test_proof_readback_requires_real_component_call(self):
        r = self.runner_required()
        body = 'theorem JointFinite.claim : True := Component.original\n'
        log = 'PROOF_BEGIN JointFinite.claim\n' + body + 'PROOF_END JointFinite.claim\n'
        result = r.parse_proofs(log, ['JointFinite.claim'], ['Component.original'])
        self.assertEqual(result['component_uses']['Component.original'], ['JointFinite.claim'])
        with self.assertRaisesRegex(RuntimeError, 'component call'):
            r.parse_proofs(log.replace('Component.original', 'Component.original_extra'), ['JointFinite.claim'], ['Component.original'])

    def test_definition_body_is_labeled_separately_from_theorem(self):
        r = self.runner_required()
        text = 'PROOF_BEGIN JointFinite.table\ndef JointFinite.table : Nat := 2\nPROOF_END JointFinite.table\n'
        got = r.parse_proofs(text, ['JointFinite.table'], [])
        self.assertEqual(got['proofs']['JointFinite.table'].get('declaration_kind'), 'def')

    def test_proof_mapping_rejects_call_in_wrong_theorem(self):
        r = self.runner_required()
        proofs = {'proofs': {'JointFinite.a': {'body': 'Component.call'},
                             'JointFinite.b': {'body': 'True.intro'}}}
        self.assertEqual(r.verify_proof_map(proofs, {'JointFinite.a': ['Component.call']}),
                         {'JointFinite.a': ['Component.call']})
        with self.assertRaisesRegex(RuntimeError, 'Required mapped component call'):
            r.verify_proof_map(proofs, {'JointFinite.b': ['Component.call']})

    def test_bound_cache_rejects_changed_object(self):
        r = self.runner_required()
        with tempfile.TemporaryDirectory() as temp:
            root = pathlib.Path(temp)
            cache = root / 'Init.olean'
            cache.write_bytes(b'bound object')
            bindings = [{'module': 'Init', 'object': str(cache), 'sha256': r.sha(cache), 'fresh_local': False}]
            self.assertEqual(r.verify_cached_objects(bindings)[0]['module'], 'Init')
            cache.write_bytes(b'changed object')
            with self.assertRaisesRegex(RuntimeError, 'Cached object binding'):
                r.verify_cached_objects(bindings)

    def test_admission_scan_ignores_comments_but_rejects_terms(self):
        r = self.runner_required()
        r.check_authored_source('/- no sorry, axiom, or native_decide is used -/\ntheorem good : True := by trivial')
        for source in ['theorem bad : True := by sorry', 'axiom bad : True', 'theorem bad : True := by native_decide']:
            with self.assertRaisesRegex(RuntimeError, 'Forbidden'):
                r.check_authored_source(source)

    def test_comment_stripping_handles_nested_comments(self):
        r = self.runner_required()
        self.assertEqual(r.direct_imports('/- outer /- import Bad -/ end -/\nimport Init\n-- import Wrong\n'), ['Init'])


if __name__ == '__main__':
    unittest.main(verbosity=2)

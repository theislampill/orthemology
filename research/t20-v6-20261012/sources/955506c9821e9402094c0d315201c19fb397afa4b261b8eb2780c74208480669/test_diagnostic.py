"""Adversarial concrete-syntax tests. No test asserts HasE from JSON."""
import copy
import json
import unittest
from pathlib import Path
import diagnostic as d

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT / 'source_ast.json').read_text())

class CertificateTests(unittest.TestCase):
    def certify(self, n, **kw):
        result = d.diagnose(n, **kw)
        self.assertEqual(result['status'], 'certified_conversion', result)
        cert = result['certificate']
        self.assertTrue(d.check_certificate(cert, expected_input=n))
        return cert

    def test_actual_source_numerals(self):
        for k, n in enumerate(SOURCE['numerals']):
            with self.subTest(k=k):
                self.assertEqual(self.certify(n, max_nodes=5000000)['count'], k)

    def test_packed_compound_atoms_preserved(self):
        n = ['atom', d.pack_closed(SOURCE['numerals'][3])]
        cert = self.certify(n)
        self.assertEqual(cert['input'], n)
        self.assertEqual(cert['count'], 3)

    def test_erased_omega_does_not_require_strong_normalization(self):
        n = ['app', ['app', ['atom', ['k']], SOURCE['numerals'][2]], ['atom', SOURCE['omega']]]
        self.assertEqual(self.certify(n)['count'], 2)

    def test_i_wrapped_nonliteral_numeral(self):
        n = ['app', ['atom', ['i']], SOURCE['numerals'][4]]
        self.assertEqual(self.certify(n)['count'], 4)

    def test_corrupt_path_endpoint_count_and_binding_rejected(self):
        original = self.certify(SOURCE['numerals'][1])
        for mutation in ['path', 'endpoint', 'count', 'input', 'steps', 'q_digest', 'invalid_direction']:
            cert = copy.deepcopy(original)
            if mutation == 'path': cert['right']['trace'][0] = 'R' * 100
            if mutation == 'endpoint': cert['right']['endpoint'] = ['var', 17]
            if mutation == 'count': cert['count'] += 1
            if mutation == 'input': cert['input'] = SOURCE['numerals'][2]
            if mutation == 'steps': cert['left']['steps'] += 1
            if mutation == 'q_digest': cert['original_q_sha256'] = '0' * 64
            if mutation == 'invalid_direction': cert['right']['trace'][0] = 'X'
            with self.subTest(mutation=mutation):
                self.assertFalse(d.check_certificate(cert, expected_input=SOURCE['numerals'][1]))

    def test_budget_exhaustion_is_inconclusive(self):
        r = d.diagnose(SOURCE['numerals'][2], max_rounds=0)
        self.assertEqual(r['status'], 'budget_exhausted')
        self.assertNotIn('certificate', r)
        self.assertEqual(d.diagnose(['atom', SOURCE['omega']], max_rounds=8)['status'], 'budget_exhausted')

    def test_reducible_development_fixed_point_is_not_accepted(self):
        # Complete-development equality alone must never certify an iteration.
        omega = d.interpret(['atom', SOURCE['omega']])
        self.assertIsNone(d.iteration_count(omega))
        self.assertFalse(d.is_normal(omega))

    def test_non_iteration_normal_endpoint_is_not_a_certificate(self):
        r = d.diagnose(['atom', ['zero']])
        self.assertEqual(r['status'], 'normal_non_iteration')
        self.assertNotIn('certificate', r)

    def test_constructor_whitelist_no_lean_injection_or_boolean_naturals(self):
        for n in [['atom', ['i); axiom injected : False']], ['var', True], ['var', -1], ['atom', ['var', 0]], ['app', ['atom', ['i']]], ['i']]:
            with self.subTest(n=n), self.assertRaises(ValueError):
                d.validate_poly(n)

    def test_source_size_budget_is_retained(self):
        self.assertEqual(d.diagnose(SOURCE['numerals'][6], max_nodes=200000)['status'], 'budget_exhausted')
        self.assertEqual(self.certify(SOURCE['numerals'][6], max_nodes=5000000)['count'], 6)

    def test_deep_valid_source_reports_resource_exhaustion(self):
        n = SOURCE['numerals'][0]
        for _ in range(1500): n = ['app', ['atom', ['i']], n]
        self.assertEqual(d.diagnose(n)['status'], 'budget_exhausted')

    def test_open_erased_variable_gets_conversion_only(self):
        n = ['app', ['app', ['atom', ['k']], SOURCE['numerals'][0]], ['var', 42]]
        cert = self.certify(n)
        output = d.lean_certificate(cert)
        self.assertIn('_conversion', output)
        self.assertNotIn('_source_instance', output)

    def test_checker_host_exhaustion_is_not_invalid_certificate(self):
        cert = self.certify(SOURCE['numerals'][0])
        deep = SOURCE['numerals'][0]
        for _ in range(1500): deep = ['app', ['atom', ['i']], deep]
        cert['input'] = deep
        with self.assertRaises(RecursionError): d.check_certificate(cert)

    def test_untrusted_count_does_not_allocate_iteration(self):
        cert = self.certify(SOURCE['numerals'][0])
        cert['count'] = 10 ** 18
        saved = d.iteration
        d.iteration = lambda *args: (_ for _ in ()).throw(AssertionError('untrusted count allocated'))
        try: self.assertFalse(d.check_certificate(cert))
        finally: d.iteration = saved

    def test_checker_does_not_call_producer(self):
        cert = self.certify(SOURCE['numerals'][2])
        saved = d.develop
        d.develop = lambda *a, **kw: (_ for _ in ()).throw(AssertionError('producer called'))
        try: self.assertTrue(d.check_certificate(cert, expected_input=cert['input']))
        finally: d.develop = saved

if __name__ == '__main__': unittest.main()

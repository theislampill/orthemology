"""Executable regressions, not substitutes for the written general proof."""
import copy
import importlib.util
import itertools
import random
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / 'certificate_checker.py'
SPEC = importlib.util.spec_from_file_location('certificate_checker', PATH)
if PATH.exists():
    C = importlib.util.module_from_spec(SPEC)
    SPEC.loader.exec_module(C)
else:
    C = None

c = lambda n: ['c', n]
x = lambda i: ['v', i]
a = lambda e, f: ['add', e, f]
m = lambda e, f: ['mul', e, f]
z = lambda t, e, f: ['if0', t, e, f]

class CertificateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(C, 'the fragment certificate checker has not been implemented')

    def test_distributive_positive_certificate(self):
        e = m(x(0), a(x(1), c(3)))
        f = a(m(x(0), x(1)), m(c(3), x(0)))
        cert = C.certify(2, e, f)
        self.assertTrue(C.verify_positive(cert))
        self.assertEqual(len(cert['normal_forms']), 4)
        self.assertIsNone(C.distinguish(2, e, f))

    def test_conditional_is_not_global_single_polynomial(self):
        e = z(x(0), c(7), x(0))
        self.assertEqual(C.normalise(1, e, (False,)), {(0,): 7})
        self.assertEqual(C.normalise(1, e, (True,)), {(1,): 1})
        self.assertFalse(C.equivalent(1, e, x(0)))
        self.assertEqual(C.distinguish(1, e, x(0)), (0,))

    def test_zero_test_of_nonnegative_polynomial(self):
        e = z(a(m(x(0), x(1)), x(2)), c(11), c(13))
        for v in itertools.product(range(4), repeat=3):
            mask = tuple(t != 0 for t in v)
            self.assertEqual(C.eval_poly(C.normalise(3, e, mask), v), C.evaluate(e, v))

    def test_zero_factors_nested_tests_and_identically_zero_test(self):
        e = z(m(x(0), c(0)), z(x(1), c(3), c(4)), c(999))
        f = z(x(1), c(3), c(4))
        self.assertTrue(C.verify_positive(C.certify(2, e, f)))
        self.assertEqual(C.normalise(2, e, (True, True)), {(0, 0): 4})

    def test_degree_plus_one_required(self):
        # X and X² agree at the only positive degree-one test value 1.
        e, f = x(0), m(x(0), x(0))
        self.assertEqual(C.evaluate(e, (1,)), C.evaluate(f, (1,)))
        self.assertEqual(C.distinguish(1, e, f), (2,))
        self.assertIn((3,), list(C.grid(1, C.normalise(1, e, (True,)),
                                         C.normalise(1, f, (True,)), (True,))))

    def test_arity_zero_singleton_mask_and_grid(self):
        e, f = z(c(0), c(8), c(9)), c(8)
        cert = C.certify(0, e, f)
        self.assertTrue(C.verify_positive(cert))
        self.assertEqual(len(cert['normal_forms']), 1)
        self.assertEqual(list(C.grid(0, {(): 8}, {(): 9}, ())), [()])
        self.assertEqual(C.distinguish(0, e, c(9)), ())
        self.assertTrue(C.equivalent(0, c(0), m(c(0), c(927))))

    def test_zero_map_and_empty_positive_coordinate_set(self):
        self.assertEqual(C.normalise(2, c(0), (False, False)), {})
        self.assertEqual(list(C.grid(2, {}, {}, (False, False))), [(0, 0)])

    def test_forged_coefficients_missing_masks_duplicates_and_payload(self):
        valid = C.certify(1, a(x(0), c(1)), a(c(1), x(0)))
        mutations = []
        q = copy.deepcopy(valid); q['normal_forms'][1]['left'][0][1] = 98; mutations.append(q)
        q = copy.deepcopy(valid); q['normal_forms'].pop(); mutations.append(q)
        q = copy.deepcopy(valid); q['normal_forms'][1] = q['normal_forms'][0]; mutations.append(q)
        q = copy.deepcopy(valid); q['right'] = c(43); mutations.append(q)
        q = copy.deepcopy(valid); q['normal_forms'][0]['left'].append([[0], 0]); mutations.append(q)
        q = copy.deepcopy(valid); q['normal_forms'][1]['left'].reverse(); mutations.append(q)
        q = copy.deepcopy(valid); q['trusted'] = True; mutations.append(q)
        for bad in mutations:
            self.assertFalse(C.verify_positive(bad))

    def test_rejects_out_of_fragment_and_malformed_input(self):
        for r, e in [(-1,c(1)), (True,c(1)), (0,x(0)), (1,x(1)),
                     (1,c(-1)), (1,c(True)), (1,['sub',c(1),c(2)]),
                     (1,['prec',c(1),c(2)]), (1,['add',c(1)]),
                     (1,['c',1,2]), (1, {'tag':'c','n':1})]:
            with self.assertRaises(ValueError): C.certify(r, e, c(0))
        for bad in [None, [], {}, {'version': 1}, {'version': True}]:
            self.assertFalse(C.verify_positive(bad))
        with self.assertRaises(ValueError): C.normalise(1, c(0), (0,))
        with self.assertRaises(ValueError): C.certify(1, c(0), c(1))

    def test_random_normalisation_and_separation(self):
        rng = random.Random(501031)
        def expression(r, depth):
            if depth == 0 or rng.randrange(4) == 0:
                return x(rng.randrange(r)) if r and rng.randrange(2) else c(rng.randrange(4))
            op = rng.randrange(3)
            if op == 0: return a(expression(r,depth-1), expression(r,depth-1))
            if op == 1: return m(expression(r,depth-1), expression(r,depth-1))
            return z(*(expression(r,depth-1) for _ in range(3)))
        for r in range(4):
            es = [expression(r,3) for _ in range(35)]
            for e in es:
                for v in itertools.product(range(4),repeat=r):
                    self.assertEqual(C.eval_poly(C.normalise(r,e,tuple(i>0 for i in v)),v), C.evaluate(e,v))
                self.assertTrue(C.verify_positive(C.certify(r,e,a(e,c(0)))))
            for e, f in zip(es, es[1:]):
                witness = C.distinguish(r,e,f)
                if witness is None:
                    self.assertTrue(C.verify_positive(C.certify(r,e,f)))
                    for v in itertools.product(range(5), repeat=r):
                        self.assertEqual(C.evaluate(e,v), C.evaluate(f,v))
                else:
                    self.assertNotEqual(C.evaluate(e,witness), C.evaluate(f,witness))

if __name__ == '__main__': unittest.main(verbosity=2)

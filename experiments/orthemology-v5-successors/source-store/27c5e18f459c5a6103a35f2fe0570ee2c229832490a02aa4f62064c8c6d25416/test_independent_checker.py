"""Independent adversarial checks of the frozen reference implementation.

These finite tests do not formalize the general algebraic theorem.
"""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import unittest

HERE = Path(__file__).resolve().parents[1]
CHECKER = HERE / 'certificate_checker.py'
SPEC = importlib.util.spec_from_file_location('reviewed_checker', CHECKER)
C = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(C)

def c(n): return ['c', n]
def x(i): return ['v', i]
def add(a, b): return ['add', a, b]
def mul(a, b): return ['mul', a, b]
def if0(t, a, b): return ['if0', t, a, b]

def direct(e, v):
    """Independent evaluator used as the witness/output oracle."""
    if e[0] == 'c': return e[1]
    if e[0] == 'v': return v[e[1]]
    if e[0] == 'add': return sum(direct(t, v) for t in e[1:])
    if e[0] == 'mul': return direct(e[1], v) * direct(e[2], v)
    assert e[0] == 'if0'
    return direct(e[2 if direct(e[1], v) == 0 else 3], v)

def expression_of_map(p):
    terms = []
    for alpha, coefficient in sorted(p.items()):
        if coefficient == 0: continue
        t = c(coefficient)
        for i, power in enumerate(alpha):
            for _ in range(power): t = mul(t, x(i))
        terms.append(t)
    result = c(0)
    for term in terms: result = add(result, term)
    return result

def signed_product_roots(bounds):
    """Integer coefficient oracle for product_i product_{j=1}^{d_i}(Xi-j)."""
    r = len(bounds)
    p = {(0,) * r: 1}
    for i, d in enumerate(bounds):
        for j in range(1, d + 1):
            q = {}
            for alpha, a in p.items():
                beta = list(alpha); beta[i] += 1; beta = tuple(beta)
                q[beta] = q.get(beta, 0) + a
                q[alpha] = q.get(alpha, 0) - j * a
            p = {alpha: a for alpha, a in q.items() if a}
    return p

def split_signed(p):
    return (expression_of_map({a: v for a, v in p.items() if v > 0}),
            expression_of_map({a: -v for a, v in p.items() if v < 0}))

def zero_unless_all_live(e, bounds):
    for i in reversed(range(len(bounds))):
        if bounds[i] > 0: e = if0(x(i), c(0), e)
    return e

def verifies_negative(r, e, f, witness):
    return (type(witness) in (tuple, list) and len(witness) == r
            and all(type(n) is int and n >= 0 for n in witness)
            and direct(e, witness) != direct(f, witness))

class IndependentCheckerTests(unittest.TestCase):
    def test_zero_sparse_maps_and_combined_monomials(self):
        cases = [(c(0), {}), (mul(x(0), c(0)), {}),
                 (add(mul(c(0), x(1)), mul(c(0), x(0))), {}),
                 (add(mul(x(0), x(1)), mul(x(1), x(0))), {(1, 1): 2})]
        for e, expected in cases:
            self.assertEqual(C.normalise(2, e, [True, True]), expected)
        e = if0(add(mul(c(0), x(0)), mul(x(0), x(1))), c(7), c(9))
        for s in itertools.product([False, True], repeat=2):
            self.assertEqual(C.normalise(2, e, s), {(0, 0): 9 if all(s) else 7})

    def test_sparse_term_duplicate_exponent_and_coefficient_forgery(self):
        cert = C.certify(2, add(c(1), add(x(0), mul(x(1), x(1)))),
                           add(c(1), add(x(0), mul(x(1), x(1)))))
        mutations = []
        def mutate(fn):
            q = copy.deepcopy(cert); fn(q); mutations.append(q)
        for side in ['left', 'right']:
            def entries(q): return q['normal_forms'][-1][side]
            mutate(lambda q: entries(q).append([[0, 0], 0]))
            mutate(lambda q: entries(q).append(copy.deepcopy(entries(q)[0])))
            mutate(lambda q: entries(q).reverse())
            mutate(lambda q: entries(q).__setitem__(0, [[0, 0], -1]))
            mutate(lambda q: entries(q).__setitem__(0, [[0, 0], 0]))
            for bad in [True, False, 1.0, '1', None, [], {}]:
                mutate(lambda q, bad=bad: entries(q)[0].__setitem__(1, bad))
            for alpha in [[], [0], [0, 0, 0], [-1, 0], [True, 0], [0.0, 0], ['0', 0]]:
                mutate(lambda q, alpha=alpha: entries(q)[0].__setitem__(0, alpha))
            # A dead-coordinate positive exponent is forbidden even if evaluating
            # the supplied map at the dead coordinate would erase its term.
            mutate(lambda q: q['normal_forms'][0][side].append([[3, 0], 17]))
        for q in mutations: self.assertFalse(C.verify_positive(q))
        self.assertEqual(len(mutations), 40)

    def test_exact_schema_masks_and_scalar_types(self):
        cert = C.certify(2, c(0), c(0))
        variants = []
        def mutate(fn):
            q = copy.deepcopy(cert); fn(q); variants.append(q)
        for k in list(cert): mutate(lambda q, k=k: q.pop(k))
        for val in [True, False, 1.0, 0, 2, '1', None]:
            mutate(lambda q, val=val: q.__setitem__('version', val))
        for val in [True, False, 2.0, -1, '2', None]:
            mutate(lambda q, val=val: q.__setitem__('arity', val))
        mutate(lambda q: q.__setitem__('extra', True))
        mutate(lambda q: q['normal_forms'].reverse())
        mutate(lambda q: q['normal_forms'].pop())
        mutate(lambda q: q['normal_forms'].append(q['normal_forms'][0]))
        mutate(lambda q: q['normal_forms'].__setitem__(1, q['normal_forms'][0]))
        for mask in [[], [True], [True, True, True], [0, 0], [False, 0], [None, False], '00']:
            mutate(lambda q, mask=mask: q['normal_forms'][0].__setitem__('mask', mask))
        mutate(lambda q: q['normal_forms'][0].__setitem__('degree', 999))
        mutate(lambda q: q['normal_forms'][0].__setitem__('left', None))
        mutate(lambda q: q['normal_forms'][0].__setitem__('right', {}))
        for q in variants: self.assertFalse(C.verify_positive(q))
        self.assertTrue(C.verify_positive(json.loads(json.dumps(cert))))

    def test_malformed_unselected_branch_is_rejected(self):
        for bad in [[], ['unknown'], ['c', -1], ['c', True], ['c', 1.0],
                    ['v', 2], ['v', -1], ['mul', c(1)], {'tag': 'c'},
                    ['sub', c(1), c(2)], ['if0', c(1), c(2)]]:
            for e in [if0(c(0), c(3), bad), if0(c(1), bad, c(3))]:
                with self.assertRaises(ValueError): C.certify(2, e, c(3))

    def test_sharp_univariate_degree_plus_one(self):
        for d in range(1, 8):
            e, f = split_signed(signed_product_roots([d]))
            e, f = if0(x(0), c(0), e), if0(x(0), c(0), f)
            for n in range(d + 1): self.assertEqual(direct(e, [n]), direct(f, [n]))
            self.assertEqual(C.distinguish(1, e, f), (d + 1,))
            self.assertEqual(list(C.grid(1, C.normalise(1, e, [True]),
                                         C.normalise(1, f, [True]), [True])),
                             [(i,) for i in range(1, d + 2)])

    def test_sharp_multivariate_degree_and_absent_variable(self):
        bounds = [2, 0, 3]
        e, f = split_signed(signed_product_roots(bounds))
        e, f = zero_unless_all_live(e, bounds), zero_unless_all_live(f, bounds)
        p, q = C.normalise(3, e, [True] * 3), C.normalise(3, f, [True] * 3)
        points = list(C.grid(3, p, q, [True] * 3))
        self.assertEqual(len(points), 3 * 1 * 4)
        separating = [v for v in points if direct(e, v) != direct(f, v)]
        self.assertEqual(separating, [(3, 1, 4)])
        self.assertEqual(C.distinguish(3, e, f), (3, 0, 4))
        self.assertTrue(verifies_negative(3, e, f, (3, 0, 4)))

    def test_zero_and_degree_zero_coordinates(self):
        for r in range(5):
            for mask in itertools.product([False, True], repeat=r):
                self.assertEqual(list(C.grid(r, {}, {}, mask)), [tuple(map(int, mask))])
                self.assertEqual(C.normalise(r, c(0), mask), {})
                self.assertEqual(C.normalise(r, c(27), mask), {(0,) * r: 27})
            self.assertEqual(C.distinguish(r, c(27), c(28)), (0,) * r)
        e, f = if0(x(0), c(0), c(1)), c(0)
        self.assertEqual(C.distinguish(1, e, f), (1,))

    def test_arbitrary_mask_table_reification(self):
        rng = random.Random(962344)
        for r in range(4):
            table = {}
            for mask in itertools.product([False, True], repeat=r):
                p = {}
                for _ in range(4):
                    alpha = tuple(rng.randrange(3) if live else 0 for live in mask)
                    coefficient = rng.randrange(5)
                    if coefficient: p[alpha] = p.get(alpha, 0) + coefficient
                table[mask] = p
            def tree(prefix):
                if len(prefix) == r: return expression_of_map(table[prefix])
                return if0(x(len(prefix)), tree(prefix + (False,)), tree(prefix + (True,)))
            e = tree(())
            for mask, expected in table.items():
                self.assertEqual(C.normalise(r, e, mask), expected)
            self.assertTrue(C.verify_positive(C.certify(r, e, add(c(0), e))))

    def test_independent_random_direct_evaluation(self):
        rng = random.Random(91834721)
        def gen(r, depth):
            if not depth or rng.randrange(5) == 0:
                return x(rng.randrange(r)) if r and rng.randrange(2) else c(rng.randrange(5))
            tag = rng.randrange(3)
            if tag == 0: return add(gen(r, depth-1), gen(r, depth-1))
            if tag == 1: return mul(gen(r, depth-1), gen(r, depth-1))
            return if0(gen(r, depth-1), gen(r, depth-1), gen(r, depth-1))
        checks = 0
        for r in range(4):
            es = [gen(r, 4) for _ in range(60)]
            for e in es:
                for v in itertools.product(range(4), repeat=r):
                    p = C.normalise(r, e, tuple(n > 0 for n in v))
                    self.assertEqual(C.eval_poly(p, v), direct(e, v)); checks += 1
                    self.assertTrue(all(n > 0 for n in p.values()))
                    self.assertTrue(all(len(a) == r for a in p))
                self.assertTrue(C.verify_positive(C.certify(r, e, add(e, c(0)))))
            for e, f in zip(es, es[1:]):
                w = C.distinguish(r, e, f)
                if w is None: self.assertTrue(C.verify_positive(C.certify(r, e, f)))
                else:
                    self.assertTrue(verifies_negative(r, e, f, w))
                    with self.assertRaises(ValueError): C.certify(r, e, f)
        self.assertEqual(checks, 5100)

    def test_negative_witness_validation_edges(self):
        self.assertTrue(verifies_negative(0, c(1), c(2), ()))
        self.assertFalse(verifies_negative(0, c(1), c(1), ()))
        for w in [None, False, 0, [False], [1.0], [-1], [1, 2], []]:
            self.assertFalse(verifies_negative(1, c(1), c(2), w))
        self.assertTrue(verifies_negative(1, c(1), c(2), [0]))

    def test_external_claim_binding_is_separate(self):
        cert = C.certify(1, x(0), x(0))
        self.assertTrue(C.verify_positive(cert))
        external_right = add(x(0), c(1))
        self.assertNotEqual(cert['right'], external_right)
        forged = copy.deepcopy(cert); forged['right'] = external_right
        self.assertFalse(C.verify_positive(forged))

    def test_cli_empty_witness_is_not_equal(self):
        for r, e, f, expected in [(0, c(1), c(1), {'equal': True, 'counterexample': None}),
                                  (0, c(1), c(2), {'equal': False, 'counterexample': []}),
                                  (1, x(0), mul(x(0), x(0)), {'equal': False, 'counterexample': [2]})]:
            proc = subprocess.run([sys.executable, str(CHECKER), 'decide'],
                                  input=json.dumps({'arity': r, 'left': e, 'right': f}),
                                  text=True, capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout), expected)
        cert = C.certify(0, c(0), c(0)); cert['normal_forms'][0]['left'] = [[[], 0]]
        proc = subprocess.run([sys.executable, str(CHECKER), 'verify'], input=json.dumps(cert),
                              text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {'accepted': False})

if __name__ == '__main__': unittest.main(verbosity=2)

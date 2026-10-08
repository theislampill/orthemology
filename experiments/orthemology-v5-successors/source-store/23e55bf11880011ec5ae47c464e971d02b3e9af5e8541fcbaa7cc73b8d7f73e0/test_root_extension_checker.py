import itertools
import random
import unittest
import root_extension_checker as checker

c = lambda n: ['c',n]
x = ['v',0]
old = lambda e: ['old',e]
test = lambda p,q: ['test',p,q]

def polynomial(coeff):
    result = c(0)
    for value in reversed(coeff):
        result = ['add',c(value),['mul',x,result]]
    return result

class ReferenceTests(unittest.TestCase):
    def test_constants_and_zero_polynomial(self):
        self.assertEqual(checker.root_bound({}),1)
        self.assertEqual(checker.root_bound({100:0,0:-3}),1)
        self.assertTrue(checker.equivalent(test(c(7),c(7)),old(c(1))))
        self.assertTrue(checker.equivalent(test(c(7),c(8)),old(c(0))))

    def test_zero_only_root(self):
        self.assertTrue(checker.equivalent(test(x,c(0)),old(['if0',x,c(1),c(0)])))
        self.assertEqual(checker.distinguish(test(x,c(0)),old(c(0))),0)

    def test_root_at_large_input(self):
        s,t = test(x,c(173)),old(c(0))
        self.assertFalse(checker.equivalent(s,t))
        self.assertEqual(checker.distinguish(s,t),173)
        self.assertEqual(checker.comparison_bound(s,t),174)

    def test_multiple_roots(self):
        # x^2 + 6 = 5*x at exactly 2 and 3 over naturals.
        s = test(['add',['mul',x,x],c(6)],['mul',c(5),x])
        self.assertEqual([n for n in range(20) if checker.evaluate(s,n)], [2,3])
        self.assertFalse(checker.equivalent(s,old(c(0))))

    def test_nonzero_tail_witness(self):
        s,t = old(x),test(x,x)
        n = checker.distinguish(s,t)
        self.assertEqual(n,checker.comparison_bound(s,t))
        self.assertNotEqual(checker.evaluate(s,n),checker.evaluate(t,n))

    def test_all_small_integer_polynomial_bounds(self):
        for coeff in itertools.product(range(-3,4),repeat=4):
            p = {k:a for k,a in enumerate(coeff) if a}
            if not p: continue
            bound = checker.root_bound(p)
            for n in range(bound,bound+12):
                self.assertNotEqual(sum(a*n**k for k,a in p.items()),0)

    def test_generated_full_finite_criterion(self):
        rng = random.Random(150510)
        for _ in range(240):
            p,q,r = [polynomial([rng.randrange(4) for _ in range(4)]) for _ in range(3)]
            expressions = [test(p,q),old(p),old(['if0',x,q,r]),test(p,p),old(c(0))]
            s,t = rng.sample(expressions,2)
            m = checker.comparison_bound(s,t)
            bounded = all(checker.evaluate(s,n)==checker.evaluate(t,n) for n in range(m+1))
            self.assertEqual(checker.equivalent(s,t),bounded)
            w = checker.distinguish(s,t)
            if w is not None:
                self.assertLessEqual(w,m)
                self.assertNotEqual(checker.evaluate(s,w),checker.evaluate(t,w))
            # Check substantially beyond the selected boundary as a control,
            # without mislabelling these finitely many tests as the proof.
            if bounded:
                for n in [m+1,m+37,2*m+100,1000]:
                    self.assertEqual(checker.evaluate(s,n),checker.evaluate(t,n))

    def test_reject_grammar_expansion(self):
        bad = [test(['if0',x,c(1),c(0)],x),['test',x,x,c(0)],
               ['old',['test',x,x]],test(['v',1],x),test(c(True),x),test(c(-1),x)]
        for s in bad:
            with self.assertRaises(ValueError): checker.tail(s)
        for n in [-1,True,0.5]:
            with self.assertRaises(ValueError): checker.evaluate(old(x),n)

if __name__ == '__main__': unittest.main()

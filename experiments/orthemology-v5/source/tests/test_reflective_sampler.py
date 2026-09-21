"""Exact arithmetic checks for the productive irrational fixed-point sampler."""
import unittest
import extensions as e

class SamplerImplementationGate(unittest.TestCase):
    def test_prefix_sampler_implemented(self):
        self.assertTrue(hasattr(e, 'irrational_selector_prefix'),
                        'productive irrational-response sampler has not been implemented')

from fractions import Fraction as F
from itertools import product
import reference as r

class IrrationalReflectiveSampler(unittest.TestCase):
    def test_all_prefixes_through_twelve_bits(self):
        for n in range(13):
            counts={0:0,1:0,None:0}
            for bits in product((0,1),repeat=n):
                counts[e.irrational_selector_prefix(bits)]+=1
            mass=e.irrational_prefix_mass(n)
            self.assertEqual(F(counts[0],1<<n),mass['first'])
            self.assertEqual(F(counts[1],1<<n),mass['second'])
            self.assertEqual(F(counts[None],1<<n),mass['unresolved'])
            self.assertEqual(counts[None],1)
    def test_probability_mass_and_nested_bounds(self):
        lo,hi=F(0),F(1)
        for n in range(513):
            m=e.irrational_prefix_mass(n)
            self.assertEqual(m['first']+m['second']+m['unresolved'],1)
            self.assertGreaterEqual(m['first'],lo)
            self.assertLessEqual(m['first']+m['unresolved'],hi)
            lo,hi=m['first'],m['first']+m['unresolved']
            self.assertGreater(e.quadratic_response(lo),lo)
            self.assertLess(e.quadratic_response(hi),hi)
    def test_no_finite_rational_fixed_point_in_declared_census(self):
        for den in range(1,101):
            for num in range(den+1):
                p=F(num,den)
                self.assertNotEqual(e.quadratic_response(p),p)
    def test_prefix_tail_expected_cost_identity(self):
        for n in (0,1,2,10,100,512):
            self.assertEqual(sum((e.irrational_prefix_mass(k)['unresolved'] for k in range(n)),F()),
                             2-F(2,1<<n))
    def test_sampler_rejects_nonbits(self):
        for bad in ([True],[2],[-1],[F(0)],'01',None):
            with self.assertRaises(r.Rejection): e.irrational_selector_prefix(bad)
    def test_settled_prefix_remains_settled(self):
        for n in range(7):
            for prefix in product((0,1),repeat=n):
                v=e.irrational_selector_prefix(prefix)
                if v is not None:
                    for tail in product((0,1),repeat=4):
                        self.assertEqual(e.irrational_selector_prefix(prefix+tail),v)

    def test_rational_iteration_certified_error_bounds(self):
        cert=e.irrational_prefix_mass(512)
        lo,hi=cert['first'],cert['first']+cert['unresolved']
        for initial in (F(0),F(1),F(1,3),F(3,4)):
            q=initial
            for n in range(1,13):
                q=e.quadratic_response(q)
                self.assertGreaterEqual(q,0);self.assertLessEqual(q,F(1,2))
                self.assertLessEqual(max(abs(q-lo),abs(q-hi)),F(1,1<<n))
        for p in (F(i,32) for i in range(17)):
            for q in (F(i,32) for i in range(17)):
                self.assertLessEqual(abs(e.quadratic_response(p)-e.quadratic_response(q)),abs(p-q)/2)

if __name__=="__main__":unittest.main()

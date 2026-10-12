import unittest
from fractions import Fraction as F
from accuracy_checks import brier, project_complements, uniform_coherent_repair, convex_regret


class AccuracyChecks(unittest.TestCase):
    def test_projection_depends_on_weight_but_target_remains_coherent(self):
        b=(F(7,10),F(3,5))
        for a,expected in [(F(1,4),(F(19,40),F(21,40))),
                           (F(1,2),(F(11,20),F(9,20))),
                           (F(3,4),(F(5,8),F(3,8)))]:
            self.assertEqual(project_complements(b,a),expected)

    def test_projection_has_the_claimed_uniform_gain(self):
        b=(F(7,10),F(3,5)); a=F(1,4); c=project_complements(b,a)
        self.assertIsNotNone(c)
        expected=a*(1-a)*(sum(b)-1)**2
        for v in [(1,0),(0,1)]:self.assertEqual(brier(b,v,a)-brier(c,v,a),expected)
        self.assertGreater(expected,0)

    def test_wide_interval_has_no_common_weak_repair(self):
        r=uniform_coherent_repair((F(7,10),F(3,5)),F(1,4),F(3,4),strict=False)
        self.assertEqual(r,{'exists':False,'m_true':F(63,400),'m_false':F(97,400)})

    def test_narrow_interval_has_a_strict_repair(self):
        b=(F(7,10),F(3,5));c=(F(11,20),F(9,20))
        r=uniform_coherent_repair(b,F(9,20),F(11,20)); self.assertIsInstance(r,dict)
        self.assertTrue(r['exists'])
        self.assertEqual(min(brier(b,v,a)-brier(c,v,a)
                             for a in [F(9,20),F(11,20)] for v in [(1,0),(0,1)]),F(3,500))

    def test_known_coherent_base_has_no_strict_repair(self):
        b=(F(7,10),F(3,10))
        r=uniform_coherent_repair(b,F(1,4),F(3,4)); self.assertIsInstance(r,dict)
        self.assertFalse(r['exists'])
        self.assertTrue(uniform_coherent_repair(b,F(1,4),F(3,4),strict=False)['exists'])

    def test_strictly_proper_generators_reverse_imperfect_report_ranking(self):
        p=F(1,10);a=F(1,100);b=F(1,5)
        self.assertEqual(convex_regret(p,a,'quadratic'),F(81,10000))
        self.assertEqual(convex_regret(p,b,'quadratic'),F(1,100))
        self.assertEqual(convex_regret(p,a,'complement_quartic'),F(4481163,100000000))
        self.assertEqual(convex_regret(p,b,'complement_quartic'),F(417,10000))
        self.assertLess(convex_regret(p,a,'quadratic'),convex_regret(p,b,'quadratic'))
        self.assertGreater(convex_regret(p,a,'complement_quartic'),convex_regret(p,b,'complement_quartic'))


    def test_reversal_survives_outcome_symmetry(self):
        p=F(1,10);a=F(1,100);b=F(1,5)
        try:
            values=[convex_regret(p,q,g) for g in ['symmetric_quadratic','symmetric_quartic'] for q in [a,b]]
        except ValueError:
            values=None
        self.assertEqual(values,[F(81,5000),F(1,50),F(2245563,50000000),F(217,5000)])
        self.assertLess(values[0],values[1]);self.assertGreater(values[2],values[3])


if __name__=='__main__':unittest.main()

import unittest
from fractions import Fraction as Q
from itertools import product
from oracle_boundaries import *

class OracleBoundaryTests(unittest.TestCase):
    def test_one_finite_cauchy_prefix_fits_distinct_nonempty_models(self):
        baseline={1:1};alternative={1:1,1<<8:1}
        observations=[Approximation(profile,positive_prediction(baseline,profile),Q(1,1<<k))
                      for profile,k in ((None,5),(1,8),(3,12),(None,20))]
        self.assertNotEqual(probability(baseline),probability(alternative))
        for model in (baseline,alternative):
            self.assertTrue(all(abs(positive_prediction(model,o.profile)-o.center)<=o.error for o in observations))

    def test_effective_positive_enumerator_learning_prefix_stabilizes_in_controls(self):
        for model in ({},{1:1},{4:1},{1:1,2:1}):
            outputs=positive_learning_prefix(lambda precision:approximate(probability(model),precision,(-1)**precision),24)
            self.assertTrue(all(x==model for x in outputs[-8:]))

    def test_guarded_dovetail_learning_has_correct_provisional_limit_controls(self):
        for model in ({(1,2):1},{(1,4):1},{(1,0):1,(2,1):1}):
            outputs=guarded_learning_prefix(lambda profile,precision:approximate(guarded_prediction(model,profile),precision,(-1)**(profile+precision)),40)
            self.assertTrue(all(x==model for x in outputs[-8:]))

    def test_exact_full_readout_gives_candidate_dependent_second_query_gap(self):
        q=probability({1:2});info=inside_value_gap(q,max_inside_count=10)
        self.assertEqual(info['count_bound'],2)
        self.assertEqual(info['gap'],Q(3,16))
        # Any valid second-query enclosure with upper endpoint below q+gap
        # forces equality, conditional on the derived discrete inside class.
        upper=q+info['gap']/2
        self.assertEqual([v for v in info['values'] if v<=upper],[q])
        with self.assertRaises(ResourceInconclusive):inside_value_gap(probability({1:1,2:1}),max_inside_count=2)

    def test_finite_histogram_sum_maps_to_probability_multiplication(self):
        a={1:2,3:1};b={2:1,3:2};combined=dict(a)
        for e,n in b.items():combined[e]=combined.get(e,0)+n
        self.assertEqual(probability(combined),probability(a)*probability(b))

    def test_fixed_calibration_mixture_has_exact_count_collision(self):
        one=probability({1:1});empty=probability({});two=probability({1:2})
        self.assertEqual(one,Q(3,7)*empty+Q(4,7)*two)

    def test_stochastic_mixture_collision_survives_all_profile_rate_controls(self):
        left=({1:1},{2:1});right=({1:1,2:1},{3:1})
        for profile,x,y in product(range(4),(Q(0),Q(1,4),Q(1,2),Q(1)),(Q(0),Q(1,3),Q(2,3),Q(1))):
            l=sum(one_effect_absence(m,profile,(x,y)) for m in left)/2
            r=sum(one_effect_absence(m,profile,(x,y)) for m in right)/2
            self.assertEqual(l,r)

    def test_grouped_repeats_separate_the_specific_mixture_pair(self):
        left=({1:1},{2:1});right=({1:1,2:1},{3:1})
        for x,y in product((Q(1,4),Q(1,2),Q(3,4)),repeat=2):
            l=[one_effect_absence(m,3,(x,y)) for m in left]
            r=[one_effect_absence(m,3,(x,y)) for m in right]
            first_l=sum(l)/2;first_r=sum(r)/2
            second_l=sum(q*q for q in l)/2;second_r=sum(q*q for q in r)/2
            self.assertEqual(first_l,first_r)
            self.assertEqual(second_r-second_l,x*y*(1-x)*(1-y))
            self.assertGreater(second_r,second_l)
            # Independently redrawing inventory between repeats restores collapse.
            self.assertEqual(first_l*first_l,first_r*first_r)
        x=y=Q(1,2)
        self.assertEqual(sum(one_effect_absence(m,3,(x,y))**2 for m in left)/2,Q(1,4))
        self.assertEqual(sum(one_effect_absence(m,3,(x,y))**2 for m in right)/2,Q(5,16))

if __name__=='__main__':unittest.main(verbosity=2)

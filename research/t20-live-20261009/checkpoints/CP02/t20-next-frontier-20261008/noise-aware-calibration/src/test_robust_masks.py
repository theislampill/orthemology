import unittest,random
from decimal import Decimal,localcontext
from itertools import product
from robust_masks import *


def perturb(panel,amount):
    return {key:min(Q(1),max(Q(0),q+amount*(1 if sum(key)%2 else -1))) for key,q in panel.items()}


def random_model(r,m,K,rng):
    roots=(1<<r)-1;effects=(1<<m)-1
    kinds=[(p,n,t) for p in subsets(roots,True) for n in subsets(roots^p) for t in subsets(effects,True)]
    answer={}
    for _ in range(K):
        key=rng.choice(kinds);answer[key]=answer.get(key,0)+1
    return answer

class RobustMaskTests(unittest.TestCase):
    def test_rational_log_intervals_contain_independent_high_precision_logs(self):
        with localcontext() as context:
            context.prec=100
            for q in (Q(1,4),Q(1,2),Q(99,100),Q(1),Q(2),Q(4000,3)):
                interval=general_log_interval(q,24)
                value=(Decimal(q.numerator)/Decimal(q.denominator)).ln()
                self.assertLessEqual(Decimal(interval.lo.numerator)/Decimal(interval.lo.denominator),value)
                self.assertGreaterEqual(Decimal(interval.hi.numerator)/Decimal(interval.hi.denominator),value)

    def test_proved_precision_target_is_finite_and_avoids_zero_denominators(self):
        for r,K in product(range(1,5),(1,2,5,10,100)):
            p,_=parameters(r,K);N=required_terms(r,K)
            self.assertLessEqual(uniform_log_tail(N),p**(2*r)/Q(64*2**r))
            for degree in range(1,r+1):self.assertLess(log_interval(1-p**degree,N).hi,0)

    def test_nonsaturation_floor_for_guarded_multi_effect_models(self):
        rng=random.Random(192)
        for r,m,K in ((1,1,1),(2,2,4),(3,2,5)):
            for _ in range(8):
                model=random_model(r,m,K,rng);panel=exact_panel(model,r,m,K)
                self.assertTrue(all(Q(1,2)<=q<=1 for q in panel.values()))

    def test_positive_support_recovery_under_all_two_root_error_corners(self):
        for K in (1,2,3):
            p,epsilon=parameters(2,K)
            for counts in product(range(K+1),repeat=3):
                if sum(counts)>K:continue
                model={(s,0,1):n for s,n in zip((1,2,3),counts) if n}
                ideal={t:absence_probability(model,3,t,1,2,K) for t in (1,2,3)}
                for signs in product((-1,1),repeat=3):
                    estimates={t:min(Q(1),ideal[t]+epsilon*sign) for t,sign in zip((1,2,3),signs)}
                    recovered,certificate=certify_support_counts(estimates,2,K)
                    self.assertEqual(recovered,{s:n for s,n in zip((1,2,3),counts) if n})
                    for s,interval in certificate['intervals'].items():
                        self.assertGreater(interval.lo,counts[s-1]-Q(1,2));self.assertLess(interval.hi,counts[s-1]+Q(1,2))

    def test_noisy_guarded_effect_recovery_rounds_before_exact_inversions(self):
        rng=random.Random(525)
        for r,m,K in ((1,2,2),(2,2,4),(3,1,5)):
            _,epsilon=parameters(r,K)
            for _ in range(6):
                model=random_model(r,m,K,rng)
                estimates=perturb(exact_panel(model,r,m,K),epsilon)
                recovered,certificates=certify_guarded_effect_histogram(estimates,r,m,K)
                self.assertEqual(recovered,model)

    def test_current_joint_redundant_and_priority_fixtures_recover(self):
        fixtures=[{(3,0,1):1,(1,2,1):1,(2,1,1):1},
                  {(1,0,1):1,(2,0,1):1},
                  {(1,0,1):1,(2,1,1):1}]
        for model in fixtures:
            bound=sum(model.values());_,epsilon=parameters(2,bound)
            data=perturb(exact_panel(model,2,1,bound),epsilon)
            self.assertEqual(certify_guarded_effect_histogram(data,2,1,bound)[0],model)

    def test_sampling_budget_is_ceil_certified_and_has_polynomial_K_coefficient(self):
        for r,K in product((1,2,3),(1,2,4)):
            L=3**r-2**r;delta=Q(1,20);p,epsilon=parameters(r,K)
            budget=sample_budget(r,K,L,delta)
            self.assertEqual(1/(2*epsilon**2),128*(16*K*K)**r)
            self.assertGreaterEqual(2*epsilon**2*budget['per_setting_trials'],budget['log_upper'])
            robust=sample_budget(r,K,L,delta,True)
            self.assertEqual(robust['sampling_tolerance'],epsilon/2)
            self.assertEqual(robust['per_incidence_calibration_tolerance']*K*r,epsilon/2)

    def test_calibration_bias_and_sampling_error_fit_one_budget(self):
        rng=random.Random(339)
        for r,m,K in ((1,1,2),(2,2,4),(3,1,5)):
            p,epsilon=parameters(r,K);eta=epsilon/Q(2*K*r)
            for _ in range(5):
                model=random_model(r,m,K,rng)
                ideal=exact_panel(model,r,m,K)
                actual=exact_panel(model,r,m,K,eta)
                self.assertTrue(all(abs(actual[key]-ideal[key])<=K*r*eta for key in ideal))
                estimates=perturb(actual,epsilon/2)
                self.assertTrue(all(abs(estimates[key]-ideal[key])<=epsilon for key in ideal))
                self.assertEqual(certify_guarded_effect_histogram(estimates,r,m,K)[0],model)

    def test_marginal_calibration_does_not_bound_unknown_gate_correlation(self):
        p=Q(1,4)
        independent={0:(1-p)**2,1:p*(1-p),2:p*(1-p),3:p*p}
        correlated={0:1-p,1:Q(0),2:Q(0),3:p}
        tv=sum(abs(independent[s]-correlated[s]) for s in range(4))/2
        endpoint_bias=abs(independent[0]-correlated[0])
        self.assertEqual(endpoint_bias,p*(1-p));self.assertGreater(endpoint_bias,0)
        self.assertLessEqual(endpoint_bias,tv)
        for bit in (1,2):
            self.assertEqual(sum(v for s,v in independent.items() if s&bit),p)
            self.assertEqual(sum(v for s,v in correlated.items() if s&bit),p)

    def test_outside_good_region_or_insufficient_arithmetic_budget_abstains(self):
        with self.assertRaises(UncertifiedArithmetic):certify_support_counts({1:Q(0)},1,1)
        with self.assertRaises(UncertifiedArithmetic):certify_support_counts({1:Q(1,2)},1,1,max_terms=1)
        with self.assertRaises(UncertifiedArithmetic):Interval(Q(1),Q(2)).divide(Interval(Q(-1),Q(1)))
        with self.assertRaises(ValueError):validate_model({(1,0,1):2},1,1,1)

    def test_certified_arithmetic_rejects_inexact_float_inputs(self):
        with self.assertRaises(TypeError):log_interval(0.5,8)
        with self.assertRaises(TypeError):general_log_interval(1.5)
        with self.assertRaises(TypeError):Interval(0.1,0.2)
        with self.assertRaises(TypeError):certify_support_counts({1:0.5},1,1)
        with self.assertRaises(TypeError):sample_budget(1,2,1,0.05)
        with self.assertRaises(ValueError):sample_budget(1,2,1.5,Q(1,20))
        self.assertEqual(log_interval(1,8),Interval(Q(0),Q(0)))

if __name__=='__main__':unittest.main(verbosity=2)

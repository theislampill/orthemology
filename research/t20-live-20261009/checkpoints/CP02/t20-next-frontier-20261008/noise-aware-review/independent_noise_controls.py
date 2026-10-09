"""Independent finite exact interval controls for the K-aware mask theorem.

No floating-point logarithms or empirical-frequency prime factorisation.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json
import random
import unittest

HERE = Path(__file__).resolve().parent
METRICS = {}


def submasks(mask):
    return tuple(t for t in range(mask+1) if t&mask==t)


def panel(counts,roots,bound):
    p = F(1,2*bound)
    answer = {0:F(1)}
    for mask in range(1,1<<roots):
        value = F(1)
        for support,count in counts.items():
            if support&mask==support:
                value *= (1-p**support.bit_count())**count
        answer[mask] = value
    return answer


def log_interval(value,width):
    assert 0<value<=1 and width>0
    if value==1:
        return F(0),F(0),0
    z=(value-1)/(value+1)
    power=z
    partial=F(0)
    n=0
    while True:
        partial += 2*power/(2*n+1)
        n+=1
        power *= z*z
        tail = 2*abs(power)/((2*n+1)*(1-z*z))
        if tail<=width:
            return partial-tail,partial,n


def invert_intervals(observed,roots,bound):
    p=F(1,2*bound)
    s=p**roots
    width=s*s/(64*(1<<roots))
    assert all(F(1,4)<=q<=1 for q in observed.values())
    logs={mask:log_interval(q,width) for mask,q in observed.items()}
    answer={}
    maximum_terms=max(n for _,_,n in logs.values())
    for support in range(1,1<<roots):
        lower=upper=F(0)
        for mask in submasks(support):
            lo,hi,_=logs[mask]
            if (support.bit_count()-mask.bit_count())%2:
                lower-=hi
                upper-=lo
            else:
                lower+=lo
                upper+=hi
        dl,du,n=log_interval(1-p**support.bit_count(),width)
        assert dl<=du<0
        maximum_terms=max(maximum_terms,n)
        quotients=[a/d for a in (lower,upper) for d in (dl,du)]
        lo,hi=min(quotients),max(quotients)
        candidate=(lo+F(1,2)).numerator//(lo+F(1,2)).denominator
        if not (candidate-F(1,2)<lo<=hi<candidate+F(1,2)):
            return None,maximum_terms
        if not 0<=candidate<=bound:
            return None,maximum_terms
        if candidate:
            answer[support]=candidate
    return answer,maximum_terms


class NoiseReview(unittest.TestCase):
    def test_exact_log_intervals_nest_under_refinement(self):
        # Nesting under refinement is an exact necessary consistency control;
        # the log identity and tail enclosure are proved in the written review.
        for value in (F(1,4),F(1,2),F(3,4),F(99,100),F(1)):
            previous=None
            for width in (F(1,10),F(1,1000),F(1,10**8)):
                lo,hi,n=log_interval(value,width)
                self.assertLessEqual(hi-lo,width)
                self.assertLessEqual(lo,hi)
                self.assertLessEqual(hi,0)
                if previous is not None:
                    self.assertGreaterEqual(lo,previous[0])
                    self.assertLessEqual(hi,previous[1])
                previous=(lo,hi)

    def test_no_saturation_and_worst_sign_probability_perturbations(self):
        rng=random.Random(841007)
        cases=0
        maximum_terms=0
        for roots in range(1,5):
            for bound in (1,2,5,10):
                p=F(1,2*bound)
                epsilon=p**roots/(16*(1<<roots))
                for trial in range(3):
                    counts={}
                    for _ in range(bound):
                        support=rng.randrange(1,1<<roots)
                        counts[support]=counts.get(support,0)+1
                    truth=panel(counts,roots,bound)
                    self.assertTrue(all(q>=F(1,2) for q in truth.values()))
                    target=rng.randrange(1,1<<roots)
                    observed={0:F(1)}
                    for mask in range(1,1<<roots):
                        sign=(-1)**(target.bit_count()-mask.bit_count()) if mask&target==mask else (-1)**trial
                        observed[mask]=min(F(1),max(F(0),truth[mask]+sign*epsilon))
                        self.assertLessEqual(abs(observed[mask]-truth[mask]),epsilon)
                    recovered,n=invert_intervals(observed,roots,bound)
                    self.assertEqual(recovered,counts)
                    maximum_terms=max(maximum_terms,n)
                    cases+=1
        METRICS['adversarial_bounded_error_panels']=cases
        METRICS['largest_log_series_length']=maximum_terms

    def test_statistical_and_numeric_error_budgets_are_strict(self):
        for roots,bound in product(range(1,8),(1,2,10,100)):
            p=F(1,2*bound)
            s=p**roots
            epsilon=s/(16*(1<<roots))
            width=s*s/(64*(1<<roots))
            self.assertLess(epsilon,F(1,4))
            self.assertLessEqual(4*(1<<roots)*epsilon/s,F(1,4))
            self.assertLess(width,s/2)
            numeric=(1<<roots)*width/(s-width)+(1<<(roots+1))*width/(s*(s-width))
            self.assertLessEqual(numeric,F(5,64))
            self.assertLess(F(1,4)+numeric,F(1,2))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NoiseReview))
    (HERE/'INDEPENDENT_METRICS.json').write_text(json.dumps(METRICS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())

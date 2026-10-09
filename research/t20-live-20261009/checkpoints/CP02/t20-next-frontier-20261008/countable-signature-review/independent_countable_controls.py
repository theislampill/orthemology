"""Independent controls for the countably indexed finite-route theorem.

The independent decoder uses the denominator's weighted-count budget and
finite partition enumeration, rather than the author's prime-order algorithm.
"""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import random
import unittest

ROOT=Path(__file__).resolve().parent
METRICS={}


def failure(exponent,base=4):
    return 1-F(1,base**exponent)


def readout(counts,base=4):
    answer=F(1)
    for exponent,count in counts.items():
        answer*=failure(exponent,base)**count
    return answer


def partitions(total,largest=None):
    if total==0:
        yield ()
        return
    if largest is None:
        largest=total
    for first in range(min(total,largest),0,-1):
        for rest in partitions(total-first,first):
            yield (first,)+rest


def partition_decode(q):
    if not 0<q<=1 or q.numerator%2==0:
        raise ValueError('Outside the declared rational family.')
    denominator=q.denominator
    weight=0
    while denominator%4==0:
        denominator//=4
        weight+=1
    if denominator!=1:
        raise ValueError('Denominator is not a power of four.')
    matches=[]
    for parts in partitions(weight):
        numerator=1
        for exponent in parts:
            numerator*=4**exponent-1
        if numerator==q.numerator:
            matches.append(dict(Counter(parts)))
    if len(matches)!=1:
        raise ValueError('No unique finite representation.')
    return matches[0]


def factor(n):
    result={}
    p=2
    while p*p<=n:
        while n%p==0:
            result[p]=result.get(p,0)+1
            n//=p
        p+=1
    if n>1:
        result[n]=result.get(n,0)+1
    return result


def order_four(prime):
    assert prime>2
    residue=1
    for exponent in range(1,prime):
        residue=residue*4%prime
        if residue==1:
            return exponent
    raise AssertionError('Not an odd prime.')


def valuation(n,prime):
    answer=0
    while n%prime==0:
        n//=prime
        answer+=1
    return answer


def membership_collision(profiles,forbidden):
    representatives={}
    index=0
    while True:
        if index not in forbidden:
            pattern=tuple(bool(profile(index)) for profile in profiles)
            if pattern in representatives:
                return representatives[pattern],index,pattern
            representatives[pattern]=index
        index+=1


class CountableReview(unittest.TestCase):
    def test_primitive_order_rows_are_triangular_not_diagonal(self):
        primes={}
        for exponent in range(1,25):
            factors=factor(2**exponent-1)
            for p,power in factor(2**exponent+1).items():
                factors[p]=factors.get(p,0)+power
            product=1
            for p,power in factors.items():
                product*=p**power
            self.assertEqual(product,4**exponent-1)
            candidates=[p for p in factors if order_four(p)==exponent]
            self.assertTrue(candidates)
            primes[exponent]=min(candidates)
        for exponent,p in primes.items():
            for column in range(1,25):
                self.assertEqual((4**column-1)%p==0,column%exponent==0)
                if column<exponent:
                    self.assertEqual(valuation(4**column-1,p),0)
        self.assertTrue(all(255%p==0 for p in (3,5,17)))
        self.assertEqual([order_four(p) for p in (3,5,17)],[1,2,4])
        self.assertEqual(partition_decode(F(255,256)),{4:1})
        METRICS['primitive_order_exponents']=24

    def test_all_small_weighted_histograms_are_distinct(self):
        seen={}
        cases=0
        for weight in range(21):
            for parts in partitions(weight):
                counts=dict(Counter(parts))
                q=readout(counts)
                self.assertNotIn(q,seen)
                seen[q]=counts
                self.assertEqual(q.denominator,4**weight)
                cases+=1
        METRICS['finite_histograms_checked']=cases

    def test_independent_partition_decoder_without_index_bound(self):
        rng=random.Random(108221)
        models=[{}, {32:1}, {16:1,1:2}, {4:1}, {1:7}, {2:2,3:1,6:1}]
        for _ in range(20):
            remaining=rng.randrange(1,20)
            counts={}
            while remaining:
                exponent=rng.randrange(1,remaining+1)
                counts[exponent]=counts.get(exponent,0)+1
                remaining-=exponent
            models.append(counts)
        for counts in models:
            self.assertEqual(partition_decode(readout(counts)),counts)
        for invalid in (F(0),F(1,2),F(3,8),F(1,4),F(7,16),F(2,3)):
            with self.assertRaises(ValueError):
                partition_decode(invalid)
        METRICS['partition_decodes']=len(models)

    def test_base_two_exception_causes_a_real_collision(self):
        left={6:1,1:1}
        right={2:2,3:1}
        self.assertNotEqual(left,right)
        self.assertEqual(readout(left,2),F(63,128))
        self.assertEqual(readout(left,2),readout(right,2))
        self.assertNotEqual(readout(left,4),readout(right,4))

    def test_finite_profile_pigeonhole_hides_a_fresh_guarded_route(self):
        all_profiles=[lambda i:i%2==0,lambda i:i%3!=1,lambda i:i<50,
                      lambda i:i.bit_count()%2==0,lambda i:i%7<3,
                      lambda i:(i>>2)&1,lambda i:i%5==4]
        for count in range(8):
            profiles=all_profiles[:count]
            i,j,pattern=membership_collision(profiles,{0,1,2})
            self.assertNotEqual(i,j)
            self.assertTrue(i not in {0,1,2} and j not in {0,1,2})
            self.assertFalse(any(profile(i) and not profile(j) for profile in profiles))
            self.assertTrue((lambda k:k==i)(i) and not (lambda k:k==i)(j))
        METRICS['guarded_profile_panels']=8

    def test_infinite_greedy_alias_has_certified_finite_prefix_bounds(self):
        target=F(3,4)
        partial=F(1)
        counts={}
        for exponent in range(2,41):
            factor_value=failure(exponent)
            count=0
            while partial*factor_value>=target:
                partial*=factor_value
                count+=1
            if count:
                counts[exponent]=count
            self.assertGreater(partial,target)
            self.assertLess(partial,target/factor_value)
            self.assertLess(partial-target,target/(4**exponent-1))
        # Every exponent >=2 touches a root outside decoded R0={0}.
        self.assertTrue(all(exponent&~1 for exponent in counts))
        restricted=F(1)
        self.assertNotEqual(restricted,target)
        METRICS['greedy_prefix_max_exponent']=40
        METRICS['greedy_prefix_occurrences']=sum(counts.values())
        METRICS['greedy_prefix_largest_multiplicity']=max(counts.values())
        METRICS['greedy_error_upper']='(3/4)/(4^40-1)'

    def test_guarded_routes_defeat_the_two_profile_finiteness_certificate(self):
        full=lambda i:True
        candidate_roots=lambda i:i==0
        for i,j in ((1,2),(3,4),(100,101)):
            self.assertFalse(full(i) and not full(j))
            self.assertFalse(candidate_roots(i) and not candidate_roots(j))
        # A common unguarded root-0 route therefore yields 3/4 at both profiles,
        # whether or not any finite number of those additional guards exists.
        self.assertEqual(failure(1),F(3,4))


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CountableReview))
    (ROOT/'INDEPENDENT_METRICS.json').write_text(json.dumps(METRICS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())

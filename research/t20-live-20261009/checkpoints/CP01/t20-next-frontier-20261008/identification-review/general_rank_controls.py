"""Independent checks of the separately frozen rational-design extension."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json
import random
import sys
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('frozen_design_rank', HERE/'frozen-general-v1/design_rank.py')
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)
METRICS = {}
BAD = (F(1,2),F(1,3),F(1,5))
REPAIR = (F(1,2),F(1,3),F(1,7))
GOOD = (F(1,2),F(1,5),F(1,7))


def valuation(q, prime):
    total = 0
    for number, sign in ((q.numerator,1),(q.denominator,-1)):
        while number % prime == 0:
            total += sign
            number //= prime
    return total


def failure(support, rates):
    surviving = F(1)
    for i, rate in enumerate(rates):
        if support & (1<<i):
            surviving *= rate
    return 1-surviving


def direct_probability(counts,rates):
    q = F(1)
    for support,count in counts.items():
        for _ in range(count):
            q *= failure(support,rates)
    return q


def determinant(matrix):
    """Fraction-free Bareiss elimination; separate from the author's RREF."""
    a = [list(row) for row in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n-1):
        if a[k][k] == 0:
            target = next((i for i in range(k+1,n) if a[i][k]), None)
            if target is None:
                return 0
            a[k],a[target] = a[target],a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = a[i][j]*pivot-a[i][k]*a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator//previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1]


class RankReview(unittest.TestCase):
    def test_ranks_have_explicit_nonzero_minor_certificates(self):
        prime_rows = {BAD:(2,3,5,7,29), REPAIR:(2,3,5,7,13,41), GOOD:(2,3,5,7,13,17,23)}
        matrices = {probe:[[valuation(failure(s,probe),p) for s in range(1,8)] for p in primes] for probe,primes in prime_rows.items()}
        for probe in (BAD,REPAIR,GOOD):
            rows = matrices[probe]
            count = len(rows)
            witness = next((cols,determinant([[row[j] for j in cols] for row in rows])) for cols in combinations(range(7),count) if determinant([[row[j] for j in cols] for row in rows]))
            self.assertEqual(lib.rank((probe,)),count)
            METRICS['minor_'+str(probe)] = {'columns':[j+1 for j in witness[0]],'determinant':witness[1],'rank':count}
        stacked = matrices[BAD]+matrices[REPAIR]
        witness = next((rows,determinant([stacked[i] for i in rows])) for rows in combinations(range(len(stacked)),7) if determinant([stacked[i] for i in rows]))
        self.assertEqual(lib.rank((BAD,REPAIR)),7)
        METRICS['stacked_minor'] = {'rows':list(witness[0]),'determinant':witness[1],'rank':7}

    def test_collision_and_repaired_decoding(self):
        self.assertEqual(direct_probability({2:1},BAD),direct_probability({3:1,4:1},BAD))
        self.assertNotEqual(direct_probability({2:1},REPAIR),direct_probability({3:1,4:1},REPAIR))
        rng = random.Random(987654321)
        for _ in range(100):
            counts = {support:count for support in range(1,8) if (count := rng.randrange(8))}
            good = direct_probability(counts,GOOD)
            repaired = (direct_probability(counts,BAD),direct_probability(counts,REPAIR))
            self.assertEqual(lib.recover((GOOD,),(good,)),counts)
            self.assertEqual(lib.recover((BAD,REPAIR),repaired),counts)
        METRICS['random_reconstructed_models'] = 100

    def test_mask_design_triangular_certificate(self):
        for roots in range(1,8):
            size = (1<<roots)-1
            triangular = [[-p.bit_count() if p&t==p else 0 for p in range(1,size+1)] for t in range(1,size+1)]
            self.assertTrue(all(triangular[i][j] == 0 for i in range(size) for j in range(i+1,size)))
            self.assertTrue(all(triangular[i][i] == -(i+1).bit_count() for i in range(size)))
            for mask in range(1,size+1):
                rates = tuple(F(1,2) if mask>>i&1 else F(0) for i in range(roots))
                self.assertEqual([valuation(failure(s,rates),2) for s in range(1,size+1)],triangular[mask-1])
        METRICS['triangular_certificate_roots'] = list(range(1,8))

    def test_rank_defect_can_be_lifted_to_guarded_all_profile_collision(self):
        # Independently constructed lift, subsequently included by the author:
        # v(f_B)-v(f_C)-v(f_AB)=0 at BAD.
        z = {2:1,4:-1,3:-1}
        left,right = {},{}
        universe = 7
        for support,coefficient in z.items():
            for guard in range(8):
                if guard&support:
                    continue
                value = coefficient*((-1)**guard.bit_count())
                (left if value>0 else right)[support,guard] = abs(value)
        def guarded_probability(model,profile):
            q = F(1)
            for (support,guard),count in model.items():
                if support&profile==support and not guard&profile:
                    q *= failure(support,BAD)**count
            return q
        self.assertNotEqual(left,right)
        self.assertTrue(all(guarded_probability(left,profile)==guarded_probability(right,profile) for profile in range(universe+1)))
        METRICS['guarded_lift_profiles'] = 8

    def test_guarded_decoder_with_independently_generated_readouts(self):
        rng = random.Random(5129387)
        for _ in range(40):
            counts = {(support,guard):count for support in range(1,8) for guard in range(8)
                      if not support&guard and (count := rng.randrange(5))}
            for probes in ((GOOD,),(BAD,REPAIR)):
                panel = {}
                for profile in range(1,8):
                    active = {}
                    for (support,guard),count in counts.items():
                        if support&profile==support and not guard&profile:
                            active[support] = active.get(support,0)+count
                    panel[profile] = tuple(direct_probability(active,rates) for rates in probes)
                self.assertEqual(lib.recover_guarded(probes,panel),counts)
        METRICS['guarded_reconstructed_models'] = 40


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RankReview))
    (HERE/'results/GENERAL_INDEPENDENT_METRICS.json').write_text(json.dumps(METRICS,indent=2)+'\n')
    raise SystemExit(not result.wasSuccessful())

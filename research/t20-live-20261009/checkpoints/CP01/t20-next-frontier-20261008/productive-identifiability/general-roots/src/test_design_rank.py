import unittest,random
from itertools import product
from design_rank import *
BAD=(Q(1,2),Q(1,3),Q(1,5))
REPAIR=(Q(1,2),Q(1,3),Q(1,7))
GOOD=(Q(1,2),Q(1,5),Q(1,7))

class DesignRankTests(unittest.TestCase):
    def test_exact_rank_defect_and_hidden_ground_collision(self):
        self.assertEqual(rank((BAD,)),5)
        self.assertEqual(probability({2:1},BAD),Q(2,3))
        self.assertEqual(probability({4:1,3:1},BAD),Q(2,3))
        with self.assertRaises(ValueError):recover((BAD,),(Q(2,3),))
        left={1:1,2:2,4:1};right={1:1,2:1,4:2,3:1}
        self.assertEqual(probability(left,BAD),probability(right,BAD))
        self.assertEqual(set().union(*(set(i for i in range(3) if s>>i&1) for s in left)),set(range(3)))
        self.assertEqual(set().union(*(set(i for i in range(3) if s>>i&1) for s in right)),set(range(3)))

    def test_integer_kernel_gives_equal_probability_nonnegative_pairs(self):
        self.assertEqual(len(kernel((BAD,))),2)
        for vector in kernel((BAD,)):
            positive={s:x for s,x in zip(supports(3),vector) if x>0}
            negative={s:-x for s,x in zip(supports(3),vector) if x<0}
            self.assertNotEqual(positive,negative)
            self.assertEqual(probability(positive,BAD),probability(negative,BAD))

    def test_second_probe_repairs_bad_design(self):
        self.assertEqual(rank((REPAIR,)),6)
        self.assertEqual(rank((BAD,REPAIR)),7)
        self.assertNotEqual(probability({2:1},REPAIR),probability({4:1,3:1},REPAIR))

    def test_single_good_design_recovers_all_128_binary_support_models(self):
        self.assertEqual(rank((GOOD,)),7)
        for vector in product((0,1),repeat=7):
            counts={s:n for s,n in zip(supports(3),vector) if n}
            self.assertEqual(recover((GOOD,),(probability(counts,GOOD),)),counts)
            self.assertEqual(recover((BAD,REPAIR),tuple(probability(counts,p) for p in (BAD,REPAIR))),counts)

    def test_subset_probes_give_constructive_full_rank_and_inverse(self):
        rng=random.Random(381)
        for r in range(1,5):
            probes=subset_probes(r)
            self.assertEqual(rank(probes),2**r-1)
            for _ in range(8):
                counts={s:rng.randrange(4) for s in supports(r)};counts={s:n for s,n in counts.items() if n}
                data=tuple(probability(counts,p) for p in probes)
                self.assertEqual(recover_subset_panel(data,r),counts)
                self.assertEqual(recover(probes,data),counts)

    def test_small_bounded_class_can_be_injective_despite_rank_defect(self):
        # Rank criterion is necessary for unrestricted finite counts, not every cap.
        candidates=[{}]+[{s:1} for s in supports(3)]
        self.assertEqual(len({probability(c,BAD) for c in candidates}),len(candidates))

    def test_kernel_lift_preserves_every_proper_issued_profile(self):
        for vector in kernel((BAD,)):
            positive,negative=lift_guard_kernel(vector,3)
            self.assertNotEqual(positive,negative)
            for profile in range(8):
                self.assertEqual(guarded_probability(positive,profile,BAD),guarded_probability(negative,profile,BAD))
            self.assertNotEqual(guarded_probability(positive,7,REPAIR),guarded_probability(negative,7,REPAIR))

    def test_all_profile_guarded_histograms_reconstruct_after_rank_repair(self):
        rng=random.Random(9871)
        for _ in range(32):
            counts={(p,n):rng.randrange(3) for p in supports(3) for n in range(8) if not p&n}
            counts={key:v for key,v in counts.items() if v}
            for probes in ((GOOD,),(BAD,REPAIR)):
                self.assertEqual(recover_guarded(probes,guarded_panel(counts,probes)),counts)

if __name__=='__main__':unittest.main(verbosity=2)

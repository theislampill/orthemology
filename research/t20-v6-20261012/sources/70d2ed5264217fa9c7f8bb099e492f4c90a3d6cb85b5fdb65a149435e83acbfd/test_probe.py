import unittest
from probe import essential, closure, minimize, resets, frontier, output_for_catalogue

class ProbeTests(unittest.TestCase):
    def test_missing_dependency_closure_is_detected(self):
        # q=a, guarded revocation a'=a and not b: b is dynamically relevant.
        out=tuple(x&1 for x in range(4))
        revoke=tuple(x & ~1 if x&2 else x for x in range(4))
        self.assertEqual(closure(2,out,(revoke,)), frozenset({0,1}))
    def test_reset_equivalence_matches_minimization(self):
        out=(0,1,1,1)
        self.assertEqual(len(set(minimize(out,resets(2)))), 4)
    def test_guard_cancellation_not_syntactic_union(self):
        # (a and b) or (a and not b) has only a as semantic dependency.
        self.assertEqual(essential(2,(0,1,0,1)),frozenset({0}))
    def test_residual_frontier_fails_after_withdrawal(self):
        cat=((1,1),(2,1))
        self.assertEqual(frontier(cat,1),frontier(cat,3))
        h=output_for_catalogue(2,cat)
        self.assertNotEqual(h[0],h[2])
    def test_global_dominance_safe(self):
        self.assertEqual(output_for_catalogue(2,((1,1),(3,2))),output_for_catalogue(2,((1,1),)))
    def test_missing_resets_qualifies_necessity(self):
        out=(0,1,1,1)
        set_actions=tuple(resets(2)[2*i+1] for i in range(2))
        self.assertEqual(len(set(minimize(out,set_actions))),2)
    def test_empty_coordinate_set(self):
        self.assertEqual(closure(0,('constant',),()),frozenset())
        self.assertEqual(minimize(('constant',),()),(0,))
if __name__=='__main__': unittest.main()

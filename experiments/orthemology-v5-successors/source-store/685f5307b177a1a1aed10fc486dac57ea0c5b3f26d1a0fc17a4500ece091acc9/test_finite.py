from tests.support import BoundaryCase
from tests.fixtures import singleton, bernoulli, separator, recovery

class FiniteTests(BoundaryCase):
    def setUp(self):
        self.model=self.module('model'); self.api=self.module('finite')
    def test_even_and_odd_singletons(self):
        for p,expected in ((0,True),(1,False),(2,True)):
            m=self.model.validate_model(singleton(p))
            self.assertEqual(self.api.component(m,1,((0,0),),False),expected)
            self.assertEqual(self.api.component(m,0,((0,0),),True),expected)
        self.assertFalse(self.api.component(m,0,(),True))
    def test_closure_and_connectivity(self):
        raw=separator(); raw['priorities']=[[[0],[0]],[[0],[0]]]; m=self.model.validate_model(raw)
        self.assertFalse(self.api.component(m,0,((0,0),),True))
        self.assertFalse(self.api.component(m,1,((0,0),(1,0)),False))
        self.assertTrue(self.api.component(m,0,((0,0),(1,0)),True))
    def test_revealing_candidate_component_rejected(self):
        m=self.model.validate_model(recovery())
        self.assertFalse(self.api.component(m,1,((0,0),(1,0)),True))
    def test_full_rows_not_supports_and_used_pair_priorities(self):
        m=self.model.validate_model(bernoulli())
        for mode in (0,1): self.assertTrue(self.api.component(m,mode,((0,mode),(1,mode)),True))
        equal=self.model.validate_model(bernoulli(equal=True))
        for mode in (0,1): self.assertFalse(self.api.component(equal,mode,((0,mode),(1,mode)),True))
        self.assertFalse(self.api.component(m,0,((0,0),(0,1),(1,0),(1,1)),True))
    def test_reachable_respects_candidate_and_compatibility(self):
        m=self.model.validate_model(recovery()); pairs=((0,0),(1,0))
        self.assertEqual(self.api.reachable(m,0,pairs,1,False),frozenset((0,1)))
        self.assertEqual(self.api.reachable(m,0,pairs,1,True),frozenset((0,)))
    def test_unlawful_or_malformed_pair_rejected(self):
        m=self.model.validate_model(singleton())
        for p in (((False,0),),((0,1),),((0,0),(0,0)),((-1,0),)):
            with self.subTest(p=p): self.assertFalse(self.api.component(m,0,p,True))

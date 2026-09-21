"""Finite model algebra and its actual licence integration, not measure-kernel tests."""
import importlib.util
import itertools
from fractions import Fraction
import unittest
import operational as op
from boundaries import Rejection


def model(view,space='tagged-uniform-intervals',weights=None):
    return {'space':space,'law':'fixed-base-law','weights':weights or [[1,len(view)] for _ in view], 'view':view,'events':'full-measurable'}

def primitive():return {'op':'primitive','name':'succ'}

class ObservationModels(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('observations'),'finite observation checker absent')
        import observations
        self.m=observations
    def test_quantitative_refinement(self):
        a,b=model([0,0]),model([0,-1]);r=self.m.refinement(a,b)
        self.assertEqual(r['coarse_defect'],[0,1]);self.assertEqual(r['fine_defect'],[1,2]);self.assertEqual(r['increment'],[1,2])
        self.assertEqual(sum(Fraction(*x['weight'])*Fraction(*x['conditional_defect']) for x in r['positive_coarse_fibres']),Fraction(1,2))
    def test_bin_refinement_identity(self):
        r=self.m.refinement(model([2]),model([-1]));self.assertEqual(len(r['positive_coarse_fibres']),2);self.assertEqual(r['increment'],[1,1])
        r=self.m.refinement(model([2]),model([4]));self.assertEqual(r['increment'],[0,1])
    def test_reject_nonrefinement_and_changed_law(self):
        for b in [model([3]),model([0]),{**model([4]),'law':'other'}]:
            with self.assertRaises(Rejection):self.m.refinement(model([2]),b)
    def test_finite_carrier_refinement_zero(self):
        r=self.m.refinement(model([0,0],'finite-programs'),model([0,1],'finite-programs'))
        self.assertEqual(r['fine_defect'],[0,1]);self.assertEqual(r['increment'],[0,1])
    def test_finite_factorisation_required(self):
        with self.assertRaises(Rejection):self.m.refinement(model([0,1],'finite-programs'),model([0,0],'finite-programs'))
    def test_no_claimed_defect_no_estimator(self):
        for a in [{**model([0]),'defect':[0,1]}, {**model([0]),'weights':[[1,2]]}, {**model([0]),'events':'finite-predicates'},model([-2]),model([0],space='arbitrary-measure')]:
            with self.assertRaises(Rejection):self.m.check(a)
    def test_zero_weight_fibres(self):
        r=self.m.refinement(model([0,0],weights=[[1,1],[0,1]]),model([0,-1],weights=[[1,1],[0,1]]))
        self.assertEqual(r['fine_defect'],[0,1]);self.assertTrue(r['equality'])
    def test_exhaustive_small_refinements(self):
        cases=0
        for v in itertools.product((0,1,2,-1),repeat=2):
            for w in itertools.product((0,1,2,4,-1),repeat=2):
                try:r=self.m.refinement(model(list(v)),model(list(w)))
                except Rejection:continue
                self.assertEqual(Fraction(*r['fine_defect']),Fraction(*r['coarse_defect'])+Fraction(*r['increment']));cases+=1
        self.assertGreater(cases,100)

class ProbabilityLicences(unittest.TestCase):
    def setUp(self):
        self.eng=op.Engine.standard()
        self.assertTrue(hasattr(self.eng,'set_probability_observation'),'probability-dependent Context absent')
        self.eng.set_probability_observation('signal',model([0,0]))
    def test_add_requirement_invalidates_preexisting(self):
        old=self.eng.admit(primitive());self.eng.require_probability('primitive:succ','signal',[1,4])
        with self.assertRaises(Rejection):self.eng.dispatch(old,2)
        new=self.eng.admit(primitive());self.assertEqual(self.eng.dispatch(new,2),3)
    def test_refinement_revokes_and_evidence_rebinds(self):
        self.eng.require_probability('primitive:succ','signal',[1,4]);old=self.eng.admit(primitive())
        report=self.eng.refine_probability_observation('signal',model([0,-1]));self.assertEqual(report['increment'],[1,2])
        with self.assertRaises(Rejection):self.eng.dispatch(old,2)
        with self.assertRaises(Rejection):self.eng.admit(primitive())
        self.eng.require_probability('primitive:succ','signal',[3,4]);new=self.eng.admit(primitive())
        self.assertEqual(self.eng.dispatch(new,2),3)
        with self.assertRaises(Rejection):self.eng.dispatch(old,2)
        evidence=self.eng.describe(new)['probability_evidence'][0]
        self.assertEqual(evidence['defect'],[1,2]);self.assertEqual(evidence['epsilon'],[3,4]);self.assertEqual(evidence['status'],'CHECKED_DECLARED_MODEL')
    def test_law_version_change_same_numbers_invalidates(self):
        self.eng.require_probability('primitive:succ','signal',[0,1]);old=self.eng.admit(primitive())
        self.eng.set_probability_observation('signal',{**model([0,0]),'law':'new-law'})
        with self.assertRaises(Rejection):self.eng.dispatch(old,2)
        self.assertEqual(self.eng.dispatch(self.eng.admit(primitive()),2),3)
    def test_unrelated_observation_change_preserves(self):
        self.eng.require_probability('primitive:succ','signal',[0,1]);old=self.eng.admit(primitive())
        self.eng.set_probability_observation('unused',model([-1]))
        self.assertEqual(self.eng.dispatch(old,2),3)
    def test_requirement_propagates_through_composition(self):
        c={'op':'compose','first':primitive(),'second':{'op':'primitive','name':'iszero'}}
        old=self.eng.admit(c);self.eng.require_probability('primitive:succ','signal',[0,1])
        with self.assertRaises(Rejection):self.eng.dispatch(old,0)
        new=self.eng.admit(c);self.assertIs(self.eng.dispatch(new,0),False)
        self.eng.refine_probability_observation('signal',model([-1,-1]))
        with self.assertRaises(Rejection):self.eng.dispatch(new,0)
    def test_requirements_not_caller_assertions(self):
        self.eng.require_probability('primitive:succ','signal',[0,1]);self.eng.refine_probability_observation('signal',model([-1,-1]))
        with self.assertRaises(Rejection):self.eng.admit({**primitive(),'probability_evidence':{'pass':True}})
    def test_finite_refinement_recertifies(self):
        self.eng.set_probability_observation('finite',model([0,0],'finite-programs'));self.eng.require_probability('primitive:succ','finite',[0,1]);old=self.eng.admit(primitive())
        self.eng.refine_probability_observation('finite',model([0,1],'finite-programs'))
        with self.assertRaises(Rejection):self.eng.dispatch(old,0)
        self.assertEqual(self.eng.dispatch(self.eng.admit(primitive()),0),1)

if __name__=='__main__':unittest.main()

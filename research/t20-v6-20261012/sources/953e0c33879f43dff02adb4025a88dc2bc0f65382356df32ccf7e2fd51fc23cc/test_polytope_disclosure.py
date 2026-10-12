import copy
import unittest
from fractions import Fraction as F

from polytope_disclosure import audit, verify


def triangle(min_weight='1/10', le=None, eq=None):
    return {'min_weight':min_weight,'extra_le':le or [],'extra_eq':eq or []}


def atom(i,offset='-1/5'):
    coeff=[0,0,0]; coeff[i]=1
    return {'coefficients':coeff,'offset':offset}


def cmp(i=0,strict=True):
    return {'op':'gt' if strict else 'ge','atom':i}


def conjunction():
    return {'op':'and','args':[cmp(i) for i in range(3)]}


class PolytopeDisclosureTests(unittest.TestCase):
    def test_original_vertices_miss_interior_boolean_truth(self):
        p=triangle(); atoms=[atom(i) for i in range(3)]; target=conjunction()
        r=audit(p,atoms,target)
        self.assertEqual(r['status'],'DISAGREEMENT')
        self.assertTrue(verify(p,atoms,target,r)['accepted'])
        self.assertEqual(len(r['cells']),27)
        self.assertEqual(set(r['realized_values']),{False,True})

    def test_negation_also_defeats_original_vertex_invariance(self):
        p=triangle(); atoms=[atom(i) for i in range(3)]
        target={'op':'not','arg':conjunction()}
        self.assertEqual(audit(p,atoms,target)['status'],'DISAGREEMENT')

    def test_singleton_weak_tie_is_true(self):
        p=triangle('1/3'); atoms=[atom(0,'-1/3')]; t=cmp(strict=False)
        r=audit(p,atoms,t)
        self.assertEqual(r['status'],'INVARIANT_TRUE')
        self.assertTrue(verify(p,atoms,t,r)['accepted'])

    def test_singleton_strict_tie_is_false(self):
        p=triangle('1/3'); atoms=[atom(0,'-1/3')]
        self.assertEqual(audit(p,atoms,cmp())['status'],'INVARIANT_FALSE')

    def test_lower_dimensional_equality_face_is_retained(self):
        p=triangle(eq=[{'coefficients':[1,0,0],'bound':'1/5'}]); atoms=[atom(0)]
        self.assertEqual(audit(p,atoms,cmp())['status'],'INVARIANT_FALSE')
        self.assertEqual(audit(p,atoms,cmp(strict=False))['status'],'INVARIANT_TRUE')

    def test_empty_polytope_is_reported_separately(self):
        p=triangle('1/2'); atoms=[atom(0)]; t=cmp(); r=audit(p,atoms,t)
        self.assertEqual(r['status'],'NO_ADMISSIBLE_EXTENSION')
        self.assertTrue(verify(p,atoms,t,r)['accepted'])

    def test_slack_zero_closure_is_not_a_strict_witness(self):
        p=triangle('1/3'); atoms=[atom(0,'-1/3')]; r=audit(p,atoms,cmp())
        self.assertEqual(r['status'],'INVARIANT_FALSE')
        positive=next(c for c in r['cells'] if c['signs']==[1])
        self.assertEqual(positive['kind'],'DUAL_ZERO_BOUND')

    def test_infeasible_closure_has_farkas_certificate(self):
        p=triangle(); atoms=[{'coefficients':[0,0,0],'offset':1}]; r=audit(p,atoms,cmp())
        self.assertEqual(r['status'],'INVARIANT_TRUE')
        tie=next(c for c in r['cells'] if c['signs']==[0])
        self.assertEqual(tie['kind'],'FARKAS_CONTRADICTION')

    def test_arbitrarily_small_positive_margin_is_not_rounded_to_zero(self):
        tiny=F(1,10**12); p=triangle(); atoms=[atom(0,str(-F(4,5)+tiny))]
        r=audit(p,atoms,cmp()); self.assertEqual(r['status'],'DISAGREEMENT')
        cell=next(c for c in r['cells'] if c['signs']==[1])
        self.assertEqual(cell['kind'],'POSITIVE_WITNESS')
        self.assertTrue(0<F(cell['point'][-1])<=tiny)

    def test_incomplete_pattern_coverage_is_rejected(self):
        p=triangle(); a=[atom(0)]; t=cmp(); c=audit(p,a,t)
        self.assertTrue(verify(p,a,t,c)['accepted'])
        c['cells'].pop()
        self.assertFalse(verify(p,a,t,c)['accepted'])

    def test_false_positive_witness_is_rejected(self):
        p=triangle(); a=[atom(0)]; t=cmp(); c=audit(p,a,t)
        self.assertTrue(verify(p,a,t,c)['accepted'])
        w=next(x for x in c['cells'] if x['kind']=='POSITIVE_WITNESS')
        w['point'][-1]='0'
        self.assertFalse(verify(p,a,t,c)['accepted'])

    def test_false_dual_multipliers_are_rejected(self):
        p=triangle('1/3'); a=[atom(0,'-1/3')]; t=cmp(); c=audit(p,a,t)
        self.assertTrue(verify(p,a,t,c)['accepted'])
        w=next(x for x in c['cells'] if x['kind']=='DUAL_ZERO_BOUND')
        w['multipliers']=['0']*len(w['multipliers'])
        self.assertFalse(verify(p,a,t,c)['accepted'])

    def test_stale_input_binding_is_rejected(self):
        p=triangle(); a=[atom(0)]; t=cmp(); c=audit(p,a,t)
        self.assertTrue(verify(p,a,t,c)['accepted'])
        a[0]['offset']='-2/5'
        self.assertFalse(verify(p,a,t,c)['accepted'])

    def test_boolean_does_not_masquerade_as_a_sign(self):
        p=triangle(); a=[atom(0)]; t=cmp(); c=audit(p,a,t)
        self.assertTrue(verify(p,a,t,c)['accepted'])
        next(x for x in c['cells'] if x['signs']==[1])['signs']=[True]
        self.assertFalse(verify(p,a,t,c)['accepted'])

    def test_unsupported_target_is_invalid(self):
        self.assertEqual(audit(triangle(),[atom(0)],{'op':'execute'})['status'],'INVALID')

    def test_no_atom_constant_target_still_checks_base_nonemptiness(self):
        p=triangle(); t={'op':'const','value':True}; r=audit(p,[],t)
        self.assertEqual(r['status'],'INVARIANT_TRUE')
        self.assertTrue(verify(p,[],t,r)['accepted'])


if __name__=='__main__': unittest.main()

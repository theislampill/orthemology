"""Exact finite controls for the T20 cross-front contribution. No external packages."""
import unittest
from fractions import Fraction as Q
from itertools import product
from research.contracts import (
    normalise, tilt, pushforward, tv, transported_likelihood,
    kernel_pushforward, kernel_likelihood, audit_sidecar,
    live_claims, affected_nodes, replay_dag, euler_correction,
)

class AuditTransportTests(unittest.TestCase):
    def test_historical_factor_is_evaluated_at_origin(self):
        prior={0:Q(1,2),1:Q(1,2)}
        historical=tilt(prior,{0:1,1:2})
        moved=pushforward(historical,{0:1,1:2})
        correct=tilt(moved,{1:1,2:Q(1,2)})
        wrong=tilt(moved,{1:Q(1,2),2:Q(1,3)})
        self.assertEqual(correct,{1:Q(1,2),2:Q(1,2)})
        self.assertEqual(wrong,{1:Q(3,7),2:Q(4,7)})
    def test_invertible_transport_contract(self):
        q={'a':'x','b':'y'}; L={'a':Q(2,3),'b':Q(1,5)}
        ell=transported_likelihood(q,L)
        for k in range(11):
            mu={'a':Q(k,10),'b':1-Q(k,10)}
            self.assertEqual(pushforward(tilt(mu,L),q),tilt(pushforward(mu,q),ell))
    def test_merged_fibre_rejects_distinct_historical_factors(self):
        with self.assertRaises(ValueError):
            transported_likelihood({'a':0,'b':0},{'a':1,'b':2})
    def test_single_fibre_normalised_law_hides_evidence_mass(self):
        q={'a':0,'b':0}; L={'a':1,'b':2}
        self.assertEqual(pushforward(tilt({'a':1,'b':0},L),q),
                         pushforward(tilt({'a':0,'b':1},L),q))
        self.assertNotEqual(sum(Q(v)*Q(L[k]) for k,v in {'a':1,'b':0}.items()),
                            sum(Q(v)*Q(L[k]) for k,v in {'a':0,'b':1}.items()))
    def test_noisy_kernel_has_only_component_constant_factors(self):
        K={'a':{0:Q(1,3),1:Q(2,3)},'b':{0:Q(2,3),1:Q(1,3)}}
        with self.assertRaises(ValueError): kernel_likelihood(K,{'a':1,'b':2})
        ell=kernel_likelihood(K,{'a':3,'b':3})
        self.assertEqual(ell,{0:Q(3),1:Q(3)})
    def test_disconnected_kernel_accepts_distinct_components(self):
        K={'a':{0:1,1:0},'b':{0:0,1:1}}
        ell=kernel_likelihood(K,{'a':2,'b':3})
        for i in range(8):
            p={'a':Q(i,7),'b':1-Q(i,7)}
            self.assertEqual(kernel_pushforward(tilt(p,{'a':2,'b':3}),K),
                             tilt(kernel_pushforward(p,K),ell))
    def test_four_likelihood_profiles_need_two_bits(self):
        states=list(product([0,1],repeat=2))
        base={s:'same' for s in states}
        factors={'A':{s:1+s[0] for s in states},'B':{s:1+s[1] for s in states}}
        sidecar,alphabet,bits=audit_sidecar(base,factors)
        self.assertEqual((alphabet,bits),(4,2))
        self.assertEqual(len(set(sidecar.values())),4)
    def test_sidecar_labels_reused_in_different_base_fibres(self):
        base={'a':0,'b':0,'c':1,'d':1}
        factors={'A':{'a':1,'b':2,'c':7,'d':8}}
        sidecar,alphabet,bits=audit_sidecar(base,factors)
        self.assertEqual((alphabet,bits),(2,1))
        self.assertEqual(len(set(sidecar.values())),2)
    def test_individual_source_means_do_not_preserve_joint_audit(self):
        pos={(0,0):Q(1,2),(1,1):Q(1,2)}
        neg={(0,1):Q(1,2),(1,0):Q(1,2)}
        for j in [0,1]:
            self.assertEqual(sum(p*Q(1+s[j],2) for s,p in pos.items()),
                             sum(p*Q(1+s[j],2) for s,p in neg.items()))
        zp=sum(p*Q(1+s[0],2)*Q(1+s[1],2) for s,p in pos.items())
        zn=sum(p*Q(1+s[0],2)*Q(1+s[1],2) for s,p in neg.items())
        self.assertEqual((zp,zn),(Q(5,8),Q(1,2)))
    def test_rare_conditioning_separation(self):
        e=Q(1,10**9)
        mu={'a':e,'b':0,'c':1-e}; nu={'a':0,'b':e,'c':1-e}; L={'a':1,'b':1,'c':0}
        self.assertEqual(tv(mu,nu),e)
        self.assertEqual(tv(tilt(mu,L),tilt(nu,L)),1)
    def test_sharp_relative_factor_bound(self):
        mu={'a':Q(4,5),'b':Q(1,5)}; r={'a':Q(1,4),'b':4}
        self.assertEqual(tilt(mu,r),{'a':Q(1,5),'b':Q(4,5)})
        self.assertEqual(tv(mu,tilt(mu,r)),Q(3,5))
    def test_projective_bound_exact_rational_grid(self):
        # a=A^2,b=B^2 makes the sharp square-root bound rational.
        checks=0
        for A,B in [(Q(1,2),Q(2)),(Q(1),Q(3)),(Q(2),Q(5))]:
            a,b=A*A,B*B; bound=(B-A)/(B+A)
            for i in range(13):
                for j in range(13-i):
                    mu={0:Q(i,12),1:Q(j,12),2:Q(12-i-j,12)}
                    for k in range(9):
                        r={0:a,1:a+(b-a)*Q(k,8),2:b}
                        self.assertLessEqual(tv(mu,tilt(mu,r)),bound)
                        checks+=1
        self.assertEqual(checks,2457)
    def test_zero_evidence_is_not_normalised(self):
        with self.assertRaises(ValueError): tilt({'a':1},{'a':0})
    def test_negative_mass_is_rejected(self):
        with self.assertRaises(ValueError): normalise({'a':1,'b':-1})
    def test_missing_factor_is_rejected(self):
        with self.assertRaises(ValueError): tilt({'a':1},{'b':1})

class ProvenanceAndReplayTests(unittest.TestCase):
    def test_loss_of_one_warrant_does_not_erase_another(self):
        warrants={'c':[{'A','rule'},{'B','rule'}],'d':[{'A','rule'}]}
        self.assertEqual(live_claims(warrants,{'B','rule'}),{'c'})
        self.assertEqual(live_claims(warrants,{'A','B'}),set())
    def test_dependency_closure_and_exact_partial_replay(self):
        deps={'a':{'sourceA'},'b':{'sourceB'},'join':{'a','b'},'out':{'join'}}
        funcs={'a':lambda d:2*d['sourceA'],'b':lambda d:3*d['sourceB'],
               'join':lambda d:d['a']+d['b'],'out':lambda d:d['join']**2}
        inputs={'sourceA':2,'sourceB':5}
        initial={'a':4,'b':15,'join':19,'out':361}
        revised={'sourceA':4,'sourceB':5}
        affected=affected_nodes(deps,{'sourceA'})
        self.assertEqual(affected,{'a','join','out'})
        values,recomputed=replay_dag(deps,funcs,revised,initial,{'sourceA'})
        self.assertEqual(values['out'],529)
        self.assertEqual(values['b'],15)
        self.assertEqual(set(recomputed),affected)
        full,_=replay_dag(deps,funcs,revised,{},set(revised))
        self.assertEqual({k:values[k] for k in deps},{k:full[k] for k in deps})
    def test_cycles_rejected(self):
        with self.assertRaises(ValueError):
            replay_dag({'a':{'b'},'b':{'a'}},{'a':lambda d:0,'b':lambda d:0},{},{},set())
    def test_missing_cache_forces_build(self):
        # Caller must disclose the changed sources; empty old values still forces a full build.
        deps={'a':{'s'}}; funcs={'a':lambda d:d['s']}
        values,_=replay_dag(deps,funcs,{'s':3},{},set())
        self.assertEqual(values['a'],3)
    def test_active_correction_cannot_be_fixed_by_weight_only(self):
        n=9; h=Q(1,4)
        x=euler_correction(Q(0),Q(1),h,n)
        y=euler_correction(Q(0),Q(2),h,n)
        self.assertEqual(y-x,1-(1-h)**n)
        # Any normalised reweighting of a one-atom law leaves its position fixed.
        self.assertEqual(tilt({x:1},{x:Q(7,3)}),{x:Q(1)})
        self.assertNotEqual(x,y)
    def test_contracting_affine_sensitivity_exact(self):
        for h in [Q(0),Q(1,10),Q(1,2),Q(1)]:
            for n in range(20):
                z=euler_correction(Q(3),Q(7),h,n)
                self.assertEqual(z,(1-h)**n*3+(1-(1-h)**n)*7)
    def test_local_exclusivity_does_not_imply_common_source(self):
        owner={'event1':'source1','event2':'source2'}
        self.assertEqual(len(owner),2)
        self.assertNotEqual(owner['event1'],owner['event2'])
    def test_connected_agreement_glues_unique_owner(self):
        edges=[('a','b'),('b','c'),('c','d')]
        candidates=['s1','s2','s3']; checks=0
        for labels in product(candidates,repeat=4):
            owner=dict(zip('abcd',labels))
            if all(owner[a]==owner[b] for a,b in edges):
                self.assertEqual(len(set(owner.values())),1)
                checks+=1
        self.assertEqual(checks,3)

if __name__=='__main__': unittest.main(verbosity=2)

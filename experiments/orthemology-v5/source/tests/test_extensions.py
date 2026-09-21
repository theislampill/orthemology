from pathlib import Path
from fractions import Fraction
import itertools
import unittest

ROOT = Path(__file__).resolve().parents[1]
I, K, S, Z, O = [(s,) for s in ['i','k','s','zero','one']]
def app(f,x): return ('app',f,x)
def arr(a,b): return ('arr',a,b)
V=('v',0)
BOOL=('all',arr(V,arr(V,V)))
ID=('all',arr(V,V))

def id_proof(): return {'rule':'all_i','body':{'rule':'i','A':V}}
def true_proof(): return {'rule':'all_i','body':{'rule':'k','A':V,'B':V}}
def false_proof():
    return {'rule':'all_i','body':{'rule':'app',
       'function':{'rule':'k','A':arr(V,V),'B':V},
       'argument':{'rule':'i','A':V}}}

def pure(p): return {'op':'pure','proof':p}
def mix(p,left,right): return {'op':'mix','p':p,'left':left,'right':right}
def tapp(p,a): return {'op':'all_e','polymorphic':p,'type':a}
def papp(f,x): return {'op':'app','function':f,'argument':x}

class Presence(unittest.TestCase):
    def test_implementation_is_present(self):
        self.assertTrue((ROOT/'extensions.py').is_file(), 'new implementation absent')

class ExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import extensions, reference
        cls.e,cls.r=extensions,reference

    def test_marker_freeness(self):
        self.assertTrue(self.e.marker_free(app(S,app(K,I))))
        self.assertFalse(self.e.marker_free(app(K,Z)))

    def test_marker_substitution(self):
        self.assertEqual(self.e.substitute_markers(app(Z,O),I,K),app(I,K))

    def test_selector_certificate_true(self):
        f=app(I,K)
        _,tr=self.r.normalize(app(app(f,Z),O))
        c=self.e.certify_selector(f,tr)
        self.assertEqual(c.selector,0)
        self.assertEqual(c.overhead,2)
        self.assertEqual(self.e.replay_selector(c,I,K)[-1],I)

    def test_selector_certificate_false(self):
        f=app(K,I)
        _,tr=self.r.normalize(app(app(f,Z),O))
        c=self.e.certify_selector(f,tr)
        self.assertEqual(c.selector,1)
        self.assertEqual(self.e.replay_selector(c,I,K)[-1],K)

    def test_marker_capture_rejected(self):
        # Constant zero consumes BOTH probe arguments; without freshness it
        # mimics the left selector at this probe but fails for arbitrary inputs.
        f=app(K,app(K,Z))
        _,tr=self.r.normalize(app(app(f,Z),O))
        with self.assertRaises(self.r.Rejection): self.e.certify_selector(f,tr)

    def test_forged_trace_rejected(self):
        with self.assertRaises(self.r.Rejection):
            self.e.certify_selector(K,[app(app(K,Z),O),O])

    def test_nonselector_probe_rejected(self):
        with self.assertRaises(self.r.Rejection):
            self.e.certify_selector(S,[app(app(S,Z),O)])

    def test_specialisation_holds_for_raw_divergent_inputs(self):
        d=app(app(S,I),I); om=app(d,d)
        for f in [K,app(K,I),app(I,K),app(I,app(K,I))]:
            _,tr=self.r.normalize(app(app(f,Z),O))
            c=self.e.certify_selector(f,tr)
            for x,y in itertools.product([I,K,Z,O,om],repeat=2):
                out=self.e.replay_selector(c,x,y)
                self.assertEqual(out[-1],[x,y][c.selector])
                self.assertEqual(len(out)-1,c.overhead)

    def test_all_compatible_steps_preserve_marker_freeness(self):
        terms=[app(I,I),app(app(K,S),I),app(app(app(S,I),K),I)]
        for t in terms:
            self.assertTrue(all(self.e.marker_free(u) for u in self.e.compatible_steps(t)))

    def test_incompleteness_witness(self):
        t=app(app(K,I),Z)
        self.assertEqual(self.r.head_step(t),I)
        self.assertFalse(self.e.marker_free(t))
        with self.assertRaises(self.r.Rejection):
            self.r.check({'rule':'literal','term':Z,'type':ID})

    def test_explicit_omega_cycle(self):
        d=app(app(S,I),I); om=app(d,d)
        tr=[om,app(app(I,d),app(I,d)),app(d,app(I,d)),om]
        for a,b in zip(tr,tr[1:]): self.assertIn(b,self.e.compatible_steps(a))
        w=lambda x: app(app(K,I),x)
        for a,b in zip(tr,tr[1:]): self.assertIn(w(b),self.e.compatible_steps(w(a)))
        self.assertEqual(self.r.head_step(w(om)),I)

    def test_internal_probabilistic_boolean(self):
        p=mix([1,2],pure(true_proof()),pure(false_proof()))
        c,t=self.e.compile_probability(p)
        self.assertEqual(t,BOOL)
        self.assertEqual(self.e.evaluate_probability(c),{K:Fraction(1,2),app(K,I):Fraction(1,2)})

    def test_probabilistic_self_instantiation_is_erased(self):
        p=mix([1,2],pure(true_proof()),pure(false_proof()))
        c,t=self.e.compile_probability(p)
        c2,t2=self.e.compile_probability(tapp(p,BOOL))
        self.assertEqual(c,c2)
        self.assertEqual(t2,arr(BOOL,arr(BOOL,BOOL)))

    def test_probabilistic_application(self):
        p=mix([1,3],pure(true_proof()),pure(false_proof()))
        p=papp(papp(tapp(p,BOOL),pure(true_proof())),pure(false_proof()))
        c,t=self.e.compile_probability(p)
        self.assertEqual(t,BOOL)
        dist=self.e.normalise_probability(self.e.evaluate_probability(c))
        self.assertEqual(dist,{K:Fraction(1,3),app(K,I):Fraction(2,3)})

    def test_probability_endpoints(self):
        for q,expect in [([0,1],app(K,I)),([1,1],K)]:
            c,t=self.e.compile_probability(mix(q,pure(true_proof()),pure(false_proof())))
            self.assertEqual(self.e.evaluate_probability(c),{expect:Fraction(1)})

    def test_probability_bad_weights(self):
        for q in [[1,0],[2,1],[-1,2],[True,2],[1,False],0.5,'1/2']:
            with self.assertRaises(self.r.Rejection):
                self.e.compile_probability(mix(q,pure(true_proof()),pure(false_proof())))

    def test_probability_bad_typing(self):
        for q in [[0,1],[1,2]]:
            with self.assertRaises(self.r.Rejection):
                self.e.compile_probability(mix(q,pure(true_proof()),pure(id_proof())))

    def test_probability_no_unknown_fields(self):
        p=mix([1,2],pure(true_proof()),pure(false_proof())); p['unsafe']=True
        with self.assertRaises(self.r.Rejection): self.e.compile_probability(p)

    def test_probability_no_type_case(self):
        with self.assertRaises(self.r.Rejection):
            self.e.compile_probability({'op':'type_case','type':BOOL})

    def test_probability_type_generalisation(self):
        p={'op':'all_i','body':mix([1,2],pure({'rule':'k','A':V,'B':V}),
            pure({'rule':'app','function':{'rule':'k','A':arr(V,V),'B':V},
                  'argument':{'rule':'i','A':V}}))}
        c,t=self.e.compile_probability(p)
        self.assertEqual(t,BOOL)
        self.assertEqual(sum(self.e.evaluate_probability(c).values()),1)

    def test_quotient_effect_collapse(self):
        self.assertEqual(self.e.saturated_masks(3,[(2,0),(2,1)]),[0,7])

    def test_extension_preserves_codes_exactly_within_components(self):
        base=[(0,1)]
        self.assertEqual(self.e.saturated_masks(3,base),self.e.saturated_masks(3,base+[(1,0)]))
        self.assertNotEqual(self.e.saturated_masks(3,base),self.e.saturated_masks(3,base+[(1,2)]))

    def test_observation_factorisation_error_bound(self):
        vals=[Fraction(0),Fraction(1),Fraction(1,3)]
        pred,err=self.e.best_observation_approximation([0,0,1],vals)
        self.assertEqual(pred,{0:Fraction(1,2),1:Fraction(1,3)})
        self.assertEqual(err,Fraction(1,2))

    def test_singleton_trilemma_countermodel(self):
        # C=Unit, E(*)=Bool. All ambient sections have one coordinate.
        for b in [False,True]:
            family=lambda _: b
            packed=family(None)
            self.assertEqual((lambda value,index:value)(packed,None),family(None))

    def test_named_substitution_capture_case(self):
        b=('all',arr(('v',1),('v',0)))
        a=('v',0)
        self.assertEqual(self.e.named_instantiate(b,a),('all',arr(('v',1),('v',0))))
        self.assertEqual(self.e.named_instantiate(b,a),self.r.instantiate_type(b,a))

    def test_finite_model_substitution(self):
        b=('all',arr(('v',1),('v',0))); a=('v',0)
        # Every binary total application table, all subsets as type interpretations.
        for table in itertools.product(range(2),repeat=4):
            for rho in itertools.product(range(4),repeat=2):
                left=self.e.eval_type(self.r.instantiate_type(b,a),rho,table,2)
                av=self.e.eval_type(a,rho,table,2)
                right=self.e.eval_type(b,(av,)+rho,table,2)
                self.assertEqual(left,right)

    def test_anti_reflective_equilibrium(self):
        self.assertTrue(self.e.threshold_allows(Fraction(1,2),Fraction(1,2),Fraction(1,2)))
        for q in [Fraction(0),Fraction(1,4),Fraction(3,4),Fraction(1)]:
            self.assertFalse(self.e.threshold_allows(1-q,Fraction(1,2),q))

    def test_true_type_does_not_make_false_proof(self):
        with self.assertRaises(self.r.Rejection):
            self.e.compile_probability(papp(tapp(pure(true_proof()),('bottom',)),pure(true_proof())))

    def test_mixture_sharing_differs_from_resampling(self):
        # Independently sampled selectors have cross outcomes; one shared draw does not.
        vals=[K,app(K,I)]
        shared={(x,x):Fraction(1,2) for x in vals}
        indep={(x,y):Fraction(1,4) for x in vals for y in vals}
        self.assertNotEqual(shared,indep)
        self.assertEqual(sum(shared.values()),sum(indep.values()))

if __name__=='__main__': unittest.main()

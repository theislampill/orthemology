import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    import reference as r
except ModuleNotFoundError:
    r = None

V = ('v', 0)
I = ('i',)
K = ('k',)
S = ('s',)
Z = ('zero',)
O = ('one',)
BOT = ('bottom',)
def Arr(a, b): return ('arr', a, b)
def All(b): return ('all', b)
def App(f, x): return ('app', f, x)
def ip(a): return {'rule':'i', 'A':a}
def kp(a,b): return {'rule':'k', 'A':a,'B':b}
def ap(f,x): return {'rule':'app','function':f,'argument':x}
def ai(b): return {'rule':'all_i','body':b}
def ae(p,t): return {'rule':'all_e','polymorphic':p,'type':t}
ID = All(Arr(V,V))
BOOL = All(Arr(V,Arr(V,V)))
PID = ai(ip(V))
PT = ai(kp(V,V))
PF = ai(ap(kp(Arr(V,V),V),ip(V)))

def diagonal_proof():
    pa=Arr(V,BOOL); ppa=Arr(pa,BOOL)
    return ai(ap(kp(ppa,Arr(ppa,V)),ap(kp(BOOL,pa),PF)))

def diagonal_type():
    pa=Arr(V,BOOL); ppa=Arr(pa,BOOL)
    return All(Arr(Arr(ppa,V),ppa))

class InternalTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(r, 'reference implementation has not been provided')

    def test_poly_id_is_internal(self):
        self.assertEqual(r.check(PID), (I,ID))
    def test_same_code_is_legal_type_argument(self):
        self.assertEqual(r.check(ae(PID,ID)),(I,Arr(ID,ID)))
    def test_actual_self_application(self):
        t,typ=r.check(ap(ae(PID,ID),PID))
        self.assertEqual(typ,ID)
        self.assertEqual(r.normalize(t)[0],I)
    def test_poly_true(self): self.assertEqual(r.check(PT),(K,BOOL))
    def test_poly_false(self): self.assertEqual(r.check(PF),(App(K,I),BOOL))
    def test_bool_self_instantiation(self):
        self.assertEqual(r.check(ae(PT,BOOL)),(K,Arr(BOOL,Arr(BOOL,BOOL))))
    def test_bool_self_choice(self):
        t,ty=r.check(ap(ap(ae(PT,BOOL),PT),PF))
        self.assertEqual(ty,BOOL)
        self.assertEqual(r.normalize(t)[0],K)
    def test_false_self_choice(self):
        t,ty=r.check(ap(ap(ae(PF,BOOL),PT),PF))
        self.assertEqual(ty,BOOL)
        self.assertEqual(r.normalize(t)[0],App(K,I))
    def test_true_has_distinct_observable_output(self):
        self.assertEqual(r.normalize(App(App(K,Z),O))[0],Z)
    def test_false_has_distinct_observable_output(self):
        self.assertEqual(r.normalize(App(App(App(K,I),Z),O))[0],O)
    def test_diagonal_shape_has_internal_code(self):
        t,ty=r.check(diagonal_proof())
        self.assertEqual(ty,diagonal_type())
        self.assertEqual(t,App(K,App(K,App(K,I))))
    def test_diagonal_shape_self_instantiates(self):
        t,ty=r.check(ae(diagonal_proof(),diagonal_type()))
        self.assertEqual(t,r.check(diagonal_proof())[0])
        self.assertEqual(ty,r.instantiate_type(diagonal_type()[1],diagonal_type()))
    def test_repeated_self_application(self):
        p=PID
        for _ in range(8): p=ap(ae(PID,ID),p)
        t,ty=r.check(p)
        self.assertEqual(ty,ID)
        self.assertEqual(r.normalize(t)[0],I)
    def test_family_of_all_type_instances(self):
        for ty in [BOT,ID,BOOL,Arr(ID,BOOL),All(Arr(V,BOOL)),diagonal_type()]:
            self.assertEqual(r.check(ae(PID,ty)),(I,Arr(ty,ty)))
    def test_capture_avoidance(self):
        body=All(Arr(('v',1),('v',0)))
        self.assertEqual(r.instantiate_type(body,('v',0)),All(Arr(('v',1),('v',0))))
    def test_substitution_beneath_two_binders(self):
        body=All(All(Arr(('v',2),('v',0))))
        self.assertEqual(r.instantiate_type(body,BOOL),All(All(Arr(BOOL,('v',0)))))
    def test_s_combinator(self):
        a,b,c=ID,BOOL,BOT
        p={'rule':'s','A':a,'B':b,'C':c}
        self.assertEqual(r.check(p),(S,Arr(Arr(a,Arr(b,c)),Arr(Arr(a,b),Arr(a,c)))))
    def test_s_beta(self):
        self.assertEqual(r.head_step(App(App(App(S,I),K),Z)),App(App(I,Z),App(K,Z)))
    def test_no_raw_untyped_self_application_rule(self):
        with self.assertRaises(r.Rejection): r.check(ap(PID,PID))
    def test_reject_empty_claim(self):
        with self.assertRaises(r.Rejection): r.check({'rule':'assert','term':I,'type':BOT})
    def test_reject_semantic_pass_marker(self):
        with self.assertRaises(r.Rejection): r.check({'rule':'semantic','status':'PASS','type':BOT})
    def test_reject_full_ambient_abstraction(self):
        with self.assertRaises(r.Rejection): r.check({'rule':'all_i','body':PID,'type_case':[I,K]})
    def test_reject_free_type_variable(self):
        with self.assertRaises(r.Rejection): r.check(ip(V))
    def test_reject_bad_type_tag(self):
        with self.assertRaises(r.Rejection): r.check(ip(('universe_in_itself',)))
    def test_reject_bad_type_index(self):
        with self.assertRaises(r.Rejection): r.check(ip(('v',True)))
    def test_reject_negative_index(self):
        with self.assertRaises(r.Rejection): r.check(ip(('v',-1)))
    def test_reject_application_mismatch(self):
        with self.assertRaises(r.Rejection): r.check(ap(ae(PID,ID),PT))
    def test_reject_all_elimination_on_arrow(self):
        with self.assertRaises(r.Rejection): r.check(ae(ip(ID),BOOL))
    def test_reject_extra_proof_fields(self):
        with self.assertRaises(r.Rejection): r.check(dict(PID, trusted=True))
    def test_actual_reduction_certificate(self):
        p=ap(ae(PID,ID),PID)
        self.assertEqual(r.check({'rule':'reduce','proof':p,'trace':[App(I,I),I]}),(I,ID))
    def test_forged_reduction_certificate_rejected(self):
        p=ap(ae(PID,ID),PID)
        with self.assertRaises(r.Rejection):
            r.check({'rule':'reduce','proof':p,'trace':[App(I,I),Z]})
    def test_certificate_cannot_change_start(self):
        with self.assertRaises(r.Rejection):
            r.check({'rule':'reduce','proof':PID,'trace':[Z]})
    def test_zero_and_one_are_normal_and_distinct(self):
        self.assertIsNone(r.head_step(Z)); self.assertIsNone(r.head_step(O))
        self.assertNotEqual(Z,O)
    def test_fuel_exhaustion_not_normal_form(self):
        w=App(App(S,I),I); omega=App(w,w)
        with self.assertRaises(r.FuelExhausted): r.normalize(omega,fuel=25)
    def test_normal_form_at_zero_fuel(self):
        self.assertEqual(r.normalize(I,fuel=0)[0],I)
    def test_redex_at_zero_fuel_rejected(self):
        with self.assertRaises(r.FuelExhausted): r.normalize(App(I,I),fuel=0)
    def test_source_can_be_json_arrays(self):
        self.assertEqual(r.check({'rule':'all_i','body':{'rule':'i','A':['v',0]}}),(I,ID))
    def test_input_not_mutated(self):
        p=diagonal_proof(); old=copy.deepcopy(p); r.check(p); self.assertEqual(p,old)

class InputAudit(unittest.TestCase):
    def test_shift_rejects_nested_non_type(self):
        with self.assertRaises(r.Rejection): r.shift_type(('arr',0,0),1)
    def test_substitution_rejects_nested_non_type(self):
        with self.assertRaises(r.Rejection): r.instantiate_type(('arr',0,0),BOT)
    def test_substitution_rejects_bad_unused_argument(self):
        with self.assertRaises(r.Rejection): r.instantiate_type(BOT,('invalid',))
    def test_shift_rejects_boolean_amount(self):
        with self.assertRaises(r.Rejection): r.shift_type(V,True)
    def test_shift_rejects_underflow(self):
        with self.assertRaises(r.Rejection): r.shift_type(V,-1)
    def test_bad_program_rejected(self):
        with self.assertRaises(r.Rejection): r.normalize(('app',I,7))
    def test_boolean_fuel_rejected(self):
        with self.assertRaises(r.Rejection): r.normalize(I,True)
    def test_negative_fuel_rejected(self):
        with self.assertRaises(r.Rejection): r.normalize(I,-1)
    def test_invalid_type_depth_rejected(self):
        with self.assertRaises(r.Rejection): r.check(PID,True)
    def test_deep_type_rejected(self):
        ty=BOT
        for _ in range(120): ty=All(ty)
        with self.assertRaises(r.Rejection): r.check(ip(ty))
    def test_deep_proof_rejected(self):
        p=PID
        for _ in range(120): p=ai(p)
        with self.assertRaises(r.Rejection): r.check(p)
    def test_reduction_needs_real_trace(self):
        with self.assertRaises(r.Rejection):
            r.check({'rule':'reduce','proof':PID,'trace':[]})
    def test_declared_free_type_variable_can_be_used(self):
        self.assertEqual(r.check(ip(V),1),(I,Arr(V,V)))
    def test_scope_still_rejects_index_beyond_declared_depth(self):
        with self.assertRaises(r.Rejection): r.check(ip(('v',1)),1)
    def test_scope_shift_does_not_capture_closed_type(self):
        self.assertEqual(r.shift_type(BOOL,1),BOOL)

if __name__=='__main__': unittest.main()

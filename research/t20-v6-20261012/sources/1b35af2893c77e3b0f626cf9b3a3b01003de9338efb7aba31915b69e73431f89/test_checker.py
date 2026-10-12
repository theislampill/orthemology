"""New attempt-0003 tests, NOT recovered or re-run attempt-0002 tests."""
import unittest
from checker import check, instantiate_term, instantiate_type, rename_type, rename_term, step_at, prove_conversion, compile_poly, export_finite, Refusal, normalise

B=('bot',)
V=lambda n: ('var',n)
T=lambda n: ('tv',n)
I=lambda A: ('I',A)
App=lambda f,x: ('app',f,x)
Pi=lambda A,B: ('pi',A,B)
Sig=lambda A,B: ('sig',A,B)
Id=lambda A,x,y: ('id',A,x,y)
Lam=lambda A,b: ('lam',A,b)
All=lambda A: ('all',A)

class Checking(unittest.TestCase):
    def accept(self,t,**kw):
        r=check(t,**kw); self.assertEqual(r.status,'ACCEPTED',r.reason); return r
    def refuse(self,t,**kw):
        r=check(t,**kw); self.assertEqual(r.status,'REFUSED'); return r
    def test_finite_identity(self):
        r=self.accept(('allI',I(T(0))))
        self.assertEqual(r.ty,All(Pi(T(0),T(0))))
    def test_dependent_identity_proof(self):
        r=self.accept(Lam(B,('refl',V(0))))
        self.assertEqual(r.ty,Pi(B,Id(B,V(0),V(0))))
    def test_closed_lambda(self):
        r=self.accept(Lam(B,V(0)));self.assertEqual(r.ty,Pi(B,B))
    def test_context_rejects_unbound(self):self.refuse(V(0))
    def test_context_rejects_type_forward_reference(self):self.refuse(V(0),context=(Id(B,V(0),V(0)),))
    def test_context_variable(self):self.assertEqual(self.accept(V(0),context=(B,)).ty,B)
    def test_type_generalisation_lifts_assumptions(self):
        # x:X cannot be generalised to forall X.X: its context type becomes tv1.
        r=self.accept(('allI',V(0)),context=(T(0),),type_depth=1)
        self.assertEqual(r.ty,All(T(1)))
    def test_application_rejects_wrong_domain(self):self.refuse(App(I(B),I(B)))
    def test_identity_self_instantiation(self):
        t=('allI',I(T(0)));ty=All(Pi(T(0),T(0)))
        self.accept(App(('allE',t,ty),t))
    def test_pair_and_projections(self):
        A=Pi(B,B);s=Sig(A,A);p=('pair',s,I(B),I(B))
        self.assertEqual(self.accept(('fst',p)).ty,A)
        self.assertEqual(self.accept(('snd',p)).ty,A)
    def test_sigma_eta_is_proof_not_general_raw_eta(self):
        A=Pi(B,B);s=Sig(A,A);p=('pair',s,I(B),I(B))
        r=self.accept(('eta',p));self.assertEqual(r.ty[0],'id')
        with self.assertRaises(Refusal):step_at(('eta',p),())
    def test_dependent_pair(self):
        A=Pi(B,B);s=Sig(A,Id(A,V(0),V(0)));a=I(B)
        p=('pair',s,a,('refl',a))
        self.accept(p)
        self.assertEqual(self.accept(('snd',p)).ty,Id(A,('fst',p),('fst',p)))
    def test_pair_wrong_fibre_refused(self):
        A=Pi(B,B);s=Sig(A,Id(A,V(0),V(0)))
        self.refuse(('pair',s,I(B),I(B)))
    def test_based_J_constant_motive(self):
        A=Pi(B,B);x=I(B);p=('refl',x);C=A;d=I(B)
        j=('J',A,x,C,d,x,p)
        self.assertEqual(self.accept(j).ty,A)
        self.assertEqual(step_at(j,()),d)
    def test_based_J_proof_coordinate_motive(self):
        A=Pi(B,B);x=I(B)
        # In motive context: p = var0, y = var1.
        C=Id(Id(A,x,V(1)),V(0),V(0))
        d=('refl',('refl',x))
        j=('J',A,x,C,d,x,('refl',x))
        self.accept(j)
    def test_J_bad_proof_refused(self):
        A=Pi(B,B);x=I(B)
        self.refuse(('J',A,x,A,x,x,I(B)))
    def test_explicit_type_equality_certificate(self):
        A=Pi(B,B);x=I(B);red=App(I(A),x)
        term=('refl',x)
        target=Id(A,red,red)
        r=self.accept(('cast',term,target,(),((2,),(3,))))
        self.assertEqual(r.ty,target)
    def test_bad_equality_path_refused(self):
        A=Pi(B,B);x=I(B)
        self.refuse(('cast',('refl',x),Id(A,x,x),((99,),),()))
    def test_malformed_bool_index(self):self.refuse(('var',True),context=(B,))
    def test_malformed_negative_index(self):self.refuse(('var',-1))
    def test_unknown_tag(self):self.refuse(('axiom','arbitrary'))
    def test_marker_not_typed(self):self.refuse(('zero',))
    def test_extra_field(self):self.refuse(('refl',I(B),'ignored'))
    def test_resource_refusal_is_not_inequality(self):
        r=self.refuse(Lam(B,V(0)),max_nodes=1)
        self.assertIn('RESOURCE',r.reason)
    def test_input_not_mutated(self):
        x=['lam',['bot'],['var',0]];before=repr(x);self.accept(x);self.assertEqual(repr(x),before)
    def test_cyclic_input_refused(self):
        a=['app'];a.extend([a,['I',['bot']]]);self.refuse(a)

class Substitution(unittest.TestCase):
    def test_capture_avoidance(self):
        self.assertEqual(instantiate_term(Lam(B,V(1)),V(0)),Lam(B,V(1)))
    def test_type_substitution_under_term_binder_lifts_term_endpoints(self):
        A=Id(B,V(0),V(0))
        self.assertEqual(instantiate_type(Pi(B,T(0)),A),Pi(B,Id(B,V(1),V(1))))
    def test_term_substitution_under_type_binder_lifts_annotations(self):
        body=('allI',V(0));arg=I(T(0))
        self.assertEqual(instantiate_term(body,arg),('allI',I(T(1))))
    def test_type_variable_shadowing(self):
        self.assertEqual(instantiate_type(All(T(0)),B),All(T(0)))
    def test_J_two_term_binders(self):
        t=('J',B,V(0),Id(B,V(2),V(2)),V(0),V(0),V(0))
        out=instantiate_term(t,I(B))
        self.assertEqual(out[3],Id(B,I(B),I(B)))
    def test_type_beta(self):
        t=('allE',('allI',I(T(0))),B)
        self.assertEqual(step_at(t,()),I(B))
    def test_annotation_renaming(self):
        self.assertEqual(rename_term(Lam(T(0),V(1)),lambda n:n+2,lambda n:n+1),Lam(T(1),V(3)))

class EvidenceAndExport(unittest.TestCase):
    def test_reflexive_certificate(self):self.assertTrue(prove_conversion(B,B,(),()))
    def test_nonreduction_address_rejected(self):
        with self.assertRaises(Refusal):step_at(I(B),())
    def test_normalisation_refuses_budget_without_false_equality(self):
        with self.assertRaises(Refusal):normalise(App(I(B),I(B)),0)
    def test_bracket_compiler_actual_code(self):
        self.assertEqual(compile_poly(Lam(B,V(0))),('i',))
    def test_finite_export_is_constructor_only(self):
        r=check(('allI',I(T(0))))
        e=export_finite(r)
        self.assertEqual(e['status'],'EXPORTABLE_FINITE')
        self.assertIn('Cert.allI',e['lean_certificate'])
        self.assertFalse(e['kernel_verified'])
    def test_dependent_type_cannot_enter_canonical_cert(self):
        r=check(Lam(B,('refl',V(0))))
        self.assertEqual(r.status,'ACCEPTED')
        e=export_finite(r)
        self.assertEqual(e['status'],'REFUSED_TARGET_VOCABULARY')
        self.assertFalse(e['kernel_verified'])
    def test_unaccepted_result_never_exported(self):
        self.assertEqual(export_finite(check(V(0)))['status'],'REFUSED_NOT_ACCEPTED')
    def test_open_export_domain_is_explicit(self):
        r=check(V(0),context=(B,))
        self.assertEqual(export_finite(r)['status'],'REFUSED_OPEN_CONTEXT')


class ExtraQualification(unittest.TestCase):
    def test_simply_typed_abstraction_exports(self):
        r=check(Lam(B,V(0)))
        self.assertEqual(export_finite(r)['status'],'EXPORTABLE_FINITE')
    def test_K_abstraction_with_older_variable(self):
        r=check(Lam(B,Lam(B,V(1))))
        self.assertEqual(export_finite(r)['status'],'EXPORTABLE_FINITE')
    def test_combinatory_S_abstraction(self):
        fTy=Pi(B,Pi(B,B));gTy=Pi(B,B)
        t=Lam(fTy,Lam(gTy,Lam(B,App(App(V(2),V(0)),App(V(1),V(0))))))
        r=check(t);self.assertEqual(r.status,'ACCEPTED',r.reason)
        self.assertEqual(export_finite(r)['status'],'EXPORTABLE_FINITE')
    def test_forged_result_rejected(self):
        from checker import Result
        r=Result('ACCEPTED','forged',B,V(0),(),0)
        self.assertEqual(export_finite(r)['status'],'REFUSED_RECHECK_MISMATCH')
    def test_source_injection_is_data_not_code(self):
        self.assertEqual(check(('I\naxiom forged : False',B)).status,'REFUSED')
    def test_two_sort_substitution_composition(self):
        from checker import substitute
        base=[V(0),V(2),T(0),I(T(0)),Id(T(0),V(0),V(1)),('allI',I(T(0)))]
        terms=list(base)
        for n in range(3):
            terms += [Lam(T(0),x) for x in base]
            terms += [All(x) for x in base if x[0] in ('tv','id')]
            base=[Lam(T(0),x) for x in base]
        sm=lambda n:Lam(T(0),V(0)) if n==0 else V(n+1)
        sy=lambda n:Id(B,V(0),V(0)) if n==0 else T(n+1)
        tm=lambda n:V(n+1)
        ty=lambda n:All(T(1)) if n==0 else T(n-1)
        for x in terms:
            left=substitute(substitute(x,sm,sy),tm,ty)
            right=substitute(x,lambda n:substitute(sm(n),tm,ty),lambda n:substitute(sy(n),tm,ty))
            self.assertEqual(left,right)
    def test_missing_conversion_is_refusal_not_not_convertible(self):
        A=Pi(B,B);x=I(B);red=App(I(A),x)
        r=check(('cast',('refl',x),Id(A,red,red),(),()))
        self.assertEqual(r.status,'REFUSED')
        self.assertEqual(r.reason,'CERTIFICATE_ENDPOINT_MISMATCH')

if __name__=='__main__':unittest.main()

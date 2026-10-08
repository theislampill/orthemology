/- All-rule original F/G soundness and exact compiled-fragment completeness
   for the separately declared finite-certificate extension. -/
import UnaryCertificateSyntax
import UnaryCurrentIdentityBoundary
import AllFiniteComparison

namespace P01AC.UnaryCertificate
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.EffectiveCompleteness P01AC.BooleanPrimitive
open P01AC.UnaryIdentity

def naturalFiniteCode : TypeCode :=
  .all (.arrow (.arrow (.var 0) (.var 0)) (.arrow (.var 0) (.var 0)))

theorem natural_is_finite : N = fin naturalFiniteCode := rfl
theorem carrier_is_finite : arr N N = fin (.arrow naturalFiniteCode naturalFiniteCode) := rfl

theorem compiled_eval_constant (e : Expr) (η : Env) :
    eval e.closed η = eval e.closed zeroEnv :=
  eval_closed (P01AC.has_scoped e.closed_has) η zeroEnv

/-- Specific valuation independence of the actual finite carrier and closed
    compiled endpoints. Empty-context E does NOT relate arbitrary valuations. -/
theorem certificate_all_valuations (e f : Expr) (c : Certificate)
    (hc : verifyCertificate e f c = true) (R : REnv) (η ξ : Env) :
    G (.identity (arr N N) e.closed f.closed) R η ξ .i .i := by
  have hz := (identityCheck_iff_G_identity e f).mp
    ((identityCheck_iff_valid e f).mpr (verifyCertificate_sound e f c hc)) R
  rw [G_identity] at hz ⊢
  simpa only [carrier_is_finite, F_fin, compiled_eval_constant] using hz


theorem form_sound {Γ A} (h : FormC Γ A) : FormSound Γ A := by
  induction h using FormC.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_3 := fun Γ p A _ => TermSound Γ p A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b => exact ⟨c,type_all c b.2.laws,b.2⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws b.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 a.2.laws b.2.laws c.2.laws⟩
    | finite τ bound hτ hA hf a t => exact ⟨t,fundamental_finite t.1 (fun n hn => (a n hn).2.laws) hf⟩
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro a.1 a.2.2.laws p.2⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,fun _ _ _ _ => Conv.refl _⟩
    | rawApp hA hf hx a f x => exact ⟨a,fun r η ξ e => conv_app (f.2 r η ξ e) (x.2 r η ξ e)⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 b.2⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro r η ξ e
        have dd := a.1.hends e
        exact a.2.laws.raw dd.1 dd.2 (P01DF.polyConv_sound pq η) (P01DF.polyConv_sound pq ξ) (p.2 r η ξ e)
    | certified e f c hTarget hcheck t =>
        exact ⟨t, fun R η ξ _ => certificate_all_valuations e f c hcheck R η ξ⟩


theorem has_sound {Γ p A} (h : HasC Γ p A) : TermSound Γ p A := by
  induction h using HasC.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_2 := fun Γ A _ => FormSound Γ A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | all hΓ hB c b => exact ⟨c,type_all c b.2.laws,b.2⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws b.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 a.2.laws b.2.laws c.2.laws⟩
    | finite τ bound hτ hA hf a t => exact ⟨t,fundamental_finite t.1 (fun n hn => (a n hn).2.laws) hf⟩
    | allIntro hAll hp a p => exact ⟨a,fundamental_all_intro a.1 a.2.2.laws p.2⟩
    | allElim hAll hA hTarget hp a x t p => exact ⟨t,fundamental_all_elim a.1 x.2.laws p.2⟩
    | rawAtom hA a => exact ⟨a,fun _ _ _ _ => Conv.refl _⟩
    | rawApp hA hf hx a f x => exact ⟨a,fun r η ξ e => conv_app (f.2 r η ξ e) (x.2 r η ξ e)⟩
    | piIntro hA hb hs a b => exact ⟨a,fundamental_pi_intro a.1 a.2.2.1.laws a.2.2.2.laws b.2⟩
    | piElim hPi ht hf ha pi t f a => exact ⟨t,fundamental_pi_elim f.2 a.2⟩
    | sigmaIntro hSigma ht ha hb s t a b =>
        exact ⟨s,fundamental_sigma_intro s.1 s.2.2.1.laws s.2.2.2.laws a.2 b.2⟩
    | sigmaFst hA hSigma hz a s z => exact ⟨a,fundamental_sigma_fst z.2⟩
    | sigmaSnd hSigma ht hz s t z => exact ⟨t,fundamental_sigma_snd z.2⟩
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro r η ξ e
        have dd := a.1.hends e
        exact a.2.laws.raw dd.1 dd.2 (P01DF.polyConv_sound pq η) (P01DF.polyConv_sound pq ξ) (p.2 r η ξ e)
    | certified e f c hTarget hcheck t =>
        exact ⟨t, fun R η ξ _ => certificate_all_valuations e f c hcheck R η ξ⟩


theorem context_sound {Γ} (h : CtxC Γ) : ContextLaws Γ := (form_sound (.raw h)).1

theorem fundamental {Γ p A} (h : HasC Γ p A) : Fundamental Γ p A := (has_sound h).2

theorem unary_fundamental {Γ p A} (h : HasC Γ p A) {ρ η ξ} (e : E Γ ρ η ξ) :
    F A ρ η (eval p η) (eval p ξ) :=
  (fundamental h).unary (has_sound h).1.1 (has_sound h).1.2.laws e

theorem strong_diagonal {Γ A} (h : FormC Γ A) {ρ η ξ} (e : E Γ ρ η ξ) (t u : Term) :
    G A (diagEnv ρ) η ξ t u ↔ F A ρ η t u := (form_sound h).2.laws.diagonal e t u

theorem two_sided_invariance {Γ A} (h : FormC Γ A) {r η η' ξ ξ'}
    (e : E Γ r.left η η') (f : E Γ r.right ξ ξ') (t u : Term) :
    G A r η ξ t u ↔ G A r η' ξ' t u := (form_sound h).2.laws.invariant e f t u


theorem certified_identity (e f : Expr) (c : Certificate)
    (hc : verifyCertificate e f c = true) :
    HasC [] (.atom .i) (.identity (arr N N) e.closed f.closed) :=
  .certified e f c (form_inclusion (identity_formed e f)) hc

theorem checked_identity (e f : Expr) (h : identityCheck e f = true) :
    HasC [] (.atom .i) (.identity (arr N N) e.closed f.closed) :=
  certified_identity e f (makeCertificate e)
    (makeCertificate_complete e f ((identityCheck_iff_valid e f).mp h))

/-- The converse uses full all-rule soundness of an arbitrary proof polynomial,
    not inversion restricted to the newly added certificate constructor. -/
theorem fragment_witness_iff_check (e f : Expr) :
    (∃ r : Poly, HasC [] r (.identity (arr N N) e.closed f.closed)) ↔
      identityCheck e f = true := by
  constructor
  · rintro ⟨r,hr⟩
    apply (identityCheck_iff_semantic_witness e f).mpr
    exact ⟨r, fun R => fundamental hr R zeroEnv zeroEnv ⟨rfl, rfl⟩⟩
  · intro h
    exact ⟨.atom .i, checked_identity e f h⟩

theorem fragment_I_iff_check (e f : Expr) :
    HasC [] (.atom .i) (.identity (arr N N) e.closed f.closed) ↔
      identityCheck e f = true :=
  ⟨fun h => (fragment_witness_iff_check e f).mp ⟨.atom .i,h⟩,
    checked_identity e f⟩

theorem fragment_witness_iff_F_identity (e f : Expr) :
    (∃ r : Poly, HasC [] r (.identity (arr N N) e.closed f.closed)) ↔
      ∀ ρ, F (.identity (arr N N) e.closed f.closed) ρ zeroEnv .i .i :=
  (fragment_witness_iff_check e f).trans (identityCheck_iff_F_identity e f)

theorem fragment_witness_iff_G_identity (e f : Expr) :
    (∃ r : Poly, HasC [] r (.identity (arr N N) e.closed f.closed)) ↔
      ∀ R : REnv, G (.identity (arr N N) e.closed f.closed) R zeroEnv zeroEnv .i .i :=
  (fragment_witness_iff_check e f).trans (identityCheck_iff_G_identity e f)

theorem fragment_witness_iff_denote (e f : Expr) :
    (∃ r : Poly, HasC [] r (.identity (arr N N) e.closed f.closed)) ↔
      ∀ n, e.denote n = f.denote n :=
  (fragment_witness_iff_check e f).trans (identityCheck_iff_denote e f)

theorem fragment_rejects_unequal (e f : Expr) (h : identityCheck e f = false) :
    ¬ ∃ r : Poly, HasC [] r (.identity (arr N N) e.closed f.closed) := by
  intro hw
  have ht := (fragment_witness_iff_check e f).mp hw
  rw [h] at ht
  cases ht

theorem erase_checked_identity (e f : Expr) (h : identityCheck e f = true) :
    HasC [] (.atom .i) .raw :=
  .proofErase (form_inclusion (.raw .nil)) (form_inclusion (identity_formed e f))
    (checked_identity e f h)

/-- A genuinely new certificate is consumed by the retained J constructor.
    The full all-rule theorem also covers arbitrary dependent motives. -/
theorem j_checked_identity_raw (e f : Expr) (h : identityCheck e f = true) :
    HasC [] (jPoly (.atom .i) f.closed (.atom .i)) .raw := by
  have hA : P01AC.Form [] (arr N N) := form_arr (N_form .nil) (N_form .nil)
  have hθ := P01AC.ctx_theta P01AC.Ctx.nil hA e.closed_has
  exact HasC.j (form_inclusion hA) (form_inclusion (.raw hθ))
    (form_inclusion (identity_formed e f))
    (form_inclusion (.raw .nil)) (form_inclusion (.raw .nil))
    (has_inclusion e.closed_has) (has_inclusion f.closed_has)
    (checked_identity e f h) (has_inclusion (.rawAtom (.raw .nil)))

theorem strict_current_extension :
    HasC [] (.atom .i) (.identity (arr N N)
      IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) ∧
    ¬ ∃ r : Poly, P01AC.Has [] r (.identity (arr N N)
      IntensionalBoundary.variableExpr.closed IntensionalBoundary.redundantExpr.closed) :=
  ⟨checked_identity _ _ IntensionalBoundary.checker_accepts,
    IntensionalBoundary.no_current_identity_witness⟩

#print axioms certificate_all_valuations
#print axioms has_sound
#print axioms fragment_witness_iff_check
#print axioms j_checked_identity_raw
#print axioms strict_current_extension
end P01AC.UnaryCertificate

/- All-rule soundness of the isolated, unadopted finite extensional candidate.
   Every semantic interface here is the original P01AC F/G interpretation. -/
import ExtensionalRepairSyntax
import AllSoundness

namespace P01AC.ExtensionalRepair
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open Intensional.Plus (PolyConvPlus polyConvPlus_sound)

/-- Identity introduction uses the unchanged raw saturation law, now supplied
    with the imported eight-generator conversion relation's evaluation theorem. -/
theorem fundamental_identity_intro_plus {Γ A p q}
    (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (hp : Fundamental Γ p A) (pq : PolyConvPlus p q) :
    Fundamental Γ (.atom .i) (.identity A p q) := by
  intro r η ξ h
  have dd := hc.hends h
  have pp := ha.ends dd.1 dd.2 (hp r η ξ h)
  exact ⟨(ha.per dd.1).raw (.refl _) (polyConvPlus_sound pq η) pp.1,
    (ha.per dd.2).raw (.refl _) (polyConvPlus_sound pq ξ) pp.2,.refl _,.refl _⟩

/-- The Pi case establishes the full cross-argument relation.  Pointwise
    endpoint equality comes from h; q's membership supplies the x-to-y step. -/
theorem fundamental_pi_ext {Γ A B p q h}
    (ha : FormSound Γ A) (hb : FormSound (A :: Γ) B)
    (hq : TermSound Γ q (.pi A B))
    (hh : TermSound Γ h (.pi A (.identity B
      (.app (pren Nat.succ p) (.var 0))
      (.app (pren Nat.succ q) (.var 0))))) :
    Fundamental Γ (.atom .i) (.identity (.pi A B) p q) := by
  have unary : ∀ {ρ η}, D Γ ρ η →
      F (.pi A B) ρ η (eval p η) (eval q η) := by
    intro ρ η d
    have qq := hq.2.unary hq.1.1 hq.1.2.laws (ha.1.refl d)
    have hh' := hh.2.unary hh.1.1 hh.1.2.laws (ha.1.refl d)
    intro x y xy
    have dx : D (A :: Γ) ρ (cons x η) := ⟨d,(ha.2.laws.per d).left xy⟩
    have pointwise : F B ρ (cons x η)
        (.app (eval p η) x) (.app (eval q η) x) := by
      simpa only [eval, eval_ren, cons] using (hh' x y xy).1
    exact (hb.2.laws.per dx).trans pointwise (qq x y xy)
  intro r η ξ e
  have dd := ha.1.hends e
  exact ⟨unary dd.1,unary dd.2,.refl _,.refl _⟩

/-- The All case retains both endpoint-uniformity clauses from the outer
    endpoint typings, while h supplies equality at every unary PER. -/
theorem fundamental_all_ext {Γ B p q h}
    (hp : TermSound Γ p (.all B)) (hq : TermSound Γ q (.all B))
    (hh : TermSound (twkTel Γ) h (.identity B p q)) :
    Fundamental Γ (.atom .i) (.identity (.all B) p q) := by
  have unary : ∀ {ρ η}, D Γ ρ η →
      F (.all B) ρ η (eval p η) (eval q η) := by
    intro ρ η d
    have pp := hp.2.unary hp.1.1 hp.1.2.laws (hp.1.1.refl d)
    have qq := hq.2.unary hq.1.1 hq.1.2.laws (hq.1.1.refl d)
    refine ⟨pp.1,qq.1,?_⟩
    intro P
    have dt : D (twkTel Γ) (cons P ρ) η := by
      rw [D_twk]
      exact d
    exact (hh.2.unary hh.1.1 hh.1.2.laws (hh.1.1.refl dt)).1
  intro r η ξ e
  have dd := hp.1.1.hends e
  exact ⟨unary dd.1,unary dd.2,.refl _,.refl _⟩

theorem form_sound {Γ A} (h : FormE Γ A) : FormSound Γ A := by
  induction h using FormE.rec
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
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro_plus a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro r η ξ e
        have dd := a.1.hends e
        exact a.2.laws.raw dd.1 dd.2 (polyConvPlus_sound pq η) (polyConvPlus_sound pq ξ) (p.2 r η ξ e)
    | piExt hA hB hPi hp hq hM hPiM hh hTarget sp sq sh sA sB
        a b pi p q m pim h t =>
        exact ⟨t,fundamental_pi_ext a b q h⟩
    | allExt hB hAll hp hq hN hh hTarget sp sq sh sB
        b all p q n h t =>
        exact ⟨t,fundamental_all_ext p q h⟩


theorem has_sound {Γ p A} (h : HasE Γ p A) : TermSound Γ p A := by
  induction h using HasE.rec
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
    | identityIntro hId hp hq pq a p q => exact ⟨a,fundamental_identity_intro_plus a.1 a.2.2.laws p.2 pq⟩
    | proofErase hRaw hId hp a i p => exact ⟨a,fundamental_proof_erase p.2⟩
    | j hA hB hId hBase hTarget hx hy he hd a b i base t x y e d =>
        exact ⟨t,fundamental_j a.1 a.2.laws b.2.laws t.2.laws e.2 d.2⟩
    | conv hA hp pq hs a p =>
        refine ⟨a,?_⟩
        intro r η ξ e
        have dd := a.1.hends e
        exact a.2.laws.raw dd.1 dd.2 (polyConvPlus_sound pq η) (polyConvPlus_sound pq ξ) (p.2 r η ξ e)
    | piExt hA hB hPi hp hq hM hPiM hh hTarget sp sq sh sA sB
        a b pi p q m pim h t =>
        exact ⟨t,fundamental_pi_ext a b q h⟩
    | allExt hB hAll hp hq hN hh hTarget sp sq sh sB
        b all p q n h t =>
        exact ⟨t,fundamental_all_ext p q h⟩


theorem context_sound {Γ} (h : CtxE Γ) : ContextLaws Γ := (form_sound (.raw h)).1

theorem fundamental {Γ p A} (h : HasE Γ p A) : Fundamental Γ p A := (has_sound h).2

theorem unary_fundamental {Γ p A} (h : HasE Γ p A) {ρ η ξ} (e : E Γ ρ η ξ) :
    F A ρ η (eval p η) (eval p ξ) :=
  (fundamental h).unary (has_sound h).1.1 (has_sound h).1.2.laws e

theorem strong_diagonal {Γ A} (h : FormE Γ A) {ρ η ξ} (e : E Γ ρ η ξ) (t u : Term) :
    G A (diagEnv ρ) η ξ t u ↔ F A ρ η t u := (form_sound h).2.laws.diagonal e t u

theorem two_sided_invariance {Γ A} (h : FormE Γ A) {r η η' ξ ξ'}
    (e : E Γ r.left η η') (f : E Γ r.right ξ ξ') (t u : Term) :
    G A r η ξ t u ↔ G A r η' ξ' t u := (form_sound h).2.laws.invariant e f t u

end P01AC.ExtensionalRepair

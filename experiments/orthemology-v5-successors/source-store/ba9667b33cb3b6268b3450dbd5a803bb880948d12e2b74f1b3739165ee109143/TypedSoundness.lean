/- Simultaneous finite-derivation soundness. No semantic law is a syntax premise. -/
import TypedConstants
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R

/-- Hereditary conclusions retain precisely the smaller formation results needed
    by term rules. They are outputs of the mutual derivation recursion. -/
def Hereditary (Γ : Tel) (A : Ty) : Prop := TypeLaws Γ A ∧ match A with
  | .pi A B | .sigma A B => Hereditary Γ A ∧ Hereditary (A :: Γ) B
  | .identity A _ _ => Hereditary Γ A
  | _ => True

abbrev FormSound (Γ : Tel) (A : Ty) := ContextLaws Γ ∧ Hereditary Γ A
abbrev TermSound (Γ : Tel) (p : Poly) (A : Ty) := FormSound Γ A ∧ Fundamental Γ p A

theorem Hereditary.laws {Γ A} (h : Hereditary Γ A) : TypeLaws Γ A := by cases A <;> exact h.1

theorem form_sound {Γ A} (h : Form Γ A) : FormSound Γ A := by
  induction h using Form.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_3 := fun Γ p A _ => TermSound Γ p A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | allFinite hΓ c => exact ⟨c,type_allFinite _ _,trivial⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws b.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 a.2.laws b.2.laws c.2.laws⟩
    | finite hA hf a => exact ⟨a,fundamental_finite hf⟩
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

theorem has_sound {Γ p A} (h : Has Γ p A) : TermSound Γ p A := by
  induction h using Has.rec
    (motive_1 := fun Γ _ => ContextLaws Γ)
    (motive_2 := fun Γ A _ => FormSound Γ A) with
    | nil => exact context_nil
    | ext hΓ hA c a => exact context_ext c a.2.laws
    | param hΓ c => exact ⟨c,type_param _ _,trivial⟩
    | bottom hΓ c => exact ⟨c,type_bottom _,trivial⟩
    | allFinite hΓ c => exact ⟨c,type_allFinite _ _,trivial⟩
    | raw hΓ c => exact ⟨c,type_raw _,trivial⟩
    | pi hA hB a b => exact ⟨a.1,type_pi a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | sigma hA hB a b => exact ⟨a.1,type_sigma a.1 a.2.laws b.2.laws,a.2,b.2⟩
    | identity hA hp hq a p q => exact ⟨a.1,type_identity a.1 a.2.laws p.2 q.2,a.2⟩
    | var hA hv a => exact ⟨a,fundamental_var hv⟩
    | i hA ht a t => exact ⟨t,fundamental_i a.1 a.2.laws⟩
    | k hA hB ht a b t => exact ⟨t,fundamental_k a.1 a.2.laws b.2.laws⟩
    | s hA hB hC ht a b c t => exact ⟨t,fundamental_s a.1 a.2.laws b.2.laws c.2.laws⟩
    | finite hA hf a => exact ⟨a,fundamental_finite hf⟩
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

theorem context_sound {Γ} (h : Ctx Γ) : ContextLaws Γ := (form_sound (.raw h)).1

theorem fundamental {Γ p A} (h : Has Γ p A) : Fundamental Γ p A := (has_sound h).2

theorem unary_fundamental {Γ p A} (h : Has Γ p A) {ρ η ξ} (e : E Γ ρ η ξ) :
    F A ρ η (eval p η) (eval p ξ) :=
  (fundamental h).unary (has_sound h).1.1 (has_sound h).1.2.laws e

theorem strong_diagonal {Γ A} (h : Form Γ A) {ρ η ξ} (e : E Γ ρ η ξ) (t u : Term) :
    G A (diagEnv ρ) η ξ t u ↔ F A ρ η t u := (form_sound h).2.laws.diagonal e t u

theorem two_sided_invariance {Γ A} (h : Form Γ A) {r η η' ξ ξ'}
    (e : E Γ r.left η η') (f : E Γ r.right ξ ξ') (t u : Term) :
    G A r η ξ t u ↔ G A r η' ξ' t u := (form_sound h).2.laws.invariant e f t u

end P01TC

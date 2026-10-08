/- Genuine All laws from the smaller body's formation-law conclusion. -/
import AllTermLemmas
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def Uniform (B : Ty) (ρ : OEnv) (η : Env) (t : Term) : Prop :=
  ∀ (P Q : PER) (R : Link P Q), G B (extendEnv R (diagEnv ρ)) η η t t

theorem all_uniform_transport {Γ B} (hb : TypeLaws (twkTel Γ) B)
    {ρ η ξ} (e : E Γ ρ η ξ) (t : Term) : Uniform B ρ η t ↔ Uniform B ρ ξ t := by
  have step : ∀ (P Q : PER) (R : Link P Q),
      G B (extendEnv R (diagEnv ρ)) η η t t ↔ G B (extendEnv R (diagEnv ρ)) ξ ξ t t := by
    intro P Q R
    apply hb.invariant
    · simpa only [extendEnv,diagEnv,E_twk] using e
    · simpa only [extendEnv,diagEnv,E_twk] using e
  exact ⟨fun h P Q R => (step P Q R).mp (h P Q R), fun h P Q R => (step P Q R).mpr (h P Q R)⟩

theorem all_per {Γ B} (hb : TypeLaws (twkTel Γ) B) {ρ η} (d : D Γ ρ η) :
    RelLaws (F (.all B) ρ η) := by
  have bd : ∀ P, D (twkTel Γ) (cons P ρ) η := fun P => (D_twk Γ P ρ η).symm ▸ d
  exact {
    sym := fun h => ⟨h.2.1,h.1,fun P => (hb.per (bd P)).sym (h.2.2 P)⟩
    trans := fun h k => ⟨h.1,k.2.1,fun P => (hb.per (bd P)).trans (h.2.2 P) (k.2.2 P)⟩
    raw := by
      intro t u t' u' ct cu h
      refine ⟨?_,?_,fun P => (hb.per (bd P)).raw ct cu (h.2.2 P)⟩
      · intro P Q R
        exact hb.raw (bd P) (bd Q) ct ct (h.1 P Q R)
      · intro P Q R
        exact hb.raw (bd P) (bd Q) cu cu (h.2.1 P Q R) }

theorem all_transport {Γ B} (hb : TypeLaws (twkTel Γ) B) {ρ η ξ}
    (e : E Γ ρ η ξ) (t u : Term) : F (.all B) ρ η t u ↔ F (.all B) ρ ξ t u := by
  have b : (∀ P, F B (cons P ρ) η t u) ↔ ∀ P, F B (cons P ρ) ξ t u := by
    apply forall_congr'
    intro P
    exact hb.transport ((E_twk Γ P ρ η ξ).symm ▸ e) t u
  exact and_congr (all_uniform_transport hb e t) (and_congr (all_uniform_transport hb e u) b)

theorem type_all {Γ B} (hc : ContextLaws Γ) (hb : TypeLaws (twkTel Γ) B) :
    TypeLaws Γ (.all B) where
  per := all_per hb
  transport := all_transport hb
  ends := by intro r η ξ _ _ t u h; exact ⟨h.1,h.2.1⟩
  respect := by
    intro r η ξ dη dξ t t' u u' ht hu h
    refine ⟨(all_per hb dη).right ht,(all_per hb dξ).right hu,?_⟩
    intro P Q R
    exact hb.respect ((D_twk Γ P r.left η).symm ▸ dη)
      ((D_twk Γ Q r.right ξ).symm ▸ dξ) (ht.2.2 P) (hu.2.2 Q) (h.2.2 P Q R)
  invariant := by
    intro r η η' ξ ξ' e f t u
    have b : (∀ (P Q : PER) (R : Link P Q), G B (extendEnv R r) η ξ t u) ↔
        ∀ (P Q : PER) (R : Link P Q), G B (extendEnv R r) η' ξ' t u := by
      apply forall_congr'; intro P
      apply forall_congr'; intro Q
      apply forall_congr'; intro R
      exact hb.invariant ((E_twk Γ P r.left η η').symm ▸ e)
        ((E_twk Γ Q r.right ξ ξ').symm ▸ f) t u
    exact and_congr (all_transport hb e t t) (and_congr (all_transport hb f u u) b)
  diagonal := by
    intro ρ η ξ e t u
    have ds := hc.ends e
    have be : ∀ P, E (twkTel Γ) (cons P ρ) η ξ := fun P => (E_twk Γ P ρ η ξ).symm ▸ e
    constructor
    · intro h
      refine ⟨h.1.1,(all_uniform_transport hb e u).mpr h.2.1.1,?_⟩
      intro P
      apply (hb.diagonal (be P) t u).mp
      simpa only [extend_diag] using h.2.2 P P (diagonal P)
    · intro h
      refine ⟨(all_per hb ds.1).left h,
        (all_transport hb e u u).mp ((all_per hb ds.1).right h),?_⟩
      intro P Q R
      have bη : D (twkTel Γ) (cons P ρ) η := (D_twk Γ P ρ η).symm ▸ ds.1
      have bξ : D (twkTel Γ) (cons Q ρ) ξ := (D_twk Γ Q ρ ξ).symm ▸ ds.2
      have ut : G B (extendEnv R (diagEnv ρ)) η ξ t t :=
        (hb.invariant ((E_twk Γ P ρ η η).symm ▸ hc.refl ds.1) (be Q) t t).mp (h.1 P Q R)
      exact hb.respect bη bξ ((hb.per bη).left (h.2.2 P))
        ((hb.transport (be Q) t u).mp (h.2.2 Q)) ut

end P01AC

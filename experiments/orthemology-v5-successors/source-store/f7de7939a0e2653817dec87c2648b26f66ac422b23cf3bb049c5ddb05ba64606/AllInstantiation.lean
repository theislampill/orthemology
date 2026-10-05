/- Lawful frozen parameter environments, derived solely from smaller formation laws. -/
import AllFiniteComparison
import AllSemanticSubstitution
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def imageEnv {Γ : Tel} {τ : Nat → Ty} (h : ∀ n, TypeLaws Γ (τ n)) (r : REnv) {η ξ}
    (dη : D Γ r.left η) (dξ : D Γ r.right ξ) : REnv where
  left := fun n => objectOf (h n) dη
  right := fun n => objectOf (h n) dξ
  rel := fun n => G (τ n) r η ξ
  endpoints := fun n => (h n).ends dη dξ
  respect := fun n => (h n).respect dη dξ

theorem imageEnv_match {Γ : Tel} {τ : Nat → Ty} (hc : ContextLaws Γ) (h : ∀ n, TypeLaws Γ (τ n))
    {r η ξ} (dη : D Γ r.left η) (dξ : D Γ r.right ξ) :
    ImageMatch τ r η ξ (imageEnv h r dη dξ) where
  left := fun _ _ _ => rfl
  right := fun _ _ _ => rfl
  cross := fun _ _ _ => rfl
  diagLeft := fun n t u => propext ((h n).diagonal (hc.refl dη) t u)
  diagRight := fun n t u => propext ((h n).diagonal (hc.refl dξ) t u)

theorem semantic_tsubst {Γ : Tel} {τ : Nat → Ty} (hc : ContextLaws Γ) (h : ∀ n, TypeLaws Γ (τ n))
    (B : Ty) {r η ξ} (dη : D Γ r.left η) (dξ : D Γ r.right ξ) (t u : Term) :
    G (tsubst τ B) r η ξ t u = G B (imageEnv h r dη dξ) η ξ t u :=
  (FG_mixed B Poly.var τ r η ξ _ (imageEnv_match hc h dη dξ)).2.2 t u

theorem top_image_match {Γ A} (hc : ContextLaws Γ) (h : TypeLaws Γ A)
    {r η ξ} (dη : D Γ r.left η) (dξ : D Γ r.right ξ) :
    ImageMatch (cons A Ty.param) r η ξ (extendEnv (linkOf h dη dξ) r) where
  left := by intro n t u; cases n <;> rfl
  right := by intro n t u; cases n <;> rfl
  cross := by intro n t u; cases n <;> rfl
  diagLeft := by
    intro n t u; cases n with
    | zero => exact propext (h.diagonal (hc.refl dη) t u)
    | succ n => rfl
  diagRight := by
    intro n t u; cases n with
    | zero => exact propext (h.diagonal (hc.refl dξ) t u)
    | succ n => rfl

theorem G_tinst {Γ A} (hc : ContextLaws Γ) (h : TypeLaws Γ A)
    (B : Ty) {r η ξ} (dη : D Γ r.left η) (dξ : D Γ r.right ξ) (t u : Term) :
    G (tinst B A) r η ξ t u = G B (extendEnv (linkOf h dη dξ) r) η ξ t u :=
  (FG_mixed B Poly.var (cons A Ty.param) r η ξ _ (top_image_match hc h dη dξ)).2.2 t u

theorem F_tinst {Γ A} (hc : ContextLaws Γ) (h : TypeLaws Γ A)
    (B : Ty) {ρ η} (d : D Γ ρ η) (t u : Term) :
    F (tinst B A) ρ η t u = F B (cons (objectOf h d) ρ) η t u :=
  (FG_mixed B Poly.var (cons A Ty.param) (diagEnv ρ) η η _ (top_image_match hc h d d)).1 t u

theorem fundamental_all_intro {Γ B p} (hc : ContextLaws Γ) (hb : TypeLaws (twkTel Γ) B)
    (ht : Fundamental (twkTel Γ) p B) : Fundamental Γ p (.all B) := by
  intro r η ξ h
  have ds := hc.hends h
  have self : ∀ {ρ ζ}, D Γ ρ ζ → F (.all B) ρ ζ (eval p ζ) (eval p ζ) := by
    intro ρ ζ d
    have uni : Uniform B ρ ζ (eval p ζ) := by
      intro P Q R
      apply ht
      rw [H_twk]
      exact hc.diagonal.mpr (hc.refl d)
    refine ⟨uni,uni,?_⟩
    intro P
    apply (hb.diagonal ((E_twk Γ P ρ ζ ζ).symm ▸ hc.refl d) _ _).mp
    simpa only [extend_diag] using uni P P (diagonal P)
  refine ⟨self ds.1,self ds.2,?_⟩
  intro P Q R
  exact ht (extendEnv R r) η ξ ((H_twk Γ R r η ξ).symm ▸ h)

theorem fundamental_all_elim {Γ B A p} (hc : ContextLaws Γ) (ha : TypeLaws Γ A)
    (ht : Fundamental Γ p (.all B)) : Fundamental Γ p (tinst B A) := by
  intro r η ξ h
  have ds := hc.hends h
  rw [G_tinst hc ha B ds.1 ds.2]
  exact (ht r η ξ h).2.2 _ _ (linkOf ha ds.1 ds.2)

/-- Outside a finite image table the image is syntactically Bottom. -/
theorem typeImages_beyond (τ : List Ty) {n : Nat} (hn : τ.length ≤ n) : typeImages τ n = .bottom := by
  induction τ generalizing n with
  | nil => rfl
  | cons A τ ih =>
      cases n with
      | zero => exact False.elim (Nat.not_succ_le_zero _ hn)
      | succ n => exact ih (Nat.le_of_succ_le_succ hn)

theorem finite_image_laws {Γ τ} (h : ∀ n, n < τ.length → TypeLaws Γ (typeImages τ n)) :
    ∀ n, TypeLaws Γ (typeImages τ n) := by
  intro n
  by_cases hn : n < τ.length
  · exact h n hn
  · rw [typeImages_beyond τ (Nat.le_of_not_gt hn)]
    exact type_bottom Γ

theorem fundamental_finite {Γ C t τ} (hc : ContextLaws Γ)
    (h : ∀ n, n < τ.length → TypeLaws Γ (typeImages τ n)) (ht : FiniteDerives t C) :
    Fundamental Γ (.atom t) (tsubst (typeImages τ) (fin C)) := by
  intro r η ξ e
  have ds := hc.hends e
  rw [semantic_tsubst hc (finite_image_laws h) (fin C) ds.1 ds.2,G_fin]
  exact finite_fundamental ht _

end P01AC

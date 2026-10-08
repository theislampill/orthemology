/- Exact mixed interpretation uses joint parameter/term valuations. Replacement
   PERs depend on the target valuation; no fixed-parameter shortcut is used. -/
import AllRepresentation
namespace P01AC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

theorem MixedTerms.related {Δ Γ σ τ} (hs : MixedTerms Δ τ Γ σ)
    (hc : ContextLaws Δ) (hl : ∀ n, TypeLaws Δ (τ n)) {r η ξ} (e : H Δ r η ξ) :
    H Γ (imageEnv hl r (hc.hends e).1 (hc.hends e).2) (subEnv σ η) (subEnv σ ξ) := by
  induction hs with
  | nil hΔ => exact ⟨rfl,rfl⟩
  | @cons Γ σ A a hs hA ha ih =>
      rw [subEnv_cons,subEnv_cons]
      refine ⟨ih,?_⟩
      have v := fundamental ha r η ξ e
      rw [(FG_mixed A (images σ) τ r η ξ _ (imageEnv_match hc hl (hc.hends e).1 (hc.hends e).2)).2.2] at v
      exact v

theorem imageEnv_diagonal {Δ : Tel} {τ : Nat → Ty} (hc : ContextLaws Δ) (hl : ∀ n, TypeLaws Δ (τ n))
    {ρ η ξ} (e : E Δ ρ η ξ) :
    imageEnv hl (diagEnv ρ) (hc.ends e).1 (hc.ends e).2 =
      diagEnv (fun n => objectOf (hl n) (hc.ends e).1) := by
  apply renv_ext
  · rfl
  · funext n; apply per_ext; intro t u
    exact ((hl n).transport e t u).symm
  · funext n t u
    exact propext ((hl n).diagonal e t u)

/-- Parameter environments are explicit coordinates, with equality required by
    this unary intrinsic context. Heterogeneous transport remains in G/imageEnv. -/
def jointContext (Γ : Tel) (hc : ContextLaws Γ) : P01D.Context where
  Val := Σ ρ : OEnv, {η : Env // D Γ ρ η}
  eqv := fun x y => x.1 = y.1 ∧ E Γ x.1 x.2.val y.2.val
  refl := fun x => ⟨rfl,hc.refl x.2.property⟩
  sym := by
    intro x y h
    refine ⟨h.1.symm,?_⟩
    exact (congrArg (fun ρ => E Γ ρ y.2.val x.2.val) h.1) ▸ hc.sym h.2
  trans := by
    intro x y z h k
    refine ⟨h.1.trans k.1,hc.trans h.2 ?_⟩
    exact (congrArg (fun ρ => E Γ ρ y.2.val z.2.val) h.1.symm) ▸ k.2
  environment := fun x => x.2.val

def jointType {Γ A} (ha : Form Γ A) : P01D.Ty (jointContext Γ (form_sound ha).1) where
  obj := fun x => objectOf (form_sound ha).2.laws x.2.property
  coherent := by
    intro x y h
    apply per_ext
    intro t u
    change F A x.1 x.2.val t u ↔ F A y.1 y.2.val t u
    exact ((form_sound ha).2.laws.transport h.2 t u).trans
      (Iff.of_eq (congrArg (fun ρ => F A ρ y.2.val t u) h.1))

def jointTerm {Γ p A} (hp : Has Γ p A) :
    P01D.Tm (jointContext Γ (form_sound (has_form hp)).1) (jointType (has_form hp)) where
  code := p
  valid := by intro x y h; exact unary_fundamental hp h.2

theorem jointTerm_code {Γ p A} (hp : Has Γ p A) : (jointTerm hp).code = p := rfl

def MixedSub.imageObjects {Δ Γ σ τ} (hs : MixedSub Δ Γ σ τ) (ρ : OEnv)
    (η : Env) (d : D Δ ρ η) : OEnv :=
  fun n => objectOf (form_sound (hs.typeForm n)).2.laws d

theorem MixedSub.imageObjects_equal {Δ Γ σ τ} (hs : MixedSub Δ Γ σ τ)
    {ρ η ξ} (e : E Δ ρ η ξ) :
    hs.imageObjects ρ η ((context_sound hs.target).ends e).1 =
      hs.imageObjects ρ ξ ((context_sound hs.target).ends e).2 := by
  funext n
  apply per_ext
  exact (form_sound (hs.typeForm n)).2.laws.transport e

theorem MixedSub.respects {Δ Γ σ τ} (hs : MixedSub Δ Γ σ τ)
    {ρ η ξ} (e : E Δ ρ η ξ) :
    E Γ (hs.imageObjects ρ η ((context_sound hs.target).ends e).1) (subEnv σ η) (subEnv σ ξ) := by
  let hc := context_sound hs.target
  let hl := fun n => (form_sound (hs.typeForm n)).2.laws
  have v := hs.terms.related hc hl (hc.diagonal.mpr e)
  rw [imageEnv_diagonal hc hl e] at v
  exact (context_sound hs.source).diagonal.mp v

theorem MixedSub.valid {Δ Γ σ τ} (hs : MixedSub Δ Γ σ τ)
    {ρ η} (d : D Δ ρ η) : D Γ (hs.imageObjects ρ η d) (subEnv σ η) :=
  ((context_sound hs.source).ends (hs.respects ((context_sound hs.target).refl d))).1

/-- The source joint context can vary its parameter environment with η. -/
def representedMixedSub {Δ Γ σ τ} (hs : MixedSub Δ Γ σ τ) (ρ : OEnv) :
    P01D.Sub (representedContext Δ ρ (context_sound hs.target)) (jointContext Γ (context_sound hs.source)) where
  map := fun η => ⟨hs.imageObjects ρ η.val η.property,subEnv σ η.val,hs.valid η.property⟩
  respects := fun h => ⟨hs.imageObjects_equal h,hs.respects h⟩
  code := images σ
  tracks := fun _ _ => rfl

theorem represented_mixed_code {Δ Γ σ τ p A} (hs : MixedSub Δ Γ σ τ)
    (hp : Has Γ p A) (ρ : OEnv) :
    ((jointTerm hp).subst (representedMixedSub hs ρ)).code = psub (images σ) p := rfl

theorem represented_mixed_type {Δ Γ σ τ A} (hs : MixedSub Δ Γ σ τ)
    (ha : Form Γ A) (ρ : OEnv) :
    (jointType ha).pull (representedMixedSub hs ρ) = representedType (hs.form ha) ρ := by
  apply intrinsic_type_ext
  intro η
  apply per_ext
  intro t u
  exact (Iff.of_eq ((FG_mixed A (images σ) (typeImages τ) (diagEnv ρ) η.val η.val _
    (imageEnv_match (context_sound hs.target) (fun n => (form_sound (hs.typeForm n)).2.laws)
      η.property η.property)).1 t u)).symm

end P01AC

/- Exact source-code representation in the accepted intrinsic contextual core. -/
import TypedSoundness
import TypedStructural
namespace P01TC
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)

def subEnv (σ : List Poly) (η : Env) : Env := fun n => eval (images σ n) η

@[simp] theorem subEnv_nil (η : Env) : subEnv [] η = zeroEnv := rfl
@[simp] theorem subEnv_cons (a : Poly) (σ : List Poly) (η : Env) :
    subEnv (a :: σ) η = cons (eval a η) (subEnv σ η) := eval_cons_poly a (images σ) η

theorem TypedSub.related {Δ Γ σ} (hs : TypedSub Δ Γ σ) {r η ξ} (h : H Δ r η ξ) :
    H Γ r (subEnv σ η) (subEnv σ ξ) := by
  induction hs with
  | nil hΔ => exact ⟨rfl,rfl⟩
  | cons hs hA ha ih =>
      rw [subEnv_cons,subEnv_cons]
      refine ⟨ih,?_⟩
      have v := fundamental ha r η ξ h
      rw [G_subst] at v
      exact v

theorem TypedSub.respects {Δ Γ σ} (hs : TypedSub Δ Γ σ) {ρ η ξ} (h : E Δ ρ η ξ) :
    E Γ ρ (subEnv σ η) (subEnv σ ξ) :=
  (context_sound hs.source).diagonal.mp
    (hs.related ((context_sound hs.target).diagonal.mpr h))

theorem TypedSub.valid {Δ Γ σ} (hs : TypedSub Δ Γ σ) {ρ η} (h : D Δ ρ η) :
    D Γ ρ (subEnv σ η) :=
  ((context_sound hs.source).ends (hs.respects ((context_sound hs.target).refl h))).1

/-- The carrier is exactly the zero-padded finite valid valuations. -/
def representedContext (Γ : Tel) (ρ : OEnv) (hc : ContextLaws Γ) : P01D.Context where
  Val := {η : Env // D Γ ρ η}
  eqv := fun η ξ => E Γ ρ η.val ξ.val
  refl := fun η => hc.refl η.property
  sym := hc.sym
  trans := hc.trans
  environment := Subtype.val

def representedType {Γ A} (hA : Form Γ A) (ρ : OEnv) :
    P01D.Ty (representedContext Γ ρ (form_sound hA).1) where
  obj := fun η => objectOf (form_sound hA).2.laws η.property
  coherent := by
    intro η ξ e
    exact per_ext ((form_sound hA).2.laws.transport e)

def representedTerm {Γ p A} (hp : Has Γ p A) (ρ : OEnv) :
    P01D.Tm (representedContext Γ ρ (form_sound (has_form hp)).1) (representedType (has_form hp) ρ) where
  code := p
  valid := unary_fundamental hp

@[simp] theorem representedTerm_code {Γ p A} (hp : Has Γ p A) (ρ : OEnv) :
    (representedTerm hp ρ).code = p := rfl

@[simp] theorem representedType_relation {Γ A} (hA : Form Γ A) (ρ : OEnv)
    (η : (representedContext Γ ρ (form_sound hA).1).Val) (t u : Term) :
    ((representedType hA ρ).obj η).rel t u ↔ F A ρ η.val t u := Iff.rfl

def representedSub {Δ Γ σ} (hs : TypedSub Δ Γ σ) (ρ : OEnv) :
    P01D.Sub (representedContext Δ ρ (context_sound hs.target))
      (representedContext Γ ρ (context_sound hs.source)) where
  map := fun η => ⟨subEnv σ η.val,hs.valid η.property⟩
  respects := hs.respects
  code := images σ
  tracks := fun _ _ => rfl

theorem represented_substitution_code {Δ Γ σ p A} (hs : TypedSub Δ Γ σ) (hp : Has Γ p A) (ρ : OEnv) :
    ((representedTerm hp ρ).subst (representedSub hs ρ)).code = psub (images σ) p := rfl

theorem intrinsic_type_ext {C : P01D.Context} {A B : P01D.Ty C}
    (h : ∀ η, A.obj η = B.obj η) : A = B := by
  have e : A.obj = B.obj := funext h
  cases A; cases B; cases e; rfl

theorem represented_substitution_type {Δ Γ σ A} (hs : TypedSub Δ Γ σ) (hA : Form Γ A) (ρ : OEnv) :
    (representedType hA ρ).pull (representedSub hs ρ) = representedType (hs.form hA) ρ := by
  apply intrinsic_type_ext
  intro η
  apply per_ext
  intro t u
  exact (Iff.of_eq (F_subst A (images σ) ρ η.val t u)).symm

end P01TC

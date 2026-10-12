/- Actual-Joint pure type substitution, erased All instantiation, and composition
   with the independently checked dependent term substitution theorem. -/
import JointMixedSubstitution
namespace JointCompletion.Structural
open P01AC OrthemologyV2 OrthemologyV3 P01D P01R
open P01AC.ExtensionalRepair.Structural
open P01F (cons)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Pure type substitution preserves each term variable at its transformed
lookup type. The type images may depend on all target term variables. -/
structure TypeSubstitution (Γ Δ : Tel) (τ : Nat → Ty) : Prop where
  types : ∀ n, FormJ Δ (τ n)
  lookup : ∀ {n A}, Lookup Γ n A → HasJ Δ (.var n) (tsubst τ A)

theorem TypeSubstitution.toMixed {Γ Δ : Tel} {τ : Nat → Ty}
    (h : TypeSubstitution Γ Δ τ) : MixedSubstitution Γ Δ Poly.var τ :=
  ⟨h.types, h.lookup⟩

theorem form_tsubst {Γ Δ : Tel} {A : Ty} {τ : Nat → Ty}
    (h : FormJ Γ A) (hΔ : CtxJ Δ) (hτ : TypeSubstitution Γ Δ τ) :
    FormJ Δ (tsubst τ A) := form_mixed h hΔ hτ.toMixed

theorem has_tsubst {Γ Δ : Tel} {p : Poly} {A : Ty} {τ : Nat → Ty}
    (h : HasJ Γ p A) (hΔ : CtxJ Δ) (hτ : TypeSubstitution Γ Δ τ) :
    HasJ Δ p (tsubst τ A) := by
  simpa only [psub_id] using has_mixed h hΔ hτ.toMixed

/-- In an empty source telescope the compatibility condition is vacuous. -/
theorem TypeSubstitution.empty {Δ : Tel} {τ : Nat → Ty}
    (hτ : ∀ n, FormJ Δ (τ n)) : TypeSubstitution [] Δ τ :=
  ⟨hτ, by intro n A h; cases h⟩

theorem has_closed_tsubst {Δ : Tel} {p : Poly} {A : Ty} {τ : Nat → Ty}
    (h : HasJ [] p A) (hΔ : CtxJ Δ) (hτ : ∀ n, FormJ Δ (τ n)) :
    HasJ Δ p (tsubst τ A) := has_tsubst h hΔ (TypeSubstitution.empty hτ)

/-- Instantiating the newest type variable restores the original dependent
term telescope, without an assumed result formation judgement. -/
theorem TypeSubstitution.top {Γ : Tel} {A : Ty} (hA : FormJ Γ A) :
    TypeSubstitution (twkTel Γ) Γ (cons A Ty.param) := by
  have hΓ := form_ctx hA
  constructor
  · intro n
    cases n with
    | zero => exact hA
    | succ n => exact .param hΓ
  · intro n B hb
    obtain ⟨C, hc, rfl⟩ := lookup_trename_inv hb
    change HasJ Γ (.var n) (tinst (twk C) A)
    rw [tinst_twk]
    exact HasJ.var (lookup_form hΓ hc) hc

theorem form_tinst {Γ : Tel} {B A : Ty}
    (hB : FormJ (twkTel Γ) B) (hA : FormJ Γ A) : FormJ Γ (tinst B A) :=
  form_tsubst hB (form_ctx hA) (TypeSubstitution.top hA)

theorem has_tinst {Γ : Tel} {p : Poly} {B A : Ty}
    (hp : HasJ (twkTel Γ) p B) (hA : FormJ Γ A) : HasJ Γ p (tinst B A) :=
  has_tsubst hp (form_ctx hA) (TypeSubstitution.top hA)

/-- Actual-Joint All elimination's result-formation premise is now derivable. -/
theorem allElim_formed {Γ : Tel} {p : Poly} {B A : Ty}
    (hp : HasJ Γ p (.all B)) (hA : FormJ Γ A) : HasJ Γ p (tinst B A) := by
  have hF := has_form hp
  have hB : FormJ (twkTel Γ) B := by
    cases hF with
    | formBase hF => cases hF with | all _ hB => exact .formBase hB
    | all _ hB => exact hB
  exact .allElim hF hA (form_tinst hB hA) hp

/-- Total type maps can be specified by a finite list with the inherited
Bottom default; there is no hidden infinite family of formation obligations. -/
theorem finite_type_images {Δ : Tel} {τ : List Ty} (hΔ : CtxJ Δ)
    (hτ : ∀ n, n < τ.length → FormJ Δ (typeImages τ n)) :
    ∀ n, FormJ Δ (typeImages τ n) := by
  intro n
  by_cases hn : n < τ.length
  · exact hτ n hn
  · rw [typeImages_ge τ (Nat.le_of_not_gt hn)]
    exact .bottom hΔ

/-- Literal two-sort substitution composes; images need actual Joint evidence only. -/
theorem MixedSubstitution.comp {Γ Δ Ξ : Tel} {σ δ : Nat → Poly} {τ υ : Nat → Ty}
    (h : MixedSubstitution Γ Δ σ τ) (hΞ : CtxJ Ξ)
    (g : MixedSubstitution Δ Ξ δ υ) :
    MixedSubstitution Γ Ξ (fun n => psub δ (σ n)) (fun n => mixed δ υ (τ n)) := by
  constructor
  · intro n
    exact form_mixed (h.types n) hΞ g
  · intro n A hn
    simpa only [mixed_comp] using has_mixed (h.lookup hn) hΞ g

/-- The freshly checked pure-term theorem supplies this specialization. -/
theorem TypedSubstitution.toMixed {Γ Δ : Tel} {σ : Nat → Poly}
    (h : TypedSubstitution Γ Δ σ) (hΔ : CtxJ Δ) :
    MixedSubstitution Γ Δ σ Ty.param := by
  refine ⟨fun _ => .param hΔ, ?_⟩
  intro n A hn
  simpa only [mixed_param] using h.lookup hn

/-- Applying dependent TERM substitution after TYPE substitution acts on
replacement types as well as source endpoints. This is the exact square. -/
theorem TypeSubstitution.thenTerm {Γ Δ Ξ : Tel} {τ : Nat → Ty} {δ : Nat → Poly}
    (h : TypeSubstitution Γ Δ τ) (hΞ : CtxJ Ξ) (g : TypedSubstitution Δ Ξ δ) :
    MixedSubstitution Γ Ξ δ (fun n => subst δ (τ n)) := by
  constructor
  · intro n
    exact form_subst (h.types n) hΞ g
  · intro n A hn
    simpa only [psub, subst_tsubst] using has_subst (h.lookup hn) hΞ g

/-- Both sequential and simultaneous presentations have literal equality,
not raw conversion or reflected propositional equality. -/
theorem has_type_then_term {Γ Δ Ξ : Tel} {p : Poly} {A : Ty}
    {τ : Nat → Ty} {δ : Nat → Poly} (hp : HasJ Γ p A)
    (hΔ : CtxJ Δ) (hτ : TypeSubstitution Γ Δ τ)
    (hΞ : CtxJ Ξ) (hδ : TypedSubstitution Δ Ξ δ) :
    HasJ Ξ (psub δ p) (mixed δ (fun n => subst δ (τ n)) A) := by
  simpa only [subst_tsubst] using has_subst (has_tsubst hp hΔ hτ) hΞ hδ

/-- The reverse order keeps the already-target-relative type images unchanged. -/
theorem TypedSubstitution.thenType {Γ Δ Ξ : Tel} {σ : Nat → Poly} {τ : Nat → Ty}
    (h : TypedSubstitution Γ Δ σ) (hΞ : CtxJ Ξ) (g : TypeSubstitution Δ Ξ τ) :
    MixedSubstitution Γ Ξ σ τ := by
  constructor
  · exact g.types
  · intro n A hn
    simpa only [tsubst, mixed_subst, psub_id] using has_tsubst (h.lookup hn) hΞ g

/-- The previous pure-term structural theorem is a literal specialization. -/
theorem has_mixed_identity_types {Γ Δ : Tel} {p : Poly} {A : Ty} {σ : Nat → Poly}
    (hp : HasJ Γ p A) (hΔ : CtxJ Δ) (hσ : TypedSubstitution Γ Δ σ) :
    HasJ Δ (psub σ p) (subst σ A) := by
  simpa only [mixed_param] using has_mixed hp hΔ (hσ.toMixed hΔ)

#print axioms form_tsubst
#print axioms has_tsubst
#print axioms has_tinst
#print axioms allElim_formed
#print axioms MixedSubstitution.comp
#print axioms has_type_then_term
end JointCompletion.Structural

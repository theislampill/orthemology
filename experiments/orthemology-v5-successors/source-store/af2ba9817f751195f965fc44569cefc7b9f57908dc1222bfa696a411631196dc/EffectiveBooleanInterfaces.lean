/- Original identity and current-typing interfaces for the Boolean family.
   The arithmetic-hierarchy theorem remains in the written companion. -/
import EffectivePrimitiveRecursion
namespace P01AC.BooleanIdentity
open OrthemologyV2 OrthemologyV3 P01D P01R P01AC.EffectiveCompleteness
open P01AC.BooleanPrimitive

def IdentityValid (p q : Poly) : Prop :=
  ∀ r : REnv, G (.identity CB p q) r zeroEnv zeroEnv .i .i

theorem identity_valid_iff_endpoint_valid (p q : Poly) :
    IdentityValid p q ↔ BoolValid p q := by
  constructor
  · intro h ρ
    exact (h (diagEnv ρ)).1
  · intro h r
    exact ⟨h r.left, h r.right, .refl _, .refl _⟩

theorem identity_unary_iff_endpoint_valid (p q : Poly) :
    (∀ ρ, F (.identity CB p q) ρ zeroEnv .i .i) ↔ BoolValid p q := by
  constructor
  · intro h ρ
    exact (h ρ).1
  · intro h ρ
    exact ⟨h ρ, .refl _, .refl _⟩

theorem semantic_proof_exists_iff_valid (p q : Poly) :
    (∃ w : Poly, ∀ r, G (.identity CB p q) r zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ BoolValid p q := by
  constructor
  · rintro ⟨w, hw⟩ ρ
    exact (hw (diagEnv ρ)).1
  · intro h
    exact ⟨.atom .i, fun r => ⟨h r.left, h r.right, .refl _, .refl _⟩⟩

theorem current_identity_implies_valid {e p q : Poly}
    (h : Has [] e (.identity CB p q)) : BoolValid p q := by
  intro ρ
  exact (unary_fundamental h (ρ := ρ) ⟨rfl, rfl⟩).1

theorem identity_formed {p q : Poly} (hp : Has [] p CB) (hq : Has [] q CB) :
    Form [] (.identity CB p q) :=
  .identity (form_arr (N_form .nil) (B_form .nil)) hp hq

theorem identity_invalid_iff_mismatch {p q : Poly}
    (hp : Has [] p CB) (hq : Has [] q CB) :
    ¬ IdentityValid p q ↔ Mismatch p q := by
  rw [identity_valid_iff_endpoint_valid]
  exact invalid_iff_mismatch hp hq

theorem family_closed (f : PR 2) (e : Nat) :
    Scoped 0 (simFamily f e) ∧ Scoped 0 constantChoice :=
  ⟨has_scoped (simFamily_has f e), has_scoped constantChoice_has⟩

theorem family_identity_formed (f : PR 2) (e : Nat) :
    Form [] (.identity CB (simFamily f e) constantChoice) :=
  identity_formed (simFamily_has f e) constantChoice_has

theorem family_identity_scope (f : PR 2) (e : Nat) :
    TyScoped 0 (.identity CB (simFamily f e) constantChoice) ∧
    Intensional.TyParamScoped 0 (.identity CB (simFamily f e) constantChoice) := by
  refine ⟨form_scoped (family_identity_formed f e), ?_⟩
  change ((0 < 1 ∧ 0 < 1) ∧ (0 < 1 ∧ 0 < 1)) ∧ (0 < 1 ∧ (0 < 1 ∧ 0 < 1))
  exact ⟨⟨⟨by decide, by decide⟩, ⟨by decide, by decide⟩⟩, ⟨by decide, ⟨by decide, by decide⟩⟩⟩

theorem original_identity_iff_all_zero (f : PR 2) (e : Nat) :
    IdentityValid (simFamily f e) constantChoice ↔ ∀ n, f.denote (inputs n e) = 0 :=
  (identity_valid_iff_endpoint_valid _ _).trans (sim_valid_iff_all_zero f e)

theorem original_F_identity_iff_all_zero (f : PR 2) (e : Nat) :
    (∀ ρ, F (.identity CB (simFamily f e) constantChoice) ρ zeroEnv .i .i) ↔
      ∀ n, f.denote (inputs n e) = 0 :=
  (identity_unary_iff_endpoint_valid _ _).trans (sim_valid_iff_all_zero f e)

theorem family_semantic_proof_exists_iff_all_zero (f : PR 2) (e : Nat) :
    (∃ w : Poly, ∀ r, G (.identity CB (simFamily f e) constantChoice) r zeroEnv zeroEnv
      (eval w zeroEnv) (eval w zeroEnv)) ↔ ∀ n, f.denote (inputs n e) = 0 :=
  (semantic_proof_exists_iff_valid _ _).trans (sim_valid_iff_all_zero f e)

theorem current_family_identity_implies_all_zero {f : PR 2} {e : Nat} {w : Poly}
    (h : Has [] w (.identity CB (simFamily f e) constantChoice)) :
    ∀ n, f.denote (inputs n e) = 0 :=
  (sim_valid_iff_all_zero f e).mp (current_identity_implies_valid h)

end P01AC.BooleanIdentity

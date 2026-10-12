import FullPER
import ScalarFusionCore

namespace FullPER.Application
open P01AC P01D
open OpenTermStandardness (T SatPER Conv Arrow arrowPER churchPER)
open ImportedOpenTermTransport (embed interp)
open P01AC.EffectiveCompleteness (N NBody)
open P01AC.UnaryIdentity.IntensionalBoundary (variableExpr redundantExpr)
open P01AC.ExtensionalRepair.ExactScalarFusion (W c3)

def originalP : Poly := variableExpr.closed
def originalQ : Poly := redundantExpr.closed
def originalIdentity : Ty := .identity (arr N N) originalP originalQ

/-- Literal agreement with the frozen full-PER Church object. -/
theorem church_exact (ρ : REnv) (η : Env) : F N ρ η = churchPER.rel := rfl

theorem function_exact (ρ : REnv) (η : Env) :
    F (arr N N) ρ η = (arrowPER churchPER churchPER).rel := rfl

theorem originalP_eval (η : Env) : interp originalP η = .i := by
  unfold originalP ImportedOpenTermTransport.interp
  rw [ImportedOpenTermTransport.original_p_poly_exact]
  rfl

theorem originalQ_eval (η : Env) : interp originalQ η = OpenTermStandardness.q := by
  unfold originalQ ImportedOpenTermTransport.interp
  rw [ImportedOpenTermTransport.original_q_poly_exact]
  exact ImportedOpenTermTransport.q_eval_independent η

/-- The actual endpoints agree in this certified whole-HasE interpretation. -/
theorem original_endpoints (ρ : REnv) (η : Env) :
    F (arr N N) ρ η (interp originalP η) (interp originalQ η) := by
  rw [function_exact,originalP_eval,originalQ_eval]
  exact OpenTermStandardness.identity_q_related

/-- Semantic identity inhabitation, NOT a source HasE proof. -/
theorem original_identity_inhabited (ρ : REnv) (η : Env) :
    F originalIdentity ρ η .i .i := ⟨original_endpoints ρ η,.refl _,.refl _⟩

theorem original_raw_distinct (η : Env) : ¬ Conv (interp originalP η) (interp originalQ η) := by
  rw [originalP_eval,originalQ_eval]
  have h := ImportedOpenTermTransport.original_raw_endpoints_still_distinct
  rw [ImportedOpenTermTransport.original_p_eval_exact,ImportedOpenTermTransport.original_q_eval_exact] at h
  exact h

/-- Every finite successor numeral supplies a nonempty Church element. -/
theorem church_nonvacuous (ρ : REnv) (η : Env) (k : Nat) :
    F N ρ η (OpenTermStandardness.successorNumeral k) (OpenTermStandardness.successorNumeral k) :=
  OpenTermStandardness.successorNumeral_church k

def emptyEnv : REnv := fun _ _ _ => False

theorem emptyEnv_admissible : admissible emptyEnv := fun _ =>
  ⟨False.elim,fun h _ => h,fun _ _ h => h⟩

theorem empty_context_nonvacuous : D [] emptyEnv zeroEnv := rfl

/-- A consistency control for the newly constructed interpretation. -/
theorem no_closed_bottom (p : Poly) : ¬ P01AC.ExtensionalRepair.HasE [] p .bottom := by
  intro h
  exact fundamental h emptyEnv zeroEnv zeroEnv emptyEnv_admissible ⟨rfl,rfl⟩

theorem c3_eval (η : Env) : interp c3 η = T.k ⬝ (T.k ⬝ (T.k ⬝ T.i)) := by
  simp [c3, P01AC.ExtensionalRepair.ExactScalarFusion.i, P01D.abstract,
    P01D.freeZero, P01D.drop, P01D.pren, P01D.psub, interp_app, interp_atom,
    ImportedOpenTermTransport.embed]

/-- Actual fixed source proof polynomial, with no replacement by an eta-normal form. -/
theorem c3_application (η : Env) (n f a : T) :
    Conv (interp c3 η ⬝ n ⬝ f ⬝ a) .i := by
  rw [c3_eval]
  exact (Conv.app (Conv.app (.k _ _) (.refl _)) (.refl _)).trans
    ((Conv.app (.k _ _) (.refl _)).trans (.k _ _))

/-- The exact source W and c3 are semantically valid for the exact original q.
    This is not HasE [] c3 (W originalQ), nor semantic completeness. -/
theorem scalar_target_valid (ρ : REnv) (η : Env) :
    F (W originalQ) ρ η (interp c3 η) (interp c3 η) := by
  change ∀ n m, churchPER.rel n m → ∀ P : SatPER,
    ∀ f g, Arrow P.rel P.rel f g → ∀ a b, P.rel a b →
    P.rel (n ⬝ f ⬝ a)
      (interp originalQ (cons a (cons f (cons n η))) ⬝ n ⬝ f ⬝ a) ∧
    Conv (interp c3 η ⬝ n ⬝ f ⬝ a) .i ∧ Conv (interp c3 η ⬝ m ⬝ g ⬝ b) .i
  intro n m nm P f g fg a b ab
  rw [originalQ_eval]
  have nn := churchPER.trans nm (churchPER.symm nm)
  have ff := (arrowPER P P).trans fg ((arrowPER P P).symm fg)
  have aa := P.trans ab (P.symm ab)
  have base := nn P f f ff a a aa
  exact ⟨P.saturated (.refl _) (OpenTermStandardness.church_scalar_fusion n nn f a) base,
    c3_application η n f a,c3_application η m g b⟩

/-- The scalar validation also respects arbitrary related outer environments. -/
theorem scalar_target_fundamental (Γ : Tel) : Fundamental Γ c3 (W originalQ) := by
  intro ρ η ξ _ _
  have closed : interp c3 ξ = interp c3 η := (c3_eval ξ).trans (c3_eval η).symm
  rw [closed]
  exact scalar_target_valid ρ η

#print axioms church_exact
#print axioms original_endpoints
#print axioms original_identity_inhabited
#print axioms original_raw_distinct
#print axioms no_closed_bottom
#print axioms scalar_target_valid
#print axioms scalar_target_fundamental
end FullPER.Application

import RawMotiveBoundary

/- Reviewer-only controls. These add no source rules or axioms. -/
namespace P01AC.ExtensionalRepair.RawMotiveBoundary.IndependentReview
open OrthemologyV2 OrthemologyV3 P01D P01R
open P01F (cons)
open P01AC.EffectiveCompleteness
open P01AC.UnaryIdentity.IntensionalBoundary

set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

theorem exact_theta_shape : theta [] EndN p =
    [.identity (wk EndN) (pren Nat.succ p) (.var 0), EndN] := rfl

theorem exact_endpoint_coordinates :
    eval (.var 0) (cons p0 zeroEnv) = p0 ∧
    eval (.var 0) (cons .i (cons p0 zeroEnv)) = .i ∧
    eval (.var 1) (cons .i (cons p0 zeroEnv)) = p0 ∧
    eval (.var 1) (cons .i (cons q0 zeroEnv)) = q0 :=
  ⟨rfl, rfl, rfl, rfl⟩

theorem theta_both_inhabited (ρ : OEnv) :
    D (theta [] EndN p) ρ (cons .i (cons p0 zeroEnv)) ∧
    D (theta [] EndN p) ρ (cons .i (cons q0 zeroEnv)) :=
  (context_sound theta_context_formed).ends (theta_environments ρ)

theorem assumption_inhabited (ρ : OEnv) : D [B] ρ (cons .i zeroEnv) :=
  ((context_sound assumed_context_formed).ends (assumed_identity_environment ρ)).1

/-- Closed polynomial syntax is raw-typable by structural recursion; this does
    not introduce any erasure or quotation rule for a bound typed variable. -/
theorem raw_closed_at {Γ : Tel} {s : Poly} (hΓ : CtxE Γ) (hs : Scoped 0 s) :
    HasE Γ s .raw := by
  induction s with
  | var n => exact False.elim (Nat.not_lt_zero n hs)
  | atom t => exact .rawAtom (.raw hΓ)
  | app f a ihf iha => exact .rawApp (.raw hΓ) (ihf hs.1) (iha hs.2)

/-- The negative assumed-context target is genuinely formed, so its failure
    is not merely the earlier failed formation of the varying-endpoint motive. -/
theorem reflection_target_formed : FormE [B] (.identity .raw p q) :=
  .identity (.raw assumed_context_formed)
    (raw_closed_at assumed_context_formed (has_scoped variableExpr.closed_has))
    (raw_closed_at assumed_context_formed (has_scoped redundantExpr.closed_has))

theorem q_is_raw_in_theta : HasE (theta [] EndN p) q .raw :=
  raw_closed_at theta_context_formed (has_scoped redundantExpr.closed_has)

theorem reflection_target_has_no_witness : ¬ ∃ r, HasE [B] r (.identity .raw p q) := by
  rintro ⟨r, hr⟩
  exact no_raw_reflection_under_assumption r hr

#print axioms exact_theta_shape
#print axioms exact_endpoint_coordinates
#print axioms theta_both_inhabited
#print axioms assumption_inhabited
#print axioms raw_closed_at
#print axioms reflection_target_formed
#print axioms q_is_raw_in_theta
#print axioms reflection_target_has_no_witness
end P01AC.ExtensionalRepair.RawMotiveBoundary.IndependentReview

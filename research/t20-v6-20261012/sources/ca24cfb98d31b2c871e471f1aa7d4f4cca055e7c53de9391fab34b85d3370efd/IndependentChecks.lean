import JointInductionAudit
import Lean

namespace JointInductionIndependentReview
open P01AC P01D
open P01AC.EffectiveCompleteness (N)
open P01AC.Intensional.Plus (PolyConvPlus)
open JointCompletion
open JointCompletion.InductionComputation.RawBoundary

/-- These same endpoints refute unrestricted reflection of typed natural identity. -/
theorem no_unrestricted_identity_reflection :
    ¬ (∀ {Γ : Tel} {e x y : Poly}, HasJ Γ e (.identity N x y) → PolyConvPlus x y) := by
  intro reflect
  obtain ⟨e, he⟩ := successor_typed_identity
  exact successor_not_raw (reflect he)

/-- The existing positive model receives the exact new typed result. -/
theorem successor_in_retained_model :
    ∃ e, FullPER.Fundamental [N] e (.identity N left right) := by
  obtain ⟨e, he⟩ := successor_typed_identity
  exact ⟨e, JointCompletion.fundamental he⟩

/-- Retained Joint consistency remains applicable without any new rule. -/
theorem no_closed_bottom_retained (p : Poly) : ¬ HasJ [] p .bottom :=
  JointCompletion.no_closed_bottom p

#print axioms no_unrestricted_identity_reflection
#print axioms successor_in_retained_model
#print axioms no_closed_bottom_retained
end JointInductionIndependentReview

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if n.getPrefix == `JointCompletion.InductionComputation then
      match ci with
      | .thmInfo _ =>
        let (_, report) := ((Lean.CollectAxioms.collect n).run env).run {}
        for a in report.axioms do
          unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
            throwError "Unexpected axiom in {n}: {a}"
        for dep in report.visited do
          if dep.toString.endsWith ".fundamental" ||
              [``FullPER.form_sound, ``FullPER.has_sound,
               ``JointCompletion.form_sound, ``JointCompletion.has_sound,
               ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction].contains dep then
            throwError "Semantic construction in positive helper {n}: {dep}"
        count := count + 1
      | _ => pure ()
  logInfo m!"PASS: independently inspected {count} positive helper/public theorem dependency closures."

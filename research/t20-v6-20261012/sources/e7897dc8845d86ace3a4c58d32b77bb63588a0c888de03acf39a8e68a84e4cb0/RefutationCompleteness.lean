import ConditionalRefutation
import Lean

namespace PRConditionalRefutation
open P01AC P01D P01AC.ExtensionalRepair
open P01AC.BooleanPrimitive P01AC.BooleanIdentity
open FullPERTests JointCompletion
open OpenTermStandardness (T)
set_option maxRecDepth 8192
set_option maxHeartbeats 8000000

/-- Failure of the actual full-PER predicate has an actual finite PR witness. -/
theorem invalid_iff_finite_counterexample (f : PR 2) (e : Nat) :
    ¬ Holds (programType f e) ↔ ∃ k, f.denote (inputs k e) ≠ 0 := by
  classical
  rw [program_holds_iff]
  simp only [not_forall]

/-- No-confusion is valid in the faithful declared interpretation. This is a
    semantic theorem, not source adoption of a no-confusion principle. -/
theorem noConfusion_valid (ρ : FullPER.REnv) (η : FullPER.Env) :
    FullPER.F NoConfusion ρ η T.i T.i := by
  intro x y h
  exact choices_separate ((ImportedOpenTermTransport.embed_conversion_iff _ _).mp h.1)

/-- Exact conditional source-certificate completeness on the PR test family.
    NoConfusion remains an antecedent of the actual unchanged HasE type. -/
theorem invalid_iff_conditional_refutation (f : PR 2) (e : Nat) :
    ¬ Holds (programType f e) ↔
      ∃ q : Poly, HasE [] q (arr NoConfusion (arr (programType f e) .bottom)) := by
  constructor
  · intro h
    obtain ⟨k,hk⟩ := (invalid_iff_finite_counterexample f e).mp h
    exact refutation_template f e k hk
  · rintro ⟨q,hq⟩ hvalid
    have hs := FullPER.fundamental hq rawEnv FullPER.zeroEnv FullPER.zeroEnv rawEnv_admissible ⟨rfl,rfl⟩
    rw [FullPER.F_arr] at hs
    have hr := hs T.i T.i (noConfusion_valid rawEnv FullPER.zeroEnv)
    rw [FullPER.F_arr] at hr
    obtain ⟨a,ha⟩ := hvalid rawEnv rawEnv_admissible
    exact hr a a ha

/-- An actually supplied no-confusion proof converts every invalid instance
    into an internal negation, without any new source rule. -/
theorem conditional_negative_completeness {c : Poly}
    (hc : HasJ [] c NoConfusion) (f : PR 2) (e : Nat)
    (invalid : ¬ Holds (programType f e)) :
    ∃ r : Poly, HasJ [] r (arr (programType f e) .bottom) := by
  obtain ⟨k,hk⟩ := (invalid_iff_finite_counterexample f e).mp invalid
  exact refute_failed_test f e k hk hc

#print axioms invalid_iff_finite_counterexample
#print axioms invalid_iff_conditional_refutation
#print axioms conditional_negative_completeness
end PRConditionalRefutation

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``PRConditionalRefutation.refutation_template,
      ``PRConditionalRefutation.refute_failed_test] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for forbidden in [``FullPER.fundamental, ``FullPERTests.inhabited_iff_observations,
        ``FullPERTests.program_holds_iff, ``FullPERTests.exists_non_re_formed_family,
        ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction] do
      if report.visited.contains forbidden then
        throwError "Forbidden semantic/reflection dependency in source construction {target}: {forbidden}"
    logInfo m!"PASS {target}: source-only finite-counterexample construction."

import NegativeSearch
import FullPERBoundaryControls
import Lean

namespace PRNegativeSearch
open P01AC P01D P01AC.ExtensionalRepair P01AC.BooleanPrimitive
open FullPERTests PRConditionalRefutation

/-- This actual retained program returns the search bound. Its first failure is 1. -/
def lateProgram : PR 2 := .proj ⟨0, by decide⟩

example : scan (.zero 2) 7 64 = none := rfl
example : scan oneProgram 7 64 = some 0 := rfl
example : scan lateProgram 7 1 = none := rfl
example : scan lateProgram 7 2 = some 1 := rfl

example : scanCertificate lateProgram 7 2 = some (1,certificateTerm 1) := rfl

/-- A bounded failure to find anything is explicitly not a validity certificate. -/
theorem bounded_none_with_invalid_input :
    scan lateProgram 7 1 = none ∧ ¬ Holds (programType lateProgram 7) := by
  refine ⟨rfl,(invalid_iff_finite_counterexample lateProgram 7).mpr ⟨1,?_⟩⟩
  decide

theorem zero_search_undefined (e : Nat) : ¬ (certificateSearch (.zero 2) e).Dom := by
  exact valid_search_undefined ((program_holds_iff (.zero 2) e).mpr (fun _ => rfl))

theorem exact_late_certificate : HasE [] (certificateTerm 1)
    (arr NoConfusion (arr (programType lateProgram 7) .bottom)) :=
  certificateTerm_has lateProgram 7 1 (by decide)

theorem actual_search_class (f : PR 2) :
    Nat.Partrec (fun e => Nat.rfind (fun k =>
      (decide (f.denote (inputs k e) ≠ 0) : Bool))) := f.nonzeroSearch_nat_partrec

#eval scan (.zero 2) 7 64
#eval scan oneProgram 7 64
#eval scan lateProgram 7 1
#eval scan lateProgram 7 2

#print axioms exact_late_certificate
#print axioms actual_search_class
end PRNegativeSearch

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``PRNegativeSearch.certificateTerm_has,
      ``PRNegativeSearch.scan_terminates_iff_invalid,
      ``PRNegativeSearch.returned_source_certificate,
      ``PRNegativeSearch.actual_search_class] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    logInfo m!"PASS {target}: only standard logical axioms."
  let (_, source) := ((Lean.CollectAxioms.collect ``PRNegativeSearch.certificateTerm_has).run env).run {}
  for forbidden in [``FullPER.fundamental, ``FullPERTests.program_holds_iff,
      ``JointCompletion.sigma_elimination, ``JointCompletion.dependent_induction] do
    if source.visited.contains forbidden then
      throwError "Semantic shortcut in literal source certificate: {forbidden}"
  logInfo m!"PASS literal certificate derivation is source-only."

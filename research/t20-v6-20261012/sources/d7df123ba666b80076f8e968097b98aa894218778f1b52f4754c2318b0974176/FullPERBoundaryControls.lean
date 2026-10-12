import FullPERHalting
import Lean

namespace FullPERTests
open P01AC P01D P01AC.BooleanPrimitive
open ImportedOpenTermTransport (interp)

/-- The common semantic realizer is itself literal closed source syntax. -/
def uniformEvidence : Poly := .app (.atom .k) (.atom .i)

theorem uniformEvidence_interp : interp uniformEvidence FullPER.zeroEnv = uniformWitness := rfl

theorem zero_program_valid (e : Nat) : FixedValid (programType (.zero 2) e) := by
  apply (program_fixed_iff _ _).mpr
  exact (program_holds_iff _ _).mpr (fun _ => rfl)

def oneProgram : PR 2 := .comp .succ (fun _ => .zero 2)

theorem one_program_empty (e : Nat) : ¬ Holds (programType oneProgram e) := by
  intro h
  have hz := (program_holds_iff oneProgram e).mp h 0
  simp [oneProgram, PR.denote] at hz

theorem raw_zero_one_distinct : ¬ FullPER.F .raw rawEnv FullPER.zeroEnv
    (ImportedOpenTermTransport.embed .zero) (ImportedOpenTermTransport.embed .one) := by
  intro h
  exact P01AC.BooleanIdentity.choices_separate
    ((ImportedOpenTermTransport.embed_conversion_iff _ _).mp h)

end FullPERTests

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  for target in [``FullPERTests.testType_formE, ``FullPERTests.inhabited_iff_observations,
      ``FullPERTests.exists_non_re_formed_family, ``FullPERTests.no_re_sound_complete_acceptance] do
    let (_, report) := ((Lean.CollectAxioms.collect target).run env).run {}
    for a in report.axioms do
      unless [``propext, ``Classical.choice, ``Quot.sound].contains a do
        throwError "Unexpected axiom in {target}: {a}"
    for forbidden in [``P01AC.BooleanIdentity.bool_valid_iff_tests,
        ``P01AC.BooleanPrimitive.sim_valid_iff_all_zero,
        ``P01AC.BooleanIdentity.boolean_standardness] do
      if report.visited.contains forbidden then
        throwError "Forbidden old-semantic shortcut in {target}: {forbidden}"
    logInfo m!"PASS {target}: no old Boolean-validity theorem or extra axiom."

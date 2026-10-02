import IndexedSplitProgram

namespace Orthemology.CertifiedObserver.Indexed.Controls
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open P02.Codec P02A2.ObserverCore
open Q8.Fixtures

/-- The empty horizon legitimately requires no runtime steps. -/
theorem empty_horizon_fuel (index : ℕ) : uniformFuel index 0 = 0 := by
  apply (Nat.find_eq_zero _).mpr
  intro w k
  exact Fin.elim0 k

/-- Requesting the empty prefix budget for tick0 really loses a valid output. -/
theorem undersized_horizon_loses_tick :
    tick (uniformFuel (ParsedQ8.code haltNow) 0) (ParsedQ8.code haltNow) (fun _ => true) 0 = none ∧
      output (machine (ParsedQ8.code haltNow)) initial (fun _ => true) 0 = true := by
  constructor
  · rw [empty_horizon_fuel]
    exact ParsedQ8.Fixtures.zero_fuel_is_not_zero haltNow (fun _ => true) 0
  · rw [source_output_exact]
    change ParsedQ8.observer haltNow (fun _ => true) 0 = true
    rw [ParsedQ8.parsed_output_mealy haltNow (by decide)]
    rfl

def copySource : PackedProgram := ⟨2,2,.set 2 (.reg 1)⟩
def reducedCopySource : PackedProgram := ⟨2,2,.set 2 (.mod (.reg 1) (.constant 2))⟩

theorem distinct_generated_codes : programIndex copySource ≠ programIndex reducedCopySource := by
  intro h
  have he := congrArg decodeIndex h
  rw [decodeIndex_programIndex, decodeIndex_programIndex] at he
  have hp := Option.some.inj he
  simp [copySource, reducedCopySource] at hp

theorem equivalent_actual_evaluators :
    evaluateIndex (programIndex copySource) = evaluateIndex (programIndex reducedCopySource) := by
  funext n w
  simp [evaluateIndex, decodeIndex_programIndex, copySource, reducedCopySource,
    exec, evalExpr, binaryStore, Nat.mod_mod]

/-- Even source-owned parser/runtime equality has no converse numeric-source
identity: two distinct generated programs can compute the same observer. -/
theorem same_runtime_law_distinct_source :
    programIndex copySource ≠ programIndex reducedCopySource ∧
      P02A2.Q8Measure.fairCantor.map (runtimeOutput (programIndex copySource)) =
        P02A2.Q8Measure.fairCantor.map (runtimeOutput (programIndex reducedCopySource)) := by
  refine ⟨distinct_generated_codes, ?_⟩
  rw [runtime_law_exact, runtime_law_exact]
  unfold sourceLaw
  rw [equivalent_actual_evaluators]

end Orthemology.CertifiedObserver.Indexed.Controls

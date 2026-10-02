import CallableSourceRuntime
namespace Orthemology.RuntimeBridge.PhaseUpdate.Controls
open P02A2.PRProgram P02.Codec P02.Codec.UniformComputability

theorem no_zero_fuel_value {k : ℕ} (p : Program k) (args : Fin k → ℕ) :
    callFuel 0 (programIndex (pack p)) args = none := by
  simp [callFuel,decodeIndex_programIndex,pack,runFuel]

theorem wrong_callable_arity (fuel : ℕ) (args : Fin 2 → ℕ) :
    callFuel fuel (programIndex (pack phaseProgram)) args = none := by
  simp [callFuel,decodeIndex_programIndex,pack]

/-- The retained binary indexed observer is intentionally not an arity-six
component evaluator; its original wrong-arity zero convention is unchanged. -/
theorem binary_observer_wrong_arity (n word : ℕ) :
    evaluateIndex (programIndex (pack phaseProgram)) n word = 0 := by
  simp [evaluateIndex,decodeIndex_programIndex,pack]

end Orthemology.RuntimeBridge.PhaseUpdate.Controls

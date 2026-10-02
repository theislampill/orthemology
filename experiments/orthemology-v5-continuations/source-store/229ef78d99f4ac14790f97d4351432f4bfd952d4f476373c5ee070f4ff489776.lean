import IndexedControls
namespace IndependentIndexedControls
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.CertifiedObserver Orthemology.CertifiedObserver.Indexed
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore

theorem literal_initial_is_fixed : initial = (0,1) := rfl

theorem acquired_word_three_bits (index : ℕ) :
    state (machine index) initial (fun n => decide (n ≠ 1)) 3 = (3,13) := by rfl

theorem unacquired_bits_do_not_change_state (index : ℕ) (x y : Cantor) (k : ℕ)
    (h : pref k x = pref k y) :
    state (machine index) initial x k = state (machine index) initial y k := acquired_prefix_only index x y k h

theorem invalid_numeric_code_rejected : decodeIndex 0 = none := rfl

theorem invalid_numeric_code_has_specified_default (fuel n w : ℕ) :
    evaluateIndexFuel fuel 0 n w = some 0 := rfl

theorem invalid_code_tick_is_some_false (fuel : ℕ) (x : Cantor) (k : ℕ) :
    tick fuel 0 x k = some false := rfl

def wrongArity : PackedProgram := ⟨1,2,.set 2 (.constant 1)⟩

theorem wrong_arity_default_is_not_execution (fuel n w : ℕ) :
    evaluateIndexFuel fuel (programIndex wrongArity) n w = some 0 := by
  simp [evaluateIndexFuel,decodeIndex_programIndex,wrongArity]

def one : PackedProgram := ⟨2,2,.set 2 (.constant 1)⟩

theorem valid_code_zero_fuel_is_timeout (x : Cantor) (k : ℕ) :
    tick 0 (programIndex one) x k = none := by
  simp [tick,evaluateIndexFuel,decodeIndex_programIndex,one,runFuel]

theorem valid_one_source_is_true (x : Cantor) (k : ℕ) :
    output (machine (programIndex one)) initial x k = true := by
  rw [source_output_exact]
  simp [P02A2.ObserverCore.output,evaluateIndex,decodeIndex_programIndex,one,exec,evalExpr]

theorem scheduled_one_is_true (x : Cantor) (k : ℕ) :
    runtimeOutput (programIndex one) x k = true := by
  rw [runtime_output_exact]
  exact valid_one_source_is_true x k

theorem successful_scheduled_invocation_precedes_default (index : ℕ) (x : Cantor) (k : ℕ) :
    ∃ b, tick (uniformFuel index (k+1)) index x k = some b :=
  ⟨_,scheduled_tick_success index x k⟩

theorem empty_horizon_does_not_cover_tick_zero :
    tick (uniformFuel (programIndex one) 0) (programIndex one) (fun _ => false) 0 = none := by
  rw [Indexed.Controls.empty_horizon_fuel]
  exact valid_code_zero_fuel_is_timeout _ _

theorem literal_stream_equality_transports_actual_law (index : ℕ) :
    P02A2.Q8Measure.fairCantor.map (runtimeOutput index) = sourceLaw index := runtime_law_exact index
end IndependentIndexedControls

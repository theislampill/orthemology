import UniformComputabilityMachine
namespace OperationalInterpreterAudit
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore

theorem latest_write_wins : readRegs [(3,8),(3,2)] 3 = 8 := by decide
theorem absent_register_zero : readRegs [(3,8),(3,2)] 4 = 0 := by decide

theorem terminal_zero_fuel (rs : RegFile) : runFuel 0 [] rs = some rs := by
  simp [runFuel]

theorem pending_skip_zero_fuel (rs : RegFile) : runFuel 0 [.stmt .skip] rs = none := by
  simp [runFuel]

theorem semantic_noop_still_needs_transition (rs : RegFile) :
    runFuel 1 [.stmt .skip] rs = some rs := by
  simp [runFuel, step]

-- One stack step does not mean one bounded-size arithmetic operation.
theorem one_transition_unbounded_value (n : Nat) :
    runFuel 1 [.stmt (.set 0 (.pow2 (.constant n)))] [] = some [(0,2^n)] := by
  simp [runFuel, step, writeRegs, evalRegs]

theorem division_zero_semantics : evalRegs (.div (.constant 7) (.constant 0)) [] = 0 := by decide
theorem modulo_zero_semantics : evalRegs (.mod (.constant 7) (.constant 0)) [] = 7 := by decide

-- If the bound register is also the loop index, the count is still captured.
def aliasBound : PackedProgram := ⟨2,2,
  .loop 0 (.reg 0) (.set 2 (.add (.reg 2) (.constant 1)))⟩
theorem captured_aliased_count : evaluateIndexFuel 16 (programIndex aliasBound) 3 0 = some 1 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, aliasBound, ↓reduceIte]
  decide

theorem successful_fuel_agrees (e n word fuel value : Nat)
    (h : evaluateIndexFuel fuel e n word = some value) :
    value = evaluateIndex e n word := by
  exact evaluateIndexFuel_sound h

end OperationalInterpreterAudit

#check @OperationalInterpreterAudit.latest_write_wins
#print axioms OperationalInterpreterAudit.latest_write_wins
#check @OperationalInterpreterAudit.absent_register_zero
#print axioms OperationalInterpreterAudit.absent_register_zero
#check @OperationalInterpreterAudit.terminal_zero_fuel
#print axioms OperationalInterpreterAudit.terminal_zero_fuel
#check @OperationalInterpreterAudit.pending_skip_zero_fuel
#print axioms OperationalInterpreterAudit.pending_skip_zero_fuel
#check @OperationalInterpreterAudit.semantic_noop_still_needs_transition
#print axioms OperationalInterpreterAudit.semantic_noop_still_needs_transition
#check @OperationalInterpreterAudit.one_transition_unbounded_value
#print axioms OperationalInterpreterAudit.one_transition_unbounded_value
#check @OperationalInterpreterAudit.division_zero_semantics
#print axioms OperationalInterpreterAudit.division_zero_semantics
#check @OperationalInterpreterAudit.modulo_zero_semantics
#print axioms OperationalInterpreterAudit.modulo_zero_semantics
#check @OperationalInterpreterAudit.captured_aliased_count
#print axioms OperationalInterpreterAudit.captured_aliased_count
#check @OperationalInterpreterAudit.successful_fuel_agrees
#print axioms OperationalInterpreterAudit.successful_fuel_agrees

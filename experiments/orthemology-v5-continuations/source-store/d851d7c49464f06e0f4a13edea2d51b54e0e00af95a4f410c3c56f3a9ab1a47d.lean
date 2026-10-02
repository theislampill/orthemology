import UniformComputabilityMachine

/-! Kernel-checked semantic controls and supplemental compiled execution vectors.
Transition fuel counts statement/repeat tasks, not Python expression-meter ticks. -/
namespace P02.Codec.UniformComputability
open P02A2.ObserverCore

/-- Changing the bound register in the body must not change the captured count. -/
def capturedBoundProgram : PackedProgram :=
  ⟨2, 2, .seq (.set 2 (.constant 0))
    (.loop 3 (.reg 0) (.seq (.set 0 (.constant 0))
      (.set 2 (.add (.reg 2) (.constant 1)))))⟩

/-- A body may overwrite the loop register; the next index is still written. -/
def overwrittenIndexProgram : PackedProgram :=
  ⟨2, 2, .loop 3 (.reg 0)
    (.seq (.set 2 (.reg 3)) (.set 3 (.constant 99)))⟩

def arithmeticProgram : PackedProgram :=
  ⟨2, 2, .set 2
    (.add (.mul (.reg 0) (.reg 1))
      (.add (.sub (.reg 0) (.reg 1))
        (.add (.div (.reg 1) (.constant 0))
          (.add (.mod (.reg 0) (.constant 0))
            (.add (.le (.reg 0) (.reg 1))
              (.add (.eq (.reg 0) (.reg 1)) (.pow2 (.constant 2))))))))⟩

def branchProgram : PackedProgram :=
  ⟨2, 2, .branch (.reg 0) (.set 2 (.constant 1)) (.set 2 (.constant 0))⟩

theorem captured_count_control :
    evaluateIndexFuel 64 (programIndex capturedBoundProgram) 3 0 = some 1 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, capturedBoundProgram, ↓reduceIte]
  decide

theorem overwritten_index_control :
    evaluateIndexFuel 64 (programIndex overwrittenIndexProgram) 3 0 = some 0 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, overwrittenIndexProgram, ↓reduceIte]
  decide

theorem arithmetic_control :
    evaluateIndexFuel 8 (programIndex arithmeticProgram) 3 2 = some 0 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, arithmeticProgram, ↓reduceIte]
  decide

theorem branch_zero_control :
    evaluateIndexFuel 8 (programIndex branchProgram) 0 9 = some 0 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, branchProgram, ↓reduceIte]
  decide

theorem branch_nonzero_control :
    evaluateIndexFuel 8 (programIndex branchProgram) 2 9 = some 1 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, branchProgram, ↓reduceIte]
  decide

theorem zero_loop_control :
    evaluateIndexFuel 8 (programIndex overwrittenIndexProgram) 0 0 = some 0 := by
  simp only [evaluateIndexFuel, decodeIndex_programIndex, overwrittenIndexProgram, ↓reduceIte]
  decide

theorem invalid_zero_control : evaluateIndexFuel 0 0 9 9 = some 0 := by
  simp [evaluateIndexFuel, decodeIndex, decodeNumeric]

theorem wrong_arity_control :
    evaluateIndexFuel 0 (programIndex ⟨1,0,.skip⟩) 9 9 = some 0 := by
  simp [evaluateIndexFuel, decodeIndex_programIndex]

/-- All these values use the actual numeric serialization and actual decoder. -/
def executionVectors : List (String × List (Option ℕ)) :=
  [("captured-count", (List.range 6).map (fun n => evaluateIndexFuel 128 (programIndex capturedBoundProgram) n 0)),
   ("overwrite-index", (List.range 6).map (fun n => evaluateIndexFuel 128 (programIndex overwrittenIndexProgram) n 0)),
   ("arithmetic", (List.range 6).map (fun n => evaluateIndexFuel 8 (programIndex arithmeticProgram) n 2)),
   ("branch", (List.range 6).map (fun n => evaluateIndexFuel 8 (programIndex branchProgram) n 0))]

#eval executionVectors
#print axioms decodeNumeric_primrec
#print axioms execRegs_correct
#print axioms runFuel_sound
#print axioms runFuel_complete
#print axioms evaluateIndexFuel_sound
#print axioms evaluateIndexFuel_complete
#print axioms evaluateIndexFuel_mono
#print axioms evaluateIndexSearch_exact
#print axioms evaluateIndex_computable_of_fuel
#print axioms exhausted_one
#print axioms captured_count_control
#print axioms overwritten_index_control
#print axioms arithmetic_control
end P02.Codec.UniformComputability

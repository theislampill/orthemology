import IndexedRuntime
import ObserverFixtures

namespace Orthemology.CertifiedObserver.Indexed.Fixtures
open Orthemology.Frontier Orthemology.Frontier.MealyMeasure
open Orthemology.Frontier.MealyMeasure.Fixtures
open P02.Codec P02A2.ObserverCore
open Set MeasureTheory
open P02A2.Q8Measure (fairCantor)

/-- An actual binary P02 program: stage0 emits zero; later stages copy the
latest bit precisely when the first acquired bit was one. -/
def splitProgram : PackedProgram where
  arity := 2
  output := 2
  body := .branch (.eq (.reg 0) (.constant 0)) (.set 2 (.constant 0))
    (.set 2 (.mul (.mod (.div (.reg 1) (.pow2 (.reg 0))) (.constant 2))
      (.mod (.reg 1) (.constant 2))))

def splitIndex : ℕ := programIndex splitProgram

theorem split_decode : decodeIndex splitIndex = some splitProgram := decodeIndex_programIndex _

theorem split_evaluate (n word : ℕ) :
    evaluateIndex splitIndex n word =
      if n = 0 then 0 else ((word / 2^n % 2) * (word % 2)) % 2 := by
  rw [evaluateIndex, split_decode]
  by_cases h : n = 0 <;> simp [splitProgram, exec, evalExpr, binaryStore, h]

theorem append_half (w : ℕ) (b : Bool) : appendBit w b / 2 = w := by
  cases b <;> simp only [appendBit, Bool.false_eq_true, ↓reduceIte] <;> omega

theorem append_last (w : ℕ) (b : Bool) : appendBit w b % 2 = if b then 1 else 0 := by
  cases b <;> simp [appendBit, Nat.add_mod, Nat.mul_mod]

theorem append_first (w k : ℕ) (b : Bool) :
    appendBit w b / 2^(k+1) % 2 = w / 2^k % 2 := by
  rw [pow_succ', ← Nat.div_div_eq_div_mul, append_half]

def classify (cfg : Indexed.Config) : Fin 3 :=
  if cfg.1 = 0 then 0 else if cfg.2 / 2^(cfg.1-1) % 2 = 1 then 2 else 1

theorem split_local_output (cfg : Indexed.Config) (b : Bool) :
    (machine splitIndex).out cfg b = splitMachine.out (classify cfg) b := by
  rcases cfg with ⟨n,w⟩
  cases n with
  | zero => simp [machine, split_evaluate, classify, splitMachine]
  | succ k =>
      change decide (evaluateIndex splitIndex (k+1) (appendBit w b) % 2 = 1) = _
      rw [split_evaluate]
      simp only [Nat.add_eq_zero_iff, Nat.one_ne_zero, and_false, ↓reduceIte, Nat.mod_mod]
      rw [append_first, append_last]
      have hz : w / 2^k % 2 = 0 ∨ w / 2^k % 2 = 1 := by omega
      rcases hz with hz | hz <;> cases b <;> simp [classify, splitMachine, hz]

theorem split_local_next (cfg : Indexed.Config) (b : Bool) :
    classify ((machine splitIndex).next cfg b) = splitMachine.next (classify cfg) b := by
  rcases cfg with ⟨n,w⟩
  cases n with
  | zero => cases b <;> simp [classify, machine, append_last, splitMachine, appendBit]
  | succ k =>
      change classify (k+1+1, appendBit w b) = _
      simp only [classify, Nat.add_eq_zero_iff, Nat.one_ne_zero, and_false, ↓reduceIte,
        Nat.add_sub_cancel]
      rw [append_first]
      by_cases h : w / 2^k % 2 = 1 <;> simp [h, splitMachine]

def splitSimulation : Simulation (machine splitIndex) splitMachine :=
  simulationOfMap _ _ classify split_local_output split_local_next

theorem indexed_split_law : sourceLaw splitIndex = law splitMachine 0 := by
  rw [source_law_exact]
  exact simulation_law splitSimulation rfl

theorem indexed_split_solver :
    (solveDefect splitMachine 0 : ℝ) = P02A2.defect (sourceLaw splitIndex) :=
  certified_index_defect splitIndex splitMachine splitSimulation 0 rfl

/-- This nontrivial source, actual parser, growing-prefix state and scheduled
stack-runtime output all share the literal one-half nonatomic defect. -/
theorem runtime_split_defect :
    P02A2.defect (fairCantor.map (runtimeOutput splitIndex)) = (1/2 : ℝ) := by
  rw [runtime_law_exact, indexed_split_law, P02A2.defect, split_atomic_mass_half]
  norm_num

#eval decodeIndex splitIndex == some splitProgram
#eval uniformFuel splitIndex 0
#eval uniformFuel splitIndex 1
#eval uniformFuel splitIndex 3
#eval List.ofFn (fun k : Fin 3 => runtimeOutput splitIndex (fun n => decide (n ≠ 1)) k)
#eval List.ofFn (fun k : Fin 3 => runtimeOutput splitIndex (fun n => decide (n ≠ 0)) k)

end Orthemology.CertifiedObserver.Indexed.Fixtures

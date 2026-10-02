import Q8Compiler

namespace P02A2.Q8Witnesses
open P02A2.Q8Machine P02A2.Q8Compiler P02A2.ObserverCore

def immediateHalt : Machine 1 := fun _ => .halt
def foreverIncrement : Machine 1 := fun _ => .inc 0 0

theorem immediateHalt_halts : Halts immediateHalt (by decide) := ⟨1, rfl⟩

theorem foreverIncrement_flags (k : ℕ) :
    (run foreverIncrement (by decide) k).halted = false := by
  induction k with
  | zero => rfl
  | succ k ih => simp [run, step, ih, foreverIncrement, execute]

theorem foreverIncrement_never_halts : ¬ Halts foreverIncrement (by decide) := by
  rintro ⟨k, hk⟩
  rw [foreverIncrement_flags] at hk
  cases hk

theorem immediateHalt_defect : defect (compiledLaw immediateHalt) = 1 :=
  (compiled_defect_one_iff_halting immediateHalt (by decide)).mpr immediateHalt_halts

theorem foreverIncrement_defect : defect (compiledLaw foreverIncrement) = 0 :=
  (compiled_defect_zero_iff_nonhalting foreverIncrement (by decide)).mpr foreverIncrement_never_halts

-- Direct kernel reductions of the actual generated LOOP syntax.
example : programValue immediateHalt 0 3 = 1 := by decide +kernel
example : programValue immediateHalt 5 64 = 0 := by decide +kernel
example : programValue foreverIncrement 5 127 = 0 := by decide +kernel

def wrongBound {n : ℕ} (M : Machine n) : Stmt :=
  .seq initCode (.seq (.loop 6 (.reg 0) (compiledStep M))
    (.seq (.set 2 (.constant 0))
      (.branch (.reg 5) (.set 2 (.mod (.reg 1) (.constant 2))) .skip)))

def movingPcScan {n : ℕ} (M : Machine n) : List (Fin n) → Stmt
  | [] => .skip
  | i::is => .seq
      (.branch (.eq (.reg 3) (.constant i.val)) (compileInstruction (M i)) .skip)
      (movingPcScan M is)

def movingPcStep {n : ℕ} (M : Machine n) : Stmt :=
  .branch (.eq (.reg 5) (.constant 0)) (movingPcScan M (List.finRange n)) .skip

def wrongSnapshot {n : ℕ} (M : Machine n) : Stmt :=
  .seq initCode (.seq (.loop 6 (.add (.reg 0) (.constant 1)) (movingPcStep M))
    (.seq (.set 2 (.constant 0))
      (.branch (.reg 5) (.set 2 (.mod (.reg 1) (.constant 2))) .skip)))

def delayedHalt : Machine 2 := fun i => if i = 0 then .inc 0 1 else .halt

theorem wrong_bound_changes_immediate_output :
    exec (wrongBound immediateHalt) (inputStore 0 3) 2 = 0 ∧
    programValue immediateHalt 0 3 = 1 := by decide +kernel

theorem wrong_snapshot_changes_delayed_output :
    exec (wrongSnapshot delayedHalt) (inputStore 0 3) 2 = 1 ∧
    programValue delayedHalt 0 3 = 0 := by decide +kernel

end P02A2.Q8Witnesses

import PRWitnesses
namespace IndependentPR
open P02A2.PRProgram P02A2.PRDerivation P02A2.ObserverCore

-- Reversing a noncommutative two-input source must survive composition.
def selectFirst : Code 2 := .projection 0
def swapFirst : Code 2 := .compose selectFirst (fun i => if i.val = 0 then .projection 1 else .projection 0)
theorem swap_source (a b : Nat) : denote (compile swapFirst) ![a,b] = b := by
  rw [compile_correct]
  rfl

-- A program may reuse an input register as its output.
def inPlace : Program 1 := ⟨.set 0 (.add (.reg 0) (.constant 1)), 0⟩
theorem specialize_in_place (a : Nat) :
    denote (P02A2.PRSpecialize.specialize inPlace a) Fin.elim0 = a+1 := by
  rw [P02A2.PRSpecialize.specialize_correct]
  simp [denote, inPlace, exec, evalExpr, P02A2.LoopPrimrec.extend]

-- Scratch registers start at zero for every call, not at the caller's value.
def scratchCounter : Program 0 := ⟨.set 7 (.add (.reg 7) (.constant 1)), 7⟩
theorem reset_scratch (caller : Store) :
    exec (call scratchCounter 10 Fin.elim0 0) caller 0 = 1 := by
  rw [call_value scratchCounter 10 Fin.elim0 0 (by intro i; exact Fin.elim0 i)]
  simp [denote, scratchCounter, exec, evalExpr, P02A2.LoopPrimrec.extend]
theorem repeated_reset_scratch (caller : Store) :
    exec (.seq (call scratchCounter 10 Fin.elim0 0) (call scratchCounter 10 Fin.elim0 0)) caller 0 = 1 := by
  change exec (call scratchCounter 10 Fin.elim0 0) (exec (call scratchCounter 10 Fin.elim0 0) caller) 0 = 1
  exact reset_scratch _
theorem reset_not_accumulation (caller : Store) :
    exec (.seq (call scratchCounter 10 Fin.elim0 0) (call scratchCounter 10 Fin.elim0 0)) caller 0 ≠ 2 := by
  rw [repeated_reset_scratch]
  decide

-- LOOP evaluates the bound once, before body mutation of that bound register.
def overwriteBound : Stmt := .loop 1 (.reg 0)
  (.seq (.set 0 (.constant 0)) (.set 2 (.add (.reg 2) (.constant 1))))
theorem snapshot_bound : exec overwriteBound (fun r => if r = 0 then 3 else 0) 2 = 3 := by
  decide

-- Extensional coverage does not say arbitrary supplied source syntax is correct.
def wrongSuccessor : Program 1 := zeroProgram 1
theorem wrong_program_not_covered_by_name : denote wrongSuccessor ![4] ≠ 5 := by
  rw [show wrongSuccessor = zeroProgram 1 from rfl, zeroProgram_correct]
  decide
end IndependentPR
#print axioms IndependentPR.swap_source
#print axioms IndependentPR.specialize_in_place
#print axioms IndependentPR.reset_scratch
#print axioms IndependentPR.repeated_reset_scratch
#print axioms IndependentPR.reset_not_accumulation
#print axioms IndependentPR.snapshot_bound
#print axioms IndependentPR.wrong_program_not_covered_by_name

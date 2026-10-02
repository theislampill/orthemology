import CandidateSource

namespace P02A2.CandidateWitnesses
open P02A2.ObserverCore P02A2.CandidateCompiler P02A2.CandidateSource

def zeroStore : Store := fun _ => 0
def boundedMatrix : Stmt := .set 3 (.le (.reg 2) (.reg 1))
def trueMatrixCode : Stmt := .set 3 (.constant 1)

theorem bounded_registers : registerSet boundedMatrix 3 = Finset.range 4 := by
  ext r
  simp only [registerSet, boundedMatrix, P02A2.LoopRenaming.stmtRegs,
    P02A2.LoopRenaming.exprRegs, Finset.mem_union, Finset.mem_insert,
    Finset.mem_singleton, Finset.mem_range]
  omega

theorem true_registers : registerSet trueMatrixCode 3 = Finset.range 4 := by
  ext r
  simp only [registerSet, trueMatrixCode, P02A2.LoopRenaming.stmtRegs,
    P02A2.LoopRenaming.exprRegs, Finset.mem_union, Finset.mem_insert,
    Finset.not_mem_empty, or_false, Finset.mem_range]
  omega

theorem bounded_registerList : registerList boundedMatrix 3 = [0,1,2,3] := by
  rw [registerList, bounded_registers, Finset.sort_range]
  rfl

theorem true_registerList : registerList trueMatrixCode 3 = [0,1,2,3] := by
  rw [registerList, true_registers, Finset.sort_range]
  rfl

def wrongTestTry (call : Stmt) : Stmt :=
  .seq (.set 9 (.constant 1))
    (.seq (.loop 7 (.reg 5) (testBody call))
      (.branch (.reg 9) (.seq (.set 3 (.reg 6)) (.set 8 (.constant 1))) .skip))

def wrongTestBound (call : Stmt) (stage : Expr) : Stmt :=
  .seq (.set 5 stage) (.seq (.set 3 (.add (.reg 5) (.constant 1)))
    (.seq (.set 8 (.constant 0)) (.loop 6 (.add (.reg 5) (.constant 1))
      (.branch (.eq (.reg 8) (.constant 0)) (wrongTestTry call) .skip))))

def noFoundGuard (call : Stmt) (stage : Expr) : Stmt :=
  .seq (.set 5 stage) (.seq (.set 3 (.add (.reg 5) (.constant 1)))
    (.seq (.set 8 (.constant 0)) (.loop 6 (.add (.reg 5) (.constant 1)) (tryCandidate call))))

theorem candidate_checks_inclusive_test_bound :
    exec (sourceCandidate boundedMatrix 3 0 (.constant 2)) zeroStore 3 = 2 ∧
    exec (wrongTestBound (matrixCall boundedMatrix 3 0) (.constant 2)) zeroStore 3 = 1 := by
  unfold sourceCandidate matrixCall registerMap
  simp only [bounded_registerList]
  decide +kernel

theorem candidate_retains_first_success :
    exec (sourceCandidate trueMatrixCode 3 0 (.constant 2)) zeroStore 3 = 0 ∧
    exec (noFoundGuard (matrixCall trueMatrixCode 3 0) (.constant 2)) zeroStore 3 = 2 := by
  unfold sourceCandidate matrixCall registerMap
  simp only [true_registerList]
  decide +kernel

end P02A2.CandidateWitnesses

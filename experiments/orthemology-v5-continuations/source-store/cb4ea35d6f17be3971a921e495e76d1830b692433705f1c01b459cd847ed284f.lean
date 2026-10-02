import LoopRenaming

namespace P02A2.LoopInliningWitnesses
open P02A2.ObserverCore P02A2.LoopRenaming

def zeroStore : Store := fun _ => 0
def localMap (r : ℕ) : ℕ := r + 10
def incrementScratch : Stmt := .set 1 (.add (.reg 1) (.constant 1))
def safeInline : Stmt := inlineCode localMap [0,1] [(0,.constant 0)] incrementScratch 1 0

def missingReset : Stmt := .seq (loadArgs localMap [(0,.constant 0)])
  (.seq (renameStmt localMap incrementScratch) (.set 0 (.reg (localMap 1))))

theorem full_reset_prevents_history_dependence :
    exec safeInline zeroStore 0 = 1 ∧ exec safeInline (exec safeInline zeroStore) 0 = 1 := by
  decide +kernel

theorem omitted_reset_creates_history_dependence :
    exec missingReset zeroStore 0 = 1 ∧ exec missingReset (exec missingReset zeroStore) 0 = 2 := by
  decide +kernel

def twoAssignments : Stmt := .seq (.set 0 (.constant 1)) (.set 1 (.constant 2))

theorem colliding_renaming_changes_semantics :
    exec twoAssignments zeroStore 0 = 1 ∧ exec (renameStmt (fun _ => 10) twoAssignments) zeroStore 10 = 2 := by
  decide +kernel

def capturedArgCaller : Store := fun r => if r = 10 then 7 else 0

def capturedArgInline : Stmt := inlineCode localMap [0,1] [(0,.reg 10)] (.set 1 (.reg 0)) 1 0

theorem nonfresh_argument_is_overwritten :
    exec capturedArgInline capturedArgCaller 0 = 0 ∧
    exec (.set 1 (.reg 0)) (sourceLoad [(0,.reg 10)] capturedArgCaller zeroStore) 1 = 7 := by
  decide +kernel

end P02A2.LoopInliningWitnesses

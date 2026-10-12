import LoopInliningWitnesses
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopInliningWitnesses
example : exec twoAssignments zeroStore 0 = exec (renameStmt (fun _ => 10) twoAssignments) zeroStore 10 := by decide +kernel

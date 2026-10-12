import LoopInliningWitnesses
open P02A2.ObserverCore P02A2.LoopInliningWitnesses
example : exec safeInline (exec safeInline zeroStore) 0 = 1 := by decide +kernel
example : exec twoAssignments zeroStore 0 = 1 := by decide +kernel

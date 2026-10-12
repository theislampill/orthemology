import LoopInliningWitnesses
open P02A2.ObserverCore P02A2.LoopInliningWitnesses
example : exec missingReset (exec missingReset zeroStore) 0 = 1 := by decide +kernel

import LoopInliningWitnesses
open P02A2.ObserverCore P02A2.LoopRenaming P02A2.LoopInliningWitnesses
example : exec capturedArgInline capturedArgCaller 0 = exec (.set 1 (.reg 0)) (sourceLoad [(0,.reg 10)] capturedArgCaller zeroStore) 1 := by decide +kernel

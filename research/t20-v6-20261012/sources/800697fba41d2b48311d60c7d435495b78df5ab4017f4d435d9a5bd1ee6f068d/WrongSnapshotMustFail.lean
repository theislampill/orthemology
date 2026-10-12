import Q8Witnesses
open P02A2.Q8Witnesses P02A2.Q8Compiler P02A2.ObserverCore
example : exec (wrongSnapshot delayedHalt) (inputStore 0 3) 2 = programValue delayedHalt 0 3 := by decide +kernel

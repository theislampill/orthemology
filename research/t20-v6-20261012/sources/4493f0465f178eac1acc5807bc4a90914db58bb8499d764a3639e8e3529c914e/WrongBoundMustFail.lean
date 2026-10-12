import Q8Witnesses
open P02A2.Q8Witnesses P02A2.Q8Compiler P02A2.ObserverCore
example : exec (wrongBound immediateHalt) (inputStore 0 3) 2 = programValue immediateHalt 0 3 := by decide +kernel

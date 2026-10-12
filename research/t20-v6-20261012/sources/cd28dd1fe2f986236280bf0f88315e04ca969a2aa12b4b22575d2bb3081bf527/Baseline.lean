import Q8Witnesses
open P02A2.Q8Witnesses P02A2.Q8Compiler
example : programValue immediateHalt 0 3 = 1 := by decide +kernel
example : programValue delayedHalt 0 3 = 0 := by decide +kernel

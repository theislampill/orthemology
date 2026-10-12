import LiteralShiftControls
open P02A2.ObserverCore P02.LiteralShift P02.LiteralShift.Controls
example : exec (compileShift zeroBody 2 1 3) (initial 1 5) 2 = 0 := by decide

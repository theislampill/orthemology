import LiteralShiftControls
open P02A2.ObserverCore P02.LiteralShift P02.LiteralShift.Controls
example : exec (compileShift oneBody 2 1 2) (initial 0 2) 2 = 1 := by decide

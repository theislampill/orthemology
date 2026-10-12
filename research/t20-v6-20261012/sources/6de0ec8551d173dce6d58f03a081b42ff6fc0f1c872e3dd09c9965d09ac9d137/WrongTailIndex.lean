import LiteralShiftControls
open P02A2.ObserverCore P02.LiteralShift P02.LiteralShift.Controls
example : exec (compileShift indexBody 2 1 2) (initial 1 6) 2 = 1 := by
  rw [fresh_tail_index_zero]
  decide

import LiteralShiftControls
open P02A2.ObserverCore P02.LiteralShift P02.LiteralShift.Controls
example : exec (compileShift sentinelBody 2 1 2) (initial 1 6) 2 = 0 := by
  rw [fresh_tail_sentinel]
  decide

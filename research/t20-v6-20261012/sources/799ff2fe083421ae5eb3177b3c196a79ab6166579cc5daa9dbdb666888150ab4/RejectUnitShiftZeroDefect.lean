import LiteralShiftDefect
open P02.LiteralShift P02A2 P02A2.Q8Measure
example : defect (fairCantor.map (compiledOutput .skip 2 1 1)) = 0 := by
  rw [compileShift_one_defect .skip 2 1 (by decide)]
  simp only [one_ne_zero]
  decide

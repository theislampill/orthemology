import VeracityControls
set_option synthInstance.maxSize 100000
open VeracityBoundary VeracityBoundary.Controls
-- This false strengthening must fail by kernel decision, not by missing imports.
example : Veracity dropC false := by
  simp only [Veracity, dropC, fixture]
  decide

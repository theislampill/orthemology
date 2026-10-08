import VeracityControls
set_option synthInstance.maxSize 100000
open VeracityBoundary VeracityBoundary.Controls
-- This false strengthening must fail by kernel decision, not by missing imports.
example : Veracity dropN false := by
  simp only [Veracity, dropN, fixture]
  decide

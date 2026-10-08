import VeracityControls
set_option synthInstance.maxSize 100000
open VeracityBoundary VeracityBoundary.Controls
example : Veracity localGlobal false := by
  simp only [Veracity, localGlobal]
  decide

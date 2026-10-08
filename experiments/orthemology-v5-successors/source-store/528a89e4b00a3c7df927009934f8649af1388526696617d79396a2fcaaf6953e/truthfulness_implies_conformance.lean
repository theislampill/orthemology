import VeracityControls
set_option synthInstance.maxSize 100000
open VeracityBoundary VeracityBoundary.Controls
example : P nonconforming false := by
  simp only [P, nonconforming, positive]
  decide

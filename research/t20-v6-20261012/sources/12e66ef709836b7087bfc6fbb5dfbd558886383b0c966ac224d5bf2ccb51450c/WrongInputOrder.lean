import BoundaryControls
open P02.Codec IndependentBoundaryControls
example : evaluateIndex (programIndex (pack difference)) 1 2 = (2-1)%2 := by
  rw [binary_input_order]
  norm_num

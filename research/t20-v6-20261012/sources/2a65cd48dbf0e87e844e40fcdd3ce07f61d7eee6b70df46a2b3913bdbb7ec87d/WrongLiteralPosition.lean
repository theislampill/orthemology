import BoundaryControls
open P02.Codec IndependentBoundaryControls
example : evaluateIndex (parameterIndex firstParameter 3) 0 0 = 0 := by
  rw [literal_parameter_is_first]
  norm_num

import CodecVarint
open P02.Codec
example : uvRead [128,0] = some (0,[]) := by
  rw [uvRead_reject_overlong_zero]
  decide

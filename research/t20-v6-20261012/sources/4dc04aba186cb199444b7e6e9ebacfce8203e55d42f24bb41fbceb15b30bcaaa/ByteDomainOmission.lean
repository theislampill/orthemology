import BoundaryControls
open P02.Codec
example : Bytes [256] := by
  intro b hb
  simp only [List.mem_singleton] at hb
  subst b
  norm_num

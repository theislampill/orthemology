import CodecProgram
open P02.Codec P02A2.ObserverCore
example : encodeBytes (PackedProgram.mk 2 2 (.set 2 (.constant 1))) =
    [80,48,50,76,1,2,2,17,1,16,2,1,1] := by
  have h2 : uv 2 = [2] := by rw [uv]; norm_num
  norm_num [encodeBytes, magic, stmtBytes, exprBytes, h2, uv_one]

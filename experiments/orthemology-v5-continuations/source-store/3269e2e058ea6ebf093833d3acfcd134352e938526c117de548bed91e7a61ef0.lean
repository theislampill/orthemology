import CodecProgram
import PRWitnesses

namespace P02.Codec
open P02A2.ObserverCore

def literal128 : PackedProgram := ⟨2,2,.set 2 (.constant 128)⟩

theorem literal128_bytes : encodeBytes literal128 = [80,48,50,76,1,2,2,16,2,1,128,1] := by
  have h2 : uv 2 = [2] := by rw [uv]; norm_num
  simp [encodeBytes, literal128, magic, stmtBytes, exprBytes, h2, uv_128]

theorem literal128_roundtrip : decodeIndex (programIndex literal128) = some literal128 :=
  decodeIndex_programIndex literal128

theorem rejects_wrong_magic_version : decodeBytes [80,48,50,76,2,2,2,17,0] = none := by
  decide +kernel

theorem rejects_trailing_byte : decodeBytes (encodeBytes literal128 ++ [0]) = none := by
  have hh : stmtDepth literal128.body ≤ (stmtBytes literal128.body ++ [0]).length := by
    have := stmtDepth_le_length literal128.body
    simp only [List.length_append, List.length_singleton]
    omega
  have hr := readStmt_append literal128.body [0] (stmtBytes literal128.body ++ [0]).length hh
  simp only [List.length_append, List.length_singleton] at hr
  simp [decodeBytes, encodeBytes, List.append_assoc, stripMagic_append, uvRead_append, hr]

theorem compiled_addition_index (a b : ℕ) :
    evaluateIndex (programIndex (pack (P02A2.PRDerivation.compile P02A2.PRWitnesses.addition))) a b = (b+a)%2 := by
  rw [evaluateIndex_programIndex, P02A2.PRWitnesses.compiled_addition]

theorem rejects_specialized_arity_one (a b : ℕ) :
    evaluateIndex (programIndex (pack (P02A2.PRSpecialize.specialize
      (P02A2.PRDerivation.compile P02A2.PRWitnesses.addition) a))) b 0 = 0 := by
  -- This is deliberately a Program 1 after specialization, so not an observer.
  rw [evaluateIndex, decodeIndex_programIndex]
  simp [pack]

end P02.Codec

import UniformComputabilityControls

/-! Independent adversarial controls for the actual unchanged decoder and parser.
These exercise inputs outside canonical generated program encodings. -/
namespace UniformIndependentAudit
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore

@[local simp] theorem uv_small {n : ℕ} (h : n < 128) : uv n = [n] := by
  rw [uv, dif_pos h]

@[local simp] theorem uv_255 : uv 255 = [255,1] := by
  rw [uv]
  norm_num
  decide

@[local simp] theorem numeric_decode (bs : List ℕ) (hbs : Bytes bs) :
    decodeIndex (encodeNumeric bs) = decodeBytes bs := by
  simp [decodeIndex, hbs]

theorem reject_truncated_varint : uvRead [128] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem reject_overlong_zero : uvRead [128,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem reject_overlong_one : uvRead [129,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem reject_nonbyte : uvRead [256] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem varint_exact_suffix : uvRead [255,1,999,0] = some (255,[999,0]) := by
  simp only [uvRead]
  change (if [255,1] = uv 255 then some (255,[999,0]) else none) = some (255,[999,0])
  rw [uv_255]; decide

theorem expr_zero_fuel : readExpr 0 [1,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_unknown_tag : readExpr 8 [0,1,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_malformed_literal : readExpr 8 [1,128,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_nonbyte_literal : readExpr 8 [1,256] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_exact_suffix : readExpr 1 [1,0,999,17] = some (.constant 0,[999,17]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_shared_child_fuel :
    readExpr 2 [3,1,1,1,2,999] = some (.add (.constant 1) (.constant 2),[999]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem expr_insufficient_depth : readExpr 1 [3,1,1,1,2] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

theorem stmt_zero_fuel : readStmt 0 [17,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_unknown_tag : readStmt 8 [20,17,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_empty_variadic : readStmt 1 [17,0,999] = some (.skip,[999]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_singleton_variadic : readStmt 2 [17,1,17,0,999] = some (.skip,[999]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_three_variadic :
    readStmt 2 [17,3,17,0,17,0,17,0,999] =
      some (.seq .skip (.seq .skip .skip),[999]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_count_exceeds_payload : readStmt 8 [17,2,17,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_malformed_count : readStmt 8 [17,128,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem stmt_insufficient_depth : readStmt 1 [17,1,17,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem readMany_zero_preserves_arbitrary :
    readMany (readStmt 0) 0 [999,256] = some ([],[999,256]) := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

theorem decode_noncanonical_syntax :
    decodeBytes (magic ++ [2,0,17,1,17,0]) = some ⟨2,0,.skip⟩ := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem decode_trailing_rejected :
    decodeBytes (magic ++ [2,0,17,0,999]) = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem decode_wrong_magic : decodeBytes [80,48,50,76,2,2,0,17,0] = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem decode_overlong_arity : decodeBytes (magic ++ [130,0,0,17,0]) = none := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]
theorem numeric_missing_sentinel : decodeIndex 0 = none := by decide

/-- The actual numeric decoder accepts source-valid singleton Seq syntax that
is never emitted for skip by stmtBytes; this is beyond generated-code tests. -/
theorem numeric_nongenerated_syntax :
    decodeIndex (encodeNumeric (magic ++ [2,0,17,1,17,0])) = some ⟨2,0,.skip⟩ := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

theorem actual_numeric_nongenerated_value :
    evaluateIndex (encodeNumeric (magic ++ [2,0,17,1,17,0])) 3 9 = 1 := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

theorem actual_numeric_trailing_zero :
    evaluateIndex (encodeNumeric (magic ++ [2,0,17,0,99])) 3 9 = 0 := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

theorem wrong_arity_at_zero_fuel :
    evaluateIndexFuel 0 (encodeNumeric (magic ++ [1,0,17,0])) 3 9 = some 0 := by norm_num [readExpr, readStmt, readBinary, readMany, sequenceList, uvRead, readAccum, decodeBytes, stripMagic, magic, evaluateIndex, evaluateIndexFuel, binaryStore, exec, evalExpr, Bytes, payload_eq_mod, Nat.shiftLeft_eq]

/-- This malformed byte list is arbitrary in length and outside the byte range. -/
theorem unknown_expr_tag_all_fuels (fuel : ℕ) (bs : List ℕ) :
    readExpr fuel (999::bs) = none := by cases fuel <;> simp [readExpr]

theorem unknown_stmt_tag_all_fuels (fuel : ℕ) (bs : List ℕ) :
    readStmt fuel (999::bs) = none := by cases fuel <;> simp [readStmt]

end UniformIndependentAudit

import UniformDecoderPrimrec
import MalformedControls

/-! Independent type checks: no hidden effective-decoder or generated-code premise. -/
namespace UniformIndependentAudit
open P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore

theorem expression_parser_all_inputs : Primrec₂ readExpr := readExpr_primrec
theorem statement_parser_all_inputs : Primrec₂ readStmt := readStmt_primrec
theorem actual_numeric_decoder : Primrec decodeIndex := decodeIndex_primrec
theorem actual_bounded_numeric_machine :
    Primrec₂ (fun input : ℕ × ℕ × ℕ => fun fuel =>
      evaluateIndexFuel fuel input.1 input.2.1 input.2.2) := evaluateIndexFuel_primrec

theorem exact_existing_premise :
    Computable₂ (fun (input : ℕ × ℕ × ℕ) fuel =>
      evaluateIndexFuel fuel input.1 input.2.1 input.2.2) := evaluateIndexFuel_primrec.to_comp

theorem exact_external_endpoint :
    Computable (fun code : ℕ =>
      evaluateIndex code.unpair.1 code.unpair.2.unpair.1 code.unpair.2.unpair.2) :=
  evaluateIndex_nat_computable

theorem external_input_projection (index n word : ℕ) :
    (fun code : ℕ => evaluateIndex code.unpair.1 code.unpair.2.unpair.1 code.unpair.2.unpair.2)
      (Nat.pair index (Nat.pair n word)) = evaluateIndex index n word := by simp

/-- Arbitrary byte lists and fuel, rather than generated syntax only. -/
theorem expression_suffix_table_exact (bs : List ℕ) (fuel : ℕ) :
    (exprTable bs fuel).getD 0 none = readExpr fuel bs := by
  simpa using exprTable_correct bs fuel 0 (Nat.zero_le _)

theorem statement_suffix_table_exact (bs : List ℕ) (fuel : ℕ) :
    (stmtTable bs fuel).getD 0 none = readStmt fuel bs := by
  simpa using stmtTable_correct bs fuel 0 (Nat.zero_le _)

/-- The suffix restriction in the table lookup lemma is essential. A same-length
unrelated list must not be substituted as if its length identified its content. -/
theorem expression_lookup_requires_suffix :
    exprLookup [1,0] (exprTable [1,0] 1) [1,1] ≠ readExpr 1 [1,1] := by
  have h : exprLookup [1,0] (exprTable [1,0] 1) [1,1] = readExpr 1 [1,0] := by
    simpa [exprLookup] using exprTable_correct [1,0] 1 0 (by decide)
  rw [h]
  norm_num [readExpr, uvRead, readAccum, payload_eq_mod, Nat.shiftLeft_eq, uv_small]

/-- Serialization and internal syntax numbering are genuinely separate. -/
theorem byte_index_is_not_internal_syntax_code :
    programIndex ⟨2,0,.skip⟩ ≠ packedEncode ⟨2,0,.skip⟩ := by
  norm_num [programIndex, encodeNumeric, encodeBytes, fromBytes, magic,
    stmtBytes, packedEncode, stmtEncode, uv_small, Nat.pair]

end UniformIndependentAudit

import CodecVarint
import CodecNumeric
import CodecExpr
import CodecStmt
import CodecProgram
import CodecParameter
import CodecPrimrec
import CodecIndexPrimrec
import CodecWitnesses
import Pi3Program
import Pi3IndexReduction
set_option pp.universes true
#check @P02.Codec.continuation_byte
#print axioms P02.Codec.continuation_byte
#check @P02.Codec.payload_eq_mod
#print axioms P02.Codec.payload_eq_mod
#check @P02.Codec.accumulator_or
#print axioms P02.Codec.accumulator_or
#check @P02.Codec.uv_nonempty
#print axioms P02.Codec.uv_nonempty
#check @P02.Codec.uv_bytes
#print axioms P02.Codec.uv_bytes
#check @P02.Codec.readAccum_uv
#print axioms P02.Codec.readAccum_uv
#check @P02.Codec.uvRead_append
#print axioms P02.Codec.uvRead_append
#check @P02.Codec.uvRead_uv
#print axioms P02.Codec.uvRead_uv
#check @P02.Codec.uv_injective
#print axioms P02.Codec.uv_injective
#check @P02.Codec.readAccum_split
#print axioms P02.Codec.readAccum_split
#check @P02.Codec.uvRead_eq_some_iff
#print axioms P02.Codec.uvRead_eq_some_iff
#check @P02.Codec.uv_zero
#print axioms P02.Codec.uv_zero
#check @P02.Codec.uv_one
#print axioms P02.Codec.uv_one
#check @P02.Codec.uv_127
#print axioms P02.Codec.uv_127
#check @P02.Codec.uv_128
#print axioms P02.Codec.uv_128
#check @P02.Codec.uv_16384
#print axioms P02.Codec.uv_16384
#check @P02.Codec.uv_624485
#print axioms P02.Codec.uv_624485
#check @P02.Codec.uvRead_reject_overlong_zero
#print axioms P02.Codec.uvRead_reject_overlong_zero
#check @P02.Codec.uvRead_reject_overlong_one
#print axioms P02.Codec.uvRead_reject_overlong_one
#check @P02.Codec.uvRead_reject_truncated
#print axioms P02.Codec.uvRead_reject_truncated
#check @P02.Codec.uvRead_reject_nonbyte
#print axioms P02.Codec.uvRead_reject_nonbyte
#check @P02.Codec.fromBytes_nil
#print axioms P02.Codec.fromBytes_nil
#check @P02.Codec.fromBytes_append_byte
#print axioms P02.Codec.fromBytes_append_byte
#check @P02.Codec.encodeNumeric_nil
#print axioms P02.Codec.encodeNumeric_nil
#check @P02.Codec.encodeNumeric_append_byte
#print axioms P02.Codec.encodeNumeric_append_byte
#check @P02.Codec.encodeNumeric_pos
#print axioms P02.Codec.encodeNumeric_pos
#check @P02.Codec.toBytes_zero
#print axioms P02.Codec.toBytes_zero
#check @P02.Codec.toBytes_one
#print axioms P02.Codec.toBytes_one
#check @P02.Codec.toBytes_step
#print axioms P02.Codec.toBytes_step
#check @P02.Codec.toBytes_encodeNumeric
#print axioms P02.Codec.toBytes_encodeNumeric
#check @P02.Codec.decodeNumeric_encodeNumeric
#print axioms P02.Codec.decodeNumeric_encodeNumeric
#check @P02.Codec.encodeNumeric_injective
#print axioms P02.Codec.encodeNumeric_injective
#check @P02.Codec.toBytes_bytes
#print axioms P02.Codec.toBytes_bytes
#check @P02.Codec.fromBytes_toBytes
#print axioms P02.Codec.fromBytes_toBytes
#check @P02.Codec.decodeNumeric_sound
#print axioms P02.Codec.decodeNumeric_sound
#check @P02.Codec.decodeNumeric_eq_some_iff
#print axioms P02.Codec.decodeNumeric_eq_some_iff
#check @P02.Codec.numeric_uv_roundtrip
#print axioms P02.Codec.numeric_uv_roundtrip
#check @P02.Codec.readExpr_append
#print axioms P02.Codec.readExpr_append
#check @P02.Codec.bytes_cons
#print axioms P02.Codec.bytes_cons
#check @P02.Codec.bytes_append
#print axioms P02.Codec.bytes_append
#check @P02.Codec.exprBytes_bytes
#print axioms P02.Codec.exprBytes_bytes
#check @P02.Codec.exprDepth_le_length
#print axioms P02.Codec.exprDepth_le_length
#check @P02.Codec.readStmt_append
#print axioms P02.Codec.readStmt_append
#check @P02.Codec.stmtBytes_bytes
#print axioms P02.Codec.stmtBytes_bytes
#check @P02.Codec.stmtDepth_le_length
#print axioms P02.Codec.stmtDepth_le_length
#check @P02.Codec.sequenceList_execution
#print axioms P02.Codec.sequenceList_execution
#check @P02.Codec.stripMagic_append
#print axioms P02.Codec.stripMagic_append
#check @P02.Codec.encodeBytes_bytes
#print axioms P02.Codec.encodeBytes_bytes
#check @P02.Codec.readStmt_self
#print axioms P02.Codec.readStmt_self
#check @P02.Codec.decodeBytes_encodeBytes
#print axioms P02.Codec.decodeBytes_encodeBytes
#check @P02.Codec.decodeIndex_programIndex
#print axioms P02.Codec.decodeIndex_programIndex
#check @P02.Codec.binaryStore_extend
#print axioms P02.Codec.binaryStore_extend
#check @P02.Codec.evaluateIndex_programIndex
#print axioms P02.Codec.evaluateIndex_programIndex
#check @P02.Codec.parameterIndex_correct
#print axioms P02.Codec.parameterIndex_correct
#check @P02.Codec.derivation_parameterIndex_correct
#print axioms P02.Codec.derivation_parameterIndex_correct
#check @P02.Codec.exists_parameterIndex_of_primrec
#print axioms P02.Codec.exists_parameterIndex_of_primrec
#check @P02.Codec.uvTableStep_primrec
#print axioms P02.Codec.uvTableStep_primrec
#check @P02.Codec.uvTableStep_table
#print axioms P02.Codec.uvTableStep_table
#check @P02.Codec.uv_primrec
#print axioms P02.Codec.uv_primrec
#check @P02.Codec.fromBytes_primrec
#print axioms P02.Codec.fromBytes_primrec
#check @P02.Codec.encodeNumeric_primrec
#print axioms P02.Codec.encodeNumeric_primrec
#check @P02.Codec.numeric_uv_primrec
#print axioms P02.Codec.numeric_uv_primrec
#check @P02.Codec.encodeNumeric_comp_primrec
#print axioms P02.Codec.encodeNumeric_comp_primrec
#check @P02.Codec.stmtBytes_seq_primrec
#print axioms P02.Codec.stmtBytes_seq_primrec
#check @P02.Codec.stmtBytes_constant_primrec
#print axioms P02.Codec.stmtBytes_constant_primrec
#check @P02.Codec.parameterAssignments
#print axioms P02.Codec.parameterAssignments
#check @P02.Codec.specialize_body_bytes_primrec
#print axioms P02.Codec.specialize_body_bytes_primrec
#check @P02.Codec.specialize_bytes_primrec
#print axioms P02.Codec.specialize_bytes_primrec
#check @P02.Codec.parameterIndex_primrec
#print axioms P02.Codec.parameterIndex_primrec
#check @P02.Codec.literal128_bytes
#print axioms P02.Codec.literal128_bytes
#check @P02.Codec.literal128_roundtrip
#print axioms P02.Codec.literal128_roundtrip
#check @P02.Codec.rejects_wrong_magic_version
#print axioms P02.Codec.rejects_wrong_magic_version
#check @P02.Codec.rejects_trailing_byte
#print axioms P02.Codec.rejects_trailing_byte
#check @P02.Codec.compiled_addition_index
#print axioms P02.Codec.compiled_addition_index
#check @P02.Codec.rejects_specialized_arity_one
#print axioms P02.Codec.rejects_specialized_arity_one
#check @P02A2.Pi3Program.family_primrec
#print axioms P02A2.Pi3Program.family_primrec
#check @P02A2.Pi3Program.exists_fixed_program
#print axioms P02A2.Pi3Program.exists_fixed_program
#check @P02A2.Pi3Program.numeric_observer_eq
#print axioms P02A2.Pi3Program.numeric_observer_eq
#check @P02A2.Pi3Program.numeric_zero_defect_iff
#print axioms P02A2.Pi3Program.numeric_zero_defect_iff
#check @P02A2.Pi3Program.exists_numeric_family
#print axioms P02A2.Pi3Program.exists_numeric_family
#check @P02A2.Pi3IndexReduction.exists_primrec_zero_defect_reduction
#print axioms P02A2.Pi3IndexReduction.exists_primrec_zero_defect_reduction
#check @P02A2.Pi3IndexReduction.exists_primrec_positive_defect_reduction
#print axioms P02A2.Pi3IndexReduction.exists_primrec_positive_defect_reduction

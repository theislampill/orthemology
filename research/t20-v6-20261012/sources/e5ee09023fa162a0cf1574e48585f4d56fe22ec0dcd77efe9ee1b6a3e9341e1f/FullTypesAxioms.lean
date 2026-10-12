import UniformComputabilityAudit
import EndpointChecks
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
#check @P02.Codec.UniformComputability.bytesTableStep
#print axioms P02.Codec.UniformComputability.bytesTableStep
#check @P02.Codec.UniformComputability.bytesTableStep_primrec
#print axioms P02.Codec.UniformComputability.bytesTableStep_primrec
#check @P02.Codec.UniformComputability.bytesTableStep_table
#print axioms P02.Codec.UniformComputability.bytesTableStep_table
#check @P02.Codec.UniformComputability.toBytes_primrec
#print axioms P02.Codec.UniformComputability.toBytes_primrec
#check @P02.Codec.UniformComputability.decodeNumeric_primrec
#print axioms P02.Codec.UniformComputability.decodeNumeric_primrec
#check @P02.Codec.UniformComputability.decodeNumeric_computable
#print axioms P02.Codec.UniformComputability.decodeNumeric_computable
#check @P02.Codec.UniformComputability.RegFile
#print axioms P02.Codec.UniformComputability.RegFile
#check @P02.Codec.UniformComputability.readRegs
#print axioms P02.Codec.UniformComputability.readRegs
#check @P02.Codec.UniformComputability.writeRegs
#print axioms P02.Codec.UniformComputability.writeRegs
#check @P02.Codec.UniformComputability.readRegs_write
#print axioms P02.Codec.UniformComputability.readRegs_write
#check @P02.Codec.UniformComputability.evalRegs
#print axioms P02.Codec.UniformComputability.evalRegs
#check @P02.Codec.UniformComputability.evalRegs_correct
#print axioms P02.Codec.UniformComputability.evalRegs_correct
#check @P02.Codec.UniformComputability.repeatFrom
#print axioms P02.Codec.UniformComputability.repeatFrom
#check @P02.Codec.UniformComputability.repeatFrom_succ_last
#print axioms P02.Codec.UniformComputability.repeatFrom_succ_last
#check @P02.Codec.UniformComputability.repeatFrom_runLoop
#print axioms P02.Codec.UniformComputability.repeatFrom_runLoop
#check @P02.Codec.UniformComputability.execRegs
#print axioms P02.Codec.UniformComputability.execRegs
#check @P02.Codec.UniformComputability.repeatFrom_read
#print axioms P02.Codec.UniformComputability.repeatFrom_read
#check @P02.Codec.UniformComputability.execRegs_correct
#print axioms P02.Codec.UniformComputability.execRegs_correct
#check @P02.Codec.UniformComputability.Task
#print axioms P02.Codec.UniformComputability.Task
#check @P02.Codec.UniformComputability.Config
#print axioms P02.Codec.UniformComputability.Config
#check @P02.Codec.UniformComputability.step
#print axioms P02.Codec.UniformComputability.step
#check @P02.Codec.UniformComputability.runFuel
#print axioms P02.Codec.UniformComputability.runFuel
#check @P02.Codec.UniformComputability.runFuel_complete
#print axioms P02.Codec.UniformComputability.runFuel_complete
#check @P02.Codec.UniformComputability.taskDenote
#print axioms P02.Codec.UniformComputability.taskDenote
#check @P02.Codec.UniformComputability.tasksDenote
#print axioms P02.Codec.UniformComputability.tasksDenote
#check @P02.Codec.UniformComputability.configDenote
#print axioms P02.Codec.UniformComputability.configDenote
#check @P02.Codec.UniformComputability.step_preserves
#print axioms P02.Codec.UniformComputability.step_preserves
#check @P02.Codec.UniformComputability.iterate_preserves
#print axioms P02.Codec.UniformComputability.iterate_preserves
#check @P02.Codec.UniformComputability.runFuel_sound
#print axioms P02.Codec.UniformComputability.runFuel_sound
#check @P02.Codec.UniformComputability.binaryRegs
#print axioms P02.Codec.UniformComputability.binaryRegs
#check @P02.Codec.UniformComputability.readRegs_binary
#print axioms P02.Codec.UniformComputability.readRegs_binary
#check @P02.Codec.UniformComputability.evaluateIndexFuel
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel
#check @P02.Codec.UniformComputability.evaluateIndexFuel_sound
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_sound
#check @P02.Codec.UniformComputability.evaluateIndexFuel_complete
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_complete
#check @P02.Codec.UniformComputability.runFuel_mono
#print axioms P02.Codec.UniformComputability.runFuel_mono
#check @P02.Codec.UniformComputability.evaluateIndexFuel_mono
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_mono
#check @P02.Codec.UniformComputability.evaluateIndexFuel_eventually
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_eventually
#check @P02.Codec.UniformComputability.evaluateIndexSearch
#print axioms P02.Codec.UniformComputability.evaluateIndexSearch
#check @P02.Codec.UniformComputability.evaluateIndexSearch_exact
#print axioms P02.Codec.UniformComputability.evaluateIndexSearch_exact
#check @P02.Codec.UniformComputability.evaluateIndex_computable_of_fuel
#print axioms P02.Codec.UniformComputability.evaluateIndex_computable_of_fuel
#check @P02.Codec.UniformComputability.evaluateIndexFuel_invalid
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_invalid
#check @P02.Codec.UniformComputability.evaluateIndexFuel_wrong_arity
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_wrong_arity
#check @P02.Codec.UniformComputability.evaluateIndexFuel_programIndex
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_programIndex
#check @P02.Codec.UniformComputability.exhausted_one
#print axioms P02.Codec.UniformComputability.exhausted_one
#check @P02.Codec.UniformComputability.exprEncode
#print axioms P02.Codec.UniformComputability.exprEncode
#check @P02.Codec.UniformComputability.exprOfNat
#print axioms P02.Codec.UniformComputability.exprOfNat
#check @P02.Codec.UniformComputability.exprOfNat_exprEncode
#print axioms P02.Codec.UniformComputability.exprOfNat_exprEncode
#check @P02.Codec.UniformComputability.exprEncode_exprOfNat
#print axioms P02.Codec.UniformComputability.exprEncode_exprOfNat
#check @P02.Codec.UniformComputability.exprDenumerable
#print axioms P02.Codec.UniformComputability.exprDenumerable
#check @P02.Codec.UniformComputability.expr_encode_eq
#print axioms P02.Codec.UniformComputability.expr_encode_eq
#check @P02.Codec.UniformComputability.expr_ofNat_eq
#print axioms P02.Codec.UniformComputability.expr_ofNat_eq
#check @P02.Codec.UniformComputability.readRegs_primrec
#print axioms P02.Codec.UniformComputability.readRegs_primrec
#check @P02.Codec.UniformComputability.exprTableValue
#print axioms P02.Codec.UniformComputability.exprTableValue
#check @P02.Codec.UniformComputability.exprTableValue_primrec
#print axioms P02.Codec.UniformComputability.exprTableValue_primrec
#check @P02.Codec.UniformComputability.exprTableValue_table
#print axioms P02.Codec.UniformComputability.exprTableValue_table
#check @P02.Codec.UniformComputability.evalRegs_primrec
#print axioms P02.Codec.UniformComputability.evalRegs_primrec
#check @P02.Codec.UniformComputability.stmtEncode
#print axioms P02.Codec.UniformComputability.stmtEncode
#check @P02.Codec.UniformComputability.stmtOfNat
#print axioms P02.Codec.UniformComputability.stmtOfNat
#check @P02.Codec.UniformComputability.stmtOfNat_stmtEncode
#print axioms P02.Codec.UniformComputability.stmtOfNat_stmtEncode
#check @P02.Codec.UniformComputability.stmtEncode_stmtOfNat
#print axioms P02.Codec.UniformComputability.stmtEncode_stmtOfNat
#check @P02.Codec.UniformComputability.stmtDenumerable
#print axioms P02.Codec.UniformComputability.stmtDenumerable
#check @P02.Codec.UniformComputability.stmt_encode_eq
#print axioms P02.Codec.UniformComputability.stmt_encode_eq
#check @P02.Codec.UniformComputability.stmt_ofNat_eq
#print axioms P02.Codec.UniformComputability.stmt_ofNat_eq
#check @P02.Codec.UniformComputability.taskEncode
#print axioms P02.Codec.UniformComputability.taskEncode
#check @P02.Codec.UniformComputability.taskOfNat
#print axioms P02.Codec.UniformComputability.taskOfNat
#check @P02.Codec.UniformComputability.taskOfNat_taskEncode
#print axioms P02.Codec.UniformComputability.taskOfNat_taskEncode
#check @P02.Codec.UniformComputability.taskEncode_taskOfNat
#print axioms P02.Codec.UniformComputability.taskEncode_taskOfNat
#check @P02.Codec.UniformComputability.taskDenumerable
#print axioms P02.Codec.UniformComputability.taskDenumerable
#check @P02.Codec.UniformComputability.task_encode_eq
#print axioms P02.Codec.UniformComputability.task_encode_eq
#check @P02.Codec.UniformComputability.task_ofNat_eq
#print axioms P02.Codec.UniformComputability.task_ofNat_eq
#check @P02.Codec.UniformComputability.stmtOfNat_primrec
#print axioms P02.Codec.UniformComputability.stmtOfNat_primrec
#check @P02.Codec.UniformComputability.taskOfNat_primrec
#print axioms P02.Codec.UniformComputability.taskOfNat_primrec
#check @P02.Codec.UniformComputability.stmtSet_primrec
#print axioms P02.Codec.UniformComputability.stmtSet_primrec
#check @P02.Codec.UniformComputability.stmtSeq_primrec
#print axioms P02.Codec.UniformComputability.stmtSeq_primrec
#check @P02.Codec.UniformComputability.stmtLoop_primrec
#print axioms P02.Codec.UniformComputability.stmtLoop_primrec
#check @P02.Codec.UniformComputability.stmtBranch_primrec
#print axioms P02.Codec.UniformComputability.stmtBranch_primrec
#check @P02.Codec.UniformComputability.taskStmt_primrec
#print axioms P02.Codec.UniformComputability.taskStmt_primrec
#check @P02.Codec.UniformComputability.taskRepeat_primrec
#print axioms P02.Codec.UniformComputability.taskRepeat_primrec
#check @P02.Codec.UniformComputability.stepByCode
#print axioms P02.Codec.UniformComputability.stepByCode
#check @P02.Codec.UniformComputability.stepByCode_eq_step
#print axioms P02.Codec.UniformComputability.stepByCode_eq_step
#check @P02.Codec.UniformComputability.writeRegs_primrec
#print axioms P02.Codec.UniformComputability.writeRegs_primrec
#check @P02.Codec.UniformComputability.stepByCode_primrec
#print axioms P02.Codec.UniformComputability.stepByCode_primrec
#check @P02.Codec.UniformComputability.step_primrec
#print axioms P02.Codec.UniformComputability.step_primrec
#check @P02.Codec.UniformComputability.step_computable
#print axioms P02.Codec.UniformComputability.step_computable
#check @P02.Codec.UniformComputability.runFuel_primrec
#print axioms P02.Codec.UniformComputability.runFuel_primrec
#check @P02.Codec.UniformComputability.runFuel_computable
#print axioms P02.Codec.UniformComputability.runFuel_computable
#check @P02.Codec.UniformComputability.binaryRegs_primrec
#print axioms P02.Codec.UniformComputability.binaryRegs_primrec
#check @P02.Codec.UniformComputability.packedEncode
#print axioms P02.Codec.UniformComputability.packedEncode
#check @P02.Codec.UniformComputability.packedOfNat
#print axioms P02.Codec.UniformComputability.packedOfNat
#check @P02.Codec.UniformComputability.packedOfNat_packedEncode
#print axioms P02.Codec.UniformComputability.packedOfNat_packedEncode
#check @P02.Codec.UniformComputability.packedEncode_packedOfNat
#print axioms P02.Codec.UniformComputability.packedEncode_packedOfNat
#check @P02.Codec.UniformComputability.packedDenumerable
#print axioms P02.Codec.UniformComputability.packedDenumerable
#check @P02.Codec.UniformComputability.packed_encode_eq
#print axioms P02.Codec.UniformComputability.packed_encode_eq
#check @P02.Codec.UniformComputability.packed_ofNat_eq
#print axioms P02.Codec.UniformComputability.packed_ofNat_eq
#check @P02.Codec.UniformComputability.packedMk_primrec
#print axioms P02.Codec.UniformComputability.packedMk_primrec
#check @P02.Codec.UniformComputability.packedArity_primrec
#print axioms P02.Codec.UniformComputability.packedArity_primrec
#check @P02.Codec.UniformComputability.packedOutput_primrec
#print axioms P02.Codec.UniformComputability.packedOutput_primrec
#check @P02.Codec.UniformComputability.packedBody_primrec
#print axioms P02.Codec.UniformComputability.packedBody_primrec
#check @P02.Codec.UniformComputability.sequenceList_primrec
#print axioms P02.Codec.UniformComputability.sequenceList_primrec
#check @P02.Codec.UniformComputability.readManyStep
#print axioms P02.Codec.UniformComputability.readManyStep
#check @P02.Codec.UniformComputability.readManyStep_primrec
#print axioms P02.Codec.UniformComputability.readManyStep_primrec
#check @P02.Codec.UniformComputability.readManyStep_correct
#print axioms P02.Codec.UniformComputability.readManyStep_correct
#check @P02.Codec.UniformComputability.readMany_primrec
#print axioms P02.Codec.UniformComputability.readMany_primrec
#check @P02.Codec.UniformComputability.plainRead
#print axioms P02.Codec.UniformComputability.plainRead
#check @P02.Codec.UniformComputability.plainRead_eq
#print axioms P02.Codec.UniformComputability.plainRead_eq
#check @P02.Codec.UniformComputability.UVWork
#print axioms P02.Codec.UniformComputability.UVWork
#check @P02.Codec.UniformComputability.UVState
#print axioms P02.Codec.UniformComputability.UVState
#check @P02.Codec.UniformComputability.uvAdvance
#print axioms P02.Codec.UniformComputability.uvAdvance
#check @P02.Codec.UniformComputability.uvAdvance_terminal
#print axioms P02.Codec.UniformComputability.uvAdvance_terminal
#check @P02.Codec.UniformComputability.uvAdvance_complete
#print axioms P02.Codec.UniformComputability.uvAdvance_complete
#check @P02.Codec.UniformComputability.uvFinish
#print axioms P02.Codec.UniformComputability.uvFinish
#check @P02.Codec.UniformComputability.plainInitialRead
#print axioms P02.Codec.UniformComputability.plainInitialRead
#check @P02.Codec.UniformComputability.plainInitialRead_eq
#print axioms P02.Codec.UniformComputability.plainInitialRead_eq
#check @P02.Codec.UniformComputability.UVConsWork
#print axioms P02.Codec.UniformComputability.UVConsWork
#check @P02.Codec.UniformComputability.uvConsBranch
#print axioms P02.Codec.UniformComputability.uvConsBranch
#check @P02.Codec.UniformComputability.uvConsBranch_primrec
#print axioms P02.Codec.UniformComputability.uvConsBranch_primrec
#check @P02.Codec.UniformComputability.uvAdvance_primrec
#print axioms P02.Codec.UniformComputability.uvAdvance_primrec
#check @P02.Codec.UniformComputability.uvFinish_primrec
#print axioms P02.Codec.UniformComputability.uvFinish_primrec
#check @P02.Codec.UniformComputability.plainInitialRead_primrec
#print axioms P02.Codec.UniformComputability.plainInitialRead_primrec
#check @P02.Codec.UniformComputability.initialReadAccum_primrec
#print axioms P02.Codec.UniformComputability.initialReadAccum_primrec
#check @P02.Codec.UniformComputability.uvRead_primrec
#print axioms P02.Codec.UniformComputability.uvRead_primrec
#check @P02.Codec.UniformComputability.expr_constant_primrec
#print axioms P02.Codec.UniformComputability.expr_constant_primrec
#check @P02.Codec.UniformComputability.expr_reg_primrec
#print axioms P02.Codec.UniformComputability.expr_reg_primrec
#check @P02.Codec.UniformComputability.expr_add_primrec
#print axioms P02.Codec.UniformComputability.expr_add_primrec
#check @P02.Codec.UniformComputability.expr_sub_primrec
#print axioms P02.Codec.UniformComputability.expr_sub_primrec
#check @P02.Codec.UniformComputability.expr_mul_primrec
#print axioms P02.Codec.UniformComputability.expr_mul_primrec
#check @P02.Codec.UniformComputability.expr_div_primrec
#print axioms P02.Codec.UniformComputability.expr_div_primrec
#check @P02.Codec.UniformComputability.expr_mod_primrec
#print axioms P02.Codec.UniformComputability.expr_mod_primrec
#check @P02.Codec.UniformComputability.expr_le_primrec
#print axioms P02.Codec.UniformComputability.expr_le_primrec
#check @P02.Codec.UniformComputability.expr_eq_primrec
#print axioms P02.Codec.UniformComputability.expr_eq_primrec
#check @P02.Codec.UniformComputability.expr_pow2_primrec
#print axioms P02.Codec.UniformComputability.expr_pow2_primrec
#check @P02.Codec.UniformComputability.mapParser
#print axioms P02.Codec.UniformComputability.mapParser
#check @P02.Codec.UniformComputability.bindParser
#print axioms P02.Codec.UniformComputability.bindParser
#check @P02.Codec.UniformComputability.mapParser_primrec
#print axioms P02.Codec.UniformComputability.mapParser_primrec
#check @P02.Codec.UniformComputability.bindParser_primrec
#print axioms P02.Codec.UniformComputability.bindParser_primrec
#check @P02.Codec.UniformComputability.readBinary_primrec
#print axioms P02.Codec.UniformComputability.readBinary_primrec
#check @P02.Codec.UniformComputability.list_drop_primrec
#print axioms P02.Codec.UniformComputability.list_drop_primrec
#check @P02.Codec.UniformComputability.list_replicate_primrec
#print axioms P02.Codec.UniformComputability.list_replicate_primrec
#check @P02.Codec.UniformComputability.PreservesSuffix
#print axioms P02.Codec.UniformComputability.PreservesSuffix
#check @P02.Codec.UniformComputability.pure_preservesSuffix
#print axioms P02.Codec.UniformComputability.pure_preservesSuffix
#check @P02.Codec.UniformComputability.bind_preservesSuffix
#print axioms P02.Codec.UniformComputability.bind_preservesSuffix
#check @P02.Codec.UniformComputability.map_preservesSuffix
#print axioms P02.Codec.UniformComputability.map_preservesSuffix
#check @P02.Codec.UniformComputability.uvRead_preservesSuffix
#print axioms P02.Codec.UniformComputability.uvRead_preservesSuffix
#check @P02.Codec.UniformComputability.readBinary_preservesSuffix
#print axioms P02.Codec.UniformComputability.readBinary_preservesSuffix
#check @P02.Codec.UniformComputability.readExpr_preservesSuffix
#print axioms P02.Codec.UniformComputability.readExpr_preservesSuffix
#check @P02.Codec.UniformComputability.readMany_preservesSuffix
#print axioms P02.Codec.UniformComputability.readMany_preservesSuffix
#check @P02.Codec.UniformComputability.sequenceList_preservesSuffix
#print axioms P02.Codec.UniformComputability.sequenceList_preservesSuffix
#check @P02.Codec.UniformComputability.readStmt_preservesSuffix
#print axioms P02.Codec.UniformComputability.readStmt_preservesSuffix
#check @P02.Codec.UniformComputability.readExpr_suffix
#print axioms P02.Codec.UniformComputability.readExpr_suffix
#check @P02.Codec.UniformComputability.readStmt_suffix
#print axioms P02.Codec.UniformComputability.readStmt_suffix
#check @P02.Codec.UniformComputability.readExpr_rest_length_le
#print axioms P02.Codec.UniformComputability.readExpr_rest_length_le
#check @P02.Codec.UniformComputability.readStmt_rest_length_le
#print axioms P02.Codec.UniformComputability.readStmt_rest_length_le
#check @P02.Codec.UniformComputability.readExpr_rest_mem_tails
#print axioms P02.Codec.UniformComputability.readExpr_rest_mem_tails
#check @P02.Codec.UniformComputability.readStmt_rest_mem_tails
#print axioms P02.Codec.UniformComputability.readStmt_rest_mem_tails
#check @P02.Codec.UniformComputability.parser_rest_mem_original_tails
#print axioms P02.Codec.UniformComputability.parser_rest_mem_original_tails
#check @P02.Codec.UniformComputability.StmtResult
#print axioms P02.Codec.UniformComputability.StmtResult
#check @P02.Codec.UniformComputability.stmtLayer
#print axioms P02.Codec.UniformComputability.stmtLayer
#check @P02.Codec.UniformComputability.readStmt_succ_layer
#print axioms P02.Codec.UniformComputability.readStmt_succ_layer
#check @P02.Codec.UniformComputability.stmtLookup
#print axioms P02.Codec.UniformComputability.stmtLookup
#check @P02.Codec.UniformComputability.stmtNextTable
#print axioms P02.Codec.UniformComputability.stmtNextTable
#check @P02.Codec.UniformComputability.stmtTable
#print axioms P02.Codec.UniformComputability.stmtTable
#check @P02.Codec.UniformComputability.readMany_stmt_suffix_congr
#print axioms P02.Codec.UniformComputability.readMany_stmt_suffix_congr
#check @P02.Codec.UniformComputability.stmtLayer_suffix_congr
#print axioms P02.Codec.UniformComputability.stmtLayer_suffix_congr
#check @P02.Codec.UniformComputability.stmtLookup_correct
#print axioms P02.Codec.UniformComputability.stmtLookup_correct
#check @P02.Codec.UniformComputability.stmtTable_correct
#print axioms P02.Codec.UniformComputability.stmtTable_correct
#check @P02.Codec.UniformComputability.stmtLayer_primrec
#print axioms P02.Codec.UniformComputability.stmtLayer_primrec
#check @P02.Codec.UniformComputability.ExprResult
#print axioms P02.Codec.UniformComputability.ExprResult
#check @P02.Codec.UniformComputability.exprLayer
#print axioms P02.Codec.UniformComputability.exprLayer
#check @P02.Codec.UniformComputability.readExpr_succ_layer
#print axioms P02.Codec.UniformComputability.readExpr_succ_layer
#check @P02.Codec.UniformComputability.exprLookup
#print axioms P02.Codec.UniformComputability.exprLookup
#check @P02.Codec.UniformComputability.exprNextTable
#print axioms P02.Codec.UniformComputability.exprNextTable
#check @P02.Codec.UniformComputability.exprTable
#print axioms P02.Codec.UniformComputability.exprTable
#check @P02.Codec.UniformComputability.readBinary_suffix_congr
#print axioms P02.Codec.UniformComputability.readBinary_suffix_congr
#check @P02.Codec.UniformComputability.exprLayer_suffix_congr
#print axioms P02.Codec.UniformComputability.exprLayer_suffix_congr
#check @P02.Codec.UniformComputability.exprLookup_correct
#print axioms P02.Codec.UniformComputability.exprLookup_correct
#check @P02.Codec.UniformComputability.exprTable_correct
#print axioms P02.Codec.UniformComputability.exprTable_correct
#check @P02.Codec.UniformComputability.exprLayer_primrec
#print axioms P02.Codec.UniformComputability.exprLayer_primrec
#check @P02.Codec.UniformComputability.exprLookup_primrec
#print axioms P02.Codec.UniformComputability.exprLookup_primrec
#check @P02.Codec.UniformComputability.exprNextTable_primrec
#print axioms P02.Codec.UniformComputability.exprNextTable_primrec
#check @P02.Codec.UniformComputability.exprTable_primrec
#print axioms P02.Codec.UniformComputability.exprTable_primrec
#check @P02.Codec.UniformComputability.readExpr_primrec
#print axioms P02.Codec.UniformComputability.readExpr_primrec
#check @P02.Codec.UniformComputability.stmtLookup_primrec
#print axioms P02.Codec.UniformComputability.stmtLookup_primrec
#check @P02.Codec.UniformComputability.stmtNextTable_primrec
#print axioms P02.Codec.UniformComputability.stmtNextTable_primrec
#check @P02.Codec.UniformComputability.stmtTable_primrec
#print axioms P02.Codec.UniformComputability.stmtTable_primrec
#check @P02.Codec.UniformComputability.readStmt_primrec
#print axioms P02.Codec.UniformComputability.readStmt_primrec
#check @P02.Codec.UniformComputability.evaluatePackedFuel
#print axioms P02.Codec.UniformComputability.evaluatePackedFuel
#check @P02.Codec.UniformComputability.evaluatePackedFuel_primrec
#print axioms P02.Codec.UniformComputability.evaluatePackedFuel_primrec
#check @P02.Codec.UniformComputability.evaluateIndexFuel_primrec_of_decode
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_primrec_of_decode
#check @P02.Codec.UniformComputability.evaluateIndexFuel_computable_of_decode
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_computable_of_decode
#check @P02.Codec.UniformComputability.list_take_fixed_primrec
#print axioms P02.Codec.UniformComputability.list_take_fixed_primrec
#check @P02.Codec.UniformComputability.stripMagic_primrec
#print axioms P02.Codec.UniformComputability.stripMagic_primrec
#check @P02.Codec.UniformComputability.decodeBody
#print axioms P02.Codec.UniformComputability.decodeBody
#check @P02.Codec.UniformComputability.decodeBody_primrec
#print axioms P02.Codec.UniformComputability.decodeBody_primrec
#check @P02.Codec.UniformComputability.decodeOutput
#print axioms P02.Codec.UniformComputability.decodeOutput
#check @P02.Codec.UniformComputability.decodeOutput_primrec
#print axioms P02.Codec.UniformComputability.decodeOutput_primrec
#check @P02.Codec.UniformComputability.decodeFields
#print axioms P02.Codec.UniformComputability.decodeFields
#check @P02.Codec.UniformComputability.decodeFields_primrec
#print axioms P02.Codec.UniformComputability.decodeFields_primrec
#check @P02.Codec.UniformComputability.decodeBytes_primrec
#print axioms P02.Codec.UniformComputability.decodeBytes_primrec
#check @P02.Codec.UniformComputability.decodeIndex_primrec
#print axioms P02.Codec.UniformComputability.decodeIndex_primrec
#check @P02.Codec.UniformComputability.decodeIndex_computable
#print axioms P02.Codec.UniformComputability.decodeIndex_computable
#check @P02.Codec.UniformComputability.evaluateIndexFuel_primrec
#print axioms P02.Codec.UniformComputability.evaluateIndexFuel_primrec
#check @P02.Codec.UniformComputability.evaluateIndex_computable
#print axioms P02.Codec.UniformComputability.evaluateIndex_computable
#check @P02.Codec.UniformComputability.evaluateIndex_nat_computable
#print axioms P02.Codec.UniformComputability.evaluateIndex_nat_computable
#check @P02.Codec.UniformComputability.capturedBoundProgram
#print axioms P02.Codec.UniformComputability.capturedBoundProgram
#check @P02.Codec.UniformComputability.overwrittenIndexProgram
#print axioms P02.Codec.UniformComputability.overwrittenIndexProgram
#check @P02.Codec.UniformComputability.arithmeticProgram
#print axioms P02.Codec.UniformComputability.arithmeticProgram
#check @P02.Codec.UniformComputability.branchProgram
#print axioms P02.Codec.UniformComputability.branchProgram
#check @P02.Codec.UniformComputability.captured_count_control
#print axioms P02.Codec.UniformComputability.captured_count_control
#check @P02.Codec.UniformComputability.overwritten_index_control
#print axioms P02.Codec.UniformComputability.overwritten_index_control
#check @P02.Codec.UniformComputability.arithmetic_control
#print axioms P02.Codec.UniformComputability.arithmetic_control
#check @P02.Codec.UniformComputability.branch_zero_control
#print axioms P02.Codec.UniformComputability.branch_zero_control
#check @P02.Codec.UniformComputability.branch_nonzero_control
#print axioms P02.Codec.UniformComputability.branch_nonzero_control
#check @P02.Codec.UniformComputability.zero_loop_control
#print axioms P02.Codec.UniformComputability.zero_loop_control
#check @P02.Codec.UniformComputability.invalid_zero_control
#print axioms P02.Codec.UniformComputability.invalid_zero_control
#check @P02.Codec.UniformComputability.wrong_arity_control
#print axioms P02.Codec.UniformComputability.wrong_arity_control
#check @P02.Codec.UniformComputability.executionVectors
#print axioms P02.Codec.UniformComputability.executionVectors
#check @UniformIndependentAudit.uv_small
#print axioms UniformIndependentAudit.uv_small
#check @UniformIndependentAudit.uv_255
#print axioms UniformIndependentAudit.uv_255
#check @UniformIndependentAudit.numeric_decode
#print axioms UniformIndependentAudit.numeric_decode
#check @UniformIndependentAudit.reject_truncated_varint
#print axioms UniformIndependentAudit.reject_truncated_varint
#check @UniformIndependentAudit.reject_overlong_zero
#print axioms UniformIndependentAudit.reject_overlong_zero
#check @UniformIndependentAudit.reject_overlong_one
#print axioms UniformIndependentAudit.reject_overlong_one
#check @UniformIndependentAudit.reject_nonbyte
#print axioms UniformIndependentAudit.reject_nonbyte
#check @UniformIndependentAudit.varint_exact_suffix
#print axioms UniformIndependentAudit.varint_exact_suffix
#check @UniformIndependentAudit.expr_zero_fuel
#print axioms UniformIndependentAudit.expr_zero_fuel
#check @UniformIndependentAudit.expr_unknown_tag
#print axioms UniformIndependentAudit.expr_unknown_tag
#check @UniformIndependentAudit.expr_malformed_literal
#print axioms UniformIndependentAudit.expr_malformed_literal
#check @UniformIndependentAudit.expr_nonbyte_literal
#print axioms UniformIndependentAudit.expr_nonbyte_literal
#check @UniformIndependentAudit.expr_exact_suffix
#print axioms UniformIndependentAudit.expr_exact_suffix
#check @UniformIndependentAudit.expr_shared_child_fuel
#print axioms UniformIndependentAudit.expr_shared_child_fuel
#check @UniformIndependentAudit.expr_insufficient_depth
#print axioms UniformIndependentAudit.expr_insufficient_depth
#check @UniformIndependentAudit.stmt_zero_fuel
#print axioms UniformIndependentAudit.stmt_zero_fuel
#check @UniformIndependentAudit.stmt_unknown_tag
#print axioms UniformIndependentAudit.stmt_unknown_tag
#check @UniformIndependentAudit.stmt_empty_variadic
#print axioms UniformIndependentAudit.stmt_empty_variadic
#check @UniformIndependentAudit.stmt_singleton_variadic
#print axioms UniformIndependentAudit.stmt_singleton_variadic
#check @UniformIndependentAudit.stmt_three_variadic
#print axioms UniformIndependentAudit.stmt_three_variadic
#check @UniformIndependentAudit.stmt_count_exceeds_payload
#print axioms UniformIndependentAudit.stmt_count_exceeds_payload
#check @UniformIndependentAudit.stmt_malformed_count
#print axioms UniformIndependentAudit.stmt_malformed_count
#check @UniformIndependentAudit.stmt_insufficient_depth
#print axioms UniformIndependentAudit.stmt_insufficient_depth
#check @UniformIndependentAudit.readMany_zero_preserves_arbitrary
#print axioms UniformIndependentAudit.readMany_zero_preserves_arbitrary
#check @UniformIndependentAudit.decode_noncanonical_syntax
#print axioms UniformIndependentAudit.decode_noncanonical_syntax
#check @UniformIndependentAudit.decode_trailing_rejected
#print axioms UniformIndependentAudit.decode_trailing_rejected
#check @UniformIndependentAudit.decode_wrong_magic
#print axioms UniformIndependentAudit.decode_wrong_magic
#check @UniformIndependentAudit.decode_overlong_arity
#print axioms UniformIndependentAudit.decode_overlong_arity
#check @UniformIndependentAudit.numeric_missing_sentinel
#print axioms UniformIndependentAudit.numeric_missing_sentinel
#check @UniformIndependentAudit.numeric_nongenerated_syntax
#print axioms UniformIndependentAudit.numeric_nongenerated_syntax
#check @UniformIndependentAudit.actual_numeric_nongenerated_value
#print axioms UniformIndependentAudit.actual_numeric_nongenerated_value
#check @UniformIndependentAudit.actual_numeric_trailing_zero
#print axioms UniformIndependentAudit.actual_numeric_trailing_zero
#check @UniformIndependentAudit.wrong_arity_at_zero_fuel
#print axioms UniformIndependentAudit.wrong_arity_at_zero_fuel
#check @UniformIndependentAudit.unknown_expr_tag_all_fuels
#print axioms UniformIndependentAudit.unknown_expr_tag_all_fuels
#check @UniformIndependentAudit.unknown_stmt_tag_all_fuels
#print axioms UniformIndependentAudit.unknown_stmt_tag_all_fuels
#check @UniformIndependentAudit.expression_parser_all_inputs
#print axioms UniformIndependentAudit.expression_parser_all_inputs
#check @UniformIndependentAudit.statement_parser_all_inputs
#print axioms UniformIndependentAudit.statement_parser_all_inputs
#check @UniformIndependentAudit.actual_numeric_decoder
#print axioms UniformIndependentAudit.actual_numeric_decoder
#check @UniformIndependentAudit.actual_bounded_numeric_machine
#print axioms UniformIndependentAudit.actual_bounded_numeric_machine
#check @UniformIndependentAudit.exact_existing_premise
#print axioms UniformIndependentAudit.exact_existing_premise
#check @UniformIndependentAudit.exact_external_endpoint
#print axioms UniformIndependentAudit.exact_external_endpoint
#check @UniformIndependentAudit.external_input_projection
#print axioms UniformIndependentAudit.external_input_projection
#check @UniformIndependentAudit.expression_suffix_table_exact
#print axioms UniformIndependentAudit.expression_suffix_table_exact
#check @UniformIndependentAudit.statement_suffix_table_exact
#print axioms UniformIndependentAudit.statement_suffix_table_exact
#check @UniformIndependentAudit.expression_lookup_requires_suffix
#print axioms UniformIndependentAudit.expression_lookup_requires_suffix
#check @UniformIndependentAudit.byte_index_is_not_internal_syntax_code
#print axioms UniformIndependentAudit.byte_index_is_not_internal_syntax_code

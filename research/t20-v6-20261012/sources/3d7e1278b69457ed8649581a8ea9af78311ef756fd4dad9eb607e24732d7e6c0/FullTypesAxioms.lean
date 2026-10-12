import ComputableMatrixAudit
import MatrixVectors
set_option pp.universes true
set_option pp.explicit true
set_option pp.fullNames true
#check @P02A2.FiniteOutputTable.extendWord
#print axioms P02A2.FiniteOutputTable.extendWord
#check @P02A2.FiniteOutputTable.finiteOutput
#print axioms P02A2.FiniteOutputTable.finiteOutput
#check @P02A2.FiniteOutputTable.finiteOutput_actual
#print axioms P02A2.FiniteOutputTable.finiteOutput_actual
#check @P02A2.FiniteOutputTable.output_measurable
#print axioms P02A2.FiniteOutputTable.output_measurable
#check @P02A2.FiniteOutputTable.fair_cylinder
#print axioms P02A2.FiniteOutputTable.fair_cylinder
#check @P02A2.FiniteOutputTable.preimageWords
#print axioms P02A2.FiniteOutputTable.preimageWords
#check @P02A2.FiniteOutputTable.output_cylinder_preimage
#print axioms P02A2.FiniteOutputTable.output_cylinder_preimage
#check @P02A2.FiniteOutputTable.outputLaw
#print axioms P02A2.FiniteOutputTable.outputLaw
#check @P02A2.FiniteOutputTable.outputLaw_probability
#print axioms P02A2.FiniteOutputTable.outputLaw_probability
#check @P02A2.FiniteOutputTable.cylinder_probability_count
#print axioms P02A2.FiniteOutputTable.cylinder_probability_count
#check @P02A2.FiniteOutputTable.tableProbability
#print axioms P02A2.FiniteOutputTable.tableProbability
#check @P02A2.FiniteOutputTable.tableProbability_exact
#print axioms P02A2.FiniteOutputTable.tableProbability_exact
#check @P02A2.FiniteOutputTable.indexTable
#print axioms P02A2.FiniteOutputTable.indexTable
#check @P02A2.FiniteOutputTable.indexTable_exact
#print axioms P02A2.FiniteOutputTable.indexTable_exact
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
#check @P02.Codec.UniformComputability.allWords
#print axioms P02.Codec.UniformComputability.allWords
#check @P02.Codec.UniformComputability.outputList
#print axioms P02.Codec.UniformComputability.outputList
#check @P02.Codec.UniformComputability.wordCount
#print axioms P02.Codec.UniformComputability.wordCount
#check @P02.Codec.UniformComputability.heavyCount
#print axioms P02.Codec.UniformComputability.heavyCount
#check @P02.Codec.UniformComputability.mem_allWords
#print axioms P02.Codec.UniformComputability.mem_allWords
#check @P02.Codec.UniformComputability.allWords_nodup
#print axioms P02.Codec.UniformComputability.allWords_nodup
#check @P02.Codec.UniformComputability.allWords_toFinset
#print axioms P02.Codec.UniformComputability.allWords_toFinset
#check @P02.Codec.UniformComputability.sum_allWords
#print axioms P02.Codec.UniformComputability.sum_allWords
#check @P02.Codec.UniformComputability.ofFn_take_extend
#print axioms P02.Codec.UniformComputability.ofFn_take_extend
#check @P02.Codec.UniformComputability.outputList_ofFn
#print axioms P02.Codec.UniformComputability.outputList_ofFn
#check @P02.Codec.UniformComputability.wordCount_exact
#print axioms P02.Codec.UniformComputability.wordCount_exact
#check @AtomicMembership.finiteMassTest
#print axioms AtomicMembership.finiteMassTest
#check @AtomicMembership.numeric_zero_defect_normal
#print axioms AtomicMembership.numeric_zero_defect_normal
#check @AtomicMembership.numeric_not_zero_defect_normal
#print axioms AtomicMembership.numeric_not_zero_defect_normal
#check @AtomicMembership.rationalOfCode
#print axioms AtomicMembership.rationalOfCode
#check @AtomicMembership.rationalOfCode_surjective
#print axioms AtomicMembership.rationalOfCode_surjective
#check @AtomicMembership.membershipMatrix
#print axioms AtomicMembership.membershipMatrix
#check @AtomicMembership.numeric_zero_defect_nat_normal
#print axioms AtomicMembership.numeric_zero_defect_nat_normal
#check @AtomicMembership.numeric_not_zero_defect_nat_normal
#print axioms AtomicMembership.numeric_not_zero_defect_nat_normal
#check @AtomicMembership.divNat_eq_div
#print axioms AtomicMembership.divNat_eq_div
#check @AtomicMembership.rational_imp_cross
#print axioms AtomicMembership.rational_imp_cross
#check @AtomicMembership.rational_imp_dyadic_cross
#print axioms AtomicMembership.rational_imp_dyadic_cross
#check @AtomicMembership.zero_denominator_control
#print axioms AtomicMembership.zero_denominator_control
#check @AtomicMembership.upper_rational_vacuity
#print axioms AtomicMembership.upper_rational_vacuity
#check @AtomicMembership.inclusive_rational_tie
#print axioms AtomicMembership.inclusive_rational_tie
#check @P02.Codec.UniformComputability.dyadic_threshold_count_iff
#print axioms P02.Codec.UniformComputability.dyadic_threshold_count_iff
#check @P02.Codec.UniformComputability.finiteHeavyCount
#print axioms P02.Codec.UniformComputability.finiteHeavyCount
#check @P02.Codec.UniformComputability.rationalHeavyMass_finiteCount
#print axioms P02.Codec.UniformComputability.rationalHeavyMass_finiteCount
#check @P02.Codec.UniformComputability.heavyCount_eq_finite
#print axioms P02.Codec.UniformComputability.heavyCount_eq_finite
#check @P02.Codec.UniformComputability.rationalHeavyMass_heavyCount
#print axioms P02.Codec.UniformComputability.rationalHeavyMass_heavyCount
#check @P02.Codec.UniformComputability.membershipMatrix_integer_iff
#print axioms P02.Codec.UniformComputability.membershipMatrix_integer_iff
#check @P02.Codec.UniformComputability.computable_range_map
#print axioms P02.Codec.UniformComputability.computable_range_map
#check @P02.Codec.UniformComputability.computable_list_map
#print axioms P02.Codec.UniformComputability.computable_list_map
#check @P02.Codec.UniformComputability.allWords_primrec
#print axioms P02.Codec.UniformComputability.allWords_primrec
#check @P02.Codec.UniformComputability.sentinel_primrec
#print axioms P02.Codec.UniformComputability.sentinel_primrec
#check @P02.Codec.UniformComputability.list_take_primrec
#print axioms P02.Codec.UniformComputability.list_take_primrec
#check @P02.Codec.UniformComputability.outputList_computable
#print axioms P02.Codec.UniformComputability.outputList_computable
#check @P02.Codec.UniformComputability.wordCount_computable
#print axioms P02.Codec.UniformComputability.wordCount_computable
#check @P02.Codec.UniformComputability.membershipNatSum_primrec
#print axioms P02.Codec.UniformComputability.membershipNatSum_primrec
#check @P02.Codec.UniformComputability.heavyCount_computable
#print axioms P02.Codec.UniformComputability.heavyCount_computable
#check @P02.Codec.UniformComputability.heavyCount_nat_computable
#print axioms P02.Codec.UniformComputability.heavyCount_nat_computable
#check @P02.Codec.UniformComputability.MatrixInput
#print axioms P02.Codec.UniformComputability.MatrixInput
#check @P02.Codec.UniformComputability.integerMatrix
#print axioms P02.Codec.UniformComputability.integerMatrix
#check @P02.Codec.UniformComputability.integerMatrix_computable
#print axioms P02.Codec.UniformComputability.integerMatrix_computable
#check @P02.Codec.UniformComputability.membershipMatrix_computable
#print axioms P02.Codec.UniformComputability.membershipMatrix_computable
#check @P02.Codec.UniformComputability.matrixInputOfNat
#print axioms P02.Codec.UniformComputability.matrixInputOfNat
#check @P02.Codec.UniformComputability.matrixInputOfNat_primrec
#print axioms P02.Codec.UniformComputability.matrixInputOfNat_primrec
#check @P02.Codec.UniformComputability.membershipMatrix_nat_computable
#print axioms P02.Codec.UniformComputability.membershipMatrix_nat_computable
#check @P02.Codec.UniformComputability.membershipMatrix_characteristic_computable
#print axioms P02.Codec.UniformComputability.membershipMatrix_characteristic_computable
#check @P02.Codec.UniformComputability.effective_membership_normal_form
#print axioms P02.Codec.UniformComputability.effective_membership_normal_form
#check @P02.Codec.UniformComputability.echoPacked
#print axioms P02.Codec.UniformComputability.echoPacked
#check @P02.Codec.UniformComputability.echo_value
#print axioms P02.Codec.UniformComputability.echo_value
#check @P02.Codec.UniformComputability.invalid_zero_heavy_count
#print axioms P02.Codec.UniformComputability.invalid_zero_heavy_count
#check @P02.Codec.UniformComputability.echo_below_threshold
#print axioms P02.Codec.UniformComputability.echo_below_threshold
#check @P02.Codec.UniformComputability.echo_inclusive_threshold
#print axioms P02.Codec.UniformComputability.echo_inclusive_threshold
#check @P02.Codec.UniformComputability.membership_zero_denominator
#print axioms P02.Codec.UniformComputability.membership_zero_denominator
#check @P02.Codec.UniformComputability.membership_vacuous_one
#print axioms P02.Codec.UniformComputability.membership_vacuous_one
#check @P02.Codec.UniformComputability.zero_horizon_heavy
#print axioms P02.Codec.UniformComputability.zero_horizon_heavy
#check @MatrixIndependentAudit.allWords_length
#print axioms MatrixIndependentAudit.allWords_length
#check @MatrixIndependentAudit.allWords_zero
#print axioms MatrixIndependentAudit.allWords_zero
#check @MatrixIndependentAudit.allWords_two
#print axioms MatrixIndependentAudit.allWords_two
#check @MatrixIndependentAudit.output_length
#print axioms MatrixIndependentAudit.output_length
#check @MatrixIndependentAudit.count_zero_depth
#print axioms MatrixIndependentAudit.count_zero_depth
#check @MatrixIndependentAudit.heavy_zero_depth
#print axioms MatrixIndependentAudit.heavy_zero_depth
#check @MatrixIndependentAudit.matrix_zero_depth
#print axioms MatrixIndependentAudit.matrix_zero_depth
#check @MatrixIndependentAudit.zero_denominator_all
#print axioms MatrixIndependentAudit.zero_denominator_all
#check @MatrixIndependentAudit.zero_numerator_all
#print axioms MatrixIndependentAudit.zero_numerator_all
#check @MatrixIndependentAudit.rational_at_least_one
#print axioms MatrixIndependentAudit.rational_at_least_one
#check @MatrixIndependentAudit.exact_integer_tie
#print axioms MatrixIndependentAudit.exact_integer_tie
#check @MatrixIndependentAudit.redundant_fraction
#print axioms MatrixIndependentAudit.redundant_fraction
#check @MatrixIndependentAudit.echoProgram
#print axioms MatrixIndependentAudit.echoProgram
#check @MatrixIndependentAudit.echo_value
#print axioms MatrixIndependentAudit.echo_value
#check @MatrixIndependentAudit.mixedProgram
#print axioms MatrixIndependentAudit.mixedProgram
#check @MatrixIndependentAudit.mixed_value
#print axioms MatrixIndependentAudit.mixed_value
#check @MatrixIndependentAudit.invalid_value
#print axioms MatrixIndependentAudit.invalid_value
#check @MatrixIndependentAudit.invalid_heavy_count
#print axioms MatrixIndependentAudit.invalid_heavy_count
#check @MatrixIndependentAudit.invalid_matrix_true
#print axioms MatrixIndependentAudit.invalid_matrix_true
#check @MatrixIndependentAudit.echo_below_threshold
#print axioms MatrixIndependentAudit.echo_below_threshold
#check @MatrixIndependentAudit.echo_at_threshold
#print axioms MatrixIndependentAudit.echo_at_threshold
#check @MatrixIndependentAudit.echo_matrix_false
#print axioms MatrixIndependentAudit.echo_matrix_false
#check @MatrixIndependentAudit.echo_matrix_true
#print axioms MatrixIndependentAudit.echo_matrix_true
#check @MatrixIndependentAudit.mixed_count_half
#print axioms MatrixIndependentAudit.mixed_count_half
#check @MatrixIndependentAudit.mixed_count_all
#print axioms MatrixIndependentAudit.mixed_count_all
#check @MatrixIndependentAudit.mixed_tied_membership
#print axioms MatrixIndependentAudit.mixed_tied_membership
#check @MatrixIndependentAudit.mixed_above_half_rejected
#print axioms MatrixIndependentAudit.mixed_above_half_rejected
#check @MatrixIndependentAudit.redundant_concrete_tie
#print axioms MatrixIndependentAudit.redundant_concrete_tie
#check @MatrixIndependentAudit.vacuous_one_even_zero_mass
#print axioms MatrixIndependentAudit.vacuous_one_even_zero_mass
#check @MatrixIndependentAudit.vacuous_above_one_even_zero_mass
#print axioms MatrixIndependentAudit.vacuous_above_one_even_zero_mass
#check @MatrixIndependentAudit.wrong_length_count_zero
#print axioms MatrixIndependentAudit.wrong_length_count_zero
#check @MatrixIndependentAudit.wrongArityProgram
#print axioms MatrixIndependentAudit.wrongArityProgram
#check @MatrixIndependentAudit.wrong_arity_value
#print axioms MatrixIndependentAudit.wrong_arity_value
#check @MatrixIndependentAudit.wrong_arity_heavy_count
#print axioms MatrixIndependentAudit.wrong_arity_heavy_count
#check @MatrixIndependentAudit.zero_scaling_changes_matrix
#print axioms MatrixIndependentAudit.zero_scaling_changes_matrix
#check @MatrixIndependentAudit.echo_prefix_stream
#print axioms MatrixIndependentAudit.echo_prefix_stream
#check @MatrixIndependentAudit.exact_four_input_predicate
#print axioms MatrixIndependentAudit.exact_four_input_predicate
#check @MatrixIndependentAudit.exact_nat_coded_predicate
#print axioms MatrixIndependentAudit.exact_nat_coded_predicate
#check @MatrixIndependentAudit.four_input_pairing_roundtrip
#print axioms MatrixIndependentAudit.four_input_pairing_roundtrip
#check @MatrixIndependentAudit.exact_integer_boolean
#print axioms MatrixIndependentAudit.exact_integer_boolean
#check @MatrixIndependentAudit.characteristic_nat_to_nat
#print axioms MatrixIndependentAudit.characteristic_nat_to_nat
#check @MatrixIndependentAudit.exact_quantifier_order
#print axioms MatrixIndependentAudit.exact_quantifier_order
#check @MatrixIndependentAudit.exact_heavy_mass_bridge
#print axioms MatrixIndependentAudit.exact_heavy_mass_bridge
#check @MatrixIndependentAudit.vectorPrograms
#print axioms MatrixIndependentAudit.vectorPrograms
#check @MatrixIndependentAudit.vectorRationals
#print axioms MatrixIndependentAudit.vectorRationals
#check @MatrixIndependentAudit.vectorRows
#print axioms MatrixIndependentAudit.vectorRows

import LiteralShiftSyntax
import LiteralShiftScan
import LiteralShiftReplay
import LiteralShiftCorrect
import LiteralShiftEndpoints
import LiteralShiftWord
import LiteralShiftPrefix

#print axioms P02.LiteralShift.scanBody_step
#print axioms P02.LiteralShift.runLoop_scan_agrees
#print axioms P02.LiteralShift.initialise_agrees
#print axioms P02.LiteralShift.selectedStore_agrees
#print axioms P02.LiteralShift.scanChoice_none_iff
#print axioms P02.LiteralShift.scanChoice_some_iff
#print axioms P02.LiteralShift.registerList_toFinset
#print axioms P02.LiteralShift.mem_registerList
#print axioms P02.LiteralShift.registerMap_injOn
#print axioms P02.LiteralShift.registerMap_ge
#print axioms P02.LiteralShift.not_mem_registerImage_of_lt
#print axioms P02.LiteralShift.sourceRegisters_body
#print axioms P02.LiteralShift.tailArgs_fresh
#print axioms P02.LiteralShift.sequenceList_append_exec
#print axioms P02.LiteralShift.sequenceList_resets_exec
#print axioms P02.LiteralShift.sequenceList_args_exec
#print axioms P02.LiteralShift.literalInline_exec_eq
#print axioms P02.LiteralShift.sourceLoad_tailArgs
#print axioms P02.LiteralShift.literalInline_correct
#print axioms P02.LiteralShift.replay_correct
#print axioms P02.LiteralShift.finish_correct
#print axioms P02.LiteralShift.finish_scanAgrees
#print axioms P02.LiteralShift.compileShift_exec
#print axioms P02.LiteralShift.compileShift_correct
#print axioms P02.LiteralShift.compileShift_unresolved
#print axioms P02.LiteralShift.compileShift_below
#print axioms P02.LiteralShift.compileShift_stopping
#print axioms P02.LiteralShift.compileShift_above
#print axioms P02.LiteralShift.compileShift_bit
#print axioms P02.LiteralShift.prefixValue_lowBits
#print axioms P02.LiteralShift.classify_zero
#print axioms P02.LiteralShift.classify_one
#print axioms P02.LiteralShift.scanChoice_zero
#print axioms P02.LiteralShift.scanChoice_one
#print axioms P02.LiteralShift.compileShift_zero_first
#print axioms P02.LiteralShift.compileShift_zero_tail
#print axioms P02.LiteralShift.compileShift_one
#print axioms P02.LiteralShift.cell_tests_disjoint
#print axioms P02.LiteralShift.classify_scaled
#print axioms P02.LiteralShift.scanChoice_scaled
#print axioms P02.LiteralShift.compileShift_scaled
#print axioms P02.LiteralShift.compileShift_sameRatio
#print axioms P02.LiteralShift.fold_word
#print axioms P02.LiteralShift.sentinel_payload
#print axioms P02.LiteralShift.wordPayload_lt
#print axioms P02.LiteralShift.sentinel_append_payload
#print axioms P02.LiteralShift.sentinel_append_div
#print axioms P02.LiteralShift.sentinel_append_mod
#print axioms P02.LiteralShift.sentinel_mod_payload
#print axioms P02.LiteralShift.sentinel_prefix_div
#print axioms P02.LiteralShift.sentinel_suffix
#print axioms P02.LiteralShift.streamPrefix_length
#print axioms P02.LiteralShift.streamPrefix_take
#print axioms P02.LiteralShift.streamPrefix_drop
#print axioms P02.LiteralShift.prefixValue_stream
#print axioms P02.LiteralShift.replayWord_stream
#print axioms P02.LiteralShift.sentinel_stream_last
#print axioms P02.LiteralShift.classify_stream
#print axioms P02.LiteralShift.classify_stage_consistent
#print axioms P02.LiteralShift.firstCut_or_unresolved
#print axioms P02.LiteralShift.compiledOutput_unresolved_at
#print axioms P02.LiteralShift.compiledOutput_copied_prefix
#print axioms P02.LiteralShift.compiledOutput_below
#print axioms P02.LiteralShift.compiledOutput_above_tail
#print axioms P02.LiteralShift.compiledOutput_on_firstCut
#print axioms P02.LiteralShift.compiledOutput_unresolved

import CandidateWitnesses
import Sigma2Compiled
#check @P02A2.CandidateCompiler.testBody_good
#print axioms P02A2.CandidateCompiler.testBody_good
#check @P02A2.CandidateCompiler.testBody_preserves
#print axioms P02A2.CandidateCompiler.testBody_preserves
#check @P02A2.CandidateCompiler.testLoop_preserves
#print axioms P02A2.CandidateCompiler.testLoop_preserves
#check @P02A2.CandidateCompiler.testLoop_good
#print axioms P02A2.CandidateCompiler.testLoop_good
#check @P02A2.CandidateCompiler.outerBody_matches
#print axioms P02A2.CandidateCompiler.outerBody_matches
#check @P02A2.CandidateCompiler.search_before_candidate
#print axioms P02A2.CandidateCompiler.search_before_candidate
#check @P02A2.CandidateCompiler.search_found_stable
#print axioms P02A2.CandidateCompiler.search_found_stable
#check @P02A2.CandidateCompiler.search_result
#print axioms P02A2.CandidateCompiler.search_result
#check @P02A2.CandidateCompiler.outerLoop_matches
#print axioms P02A2.CandidateCompiler.outerLoop_matches
#check @P02A2.CandidateCompiler.candidateBlock_value
#print axioms P02A2.CandidateCompiler.candidateBlock_value
#check @P02A2.CandidateCompiler.preserves_skip
#print axioms P02A2.CandidateCompiler.preserves_skip
#check @P02A2.CandidateCompiler.preserves_set
#print axioms P02A2.CandidateCompiler.preserves_set
#check @P02A2.CandidateCompiler.preserves_seq
#print axioms P02A2.CandidateCompiler.preserves_seq
#check @P02A2.CandidateCompiler.preserves_branch
#print axioms P02A2.CandidateCompiler.preserves_branch
#check @P02A2.CandidateCompiler.preserves_loop
#print axioms P02A2.CandidateCompiler.preserves_loop
#check @P02A2.CandidateCompiler.tryCandidate_preserves
#print axioms P02A2.CandidateCompiler.tryCandidate_preserves
#check @P02A2.CandidateCompiler.outerBody_preserves
#print axioms P02A2.CandidateCompiler.outerBody_preserves
#check @P02A2.CandidateCompiler.candidateBlock_preserves
#print axioms P02A2.CandidateCompiler.candidateBlock_preserves
#check @P02A2.CandidateSource.registerList_mem
#print axioms P02A2.CandidateSource.registerList_mem
#check @P02A2.CandidateSource.registerMap_injective_on
#print axioms P02A2.CandidateSource.registerMap_injective_on
#check @P02A2.CandidateSource.registerMap_fresh
#print axioms P02A2.CandidateSource.registerMap_fresh
#check @P02A2.CandidateSource.controller_not_private
#print axioms P02A2.CandidateSource.controller_not_private
#check @P02A2.CandidateSource.matrixArgs_fresh
#print axioms P02A2.CandidateSource.matrixArgs_fresh
#check @P02A2.CandidateSource.matrix_sourceLoad
#print axioms P02A2.CandidateSource.matrix_sourceLoad
#check @P02A2.CandidateSource.matrixCall_spec
#print axioms P02A2.CandidateSource.matrixCall_spec
#check @P02A2.CandidateSource.sourceCandidate_value
#print axioms P02A2.CandidateSource.sourceCandidate_value
#check @P02A2.CandidateSource.sourceCandidate_preserves
#print axioms P02A2.CandidateSource.sourceCandidate_preserves
#check @P02A2.CandidateWitnesses.bounded_registers
#print axioms P02A2.CandidateWitnesses.bounded_registers
#check @P02A2.CandidateWitnesses.true_registers
#print axioms P02A2.CandidateWitnesses.true_registers
#check @P02A2.CandidateWitnesses.bounded_registerList
#print axioms P02A2.CandidateWitnesses.bounded_registerList
#check @P02A2.CandidateWitnesses.true_registerList
#print axioms P02A2.CandidateWitnesses.true_registerList
#check @P02A2.CandidateWitnesses.candidate_checks_inclusive_test_bound
#print axioms P02A2.CandidateWitnesses.candidate_checks_inclusive_test_bound
#check @P02A2.CandidateWitnesses.candidate_retains_first_success
#print axioms P02A2.CandidateWitnesses.candidate_retains_first_success
#check @P02A2.Sigma2Compiled.secondMap_zero
#print axioms P02A2.Sigma2Compiled.secondMap_zero
#check @P02A2.Sigma2Compiled.secondMap_one
#print axioms P02A2.Sigma2Compiled.secondMap_one
#check @P02A2.Sigma2Compiled.secondMap_three
#print axioms P02A2.Sigma2Compiled.secondMap_three
#check @P02A2.Sigma2Compiled.secondMap_four
#print axioms P02A2.Sigma2Compiled.secondMap_four
#check @P02A2.Sigma2Compiled.secondMap_injective
#print axioms P02A2.Sigma2Compiled.secondMap_injective
#check @P02A2.Sigma2Compiled.renamedCandidate_value
#print axioms P02A2.Sigma2Compiled.renamedCandidate_value
#check @P02A2.Sigma2Compiled.renamedCandidate_preserves
#print axioms P02A2.Sigma2Compiled.renamedCandidate_preserves
#check @P02A2.Sigma2Compiled.previousBlock_value
#print axioms P02A2.Sigma2Compiled.previousBlock_value
#check @P02A2.Sigma2Compiled.previousBlock_preserves_zero
#print axioms P02A2.Sigma2Compiled.previousBlock_preserves_zero
#check @P02A2.Sigma2Compiled.previousBlock_preserves_one
#print axioms P02A2.Sigma2Compiled.previousBlock_preserves_one
#check @P02A2.Sigma2Compiled.previousBlock_preserves_three
#print axioms P02A2.Sigma2Compiled.previousBlock_preserves_three
#check @P02A2.Sigma2Compiled.emitComparison_value
#print axioms P02A2.Sigma2Compiled.emitComparison_value
#check @P02A2.Sigma2Compiled.compiled_value
#print axioms P02A2.Sigma2Compiled.compiled_value
#check @P02A2.Sigma2Compiled.prefixValue_eq
#print axioms P02A2.Sigma2Compiled.prefixValue_eq
#check @P02A2.Sigma2Compiled.observer_eq
#print axioms P02A2.Sigma2Compiled.observer_eq
#check @P02A2.Sigma2Compiled.law_eq
#print axioms P02A2.Sigma2Compiled.law_eq
#check @P02A2.Sigma2Compiled.zero_defect_iff
#print axioms P02A2.Sigma2Compiled.zero_defect_iff
#check @P02A2.Sigma2Compiled.one_defect_iff
#print axioms P02A2.Sigma2Compiled.one_defect_iff
#check @P02A2.Sigma2Compiled.prefixValue_primitive_recursive
#print axioms P02A2.Sigma2Compiled.prefixValue_primitive_recursive

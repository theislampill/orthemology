import PRProgram
import PRComposition
import PRRecursion
import PRHeadRecursion
import PRDerivation
import PRCoverage
import PRSpecialize
import PRWitnesses
set_option pp.universes true
#check @P02A2.PRProgram.sourceLoad_targets
#print axioms P02A2.PRProgram.sourceLoad_targets
#check @P02A2.PRProgram.sourceLoad_inputs
#print axioms P02A2.PRProgram.sourceLoad_inputs
#check @P02A2.PRProgram.call_correct
#print axioms P02A2.PRProgram.call_correct
#check @P02A2.PRProgram.call_value
#print axioms P02A2.PRProgram.call_value
#check @P02A2.PRProgram.call_frame
#print axioms P02A2.PRProgram.call_frame
#check @P02A2.PRProgram.zeroProgram_correct
#print axioms P02A2.PRProgram.zeroProgram_correct
#check @P02A2.PRProgram.successorProgram_correct
#print axioms P02A2.PRProgram.successorProgram_correct
#check @P02A2.PRProgram.projectionProgram_correct
#print axioms P02A2.PRProgram.projectionProgram_correct
#check @P02A2.PRProgram.exec_sequence
#print axioms P02A2.PRProgram.exec_sequence
#check @P02A2.PRComposition.inputArgs_fresh
#print axioms P02A2.PRComposition.inputArgs_fresh
#check @P02A2.PRComposition.buffer_lt_start
#print axioms P02A2.PRComposition.buffer_lt_start
#check @P02A2.PRComposition.buffer_injective
#print axioms P02A2.PRComposition.buffer_injective
#check @P02A2.PRComposition.componentCall_inputs
#print axioms P02A2.PRComposition.componentCall_inputs
#check @P02A2.PRComposition.componentCall_value
#print axioms P02A2.PRComposition.componentCall_value
#check @P02A2.PRComposition.componentCall_other
#print axioms P02A2.PRComposition.componentCall_other
#check @P02A2.PRComposition.componentCalls_correct
#print axioms P02A2.PRComposition.componentCalls_correct
#check @P02A2.PRComposition.bufferArgs_fresh
#print axioms P02A2.PRComposition.bufferArgs_fresh
#check @P02A2.PRComposition.composeProgram_correct
#print axioms P02A2.PRComposition.composeProgram_correct
#check @P02A2.PRRecursion.stepArgs_fresh
#print axioms P02A2.PRRecursion.stepArgs_fresh
#check @P02A2.PRRecursion.stepArgs_eval
#print axioms P02A2.PRRecursion.stepArgs_eval
#check @P02A2.PRRecursion.stepBody_matches
#print axioms P02A2.PRRecursion.stepBody_matches
#check @P02A2.PRRecursion.recursionLoop_matches
#print axioms P02A2.PRRecursion.recursionLoop_matches
#check @P02A2.PRRecursion.primitiveRecProgram_correct
#print axioms P02A2.PRRecursion.primitiveRecProgram_correct
#check @P02A2.PRHeadRecursion.permuteProgram_correct
#print axioms P02A2.PRHeadRecursion.permuteProgram_correct
#check @P02A2.PRHeadRecursion.inputPermutation_castSucc
#print axioms P02A2.PRHeadRecursion.inputPermutation_castSucc
#check @P02A2.PRHeadRecursion.inputPermutation_last
#print axioms P02A2.PRHeadRecursion.inputPermutation_last
#check @P02A2.PRHeadRecursion.stepPermutation_values
#print axioms P02A2.PRHeadRecursion.stepPermutation_values
#check @P02A2.PRHeadRecursion.headRecProgram_correct
#print axioms P02A2.PRHeadRecursion.headRecProgram_correct
#check @P02A2.PRDerivation.compile_correct
#print axioms P02A2.PRDerivation.compile_correct
#check @P02A2.PRDerivation.meaning_primitive_recursive
#print axioms P02A2.PRDerivation.meaning_primitive_recursive
#check @P02A2.PRCoverage.vector_get_cons
#print axioms P02A2.PRCoverage.vector_get_cons
#check @P02A2.PRCoverage.vector_get_tail
#print axioms P02A2.PRCoverage.vector_get_tail
#check @P02A2.PRCoverage.exists_code_of_primrec'
#print axioms P02A2.PRCoverage.exists_code_of_primrec'
#check @P02A2.PRCoverage.exists_code_of_primrec
#print axioms P02A2.PRCoverage.exists_code_of_primrec
#check @P02A2.PRCoverage.exists_program_of_primrec
#print axioms P02A2.PRCoverage.exists_program_of_primrec
#check @P02A2.PRSpecialize.parameterArgs_fresh
#print axioms P02A2.PRSpecialize.parameterArgs_fresh
#check @P02A2.PRSpecialize.specialize_correct
#print axioms P02A2.PRSpecialize.specialize_correct
#check @P02A2.PRSpecialize.compile_specialize_correct
#print axioms P02A2.PRSpecialize.compile_specialize_correct
#check @P02A2.PRWitnesses.addition_meaning
#print axioms P02A2.PRWitnesses.addition_meaning
#check @P02A2.PRWitnesses.compiled_addition
#print axioms P02A2.PRWitnesses.compiled_addition
#check @P02A2.PRWitnesses.compiled_previousIndex
#print axioms P02A2.PRWitnesses.compiled_previousIndex
#check @P02A2.PRWitnesses.specialized_addition
#print axioms P02A2.PRWitnesses.specialized_addition
#check @P02A2.PRWitnesses.zero_arity_compiles
#print axioms P02A2.PRWitnesses.zero_arity_compiles
#check @P02A2.PRWitnesses.missing_order_adapter_changes_result
#print axioms P02A2.PRWitnesses.missing_order_adapter_changes_result

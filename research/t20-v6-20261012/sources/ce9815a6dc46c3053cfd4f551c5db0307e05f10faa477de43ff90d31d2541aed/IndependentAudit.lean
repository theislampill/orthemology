import InternalPolymorphism
import FiniteBridge
import SourceTypeOps
import SourceHeadStep
import SourceChecker
import SourceCheckerProofs
import SourceResources
import SourceRepresentation
import SourceResourceBounds
import SourceControls
import SourceBranchControls
import SourceExportBoundary
import SourceCheckerAudit
import NativeDecoder
import NativeDecoderProofs
import NativeDecoderSoundness
import NativeProofGrammar
import NativeProofSoundness
import NativeCheckerBridge
import NativeFieldLemmas
import NativeDecoderCompleteness
import NativeRepresentationEquivalence
import NativeDecoderControls
import NativeDecoderAudit
set_option pp.universes true
set_option pp.explicit true
set_option format.width 180
#check @P03Source.sourceScoped_eq
#print axioms P03Source.sourceScoped_eq
#check @P03Source.sourceInstantiate_eq
#print axioms P03Source.sourceInstantiate_eq
#check @P03Source.sourceHeadStep_eq
#print axioms P03Source.sourceHeadStep_eq
#check @P03Source.trace_matches
#print axioms P03Source.trace_matches
#check @P03Source.source_core_export_square
#print axioms P03Source.source_core_export_square
#check @P03Source.sourceRun_refines_core
#print axioms P03Source.sourceRun_refines_core
#check @P03Source.sourceCheck_refines_core
#print axioms P03Source.sourceCheck_refines_core
#check @P03Source.source_checker_constructor_erasure_square
#print axioms P03Source.source_checker_constructor_erasure_square
#check @P03Source.source_checker_sound
#print axioms P03Source.source_checker_sound
#check @P03SourceControls.erased_checker_acceptance_is_not_source_acceptance
#print axioms P03SourceControls.erased_checker_acceptance_is_not_source_acceptance
#check @P03Source.proofTree_shape
#print axioms P03Source.proofTree_shape
#check @P03Source.sourceCheck_input_guards
#print axioms P03Source.sourceCheck_input_guards
#check @P03Source.semantic_refusal_preserved
#print axioms P03Source.semantic_refusal_preserved
#check @P03Source.semantic_singleton_trace
#print axioms P03Source.semantic_singleton_trace
#check @P03Source.encoded_nodes_le_export_work
#print axioms P03Source.encoded_nodes_le_export_work
#check @P03Source.partial_constructor_export_square
#print axioms P03Source.partial_constructor_export_square
#check @P03Source.source_checker_export_square
#print axioms P03Source.source_checker_export_square
#check @P03Source.checker_acceptance_not_total_export
#print axioms P03Source.checker_acceptance_not_total_export
#check @P03Source.decodeType_sound
#print axioms P03Source.decodeType_sound
#check @P03Source.decodeTerm_sound
#print axioms P03Source.decodeTerm_sound
#check @P03Source.decodeTrace_sound
#print axioms P03Source.decodeTrace_sound
#check @P03Source.decodeProof_sound
#print axioms P03Source.decodeProof_sound
#check @P03Source.decodeNativeProof_roundtrip
#print axioms P03Source.decodeNativeProof_roundtrip
#check @P03Source.NativeProofRep.decode_complete
#print axioms P03Source.NativeProofRep.decode_complete
#check @P03Source.NativeProofRep.deterministic
#print axioms P03Source.NativeProofRep.deterministic
#check @P03Source.nativeCheck_representation_equivalence
#print axioms P03Source.nativeCheck_representation_equivalence
#check @P03Source.native_checker_constructor_erasure_square
#print axioms P03Source.native_checker_constructor_erasure_square
#check @P03Source.native_checker_sound
#print axioms P03Source.native_checker_sound
#check @P03Source.native_check_rejects_duplicate_fields
#print axioms P03Source.native_check_rejects_duplicate_fields
#check @P03Source.native_checker_partial_export_square
#print axioms P03Source.native_checker_partial_export_square

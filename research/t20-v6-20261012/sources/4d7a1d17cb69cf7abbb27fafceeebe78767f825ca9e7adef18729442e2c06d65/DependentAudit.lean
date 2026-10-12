import P01DependentModel
import P01DependentSubstitution
import P01DependentFundamental
import P01DependentControls
import P01DependentRepresentation
import AuditSupport
set_option pp.universes true
set_option format.width 120
#eval IO.println "AUDIT_BEGIN P01DF.IndexRelated"
#check P01DF.IndexRelated
#ortho_audit P01DF.IndexRelated
#print axioms P01DF.IndexRelated
#eval IO.println "AUDIT_END P01DF.IndexRelated"
#eval IO.println "AUDIT_BEGIN P01DF.index_refl"
#check P01DF.index_refl
#ortho_audit P01DF.index_refl
#print axioms P01DF.index_refl
#eval IO.println "AUDIT_END P01DF.index_refl"
#eval IO.println "AUDIT_BEGIN P01DF.index_cons"
#check P01DF.index_cons
#ortho_audit P01DF.index_cons
#print axioms P01DF.index_cons
#eval IO.println "AUDIT_END P01DF.index_cons"
#eval IO.println "AUDIT_BEGIN P01DF.eval_index_related"
#check P01DF.eval_index_related
#ortho_audit P01DF.eval_index_related
#print axioms P01DF.eval_index_related
#eval IO.println "AUDIT_END P01DF.eval_index_related"
#eval IO.println "AUDIT_BEGIN P01DF.rawModel"
#check P01DF.rawModel
#ortho_audit P01DF.rawModel
#print axioms P01DF.rawModel
#eval IO.println "AUDIT_END P01DF.rawModel"
#eval IO.println "AUDIT_BEGIN P01DF.idModel"
#check P01DF.idModel
#ortho_audit P01DF.idModel
#print axioms P01DF.idModel
#eval IO.println "AUDIT_END P01DF.idModel"
#eval IO.println "AUDIT_BEGIN P01DF.idModel_transport"
#check P01DF.idModel_transport
#ortho_audit P01DF.idModel_transport
#print axioms P01DF.idModel_transport
#eval IO.println "AUDIT_END P01DF.idModel_transport"
#eval IO.println "AUDIT_BEGIN P01DF.piModel"
#check P01DF.piModel
#ortho_audit P01DF.piModel
#print axioms P01DF.piModel
#eval IO.println "AUDIT_END P01DF.piModel"
#eval IO.println "AUDIT_BEGIN P01DF.sigmaModel"
#check P01DF.sigmaModel
#ortho_audit P01DF.sigmaModel
#print axioms P01DF.sigmaModel
#eval IO.println "AUDIT_END P01DF.sigmaModel"
#eval IO.println "AUDIT_BEGIN P01DF.IndexFamily"
#check P01DF.IndexFamily
#ortho_audit P01DF.IndexFamily
#print axioms P01DF.IndexFamily
#eval IO.println "AUDIT_END P01DF.IndexFamily"
#eval IO.println "AUDIT_BEGIN P01DF.Ty"
#check P01DF.Ty
#ortho_audit P01DF.Ty
#print axioms P01DF.Ty
#eval IO.println "AUDIT_END P01DF.Ty"
#eval IO.println "AUDIT_BEGIN P01DF.interpret"
#check P01DF.interpret
#ortho_audit P01DF.interpret
#print axioms P01DF.interpret
#eval IO.println "AUDIT_END P01DF.interpret"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_index_transport"
#check P01DF.interpret_index_transport
#ortho_audit P01DF.interpret_index_transport
#print axioms P01DF.interpret_index_transport
#eval IO.println "AUDIT_END P01DF.interpret_index_transport"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_identity_extension"
#check P01DF.dependent_identity_extension
#ortho_audit P01DF.dependent_identity_extension
#print axioms P01DF.dependent_identity_extension
#eval IO.println "AUDIT_END P01DF.dependent_identity_extension"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_endpoint_restriction"
#check P01DF.dependent_endpoint_restriction
#ortho_audit P01DF.dependent_endpoint_restriction
#print axioms P01DF.dependent_endpoint_restriction
#eval IO.println "AUDIT_END P01DF.dependent_endpoint_restriction"
#eval IO.println "AUDIT_BEGIN P01DF.substIndex"
#check P01DF.substIndex
#ortho_audit P01DF.substIndex
#print axioms P01DF.substIndex
#eval IO.println "AUDIT_END P01DF.substIndex"
#eval IO.println "AUDIT_BEGIN P01DF.subIndexEnv"
#check P01DF.subIndexEnv
#ortho_audit P01DF.subIndexEnv
#print axioms P01DF.subIndexEnv
#eval IO.println "AUDIT_END P01DF.subIndexEnv"
#eval IO.println "AUDIT_BEGIN P01DF.subIndexEnv_lift"
#check P01DF.subIndexEnv_lift
#ortho_audit P01DF.subIndexEnv_lift
#print axioms P01DF.subIndexEnv_lift
#eval IO.println "AUDIT_END P01DF.subIndexEnv_lift"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_index_substitution"
#check P01DF.interpret_index_substitution
#ortho_audit P01DF.interpret_index_substitution
#print axioms P01DF.interpret_index_substitution
#eval IO.println "AUDIT_END P01DF.interpret_index_substitution"
#eval IO.println "AUDIT_BEGIN P01DF.instantiate"
#check P01DF.instantiate
#ortho_audit P01DF.instantiate
#print axioms P01DF.instantiate
#eval IO.println "AUDIT_END P01DF.instantiate"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_instantiate"
#check P01DF.interpret_instantiate
#ortho_audit P01DF.interpret_instantiate
#print axioms P01DF.interpret_instantiate
#eval IO.println "AUDIT_END P01DF.interpret_instantiate"
#eval IO.println "AUDIT_BEGIN P01DF.embedFinite"
#check P01DF.embedFinite
#ortho_audit P01DF.embedFinite
#print axioms P01DF.embedFinite
#eval IO.println "AUDIT_END P01DF.embedFinite"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_embedFinite"
#check P01DF.interpret_embedFinite
#ortho_audit P01DF.interpret_embedFinite
#print axioms P01DF.interpret_embedFinite
#eval IO.println "AUDIT_END P01DF.interpret_embedFinite"
#eval IO.println "AUDIT_BEGIN P01DF.renameType"
#check P01DF.renameType
#ortho_audit P01DF.renameType
#print axioms P01DF.renameType
#eval IO.println "AUDIT_END P01DF.renameType"
#eval IO.println "AUDIT_BEGIN P01DF.piModel_congr"
#check P01DF.piModel_congr
#ortho_audit P01DF.piModel_congr
#print axioms P01DF.piModel_congr
#eval IO.println "AUDIT_END P01DF.piModel_congr"
#eval IO.println "AUDIT_BEGIN P01DF.sigmaModel_congr"
#check P01DF.sigmaModel_congr
#ortho_audit P01DF.sigmaModel_congr
#print axioms P01DF.sigmaModel_congr
#eval IO.println "AUDIT_END P01DF.sigmaModel_congr"
#eval IO.println "AUDIT_BEGIN P01DF.piModel_rename"
#check P01DF.piModel_rename
#ortho_audit P01DF.piModel_rename
#print axioms P01DF.piModel_rename
#eval IO.println "AUDIT_END P01DF.piModel_rename"
#eval IO.println "AUDIT_BEGIN P01DF.sigmaModel_rename"
#check P01DF.sigmaModel_rename
#ortho_audit P01DF.sigmaModel_rename
#print axioms P01DF.sigmaModel_rename
#eval IO.println "AUDIT_END P01DF.sigmaModel_rename"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_type_rename"
#check P01DF.interpret_type_rename
#ortho_audit P01DF.interpret_type_rename
#print axioms P01DF.interpret_type_rename
#eval IO.println "AUDIT_END P01DF.interpret_type_rename"
#eval IO.println "AUDIT_BEGIN P01DF.liftTypes"
#check P01DF.liftTypes
#ortho_audit P01DF.liftTypes
#print axioms P01DF.liftTypes
#eval IO.println "AUDIT_END P01DF.liftTypes"
#eval IO.println "AUDIT_BEGIN P01DF.liftIndices"
#check P01DF.liftIndices
#ortho_audit P01DF.liftIndices
#print axioms P01DF.liftIndices
#eval IO.println "AUDIT_END P01DF.liftIndices"
#eval IO.println "AUDIT_BEGIN P01DF.substType"
#check P01DF.substType
#ortho_audit P01DF.substType
#print axioms P01DF.substType
#eval IO.println "AUDIT_END P01DF.substType"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_liftTypes"
#check P01DF.interpret_liftTypes
#ortho_audit P01DF.interpret_liftTypes
#print axioms P01DF.interpret_liftTypes
#eval IO.println "AUDIT_END P01DF.interpret_liftTypes"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_liftIndices"
#check P01DF.interpret_liftIndices
#ortho_audit P01DF.interpret_liftIndices
#print axioms P01DF.interpret_liftIndices
#eval IO.println "AUDIT_END P01DF.interpret_liftIndices"
#eval IO.println "AUDIT_BEGIN P01DF.piModel_substitute"
#check P01DF.piModel_substitute
#ortho_audit P01DF.piModel_substitute
#print axioms P01DF.piModel_substitute
#eval IO.println "AUDIT_END P01DF.piModel_substitute"
#eval IO.println "AUDIT_BEGIN P01DF.sigmaModel_substitute"
#check P01DF.sigmaModel_substitute
#ortho_audit P01DF.sigmaModel_substitute
#print axioms P01DF.sigmaModel_substitute
#eval IO.println "AUDIT_END P01DF.sigmaModel_substitute"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_type_substitution"
#check P01DF.interpret_type_substitution
#ortho_audit P01DF.interpret_type_substitution
#print axioms P01DF.interpret_type_substitution
#eval IO.println "AUDIT_END P01DF.interpret_type_substitution"
#eval IO.println "AUDIT_BEGIN P01DF.instantiateType"
#check P01DF.instantiateType
#ortho_audit P01DF.instantiateType
#print axioms P01DF.instantiateType
#eval IO.println "AUDIT_END P01DF.instantiateType"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_type_instantiate"
#check P01DF.interpret_type_instantiate
#ortho_audit P01DF.interpret_type_instantiate
#print axioms P01DF.interpret_type_instantiate
#eval IO.println "AUDIT_END P01DF.interpret_type_instantiate"
#eval IO.println "AUDIT_BEGIN P01DF.type_instantiate_rel"
#check P01DF.type_instantiate_rel
#ortho_audit P01DF.type_instantiate_rel
#print axioms P01DF.type_instantiate_rel
#eval IO.println "AUDIT_END P01DF.type_instantiate_rel"
#eval IO.println "AUDIT_BEGIN P01DF.type_instantiate_obj"
#check P01DF.type_instantiate_obj
#ortho_audit P01DF.type_instantiate_obj
#print axioms P01DF.type_instantiate_obj
#eval IO.println "AUDIT_END P01DF.type_instantiate_obj"
#eval IO.println "AUDIT_BEGIN P01DF.PolyConv"
#check P01DF.PolyConv
#ortho_audit P01DF.PolyConv
#print axioms P01DF.PolyConv
#eval IO.println "AUDIT_END P01DF.PolyConv"
#eval IO.println "AUDIT_BEGIN P01DF.polyConv_sound"
#check P01DF.polyConv_sound
#ortho_audit P01DF.polyConv_sound
#print axioms P01DF.polyConv_sound
#eval IO.println "AUDIT_END P01DF.polyConv_sound"
#eval IO.println "AUDIT_BEGIN P01DF.motiveAt"
#check P01DF.motiveAt
#ortho_audit P01DF.motiveAt
#print axioms P01DF.motiveAt
#eval IO.println "AUDIT_END P01DF.motiveAt"
#eval IO.println "AUDIT_BEGIN P01DF.interpret_motiveAt"
#check P01DF.interpret_motiveAt
#ortho_audit P01DF.interpret_motiveAt
#print axioms P01DF.interpret_motiveAt
#eval IO.println "AUDIT_END P01DF.interpret_motiveAt"
#eval IO.println "AUDIT_BEGIN P01DF.Has"
#check P01DF.Has
#ortho_audit P01DF.Has
#print axioms P01DF.Has
#eval IO.println "AUDIT_END P01DF.Has"
#eval IO.println "AUDIT_BEGIN P01DF.fundamental"
#check P01DF.fundamental
#ortho_audit P01DF.fundamental
#print axioms P01DF.fundamental
#eval IO.println "AUDIT_END P01DF.fundamental"
#eval IO.println "AUDIT_BEGIN P01DF.unary_soundness"
#check P01DF.unary_soundness
#ortho_audit P01DF.unary_soundness
#print axioms P01DF.unary_soundness
#eval IO.println "AUDIT_END P01DF.unary_soundness"
#eval IO.println "AUDIT_BEGIN P01DF.substitution_fundamental"
#check P01DF.substitution_fundamental
#ortho_audit P01DF.substitution_fundamental
#print axioms P01DF.substitution_fundamental
#eval IO.println "AUDIT_END P01DF.substitution_fundamental"
#eval IO.println "AUDIT_BEGIN P01DF.type_substitution_fundamental"
#check P01DF.type_substitution_fundamental
#ortho_audit P01DF.type_substitution_fundamental
#print axioms P01DF.type_substitution_fundamental
#eval IO.println "AUDIT_END P01DF.type_substitution_fundamental"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_all_fundamental"
#check P01DF.dependent_all_fundamental
#ortho_audit P01DF.dependent_all_fundamental
#print axioms P01DF.dependent_all_fundamental
#eval IO.println "AUDIT_END P01DF.dependent_all_fundamental"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_all_self_instantiation"
#check P01DF.dependent_all_self_instantiation
#ortho_audit P01DF.dependent_all_self_instantiation
#print axioms P01DF.dependent_all_self_instantiation
#eval IO.println "AUDIT_END P01DF.dependent_all_self_instantiation"
#eval IO.println "AUDIT_BEGIN P01DF.skk"
#check P01DF.skk
#ortho_audit P01DF.skk
#print axioms P01DF.skk
#eval IO.println "AUDIT_END P01DF.skk"
#eval IO.println "AUDIT_BEGIN P01DF.emptyIndices"
#check P01DF.emptyIndices
#ortho_audit P01DF.emptyIndices
#print axioms P01DF.emptyIndices
#eval IO.println "AUDIT_END P01DF.emptyIndices"
#eval IO.println "AUDIT_BEGIN P01DF.anchoredIdentity"
#check P01DF.anchoredIdentity
#ortho_audit P01DF.anchoredIdentity
#print axioms P01DF.anchoredIdentity
#eval IO.println "AUDIT_END P01DF.anchoredIdentity"
#eval IO.println "AUDIT_BEGIN P01DF.anchored_identity_inhabited"
#check P01DF.anchored_identity_inhabited
#ortho_audit P01DF.anchored_identity_inhabited
#print axioms P01DF.anchored_identity_inhabited
#eval IO.println "AUDIT_END P01DF.anchored_identity_inhabited"
#eval IO.println "AUDIT_BEGIN P01DF.anchored_identity_empty"
#check P01DF.anchored_identity_empty
#ortho_audit P01DF.anchored_identity_empty
#print axioms P01DF.anchored_identity_empty
#eval IO.println "AUDIT_END P01DF.anchored_identity_empty"
#eval IO.println "AUDIT_BEGIN P01DF.nonconstant_fibres"
#check P01DF.nonconstant_fibres
#ortho_audit P01DF.nonconstant_fibres
#print axioms P01DF.nonconstant_fibres
#eval IO.println "AUDIT_END P01DF.nonconstant_fibres"
#eval IO.println "AUDIT_BEGIN P01DF.heterogeneous_index_transport_fails"
#check P01DF.heterogeneous_index_transport_fails
#ortho_audit P01DF.heterogeneous_index_transport_fails
#print axioms P01DF.heterogeneous_index_transport_fails
#eval IO.println "AUDIT_END P01DF.heterogeneous_index_transport_fails"
#eval IO.println "AUDIT_BEGIN P01DF.totalPER"
#check P01DF.totalPER
#ortho_audit P01DF.totalPER
#print axioms P01DF.totalPER
#eval IO.println "AUDIT_END P01DF.totalPER"
#eval IO.println "AUDIT_BEGIN P01DF.inspectedFibre"
#check P01DF.inspectedFibre
#ortho_audit P01DF.inspectedFibre
#print axioms P01DF.inspectedFibre
#eval IO.println "AUDIT_END P01DF.inspectedFibre"
#eval IO.println "AUDIT_BEGIN P01DF.naivePiRel"
#check P01DF.naivePiRel
#ortho_audit P01DF.naivePiRel
#print axioms P01DF.naivePiRel
#eval IO.println "AUDIT_END P01DF.naivePiRel"
#eval IO.println "AUDIT_BEGIN P01DF.omitted_coherence_breaks_pi_symmetry"
#check P01DF.omitted_coherence_breaks_pi_symmetry
#ortho_audit P01DF.omitted_coherence_breaks_pi_symmetry
#print axioms P01DF.omitted_coherence_breaks_pi_symmetry
#eval IO.println "AUDIT_END P01DF.omitted_coherence_breaks_pi_symmetry"
#eval IO.println "AUDIT_BEGIN P01DF.dependentReflType"
#check P01DF.dependentReflType
#ortho_audit P01DF.dependentReflType
#print axioms P01DF.dependentReflType
#eval IO.println "AUDIT_END P01DF.dependentReflType"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_reflexivity_typed"
#check P01DF.dependent_reflexivity_typed
#ortho_audit P01DF.dependent_reflexivity_typed
#print axioms P01DF.dependent_reflexivity_typed
#eval IO.println "AUDIT_END P01DF.dependent_reflexivity_typed"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_reflexivity_nonempty"
#check P01DF.dependent_reflexivity_nonempty
#ortho_audit P01DF.dependent_reflexivity_nonempty
#print axioms P01DF.dependent_reflexivity_nonempty
#eval IO.println "AUDIT_END P01DF.dependent_reflexivity_nonempty"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_pair_typed"
#check P01DF.dependent_pair_typed
#ortho_audit P01DF.dependent_pair_typed
#print axioms P01DF.dependent_pair_typed
#eval IO.println "AUDIT_END P01DF.dependent_pair_typed"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_pair_nonempty"
#check P01DF.dependent_pair_nonempty
#ortho_audit P01DF.dependent_pair_nonempty
#print axioms P01DF.dependent_pair_nonempty
#eval IO.println "AUDIT_END P01DF.dependent_pair_nonempty"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_pair_projection_typed"
#check P01DF.dependent_pair_projection_typed
#ortho_audit P01DF.dependent_pair_projection_typed
#print axioms P01DF.dependent_pair_projection_typed
#eval IO.println "AUDIT_END P01DF.dependent_pair_projection_typed"
#eval IO.println "AUDIT_BEGIN P01DF.convertedProof"
#check P01DF.convertedProof
#ortho_audit P01DF.convertedProof
#print axioms P01DF.convertedProof
#eval IO.println "AUDIT_END P01DF.convertedProof"
#eval IO.println "AUDIT_BEGIN P01DF.converted_identity_proof_typed"
#check P01DF.converted_identity_proof_typed
#ortho_audit P01DF.converted_identity_proof_typed
#print axioms P01DF.converted_identity_proof_typed
#eval IO.println "AUDIT_END P01DF.converted_identity_proof_typed"
#eval IO.println "AUDIT_BEGIN P01DF.proof_dependent_j_typed"
#check P01DF.proof_dependent_j_typed
#ortho_audit P01DF.proof_dependent_j_typed
#print axioms P01DF.proof_dependent_j_typed
#eval IO.println "AUDIT_END P01DF.proof_dependent_j_typed"
#eval IO.println "AUDIT_BEGIN P01DF.proof_dependent_j_nonempty"
#check P01DF.proof_dependent_j_nonempty
#ortho_audit P01DF.proof_dependent_j_nonempty
#print axioms P01DF.proof_dependent_j_nonempty
#eval IO.println "AUDIT_END P01DF.proof_dependent_j_nonempty"
#eval IO.println "AUDIT_BEGIN P01DF.two_sort_substitution_control"
#check P01DF.two_sort_substitution_control
#ortho_audit P01DF.two_sort_substitution_control
#print axioms P01DF.two_sort_substitution_control
#eval IO.println "AUDIT_END P01DF.two_sort_substitution_control"
#eval IO.println "AUDIT_BEGIN P01DF.dependentPolyBody"
#check P01DF.dependentPolyBody
#ortho_audit P01DF.dependentPolyBody
#print axioms P01DF.dependentPolyBody
#eval IO.println "AUDIT_END P01DF.dependentPolyBody"
#eval IO.println "AUDIT_BEGIN P01DF.dependentPolyType"
#check P01DF.dependentPolyType
#ortho_audit P01DF.dependentPolyType
#print axioms P01DF.dependentPolyType
#eval IO.println "AUDIT_END P01DF.dependentPolyType"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_polymorphic_typed"
#check P01DF.dependent_polymorphic_typed
#ortho_audit P01DF.dependent_polymorphic_typed
#print axioms P01DF.dependent_polymorphic_typed
#eval IO.println "AUDIT_END P01DF.dependent_polymorphic_typed"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_polymorphic_nonempty"
#check P01DF.dependent_polymorphic_nonempty
#ortho_audit P01DF.dependent_polymorphic_nonempty
#print axioms P01DF.dependent_polymorphic_nonempty
#eval IO.println "AUDIT_END P01DF.dependent_polymorphic_nonempty"
#eval IO.println "AUDIT_BEGIN P01DF.dependent_polymorphic_self_typed"
#check P01DF.dependent_polymorphic_self_typed
#ortho_audit P01DF.dependent_polymorphic_self_typed
#print axioms P01DF.dependent_polymorphic_self_typed
#eval IO.println "AUDIT_END P01DF.dependent_polymorphic_self_typed"
#eval IO.println "AUDIT_BEGIN P01DF.raw_index_variable_not_arbitrary_type_parameter"
#check P01DF.raw_index_variable_not_arbitrary_type_parameter
#ortho_audit P01DF.raw_index_variable_not_arbitrary_type_parameter
#print axioms P01DF.raw_index_variable_not_arbitrary_type_parameter
#eval IO.println "AUDIT_END P01DF.raw_index_variable_not_arbitrary_type_parameter"
#eval IO.println "AUDIT_BEGIN P01DF.raw_omega_typed"
#check P01DF.raw_omega_typed
#ortho_audit P01DF.raw_omega_typed
#print axioms P01DF.raw_omega_typed
#eval IO.println "AUDIT_END P01DF.raw_omega_typed"
#eval IO.println "AUDIT_BEGIN P01DF.raw_omega_has_no_normal_reduct"
#check P01DF.raw_omega_has_no_normal_reduct
#ortho_audit P01DF.raw_omega_has_no_normal_reduct
#print axioms P01DF.raw_omega_has_no_normal_reduct
#eval IO.println "AUDIT_END P01DF.raw_omega_has_no_normal_reduct"
#eval IO.println "AUDIT_BEGIN P01DF.indexContext"
#check P01DF.indexContext
#ortho_audit P01DF.indexContext
#print axioms P01DF.indexContext
#eval IO.println "AUDIT_END P01DF.indexContext"
#eval IO.println "AUDIT_BEGIN P01DF.candidateTy"
#check P01DF.candidateTy
#ortho_audit P01DF.candidateTy
#print axioms P01DF.candidateTy
#eval IO.println "AUDIT_END P01DF.candidateTy"
#eval IO.println "AUDIT_BEGIN P01DF.candidateTm"
#check P01DF.candidateTm
#ortho_audit P01DF.candidateTm
#print axioms P01DF.candidateTm
#eval IO.println "AUDIT_END P01DF.candidateTm"
#eval IO.println "AUDIT_BEGIN P01DF.candidateEnvelope"
#check P01DF.candidateEnvelope
#ortho_audit P01DF.candidateEnvelope
#print axioms P01DF.candidateEnvelope
#eval IO.println "AUDIT_END P01DF.candidateEnvelope"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_envelope_code_exact"
#check P01DF.candidate_envelope_code_exact
#ortho_audit P01DF.candidate_envelope_code_exact
#print axioms P01DF.candidate_envelope_code_exact
#eval IO.println "AUDIT_END P01DF.candidate_envelope_code_exact"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_replay_sound"
#check P01DF.candidate_replay_sound
#ortho_audit P01DF.candidate_replay_sound
#print axioms P01DF.candidate_replay_sound
#eval IO.println "AUDIT_END P01DF.candidate_replay_sound"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_ty_ext"
#check P01DF.candidate_ty_ext
#ortho_audit P01DF.candidate_ty_ext
#print axioms P01DF.candidate_ty_ext
#eval IO.println "AUDIT_END P01DF.candidate_ty_ext"
#eval IO.println "AUDIT_BEGIN P01DF.candidateRaw"
#check P01DF.candidateRaw
#ortho_audit P01DF.candidateRaw
#print axioms P01DF.candidateRaw
#eval IO.println "AUDIT_END P01DF.candidateRaw"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_raw_representation"
#check P01DF.candidate_raw_representation
#ortho_audit P01DF.candidate_raw_representation
#print axioms P01DF.candidate_raw_representation
#eval IO.println "AUDIT_END P01DF.candidate_raw_representation"
#eval IO.println "AUDIT_BEGIN P01DF.rawIndexTm"
#check P01DF.rawIndexTm
#ortho_audit P01DF.rawIndexTm
#print axioms P01DF.rawIndexTm
#eval IO.println "AUDIT_END P01DF.rawIndexTm"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_identity_representation"
#check P01DF.candidate_identity_representation
#ortho_audit P01DF.candidate_identity_representation
#print axioms P01DF.candidate_identity_representation
#eval IO.println "AUDIT_END P01DF.candidate_identity_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidateBinder"
#check P01DF.candidateBinder
#ortho_audit P01DF.candidateBinder
#print axioms P01DF.candidateBinder
#eval IO.println "AUDIT_END P01DF.candidateBinder"
#eval IO.println "AUDIT_BEGIN P01DF.candidateBody"
#check P01DF.candidateBody
#ortho_audit P01DF.candidateBody
#print axioms P01DF.candidateBody
#eval IO.println "AUDIT_END P01DF.candidateBody"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_fibre"
#check P01DF.candidate_fibre
#ortho_audit P01DF.candidate_fibre
#print axioms P01DF.candidate_fibre
#eval IO.println "AUDIT_END P01DF.candidate_fibre"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_pi_representation"
#check P01DF.candidate_pi_representation
#ortho_audit P01DF.candidate_pi_representation
#print axioms P01DF.candidate_pi_representation
#eval IO.println "AUDIT_END P01DF.candidate_pi_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_sigma_representation"
#check P01DF.candidate_sigma_representation
#ortho_audit P01DF.candidate_sigma_representation
#print axioms P01DF.candidate_sigma_representation
#eval IO.println "AUDIT_END P01DF.candidate_sigma_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_lambda_code"
#check P01DF.candidate_lambda_code
#ortho_audit P01DF.candidate_lambda_code
#print axioms P01DF.candidate_lambda_code
#eval IO.println "AUDIT_END P01DF.candidate_lambda_code"
#eval IO.println "AUDIT_BEGIN P01DF.candidateIndexSub"
#check P01DF.candidateIndexSub
#ortho_audit P01DF.candidateIndexSub
#print axioms P01DF.candidateIndexSub
#eval IO.println "AUDIT_END P01DF.candidateIndexSub"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_substitution_representation"
#check P01DF.candidate_substitution_representation
#ortho_audit P01DF.candidate_substitution_representation
#print axioms P01DF.candidate_substitution_representation
#eval IO.println "AUDIT_END P01DF.candidate_substitution_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_substitution_code"
#check P01DF.candidate_substitution_code
#ortho_audit P01DF.candidate_substitution_code
#print axioms P01DF.candidate_substitution_code
#eval IO.println "AUDIT_END P01DF.candidate_substitution_code"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllBody"
#check P01DF.candidateAllBody
#ortho_audit P01DF.candidateAllBody
#print axioms P01DF.candidateAllBody
#eval IO.println "AUDIT_END P01DF.candidateAllBody"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllFormation"
#check P01DF.candidateAllFormation
#ortho_audit P01DF.candidateAllFormation
#print axioms P01DF.candidateAllFormation
#eval IO.println "AUDIT_END P01DF.candidateAllFormation"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_all_representation"
#check P01DF.candidate_all_representation
#ortho_audit P01DF.candidate_all_representation
#print axioms P01DF.candidate_all_representation
#eval IO.println "AUDIT_END P01DF.candidate_all_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllBodyTm"
#check P01DF.candidateAllBodyTm
#ortho_audit P01DF.candidateAllBodyTm
#print axioms P01DF.candidateAllBodyTm
#eval IO.println "AUDIT_END P01DF.candidateAllBodyTm"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_all_uniformity"
#check P01DF.candidate_all_uniformity
#ortho_audit P01DF.candidate_all_uniformity
#print axioms P01DF.candidate_all_uniformity
#eval IO.println "AUDIT_END P01DF.candidate_all_uniformity"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllIntro"
#check P01DF.candidateAllIntro
#ortho_audit P01DF.candidateAllIntro
#print axioms P01DF.candidateAllIntro
#eval IO.println "AUDIT_END P01DF.candidateAllIntro"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_all_intro_code"
#check P01DF.candidate_all_intro_code
#ortho_audit P01DF.candidate_all_intro_code
#print axioms P01DF.candidate_all_intro_code
#eval IO.println "AUDIT_END P01DF.candidate_all_intro_code"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_type_instantiation_representation"
#check P01DF.candidate_type_instantiation_representation
#ortho_audit P01DF.candidate_type_instantiation_representation
#print axioms P01DF.candidate_type_instantiation_representation
#eval IO.println "AUDIT_END P01DF.candidate_type_instantiation_representation"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllTm"
#check P01DF.candidateAllTm
#ortho_audit P01DF.candidateAllTm
#print axioms P01DF.candidateAllTm
#eval IO.println "AUDIT_END P01DF.candidateAllTm"
#eval IO.println "AUDIT_BEGIN P01DF.candidateAllElim"
#check P01DF.candidateAllElim
#ortho_audit P01DF.candidateAllElim
#print axioms P01DF.candidateAllElim
#eval IO.println "AUDIT_END P01DF.candidateAllElim"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_all_elim_code"
#check P01DF.candidate_all_elim_code
#ortho_audit P01DF.candidate_all_elim_code
#print axioms P01DF.candidate_all_elim_code
#eval IO.println "AUDIT_END P01DF.candidate_all_elim_code"
#eval IO.println "AUDIT_BEGIN P01DF.candidate_finite_representation"
#check P01DF.candidate_finite_representation
#ortho_audit P01DF.candidate_finite_representation
#print axioms P01DF.candidate_finite_representation
#eval IO.println "AUDIT_END P01DF.candidate_finite_representation"

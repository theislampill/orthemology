import P01DependentModel
import P01DependentSubstitution
import P01DependentFundamental
import P01DependentControls
import P01DependentRepresentation
import IndependentDependentControls
set_option pp.universes true
set_option pp.explicit true
set_option format.width 180
#print P01DF.Ty
#print P01DF.Has
#check @P01DF.IndexRelated
#print axioms P01DF.IndexRelated
#check @P01DF.index_refl
#print axioms P01DF.index_refl
#check @P01DF.index_cons
#print axioms P01DF.index_cons
#check @P01DF.eval_index_related
#print axioms P01DF.eval_index_related
#check @P01DF.rawModel
#print axioms P01DF.rawModel
#check @P01DF.idModel
#print axioms P01DF.idModel
#check @P01DF.idModel_transport
#print axioms P01DF.idModel_transport
#check @P01DF.piModel
#print axioms P01DF.piModel
#check @P01DF.sigmaModel
#print axioms P01DF.sigmaModel
#check @P01DF.IndexFamily
#print axioms P01DF.IndexFamily
#check @P01DF.Ty
#print axioms P01DF.Ty
#check @P01DF.interpret
#print axioms P01DF.interpret
#check @P01DF.interpret_index_transport
#print axioms P01DF.interpret_index_transport
#check @P01DF.dependent_identity_extension
#print axioms P01DF.dependent_identity_extension
#check @P01DF.dependent_endpoint_restriction
#print axioms P01DF.dependent_endpoint_restriction
#check @P01DF.substIndex
#print axioms P01DF.substIndex
#check @P01DF.subIndexEnv
#print axioms P01DF.subIndexEnv
#check @P01DF.subIndexEnv_lift
#print axioms P01DF.subIndexEnv_lift
#check @P01DF.interpret_index_substitution
#print axioms P01DF.interpret_index_substitution
#check @P01DF.instantiate
#print axioms P01DF.instantiate
#check @P01DF.interpret_instantiate
#print axioms P01DF.interpret_instantiate
#check @P01DF.embedFinite
#print axioms P01DF.embedFinite
#check @P01DF.interpret_embedFinite
#print axioms P01DF.interpret_embedFinite
#check @P01DF.renameType
#print axioms P01DF.renameType
#check @P01DF.piModel_congr
#print axioms P01DF.piModel_congr
#check @P01DF.sigmaModel_congr
#print axioms P01DF.sigmaModel_congr
#check @P01DF.piModel_rename
#print axioms P01DF.piModel_rename
#check @P01DF.sigmaModel_rename
#print axioms P01DF.sigmaModel_rename
#check @P01DF.interpret_type_rename
#print axioms P01DF.interpret_type_rename
#check @P01DF.liftTypes
#print axioms P01DF.liftTypes
#check @P01DF.liftIndices
#print axioms P01DF.liftIndices
#check @P01DF.substType
#print axioms P01DF.substType
#check @P01DF.interpret_liftTypes
#print axioms P01DF.interpret_liftTypes
#check @P01DF.interpret_liftIndices
#print axioms P01DF.interpret_liftIndices
#check @P01DF.piModel_substitute
#print axioms P01DF.piModel_substitute
#check @P01DF.sigmaModel_substitute
#print axioms P01DF.sigmaModel_substitute
#check @P01DF.interpret_type_substitution
#print axioms P01DF.interpret_type_substitution
#check @P01DF.instantiateType
#print axioms P01DF.instantiateType
#check @P01DF.interpret_type_instantiate
#print axioms P01DF.interpret_type_instantiate
#check @P01DF.type_instantiate_rel
#print axioms P01DF.type_instantiate_rel
#check @P01DF.type_instantiate_obj
#print axioms P01DF.type_instantiate_obj
#check @P01DF.PolyConv
#print axioms P01DF.PolyConv
#check @P01DF.polyConv_sound
#print axioms P01DF.polyConv_sound
#check @P01DF.motiveAt
#print axioms P01DF.motiveAt
#check @P01DF.interpret_motiveAt
#print axioms P01DF.interpret_motiveAt
#check @P01DF.Has
#print axioms P01DF.Has
#check @P01DF.fundamental
#print axioms P01DF.fundamental
#check @P01DF.unary_soundness
#print axioms P01DF.unary_soundness
#check @P01DF.substitution_fundamental
#print axioms P01DF.substitution_fundamental
#check @P01DF.type_substitution_fundamental
#print axioms P01DF.type_substitution_fundamental
#check @P01DF.dependent_all_fundamental
#print axioms P01DF.dependent_all_fundamental
#check @P01DF.dependent_all_self_instantiation
#print axioms P01DF.dependent_all_self_instantiation
#check @P01DF.skk
#print axioms P01DF.skk
#check @P01DF.emptyIndices
#print axioms P01DF.emptyIndices
#check @P01DF.anchoredIdentity
#print axioms P01DF.anchoredIdentity
#check @P01DF.anchored_identity_inhabited
#print axioms P01DF.anchored_identity_inhabited
#check @P01DF.anchored_identity_empty
#print axioms P01DF.anchored_identity_empty
#check @P01DF.nonconstant_fibres
#print axioms P01DF.nonconstant_fibres
#check @P01DF.heterogeneous_index_transport_fails
#print axioms P01DF.heterogeneous_index_transport_fails
#check @P01DF.totalPER
#print axioms P01DF.totalPER
#check @P01DF.inspectedFibre
#print axioms P01DF.inspectedFibre
#check @P01DF.naivePiRel
#print axioms P01DF.naivePiRel
#check @P01DF.omitted_coherence_breaks_pi_symmetry
#print axioms P01DF.omitted_coherence_breaks_pi_symmetry
#check @P01DF.dependentReflType
#print axioms P01DF.dependentReflType
#check @P01DF.dependent_reflexivity_typed
#print axioms P01DF.dependent_reflexivity_typed
#check @P01DF.dependent_reflexivity_nonempty
#print axioms P01DF.dependent_reflexivity_nonempty
#check @P01DF.dependent_pair_typed
#print axioms P01DF.dependent_pair_typed
#check @P01DF.dependent_pair_nonempty
#print axioms P01DF.dependent_pair_nonempty
#check @P01DF.dependent_pair_projection_typed
#print axioms P01DF.dependent_pair_projection_typed
#check @P01DF.convertedProof
#print axioms P01DF.convertedProof
#check @P01DF.converted_identity_proof_typed
#print axioms P01DF.converted_identity_proof_typed
#check @P01DF.proof_dependent_j_typed
#print axioms P01DF.proof_dependent_j_typed
#check @P01DF.proof_dependent_j_nonempty
#print axioms P01DF.proof_dependent_j_nonempty
#check @P01DF.two_sort_substitution_control
#print axioms P01DF.two_sort_substitution_control
#check @P01DF.dependentPolyBody
#print axioms P01DF.dependentPolyBody
#check @P01DF.dependentPolyType
#print axioms P01DF.dependentPolyType
#check @P01DF.dependent_polymorphic_typed
#print axioms P01DF.dependent_polymorphic_typed
#check @P01DF.dependent_polymorphic_nonempty
#print axioms P01DF.dependent_polymorphic_nonempty
#check @P01DF.dependent_polymorphic_self_typed
#print axioms P01DF.dependent_polymorphic_self_typed
#check @P01DF.raw_index_variable_not_arbitrary_type_parameter
#print axioms P01DF.raw_index_variable_not_arbitrary_type_parameter
#check @P01DF.raw_omega_typed
#print axioms P01DF.raw_omega_typed
#check @P01DF.raw_omega_has_no_normal_reduct
#print axioms P01DF.raw_omega_has_no_normal_reduct
#check @P01DF.indexContext
#print axioms P01DF.indexContext
#check @P01DF.candidateTy
#print axioms P01DF.candidateTy
#check @P01DF.candidateTm
#print axioms P01DF.candidateTm
#check @P01DF.candidateEnvelope
#print axioms P01DF.candidateEnvelope
#check @P01DF.candidate_envelope_code_exact
#print axioms P01DF.candidate_envelope_code_exact
#check @P01DF.candidate_replay_sound
#print axioms P01DF.candidate_replay_sound
#check @P01DF.candidate_ty_ext
#print axioms P01DF.candidate_ty_ext
#check @P01DF.candidateRaw
#print axioms P01DF.candidateRaw
#check @P01DF.candidate_raw_representation
#print axioms P01DF.candidate_raw_representation
#check @P01DF.rawIndexTm
#print axioms P01DF.rawIndexTm
#check @P01DF.candidate_identity_representation
#print axioms P01DF.candidate_identity_representation
#check @P01DF.candidateBinder
#print axioms P01DF.candidateBinder
#check @P01DF.candidateBody
#print axioms P01DF.candidateBody
#check @P01DF.candidate_fibre
#print axioms P01DF.candidate_fibre
#check @P01DF.candidate_pi_representation
#print axioms P01DF.candidate_pi_representation
#check @P01DF.candidate_sigma_representation
#print axioms P01DF.candidate_sigma_representation
#check @P01DF.candidate_lambda_code
#print axioms P01DF.candidate_lambda_code
#check @P01DF.candidateIndexSub
#print axioms P01DF.candidateIndexSub
#check @P01DF.candidate_substitution_representation
#print axioms P01DF.candidate_substitution_representation
#check @P01DF.candidate_substitution_code
#print axioms P01DF.candidate_substitution_code
#check @P01DF.candidateAllBody
#print axioms P01DF.candidateAllBody
#check @P01DF.candidateAllFormation
#print axioms P01DF.candidateAllFormation
#check @P01DF.candidate_all_representation
#print axioms P01DF.candidate_all_representation
#check @P01DF.candidateAllBodyTm
#print axioms P01DF.candidateAllBodyTm
#check @P01DF.candidate_all_uniformity
#print axioms P01DF.candidate_all_uniformity
#check @P01DF.candidateAllIntro
#print axioms P01DF.candidateAllIntro
#check @P01DF.candidate_all_intro_code
#print axioms P01DF.candidate_all_intro_code
#check @P01DF.candidate_type_instantiation_representation
#print axioms P01DF.candidate_type_instantiation_representation
#check @P01DF.candidateAllTm
#print axioms P01DF.candidateAllTm
#check @P01DF.candidateAllElim
#print axioms P01DF.candidateAllElim
#check @P01DF.candidate_all_elim_code
#print axioms P01DF.candidate_all_elim_code
#check @P01DF.candidate_finite_representation
#print axioms P01DF.candidate_finite_representation
#check @IndependentDependentAudit.varyingBody
#print axioms IndependentDependentAudit.varyingBody
#check @IndependentDependentAudit.varying_body_inhabited_everywhere
#print axioms IndependentDependentAudit.varying_body_inhabited_everywhere
#check @IndependentDependentAudit.varying_body_accepts_at_skk
#print axioms IndependentDependentAudit.varying_body_accepts_at_skk
#check @IndependentDependentAudit.varying_body_rejects_at_i
#print axioms IndependentDependentAudit.varying_body_rejects_at_i
#check @IndependentDependentAudit.varying_body_nonconstant
#print axioms IndependentDependentAudit.varying_body_nonconstant
#check @IndependentDependentAudit.varying_pi_typed
#print axioms IndependentDependentAudit.varying_pi_typed
#check @IndependentDependentAudit.varying_pi_nonempty
#print axioms IndependentDependentAudit.varying_pi_nonempty
#check @IndependentDependentAudit.nested_two_sort_capture_control
#print axioms IndependentDependentAudit.nested_two_sort_capture_control
#check @IndependentDependentAudit.nested_index_capture_control
#print axioms IndependentDependentAudit.nested_index_capture_control
#check @IndependentDependentAudit.twiceI
#print axioms IndependentDependentAudit.twiceI
#check @IndependentDependentAudit.thriceI
#print axioms IndependentDependentAudit.thriceI
#check @IndependentDependentAudit.two_coordinate_j_typed
#print axioms IndependentDependentAudit.two_coordinate_j_typed
#check @IndependentDependentAudit.two_coordinate_j_nonempty
#print axioms IndependentDependentAudit.two_coordinate_j_nonempty
#check @IndependentDependentAudit.raw_variable_not_arbitrary_parameter
#print axioms IndependentDependentAudit.raw_variable_not_arbitrary_parameter
#check @IndependentDependentAudit.no_unrestricted_link_index_transport
#print axioms IndependentDependentAudit.no_unrestricted_link_index_transport
#check @IndependentDependentAudit.mixedBody
#print axioms IndependentDependentAudit.mixedBody
#check @IndependentDependentAudit.mixedAll
#print axioms IndependentDependentAudit.mixedAll
#check @IndependentDependentAudit.mixed_all_typed
#print axioms IndependentDependentAudit.mixed_all_typed
#check @IndependentDependentAudit.mixed_all_nonempty
#print axioms IndependentDependentAudit.mixed_all_nonempty
#check @IndependentDependentAudit.mixed_all_self_typed
#print axioms IndependentDependentAudit.mixed_all_self_typed
#check @IndependentDependentAudit.mixed_all_self_nonempty
#print axioms IndependentDependentAudit.mixed_all_self_nonempty

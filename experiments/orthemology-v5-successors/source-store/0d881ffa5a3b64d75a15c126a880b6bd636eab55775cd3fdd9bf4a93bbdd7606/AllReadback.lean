/- Exact public readback and inherited transitive axiom gate. -/
import AuditSupport
import AllBaseLaws
import AllBinderLaws
import AllBoundaryResults
import AllConstants
import AllContextualJ
import AllFiniteComparison
import AllInheritedNegativeControls
import AllInheritedPositiveControls
import AllInstantiation
import AllJoinedControls
import AllLegacyChecks
import AllLegacyComparison
import AllLegacyDerivations
import AllLegacySyntax
import AllMixedAlgebra
import AllMixedRepresentation
import AllNucleus
import AllNucleusSyntax
import AllPiLaws
import AllPredicates
import AllRawRenaming
import AllRawSubstitution
import AllRepresentation
import AllSemanticSubstitution
import AllSigmaLaws
import AllSoundness
import AllStructural
import AllStructuralBase
import AllStructuralChecks
import AllStructuralRename
import AllSyntax
import AllTermAlgebra
import AllTermLemmas

#check P01AC.RelLaws
#print axioms P01AC.RelLaws
#ortho_audit P01AC.RelLaws
#check P01AC.RelLaws.per
#print axioms P01AC.RelLaws.per
#ortho_audit P01AC.RelLaws.per
#check P01AC.RelLaws.left
#print axioms P01AC.RelLaws.left
#ortho_audit P01AC.RelLaws.left
#check P01AC.RelLaws.right
#print axioms P01AC.RelLaws.right
#ortho_audit P01AC.RelLaws.right
#check P01AC.perLaws
#print axioms P01AC.perLaws
#ortho_audit P01AC.perLaws
#check P01AC.ContextLaws
#print axioms P01AC.ContextLaws
#ortho_audit P01AC.ContextLaws
#check P01AC.TypeLaws
#print axioms P01AC.TypeLaws
#ortho_audit P01AC.TypeLaws
#check P01AC.Fundamental
#print axioms P01AC.Fundamental
#ortho_audit P01AC.Fundamental
#check P01AC.TypeLaws.raw
#print axioms P01AC.TypeLaws.raw
#ortho_audit P01AC.TypeLaws.raw
#check P01AC.Fundamental.unary
#print axioms P01AC.Fundamental.unary
#ortho_audit P01AC.Fundamental.unary
#check P01AC.context_nil
#print axioms P01AC.context_nil
#ortho_audit P01AC.context_nil
#check P01AC.context_ext
#print axioms P01AC.context_ext
#ortho_audit P01AC.context_ext
#check P01AC.type_model
#print axioms P01AC.type_model
#ortho_audit P01AC.type_model
#check P01AC.type_param
#print axioms P01AC.type_param
#ortho_audit P01AC.type_param
#check P01AC.type_bottom
#print axioms P01AC.type_bottom
#ortho_audit P01AC.type_bottom
#check P01AC.type_raw
#print axioms P01AC.type_raw
#ortho_audit P01AC.type_raw
#check P01AC.type_identity
#print axioms P01AC.type_identity
#ortho_audit P01AC.type_identity
#check P01AC.Uniform
#print axioms P01AC.Uniform
#ortho_audit P01AC.Uniform
#check P01AC.all_uniform_transport
#print axioms P01AC.all_uniform_transport
#ortho_audit P01AC.all_uniform_transport
#check P01AC.all_per
#print axioms P01AC.all_per
#ortho_audit P01AC.all_per
#check P01AC.all_transport
#print axioms P01AC.all_transport
#ortho_audit P01AC.all_transport
#check P01AC.type_all
#print axioms P01AC.type_all
#ortho_audit P01AC.type_all
#check P01AC.formedObject
#print axioms P01AC.formedObject
#ortho_audit P01AC.formedObject
#check P01AC.formedLink
#print axioms P01AC.formedLink
#ortho_audit P01AC.formedLink
#check P01AC.formedObject_rel
#print axioms P01AC.formedObject_rel
#ortho_audit P01AC.formedObject_rel
#check P01AC.formedLink_rel
#print axioms P01AC.formedLink_rel
#ortho_audit P01AC.formedLink_rel
#check P01AC.context_two_sided_invariance
#print axioms P01AC.context_two_sided_invariance
#ortho_audit P01AC.context_two_sided_invariance
#check P01AC.context_strong_diagonal
#print axioms P01AC.context_strong_diagonal
#ortho_audit P01AC.context_strong_diagonal
#check P01AC.formedFibre
#print axioms P01AC.formedFibre
#ortho_audit P01AC.formedFibre
#check P01AC.formedFibre_coherent
#print axioms P01AC.formedFibre_coherent
#ortho_audit P01AC.formedFibre_coherent
#check P01AC.formed_pi_exact
#print axioms P01AC.formed_pi_exact
#ortho_audit P01AC.formed_pi_exact
#check P01AC.formed_sigma_exact
#print axioms P01AC.formed_sigma_exact
#ortho_audit P01AC.formed_sigma_exact
#check P01AC.formed_identity_exact
#print axioms P01AC.formed_identity_exact
#ortho_audit P01AC.formed_identity_exact
#check P01AC.raw_omega_typed
#print axioms P01AC.raw_omega_typed
#ortho_audit P01AC.raw_omega_typed
#check P01AC.raw_omega_has_no_normal_reduct
#print axioms P01AC.raw_omega_has_no_normal_reduct
#ortho_audit P01AC.raw_omega_has_no_normal_reduct
#check P01AC.formedAllFamily
#print axioms P01AC.formedAllFamily
#ortho_audit P01AC.formedAllFamily
#check P01AC.formed_all_exact
#print axioms P01AC.formed_all_exact
#ortho_audit P01AC.formed_all_exact
#check P01AC.objectOf
#print axioms P01AC.objectOf
#ortho_audit P01AC.objectOf
#check P01AC.linkOf
#print axioms P01AC.linkOf
#ortho_audit P01AC.linkOf
#check P01AC.F_arr
#print axioms P01AC.F_arr
#ortho_audit P01AC.F_arr
#check P01AC.G_arr
#print axioms P01AC.G_arr
#ortho_audit P01AC.G_arr
#check P01AC.fundamental_i
#print axioms P01AC.fundamental_i
#ortho_audit P01AC.fundamental_i
#check P01AC.fundamental_k
#print axioms P01AC.fundamental_k
#ortho_audit P01AC.fundamental_k
#check P01AC.fundamental_s
#print axioms P01AC.fundamental_s
#ortho_audit P01AC.fundamental_s
#check P01AC.contextual_related
#print axioms P01AC.contextual_related
#ortho_audit P01AC.contextual_related
#check P01AC.contextual_valid
#print axioms P01AC.contextual_valid
#ortho_audit P01AC.contextual_valid
#check P01AC.contextualMotive
#print axioms P01AC.contextualMotive
#ortho_audit P01AC.contextualMotive
#check P01AC.contextualProof
#print axioms P01AC.contextualProof
#ortho_audit P01AC.contextualProof
#check P01AC.contextualBase
#print axioms P01AC.contextualBase
#ortho_audit P01AC.contextualBase
#check P01AC.representedContextualJ
#print axioms P01AC.representedContextualJ
#ortho_audit P01AC.representedContextualJ
#check P01AC.representedContextualJ_code
#print axioms P01AC.representedContextualJ_code
#ortho_audit P01AC.representedContextualJ_code
#check P01AC.contextual_target_exact
#print axioms P01AC.contextual_target_exact
#ortho_audit P01AC.contextual_target_exact
#check P01AC.FG_fin
#print axioms P01AC.FG_fin
#ortho_audit P01AC.FG_fin
#check P01AC.F_fin
#print axioms P01AC.F_fin
#ortho_audit P01AC.F_fin
#check P01AC.G_fin
#print axioms P01AC.G_fin
#ortho_audit P01AC.G_fin
#check P01AC.Negative.totalRaw
#print axioms P01AC.Negative.totalRaw
#ortho_audit P01AC.Negative.totalRaw
#check P01AC.Negative.rawTotal
#print axioms P01AC.Negative.rawTotal
#ortho_audit P01AC.Negative.rawTotal
#check P01AC.Negative.rightSeparating
#print axioms P01AC.Negative.rightSeparating
#ortho_audit P01AC.Negative.rightSeparating
#check P01AC.Negative.leftSeparating
#print axioms P01AC.Negative.leftSeparating
#ortho_audit P01AC.Negative.leftSeparating
#check P01AC.Negative.pairContext
#print axioms P01AC.Negative.pairContext
#ortho_audit P01AC.Negative.pairContext
#check P01AC.Negative.equalEnv
#print axioms P01AC.Negative.equalEnv
#ortho_audit P01AC.Negative.equalEnv
#check P01AC.Negative.splitEnv
#print axioms P01AC.Negative.splitEnv
#ortho_audit P01AC.Negative.splitEnv
#check P01AC.Negative.equalityTest
#print axioms P01AC.Negative.equalityTest
#ortho_audit P01AC.Negative.equalityTest
#check P01AC.Negative.pair_context_formed
#print axioms P01AC.Negative.pair_context_formed
#ortho_audit P01AC.Negative.pair_context_formed
#check P01AC.Negative.equality_test_formed
#print axioms P01AC.Negative.equality_test_formed
#ortho_audit P01AC.Negative.equality_test_formed
#check P01AC.Negative.right_cross_links_without_equality
#print axioms P01AC.Negative.right_cross_links_without_equality
#ortho_audit P01AC.Negative.right_cross_links_without_equality
#check P01AC.Negative.left_cross_links_without_equality
#print axioms P01AC.Negative.left_cross_links_without_equality
#ortho_audit P01AC.Negative.left_cross_links_without_equality
#check P01AC.Negative.no_universal_raw_variable
#print axioms P01AC.Negative.no_universal_raw_variable
#ortho_audit P01AC.Negative.no_universal_raw_variable
#check P01AC.Negative.j_transport_requires_both_coordinates
#print axioms P01AC.Negative.j_transport_requires_both_coordinates
#ortho_audit P01AC.Negative.j_transport_requires_both_coordinates
#check P01AC.Negative.j_endpoint_omission_fails
#print axioms P01AC.Negative.j_endpoint_omission_fails
#ortho_audit P01AC.Negative.j_endpoint_omission_fails
#check P01AC.Negative.j_proof_coordinate_omission_fails
#print axioms P01AC.Negative.j_proof_coordinate_omission_fails
#ortho_audit P01AC.Negative.j_proof_coordinate_omission_fails
#check P01AC.Negative.conversion_scope_premise_necessary
#print axioms P01AC.Negative.conversion_scope_premise_necessary
#ortho_audit P01AC.Negative.conversion_scope_premise_necessary
#check P01AC.alpha
#print axioms P01AC.alpha
#ortho_audit P01AC.alpha
#check P01AC.typedPair
#print axioms P01AC.typedPair
#ortho_audit P01AC.typedPair
#check P01AC.typedPairType
#print axioms P01AC.typedPairType
#ortho_audit P01AC.typedPairType
#check P01AC.typed_pair_form
#print axioms P01AC.typed_pair_form
#ortho_audit P01AC.typed_pair_form
#check P01AC.typed_pair_has
#print axioms P01AC.typed_pair_has
#ortho_audit P01AC.typed_pair_has
#check P01AC.typed_pair_abstraction_form
#print axioms P01AC.typed_pair_abstraction_form
#ortho_audit P01AC.typed_pair_abstraction_form
#check P01AC.typed_pair_abstraction_has
#print axioms P01AC.typed_pair_abstraction_has
#ortho_audit P01AC.typed_pair_abstraction_has
#check P01AC.typed_pair_related
#print axioms P01AC.typed_pair_related
#ortho_audit P01AC.typed_pair_related
#check P01AC.typed_pair_abstraction_related
#print axioms P01AC.typed_pair_abstraction_related
#ortho_audit P01AC.typed_pair_abstraction_related
#check P01AC.jContext
#print axioms P01AC.jContext
#ortho_audit P01AC.jContext
#check P01AC.jProofType
#print axioms P01AC.jProofType
#ortho_audit P01AC.jProofType
#check P01AC.jMotive
#print axioms P01AC.jMotive
#ortho_audit P01AC.jMotive
#check P01AC.jBaseType
#print axioms P01AC.jBaseType
#ortho_audit P01AC.jBaseType
#check P01AC.jTargetType
#print axioms P01AC.jTargetType
#ortho_audit P01AC.jTargetType
#check P01AC.jBase
#print axioms P01AC.jBase
#ortho_audit P01AC.jBase
#check P01AC.literalJ
#print axioms P01AC.literalJ
#ortho_audit P01AC.literalJ
#check P01AC.j_context_formed
#print axioms P01AC.j_context_formed
#ortho_audit P01AC.j_context_formed
#check P01AC.j_x_has
#print axioms P01AC.j_x_has
#ortho_audit P01AC.j_x_has
#check P01AC.j_y_has
#print axioms P01AC.j_y_has
#ortho_audit P01AC.j_y_has
#check P01AC.j_proof_form
#print axioms P01AC.j_proof_form
#ortho_audit P01AC.j_proof_form
#check P01AC.j_e_has
#print axioms P01AC.j_e_has
#ortho_audit P01AC.j_e_has
#check P01AC.j_motive_form
#print axioms P01AC.j_motive_form
#ortho_audit P01AC.j_motive_form
#check P01AC.j_motive_base_exact
#print axioms P01AC.j_motive_base_exact
#ortho_audit P01AC.j_motive_base_exact
#check P01AC.j_motive_target_exact
#print axioms P01AC.j_motive_target_exact
#ortho_audit P01AC.j_motive_target_exact
#check P01AC.j_base_form
#print axioms P01AC.j_base_form
#ortho_audit P01AC.j_base_form
#check P01AC.j_target_form
#print axioms P01AC.j_target_form
#ortho_audit P01AC.j_target_form
#check P01AC.j_base_has
#print axioms P01AC.j_base_has
#ortho_audit P01AC.j_base_has
#check P01AC.literal_j_has
#print axioms P01AC.literal_j_has
#ortho_audit P01AC.literal_j_has
#check P01AC.literal_j_related
#print axioms P01AC.literal_j_related
#ortho_audit P01AC.literal_j_related
#check P01AC.rawFibreType
#print axioms P01AC.rawFibreType
#ortho_audit P01AC.rawFibreType
#check P01AC.raw_fibre_form
#print axioms P01AC.raw_fibre_form
#ortho_audit P01AC.raw_fibre_form
#check P01AC.raw_fibre_pair_has
#print axioms P01AC.raw_fibre_pair_has
#ortho_audit P01AC.raw_fibre_pair_has
#check P01AC.raw_fibre_inhabited
#print axioms P01AC.raw_fibre_inhabited
#ortho_audit P01AC.raw_fibre_inhabited
#check P01AC.raw_fibres_nonempty_and_vary
#print axioms P01AC.raw_fibres_nonempty_and_vary
#ortho_audit P01AC.raw_fibres_nonempty_and_vary
#check P01AC.identityParameters
#print axioms P01AC.identityParameters
#ortho_audit P01AC.identityParameters
#check P01AC.identity_parameters_I_SKK
#print axioms P01AC.identity_parameters_I_SKK
#ortho_audit P01AC.identity_parameters_I_SKK
#check P01AC.concreteJEnv
#print axioms P01AC.concreteJEnv
#ortho_audit P01AC.concreteJEnv
#check P01AC.concrete_j_environment_related
#print axioms P01AC.concrete_j_environment_related
#ortho_audit P01AC.concrete_j_environment_related
#check P01AC.concrete_j_nonraw_proof_control
#print axioms P01AC.concrete_j_nonraw_proof_control
#ortho_audit P01AC.concrete_j_nonraw_proof_control
#check P01AC.typed_pair_I_SKK_related
#print axioms P01AC.typed_pair_I_SKK_related
#ortho_audit P01AC.typed_pair_I_SKK_related
#check P01AC.typed_pair_I_SKK_control
#print axioms P01AC.typed_pair_I_SKK_control
#ortho_audit P01AC.typed_pair_I_SKK_control
#check P01AC.mandatory_raw_family_obstruction_unchanged
#print axioms P01AC.mandatory_raw_family_obstruction_unchanged
#ortho_audit P01AC.mandatory_raw_family_obstruction_unchanged
#check P01AC.imageEnv
#print axioms P01AC.imageEnv
#ortho_audit P01AC.imageEnv
#check P01AC.imageEnv_match
#print axioms P01AC.imageEnv_match
#ortho_audit P01AC.imageEnv_match
#check P01AC.semantic_tsubst
#print axioms P01AC.semantic_tsubst
#ortho_audit P01AC.semantic_tsubst
#check P01AC.top_image_match
#print axioms P01AC.top_image_match
#ortho_audit P01AC.top_image_match
#check P01AC.G_tinst
#print axioms P01AC.G_tinst
#ortho_audit P01AC.G_tinst
#check P01AC.F_tinst
#print axioms P01AC.F_tinst
#ortho_audit P01AC.F_tinst
#check P01AC.fundamental_all_intro
#print axioms P01AC.fundamental_all_intro
#ortho_audit P01AC.fundamental_all_intro
#check P01AC.fundamental_all_elim
#print axioms P01AC.fundamental_all_elim
#ortho_audit P01AC.fundamental_all_elim
#check P01AC.typeImages_beyond
#print axioms P01AC.typeImages_beyond
#ortho_audit P01AC.typeImages_beyond
#check P01AC.finite_image_laws
#print axioms P01AC.finite_image_laws
#ortho_audit P01AC.finite_image_laws
#check P01AC.fundamental_finite
#print axioms P01AC.fundamental_finite
#ortho_audit P01AC.fundamental_finite
#check P01AC.Qbody
#print axioms P01AC.Qbody
#ortho_audit P01AC.Qbody
#check P01AC.Q
#print axioms P01AC.Q
#ortho_audit P01AC.Q
#check P01AC.q
#print axioms P01AC.q
#ortho_audit P01AC.q
#check P01AC.Qbody_form
#print axioms P01AC.Qbody_form
#ortho_audit P01AC.Qbody_form
#check P01AC.q_body_has
#print axioms P01AC.q_body_has
#ortho_audit P01AC.q_body_has
#check P01AC.Q_form
#print axioms P01AC.Q_form
#ortho_audit P01AC.Q_form
#check P01AC.q_has_Q
#print axioms P01AC.q_has_Q
#ortho_audit P01AC.q_has_Q
#check P01AC.Q_self_exact
#print axioms P01AC.Q_self_exact
#ortho_audit P01AC.Q_self_exact
#check P01AC.q_self_has
#print axioms P01AC.q_self_has
#ortho_audit P01AC.q_self_has
#check P01AC.q_self_fundamental
#print axioms P01AC.q_self_fundamental
#ortho_audit P01AC.q_self_fundamental
#check P01AC.polyIdentity
#print axioms P01AC.polyIdentity
#ortho_audit P01AC.polyIdentity
#check P01AC.polyIdentity_form
#print axioms P01AC.polyIdentity_form
#ortho_audit P01AC.polyIdentity_form
#check P01AC.polyIdentity_has
#print axioms P01AC.polyIdentity_has
#ortho_audit P01AC.polyIdentity_has
#check P01AC.polyIdentity_instance_exact
#print axioms P01AC.polyIdentity_instance_exact
#ortho_audit P01AC.polyIdentity_instance_exact
#check P01AC.polymorphic_identity_at
#print axioms P01AC.polymorphic_identity_at
#ortho_audit P01AC.polymorphic_identity_at
#check P01AC.openIdentityReplacement
#print axioms P01AC.openIdentityReplacement
#ortho_audit P01AC.openIdentityReplacement
#check P01AC.open_identity_replacement_form
#print axioms P01AC.open_identity_replacement_form
#ortho_audit P01AC.open_identity_replacement_form
#check P01AC.open_identity_replacement_instance
#print axioms P01AC.open_identity_replacement_instance
#ortho_audit P01AC.open_identity_replacement_instance
#check P01AC.open_sigma_replacement_instance
#print axioms P01AC.open_sigma_replacement_instance
#ortho_audit P01AC.open_sigma_replacement_instance
#check P01AC.open_sigma_replacement_nonempty
#print axioms P01AC.open_sigma_replacement_nonempty
#ortho_audit P01AC.open_sigma_replacement_nonempty
#check P01AC.open_sigma_replacement_heterogeneous
#print axioms P01AC.open_sigma_replacement_heterogeneous
#ortho_audit P01AC.open_sigma_replacement_heterogeneous
#check P01AC.open_sigma_nested_capture
#print axioms P01AC.open_sigma_nested_capture
#ortho_audit P01AC.open_sigma_nested_capture
#check P01AC.open_raw_sigma_instance
#print axioms P01AC.open_raw_sigma_instance
#ortho_audit P01AC.open_raw_sigma_instance
#check P01AC.open_raw_sigma_nonempty_vary
#print axioms P01AC.open_raw_sigma_nonempty_vary
#ortho_audit P01AC.open_raw_sigma_nonempty_vary
#check P01AC.Legacy.dependent_type_readback
#print axioms P01AC.Legacy.dependent_type_readback
#ortho_audit P01AC.Legacy.dependent_type_readback
#check P01AC.Legacy.open_replacement_embedding
#print axioms P01AC.Legacy.open_replacement_embedding
#ortho_audit P01AC.Legacy.open_replacement_embedding
#check P01AC.Legacy.hiddenOpenReplacementTree
#print axioms P01AC.Legacy.hiddenOpenReplacementTree
#ortho_audit P01AC.Legacy.hiddenOpenReplacementTree
#check P01AC.Legacy.hidden_replacement_old_judgment
#print axioms P01AC.Legacy.hidden_replacement_old_judgment
#ortho_audit P01AC.Legacy.hidden_replacement_old_judgment
#check P01AC.Legacy.hidden_replacement_closed
#print axioms P01AC.Legacy.hidden_replacement_closed
#ortho_audit P01AC.Legacy.hidden_replacement_closed
#check P01AC.Legacy.hidden_replacement_not_supported
#print axioms P01AC.Legacy.hidden_replacement_not_supported
#ortho_audit P01AC.Legacy.hidden_replacement_not_supported
#check P01AC.Legacy.hiddenOpenPremiseTree
#print axioms P01AC.Legacy.hiddenOpenPremiseTree
#ortho_audit P01AC.Legacy.hiddenOpenPremiseTree
#check P01AC.Legacy.hidden_premise_not_supported
#print axioms P01AC.Legacy.hidden_premise_not_supported
#ortho_audit P01AC.Legacy.hidden_premise_not_supported
#check P01AC.Legacy.conversionInternalTree
#print axioms P01AC.Legacy.conversionInternalTree
#ortho_audit P01AC.Legacy.conversionInternalTree
#check P01AC.Legacy.conversion_internal_supported
#print axioms P01AC.Legacy.conversion_internal_supported
#ortho_audit P01AC.Legacy.conversion_internal_supported
#check P01AC.Legacy.conversion_internal_embedding
#print axioms P01AC.Legacy.conversion_internal_embedding
#ortho_audit P01AC.Legacy.conversion_internal_embedding
#check P01AC.Legacy.nucleus_still_excludes_all_intro
#print axioms P01AC.Legacy.nucleus_still_excludes_all_intro
#ortho_audit P01AC.Legacy.nucleus_still_excludes_all_intro
#check P01AC.Legacy.nucleus_still_excludes_dependent_type
#print axioms P01AC.Legacy.nucleus_still_excludes_dependent_type
#ortho_audit P01AC.Legacy.nucleus_still_excludes_dependent_type
#check P01AC.Legacy.FG_agrees
#print axioms P01AC.Legacy.FG_agrees
#ortho_audit P01AC.Legacy.FG_agrees
#check P01AC.Legacy.F_agrees
#print axioms P01AC.Legacy.F_agrees
#ortho_audit P01AC.Legacy.F_agrees
#check P01AC.Legacy.G_agrees
#print axioms P01AC.Legacy.G_agrees
#ortho_audit P01AC.Legacy.G_agrees
#check P01AC.Legacy.Supported.object_agrees
#print axioms P01AC.Legacy.Supported.object_agrees
#ortho_audit P01AC.Legacy.Supported.object_agrees
#check P01AC.Legacy.Supported.heterogeneous_agrees
#print axioms P01AC.Legacy.Supported.heterogeneous_agrees
#ortho_audit P01AC.Legacy.Supported.heterogeneous_agrees
#check P01AC.Legacy.Supported
#print axioms P01AC.Legacy.Supported
#ortho_audit P01AC.Legacy.Supported
#check P01AC.Legacy.Supported.scoped
#print axioms P01AC.Legacy.Supported.scoped
#ortho_audit P01AC.Legacy.Supported.scoped
#check P01AC.Legacy.Supported.type
#print axioms P01AC.Legacy.Supported.type
#ortho_audit P01AC.Legacy.Supported.type
#check P01AC.Legacy.Supported.formed
#print axioms P01AC.Legacy.Supported.formed
#ortho_audit P01AC.Legacy.Supported.formed
#check P01AC.Legacy.supported_embed
#print axioms P01AC.Legacy.supported_embed
#ortho_audit P01AC.Legacy.supported_embed
#check P01AC.Legacy.Supported.embed
#print axioms P01AC.Legacy.Supported.embed
#ortho_audit P01AC.Legacy.Supported.embed
#check P01AC.Legacy.Supported.raw_embed
#print axioms P01AC.Legacy.Supported.raw_embed
#ortho_audit P01AC.Legacy.Supported.raw_embed
#check P01AC.Legacy.Supported.old_judgment
#print axioms P01AC.Legacy.Supported.old_judgment
#ortho_audit P01AC.Legacy.Supported.old_judgment
#check P01AC.Legacy.identityTree
#print axioms P01AC.Legacy.identityTree
#ortho_audit P01AC.Legacy.identityTree
#check P01AC.Legacy.identityTree_supported
#print axioms P01AC.Legacy.identityTree_supported
#ortho_audit P01AC.Legacy.identityTree_supported
#check P01AC.Legacy.openIdentityInstance
#print axioms P01AC.Legacy.openIdentityInstance
#ortho_audit P01AC.Legacy.openIdentityInstance
#check P01AC.Legacy.openIdentityInstance_supported
#print axioms P01AC.Legacy.openIdentityInstance_supported
#ortho_audit P01AC.Legacy.openIdentityInstance_supported
#check P01AC.Legacy.dependentTree
#print axioms P01AC.Legacy.dependentTree
#ortho_audit P01AC.Legacy.dependentTree
#check P01AC.Legacy.dependentTree_supported
#print axioms P01AC.Legacy.dependentTree_supported
#ortho_audit P01AC.Legacy.dependentTree_supported
#check P01AC.Legacy.dependent_polymorphic_typed
#print axioms P01AC.Legacy.dependent_polymorphic_typed
#ortho_audit P01AC.Legacy.dependent_polymorphic_typed
#check P01AC.Legacy.dependentSelfTree
#print axioms P01AC.Legacy.dependentSelfTree
#ortho_audit P01AC.Legacy.dependentSelfTree
#check P01AC.Legacy.dependentSelfTree_supported
#print axioms P01AC.Legacy.dependentSelfTree_supported
#ortho_audit P01AC.Legacy.dependentSelfTree_supported
#check P01AC.Legacy.dependent_polymorphic_self_typed
#print axioms P01AC.Legacy.dependent_polymorphic_self_typed
#ortho_audit P01AC.Legacy.dependent_polymorphic_self_typed
#check P01AC.Legacy.Derivation
#print axioms P01AC.Legacy.Derivation
#ortho_audit P01AC.Legacy.Derivation
#check P01AC.Legacy.erase
#print axioms P01AC.Legacy.erase
#ortho_audit P01AC.Legacy.erase
#check P01AC.Legacy.translate
#print axioms P01AC.Legacy.translate
#ortho_audit P01AC.Legacy.translate
#check P01AC.Legacy.TypeSupported
#print axioms P01AC.Legacy.TypeSupported
#ortho_audit P01AC.Legacy.TypeSupported
#check P01AC.Legacy.translate_index
#print axioms P01AC.Legacy.translate_index
#ortho_audit P01AC.Legacy.translate_index
#check P01AC.Legacy.translate_inst
#print axioms P01AC.Legacy.translate_inst
#ortho_audit P01AC.Legacy.translate_inst
#check P01AC.Legacy.translate_motiveAt
#print axioms P01AC.Legacy.translate_motiveAt
#ortho_audit P01AC.Legacy.translate_motiveAt
#check P01AC.Legacy.translate_rename
#print axioms P01AC.Legacy.translate_rename
#ortho_audit P01AC.Legacy.translate_rename
#check P01AC.Legacy.translate_liftTypes
#print axioms P01AC.Legacy.translate_liftTypes
#ortho_audit P01AC.Legacy.translate_liftTypes
#check P01AC.Legacy.translate_liftIndices
#print axioms P01AC.Legacy.translate_liftIndices
#ortho_audit P01AC.Legacy.translate_liftIndices
#check P01AC.Legacy.translate_typeSubst
#print axioms P01AC.Legacy.translate_typeSubst
#ortho_audit P01AC.Legacy.translate_typeSubst
#check P01AC.Legacy.translate_tinst
#print axioms P01AC.Legacy.translate_tinst
#ortho_audit P01AC.Legacy.translate_tinst
#check P01AC.Legacy.translate_finite
#print axioms P01AC.Legacy.translate_finite
#ortho_audit P01AC.Legacy.translate_finite
#check P01AC.Legacy.RawContext
#print axioms P01AC.Legacy.RawContext
#ortho_audit P01AC.Legacy.RawContext
#check P01AC.Legacy.rawTel
#print axioms P01AC.Legacy.rawTel
#ortho_audit P01AC.Legacy.rawTel
#check P01AC.Legacy.rawTel_length
#print axioms P01AC.Legacy.rawTel_length
#ortho_audit P01AC.Legacy.rawTel_length
#check P01AC.Legacy.rawTel_twk
#print axioms P01AC.Legacy.rawTel_twk
#ortho_audit P01AC.Legacy.rawTel_twk
#check P01AC.Legacy.RawContext.ext
#print axioms P01AC.Legacy.RawContext.ext
#ortho_audit P01AC.Legacy.RawContext.ext
#check P01AC.Legacy.RawContext.twk
#print axioms P01AC.Legacy.RawContext.twk
#ortho_audit P01AC.Legacy.RawContext.twk
#check P01AC.Legacy.rawTel_context
#print axioms P01AC.Legacy.rawTel_context
#ortho_audit P01AC.Legacy.rawTel_context
#check P01AC.Legacy.raw_term
#print axioms P01AC.Legacy.raw_term
#ortho_audit P01AC.Legacy.raw_term
#check P01AC.Legacy.RawContext.theta
#print axioms P01AC.Legacy.RawContext.theta
#ortho_audit P01AC.Legacy.RawContext.theta
#check P01AC.Legacy.TypeSupported.form
#print axioms P01AC.Legacy.TypeSupported.form
#ortho_audit P01AC.Legacy.TypeSupported.form
#check P01AC.Legacy.rawTel_lookup_type
#print axioms P01AC.Legacy.rawTel_lookup_type
#ortho_audit P01AC.Legacy.rawTel_lookup_type
#check P01AC.Legacy.RawContext.identitySubstitution
#print axioms P01AC.Legacy.RawContext.identitySubstitution
#ortho_audit P01AC.Legacy.RawContext.identitySubstitution
#check P01AC.Legacy.RawContext.finiteIdentitySubstitution
#print axioms P01AC.Legacy.RawContext.finiteIdentitySubstitution
#ortho_audit P01AC.Legacy.RawContext.finiteIdentitySubstitution
#check P01AC.Legacy.RawContext.transport_form
#print axioms P01AC.Legacy.RawContext.transport_form
#ortho_audit P01AC.Legacy.RawContext.transport_form
#check P01AC.Legacy.TypeSupported.theta_form
#print axioms P01AC.Legacy.TypeSupported.theta_form
#ortho_audit P01AC.Legacy.TypeSupported.theta_form
#check P01AC.trename_id
#print axioms P01AC.trename_id
#ortho_audit P01AC.trename_id
#check P01AC.trename_comp
#print axioms P01AC.trename_comp
#ortho_audit P01AC.trename_comp
#check P01AC.subst_trename
#print axioms P01AC.subst_trename
#ortho_audit P01AC.subst_trename
#check P01AC.trename_wk
#print axioms P01AC.trename_wk
#ortho_audit P01AC.trename_wk
#check P01AC.subst_twk
#print axioms P01AC.subst_twk
#ortho_audit P01AC.subst_twk
#check P01AC.twk_wk
#print axioms P01AC.twk_wk
#ortho_audit P01AC.twk_wk
#check P01AC.trename_twk
#print axioms P01AC.trename_twk
#ortho_audit P01AC.trename_twk
#check P01AC.tup_wk
#print axioms P01AC.tup_wk
#ortho_audit P01AC.tup_wk
#check P01AC.tup_subst
#print axioms P01AC.tup_subst
#ortho_audit P01AC.tup_subst
#check P01AC.tup_param
#print axioms P01AC.tup_param
#ortho_audit P01AC.tup_param
#check P01AC.mixed_param
#print axioms P01AC.mixed_param
#ortho_audit P01AC.mixed_param
#check P01AC.mixed_id
#print axioms P01AC.mixed_id
#ortho_audit P01AC.mixed_id
#check P01AC.mixed_trename
#print axioms P01AC.mixed_trename
#ortho_audit P01AC.mixed_trename
#check P01AC.trename_mixed
#print axioms P01AC.trename_mixed
#ortho_audit P01AC.trename_mixed
#check P01AC.mixed_subst
#print axioms P01AC.mixed_subst
#ortho_audit P01AC.mixed_subst
#check P01AC.subst_mixed
#print axioms P01AC.subst_mixed
#ortho_audit P01AC.subst_mixed
#check P01AC.mixed_wk
#print axioms P01AC.mixed_wk
#ortho_audit P01AC.mixed_wk
#check P01AC.mixed_twk
#print axioms P01AC.mixed_twk
#ortho_audit P01AC.mixed_twk
#check P01AC.mixed_term_lift_comp
#print axioms P01AC.mixed_term_lift_comp
#ortho_audit P01AC.mixed_term_lift_comp
#check P01AC.mixed_type_lift_comp
#print axioms P01AC.mixed_type_lift_comp
#ortho_audit P01AC.mixed_type_lift_comp
#check P01AC.mixed_comp
#print axioms P01AC.mixed_comp
#ortho_audit P01AC.mixed_comp
#check P01AC.tsubst_id
#print axioms P01AC.tsubst_id
#ortho_audit P01AC.tsubst_id
#check P01AC.tsubst_comp
#print axioms P01AC.tsubst_comp
#ortho_audit P01AC.tsubst_comp
#check P01AC.subst_tsubst
#print axioms P01AC.subst_tsubst
#ortho_audit P01AC.subst_tsubst
#check P01AC.tinst_twk
#print axioms P01AC.tinst_twk
#ortho_audit P01AC.tinst_twk
#check P01AC.mixed_twk_cancel
#print axioms P01AC.mixed_twk_cancel
#ortho_audit P01AC.mixed_twk_cancel
#check P01AC.mixed_wk_wk
#print axioms P01AC.mixed_wk_wk
#ortho_audit P01AC.mixed_wk_wk
#check P01AC.tup_wk_wk
#print axioms P01AC.tup_wk_wk
#ortho_audit P01AC.tup_wk_wk
#check P01AC.mixed_inst
#print axioms P01AC.mixed_inst
#ortho_audit P01AC.mixed_inst
#check P01AC.mixed_motiveAt
#print axioms P01AC.mixed_motiveAt
#ortho_audit P01AC.mixed_motiveAt
#check P01AC.mixed_arr
#print axioms P01AC.mixed_arr
#ortho_audit P01AC.mixed_arr
#check P01AC.mixed_tsubst
#print axioms P01AC.mixed_tsubst
#ortho_audit P01AC.mixed_tsubst
#check P01AC.mixed_tinst
#print axioms P01AC.mixed_tinst
#ortho_audit P01AC.mixed_tinst
#check P01AC.subst_tinst
#print axioms P01AC.subst_tinst
#ortho_audit P01AC.subst_tinst
#check P01AC.trename_inst
#print axioms P01AC.trename_inst
#ortho_audit P01AC.trename_inst
#check P01AC.trename_motiveAt
#print axioms P01AC.trename_motiveAt
#ortho_audit P01AC.trename_motiveAt
#check P01AC.trename_arr
#print axioms P01AC.trename_arr
#ortho_audit P01AC.trename_arr
#check P01AC.trename_tinst
#print axioms P01AC.trename_tinst
#ortho_audit P01AC.trename_tinst
#check P01AC.tsubst_wk
#print axioms P01AC.tsubst_wk
#ortho_audit P01AC.tsubst_wk
#check P01AC.tinst_wk
#print axioms P01AC.tinst_wk
#ortho_audit P01AC.tinst_wk
#check P01AC.mixed_term_type_lifts
#print axioms P01AC.mixed_term_type_lifts
#ortho_audit P01AC.mixed_term_type_lifts
#check P01AC.mixed_double_term_type_lifts
#print axioms P01AC.mixed_double_term_type_lifts
#ortho_audit P01AC.mixed_double_term_type_lifts
#check P01AC.mixed_twk_wk
#print axioms P01AC.mixed_twk_wk
#ortho_audit P01AC.mixed_twk_wk
#check P01AC.tsubst_trename
#print axioms P01AC.tsubst_trename
#ortho_audit P01AC.tsubst_trename
#check P01AC.trename_tsubst
#print axioms P01AC.trename_tsubst
#ortho_audit P01AC.trename_tsubst
#check P01AC.tsubst_twk
#print axioms P01AC.tsubst_twk
#ortho_audit P01AC.tsubst_twk
#check P01AC.tsubst_arr
#print axioms P01AC.tsubst_arr
#ortho_audit P01AC.tsubst_arr
#check P01AC.tyScoped_trename
#print axioms P01AC.tyScoped_trename
#ortho_audit P01AC.tyScoped_trename
#check P01AC.tyScoped_twk
#print axioms P01AC.tyScoped_twk
#ortho_audit P01AC.tyScoped_twk
#check P01AC.tyScoped_tup
#print axioms P01AC.tyScoped_tup
#ortho_audit P01AC.tyScoped_tup
#check P01AC.tyScoped_mixed
#print axioms P01AC.tyScoped_mixed
#ortho_audit P01AC.tyScoped_mixed
#check P01AC.capture_both_sorts
#print axioms P01AC.capture_both_sorts
#ortho_audit P01AC.capture_both_sorts
#check P01AC.capture_term_under_all_pi
#print axioms P01AC.capture_term_under_all_pi
#ortho_audit P01AC.capture_term_under_all_pi
#check P01AC.capture_both_sorts_double_term
#print axioms P01AC.capture_both_sorts_double_term
#ortho_audit P01AC.capture_both_sorts_double_term
#check P01AC.capture_term_then_type
#print axioms P01AC.capture_term_then_type
#ortho_audit P01AC.capture_term_then_type
#check P01AC.capture_bound_type_retained
#print axioms P01AC.capture_bound_type_retained
#ortho_audit P01AC.capture_bound_type_retained
#check P01AC.capture_term_not_zero
#print axioms P01AC.capture_term_not_zero
#ortho_audit P01AC.capture_term_not_zero
#check P01AC.capture_type_not_zero
#print axioms P01AC.capture_type_not_zero
#ortho_audit P01AC.capture_type_not_zero
#check P01AC.MixedTerms.related
#print axioms P01AC.MixedTerms.related
#ortho_audit P01AC.MixedTerms.related
#check P01AC.imageEnv_diagonal
#print axioms P01AC.imageEnv_diagonal
#ortho_audit P01AC.imageEnv_diagonal
#check P01AC.jointContext
#print axioms P01AC.jointContext
#ortho_audit P01AC.jointContext
#check P01AC.jointType
#print axioms P01AC.jointType
#ortho_audit P01AC.jointType
#check P01AC.jointTerm
#print axioms P01AC.jointTerm
#ortho_audit P01AC.jointTerm
#check P01AC.jointTerm_code
#print axioms P01AC.jointTerm_code
#ortho_audit P01AC.jointTerm_code
#check P01AC.MixedSub.imageObjects
#print axioms P01AC.MixedSub.imageObjects
#ortho_audit P01AC.MixedSub.imageObjects
#check P01AC.MixedSub.imageObjects_equal
#print axioms P01AC.MixedSub.imageObjects_equal
#ortho_audit P01AC.MixedSub.imageObjects_equal
#check P01AC.MixedSub.respects
#print axioms P01AC.MixedSub.respects
#ortho_audit P01AC.MixedSub.respects
#check P01AC.MixedSub.valid
#print axioms P01AC.MixedSub.valid
#ortho_audit P01AC.MixedSub.valid
#check P01AC.representedMixedSub
#print axioms P01AC.representedMixedSub
#ortho_audit P01AC.representedMixedSub
#check P01AC.represented_mixed_code
#print axioms P01AC.represented_mixed_code
#ortho_audit P01AC.represented_mixed_code
#check P01AC.represented_mixed_type
#print axioms P01AC.represented_mixed_type
#ortho_audit P01AC.represented_mixed_type
#check P01AC.Nucleus.form
#print axioms P01AC.Nucleus.form
#ortho_audit P01AC.Nucleus.form
#check P01AC.Nucleus.has
#print axioms P01AC.Nucleus.has
#ortho_audit P01AC.Nucleus.has
#check P01AC.Nucleus.context
#print axioms P01AC.Nucleus.context
#ortho_audit P01AC.Nucleus.context
#check P01AC.Nucleus.F_agrees
#print axioms P01AC.Nucleus.F_agrees
#ortho_audit P01AC.Nucleus.F_agrees
#check P01AC.Nucleus.G_agrees
#print axioms P01AC.Nucleus.G_agrees
#ortho_audit P01AC.Nucleus.G_agrees
#check P01AC.Nucleus.D_agrees
#print axioms P01AC.Nucleus.D_agrees
#ortho_audit P01AC.Nucleus.D_agrees
#check P01AC.Nucleus.E_agrees
#print axioms P01AC.Nucleus.E_agrees
#ortho_audit P01AC.Nucleus.E_agrees
#check P01AC.Nucleus.H_agrees
#print axioms P01AC.Nucleus.H_agrees
#ortho_audit P01AC.Nucleus.H_agrees
#check P01AC.form_arr
#print axioms P01AC.form_arr
#ortho_audit P01AC.form_arr
#check P01AC.form_fin
#print axioms P01AC.form_fin
#ortho_audit P01AC.form_fin
#check P01AC.fin_tsubst_congr
#print axioms P01AC.fin_tsubst_congr
#ortho_audit P01AC.fin_tsubst_congr
#check P01AC.finiteIdentity
#print axioms P01AC.finiteIdentity
#ortho_audit P01AC.finiteIdentity
#check P01AC.finiteIdentity_length
#print axioms P01AC.finiteIdentity_length
#ortho_audit P01AC.finiteIdentity_length
#check P01AC.finiteIdentity_get
#print axioms P01AC.finiteIdentity_get
#ortho_audit P01AC.finiteIdentity_get
#check P01AC.finiteIdentity_action
#print axioms P01AC.finiteIdentity_action
#ortho_audit P01AC.finiteIdentity_action
#check P01AC.finite_import
#print axioms P01AC.finite_import
#ortho_audit P01AC.finite_import
#check P01AC.Nucleus.translate
#print axioms P01AC.Nucleus.translate
#ortho_audit P01AC.Nucleus.translate
#check P01AC.Nucleus.telescope
#print axioms P01AC.Nucleus.telescope
#ortho_audit P01AC.Nucleus.telescope
#check P01AC.Nucleus.translate_subst
#print axioms P01AC.Nucleus.translate_subst
#ortho_audit P01AC.Nucleus.translate_subst
#check P01AC.Nucleus.translate_wk
#print axioms P01AC.Nucleus.translate_wk
#ortho_audit P01AC.Nucleus.translate_wk
#check P01AC.Nucleus.translate_inst
#print axioms P01AC.Nucleus.translate_inst
#ortho_audit P01AC.Nucleus.translate_inst
#check P01AC.Nucleus.translate_motiveAt
#print axioms P01AC.Nucleus.translate_motiveAt
#ortho_audit P01AC.Nucleus.translate_motiveAt
#check P01AC.Nucleus.translate_arr
#print axioms P01AC.Nucleus.translate_arr
#ortho_audit P01AC.Nucleus.translate_arr
#check P01AC.Nucleus.translate_fin
#print axioms P01AC.Nucleus.translate_fin
#ortho_audit P01AC.Nucleus.translate_fin
#check P01AC.Nucleus.telescope_theta
#print axioms P01AC.Nucleus.telescope_theta
#ortho_audit P01AC.Nucleus.telescope_theta
#check P01AC.Nucleus.scoped_agrees
#print axioms P01AC.Nucleus.scoped_agrees
#ortho_audit P01AC.Nucleus.scoped_agrees
#check P01AC.Nucleus.lookup
#print axioms P01AC.Nucleus.lookup
#ortho_audit P01AC.Nucleus.lookup
#check P01AC.type_pi
#print axioms P01AC.type_pi
#ortho_audit P01AC.type_pi
#check P01AC.Unary
#print axioms P01AC.Unary
#ortho_audit P01AC.Unary
#check P01AC.Hetero
#print axioms P01AC.Hetero
#ortho_audit P01AC.Hetero
#check P01AC.predicates
#print axioms P01AC.predicates
#ortho_audit P01AC.predicates
#check P01AC.F
#print axioms P01AC.F
#ortho_audit P01AC.F
#check P01AC.G
#print axioms P01AC.G
#ortho_audit P01AC.G
#check P01AC.F_param
#print axioms P01AC.F_param
#ortho_audit P01AC.F_param
#check P01AC.F_bottom
#print axioms P01AC.F_bottom
#ortho_audit P01AC.F_bottom
#check P01AC.F_raw
#print axioms P01AC.F_raw
#ortho_audit P01AC.F_raw
#check P01AC.F_pi
#print axioms P01AC.F_pi
#ortho_audit P01AC.F_pi
#check P01AC.F_sigma
#print axioms P01AC.F_sigma
#ortho_audit P01AC.F_sigma
#check P01AC.F_identity
#print axioms P01AC.F_identity
#ortho_audit P01AC.F_identity
#check P01AC.G_param
#print axioms P01AC.G_param
#ortho_audit P01AC.G_param
#check P01AC.G_bottom
#print axioms P01AC.G_bottom
#ortho_audit P01AC.G_bottom
#check P01AC.G_raw
#print axioms P01AC.G_raw
#ortho_audit P01AC.G_raw
#check P01AC.G_pi
#print axioms P01AC.G_pi
#ortho_audit P01AC.G_pi
#check P01AC.G_sigma
#print axioms P01AC.G_sigma
#ortho_audit P01AC.G_sigma
#check P01AC.G_identity
#print axioms P01AC.G_identity
#ortho_audit P01AC.G_identity
#check P01AC.F_all
#print axioms P01AC.F_all
#ortho_audit P01AC.F_all
#check P01AC.G_all
#print axioms P01AC.G_all
#ortho_audit P01AC.G_all
#check P01AC.zeroEnv
#print axioms P01AC.zeroEnv
#ortho_audit P01AC.zeroEnv
#check P01AC.tail
#print axioms P01AC.tail
#ortho_audit P01AC.tail
#check P01AC.D
#print axioms P01AC.D
#ortho_audit P01AC.D
#check P01AC.E
#print axioms P01AC.E
#ortho_audit P01AC.E
#check P01AC.H
#print axioms P01AC.H
#ortho_audit P01AC.H
#check P01AC.tail_cons
#print axioms P01AC.tail_cons
#ortho_audit P01AC.tail_cons
#check P01AC.cons_head_tail
#print axioms P01AC.cons_head_tail
#ortho_audit P01AC.cons_head_tail
#check P01AC.eval_pup_env
#print axioms P01AC.eval_pup_env
#ortho_audit P01AC.eval_pup_env
#check P01AC.eval_cons_poly
#print axioms P01AC.eval_cons_poly
#ortho_audit P01AC.eval_cons_poly
#check P01AC.renvMap
#print axioms P01AC.renvMap
#ortho_audit P01AC.renvMap
#check P01AC.renvMap_diag
#print axioms P01AC.renvMap_diag
#ortho_audit P01AC.renvMap_diag
#check P01AC.cons_liftRen
#print axioms P01AC.cons_liftRen
#ortho_audit P01AC.cons_liftRen
#check P01AC.renvMap_extend
#print axioms P01AC.renvMap_extend
#ortho_audit P01AC.renvMap_extend
#check P01AC.FG_trename
#print axioms P01AC.FG_trename
#ortho_audit P01AC.FG_trename
#check P01AC.F_trename
#print axioms P01AC.F_trename
#ortho_audit P01AC.F_trename
#check P01AC.G_trename
#print axioms P01AC.G_trename
#ortho_audit P01AC.G_trename
#check P01AC.F_twk
#print axioms P01AC.F_twk
#ortho_audit P01AC.F_twk
#check P01AC.G_twk
#print axioms P01AC.G_twk
#ortho_audit P01AC.G_twk
#check P01AC.D_twk
#print axioms P01AC.D_twk
#ortho_audit P01AC.D_twk
#check P01AC.E_twk
#print axioms P01AC.E_twk
#ortho_audit P01AC.E_twk
#check P01AC.H_twk
#print axioms P01AC.H_twk
#ortho_audit P01AC.H_twk
#check P01AC.FG_subst
#print axioms P01AC.FG_subst
#ortho_audit P01AC.FG_subst
#check P01AC.F_subst
#print axioms P01AC.F_subst
#ortho_audit P01AC.F_subst
#check P01AC.G_subst
#print axioms P01AC.G_subst
#ortho_audit P01AC.G_subst
#check P01AC.F_wk
#print axioms P01AC.F_wk
#ortho_audit P01AC.F_wk
#check P01AC.G_wk
#print axioms P01AC.G_wk
#ortho_audit P01AC.G_wk
#check P01AC.F_inst
#print axioms P01AC.F_inst
#ortho_audit P01AC.F_inst
#check P01AC.G_inst
#print axioms P01AC.G_inst
#ortho_audit P01AC.G_inst
#check P01AC.F_motiveAt
#print axioms P01AC.F_motiveAt
#ortho_audit P01AC.F_motiveAt
#check P01AC.G_motiveAt
#print axioms P01AC.G_motiveAt
#ortho_audit P01AC.G_motiveAt
#check P01AC.subEnv
#print axioms P01AC.subEnv
#ortho_audit P01AC.subEnv
#check P01AC.subEnv_nil
#print axioms P01AC.subEnv_nil
#ortho_audit P01AC.subEnv_nil
#check P01AC.subEnv_cons
#print axioms P01AC.subEnv_cons
#ortho_audit P01AC.subEnv_cons
#check P01AC.TypedSub.related
#print axioms P01AC.TypedSub.related
#ortho_audit P01AC.TypedSub.related
#check P01AC.TypedSub.respects
#print axioms P01AC.TypedSub.respects
#ortho_audit P01AC.TypedSub.respects
#check P01AC.TypedSub.valid
#print axioms P01AC.TypedSub.valid
#ortho_audit P01AC.TypedSub.valid
#check P01AC.representedContext
#print axioms P01AC.representedContext
#ortho_audit P01AC.representedContext
#check P01AC.representedType
#print axioms P01AC.representedType
#ortho_audit P01AC.representedType
#check P01AC.representedTerm
#print axioms P01AC.representedTerm
#ortho_audit P01AC.representedTerm
#check P01AC.representedTerm_code
#print axioms P01AC.representedTerm_code
#ortho_audit P01AC.representedTerm_code
#check P01AC.representedType_relation
#print axioms P01AC.representedType_relation
#ortho_audit P01AC.representedType_relation
#check P01AC.representedSub
#print axioms P01AC.representedSub
#ortho_audit P01AC.representedSub
#check P01AC.represented_substitution_code
#print axioms P01AC.represented_substitution_code
#ortho_audit P01AC.represented_substitution_code
#check P01AC.intrinsic_type_ext
#print axioms P01AC.intrinsic_type_ext
#ortho_audit P01AC.intrinsic_type_ext
#check P01AC.represented_substitution_type
#print axioms P01AC.represented_substitution_type
#ortho_audit P01AC.represented_substitution_type
#check P01AC.ImageMatch
#print axioms P01AC.ImageMatch
#ortho_audit P01AC.ImageMatch
#check P01AC.ImageMatch.diagonalLeft
#print axioms P01AC.ImageMatch.diagonalLeft
#ortho_audit P01AC.ImageMatch.diagonalLeft
#check P01AC.ImageMatch.diagonalRight
#print axioms P01AC.ImageMatch.diagonalRight
#ortho_audit P01AC.ImageMatch.diagonalRight
#check P01AC.ImageMatch.termLift
#print axioms P01AC.ImageMatch.termLift
#ortho_audit P01AC.ImageMatch.termLift
#check P01AC.ImageMatch.typeLift
#print axioms P01AC.ImageMatch.typeLift
#ortho_audit P01AC.ImageMatch.typeLift
#check P01AC.EvalImages
#print axioms P01AC.EvalImages
#ortho_audit P01AC.EvalImages
#check P01AC.evalImages_pup
#print axioms P01AC.evalImages_pup
#ortho_audit P01AC.evalImages_pup
#check P01AC.FG_mixed
#print axioms P01AC.FG_mixed
#ortho_audit P01AC.FG_mixed
#check P01AC.type_sigma
#print axioms P01AC.type_sigma
#ortho_audit P01AC.type_sigma
#check P01AC.Hereditary
#print axioms P01AC.Hereditary
#ortho_audit P01AC.Hereditary
#check P01AC.FormSound
#print axioms P01AC.FormSound
#ortho_audit P01AC.FormSound
#check P01AC.TermSound
#print axioms P01AC.TermSound
#ortho_audit P01AC.TermSound
#check P01AC.Hereditary.laws
#print axioms P01AC.Hereditary.laws
#ortho_audit P01AC.Hereditary.laws
#check P01AC.form_sound
#print axioms P01AC.form_sound
#ortho_audit P01AC.form_sound
#check P01AC.has_sound
#print axioms P01AC.has_sound
#ortho_audit P01AC.has_sound
#check P01AC.context_sound
#print axioms P01AC.context_sound
#ortho_audit P01AC.context_sound
#check P01AC.fundamental
#print axioms P01AC.fundamental
#ortho_audit P01AC.fundamental
#check P01AC.unary_fundamental
#print axioms P01AC.unary_fundamental
#ortho_audit P01AC.unary_fundamental
#check P01AC.strong_diagonal
#print axioms P01AC.strong_diagonal
#ortho_audit P01AC.strong_diagonal
#check P01AC.two_sided_invariance
#print axioms P01AC.two_sided_invariance
#ortho_audit P01AC.two_sided_invariance
#check P01AC.MixedSubstitution
#print axioms P01AC.MixedSubstitution
#ortho_audit P01AC.MixedSubstitution
#check P01AC.MixedSubstitution.scope
#print axioms P01AC.MixedSubstitution.scope
#ortho_audit P01AC.MixedSubstitution.scope
#check P01AC.MixedSubstitution.lift
#print axioms P01AC.MixedSubstitution.lift
#ortho_audit P01AC.MixedSubstitution.lift
#check P01AC.MixedSubstitution.twk
#print axioms P01AC.MixedSubstitution.twk
#ortho_audit P01AC.MixedSubstitution.twk
#check P01AC.mixed_theta_head
#print axioms P01AC.mixed_theta_head
#ortho_audit P01AC.mixed_theta_head
#check P01AC.MixedSubstitution.theta
#print axioms P01AC.MixedSubstitution.theta
#ortho_audit P01AC.MixedSubstitution.theta
#check P01AC.form_mixed
#print axioms P01AC.form_mixed
#ortho_audit P01AC.form_mixed
#check P01AC.has_mixed
#print axioms P01AC.has_mixed
#ortho_audit P01AC.has_mixed
#check P01AC.images
#print axioms P01AC.images
#ortho_audit P01AC.images
#check P01AC.MixedTerms
#print axioms P01AC.MixedTerms
#ortho_audit P01AC.MixedTerms
#check P01AC.MixedSub
#print axioms P01AC.MixedSub
#ortho_audit P01AC.MixedSub
#check P01AC.MixedTerms.target
#print axioms P01AC.MixedTerms.target
#ortho_audit P01AC.MixedTerms.target
#check P01AC.MixedTerms.source
#print axioms P01AC.MixedTerms.source
#ortho_audit P01AC.MixedTerms.source
#check P01AC.MixedTerms.length
#print axioms P01AC.MixedTerms.length
#ortho_audit P01AC.MixedTerms.length
#check P01AC.mixed_cons_wk
#print axioms P01AC.mixed_cons_wk
#ortho_audit P01AC.mixed_cons_wk
#check P01AC.MixedTerms.lookup
#print axioms P01AC.MixedTerms.lookup
#ortho_audit P01AC.MixedTerms.lookup
#check P01AC.typeImages_ge
#print axioms P01AC.typeImages_ge
#ortho_audit P01AC.typeImages_ge
#check P01AC.MixedSub.target
#print axioms P01AC.MixedSub.target
#ortho_audit P01AC.MixedSub.target
#check P01AC.MixedSub.source
#print axioms P01AC.MixedSub.source
#ortho_audit P01AC.MixedSub.source
#check P01AC.MixedSub.length
#print axioms P01AC.MixedSub.length
#ortho_audit P01AC.MixedSub.length
#check P01AC.MixedSub.typeForm
#print axioms P01AC.MixedSub.typeForm
#ortho_audit P01AC.MixedSub.typeForm
#check P01AC.MixedSub.toSubstitution
#print axioms P01AC.MixedSub.toSubstitution
#ortho_audit P01AC.MixedSub.toSubstitution
#check P01AC.MixedSub.scope
#print axioms P01AC.MixedSub.scope
#ortho_audit P01AC.MixedSub.scope
#check P01AC.MixedSub.form
#print axioms P01AC.MixedSub.form
#ortho_audit P01AC.MixedSub.form
#check P01AC.MixedSub.has
#print axioms P01AC.MixedSub.has
#ortho_audit P01AC.MixedSub.has
#check P01AC.images_map
#print axioms P01AC.images_map
#ortho_audit P01AC.images_map
#check P01AC.MixedSub.comp
#print axioms P01AC.MixedSub.comp
#ortho_audit P01AC.MixedSub.comp
#check P01AC.liftImages
#print axioms P01AC.liftImages
#ortho_audit P01AC.liftImages
#check P01AC.images_lift
#print axioms P01AC.images_lift
#ortho_audit P01AC.images_lift
#check P01AC.liftTypes
#print axioms P01AC.liftTypes
#ortho_audit P01AC.liftTypes
#check P01AC.typeImages_lift
#print axioms P01AC.typeImages_lift
#ortho_audit P01AC.typeImages_lift
#check P01AC.typeImages_wk
#print axioms P01AC.typeImages_wk
#ortho_audit P01AC.typeImages_wk
#check P01AC.MixedTerms.weaken
#print axioms P01AC.MixedTerms.weaken
#ortho_audit P01AC.MixedTerms.weaken
#check P01AC.MixedSub.lift
#print axioms P01AC.MixedSub.lift
#ortho_audit P01AC.MixedSub.lift
#check P01AC.MixedTerms.twk
#print axioms P01AC.MixedTerms.twk
#ortho_audit P01AC.MixedTerms.twk
#check P01AC.MixedSub.twk
#print axioms P01AC.MixedSub.twk
#ortho_audit P01AC.MixedSub.twk
#check P01AC.MixedSub.theta
#print axioms P01AC.MixedSub.theta
#ortho_audit P01AC.MixedSub.theta
#check P01AC.typeSupport
#print axioms P01AC.typeSupport
#ortho_audit P01AC.typeSupport
#check P01AC.telTypeSupport
#print axioms P01AC.telTypeSupport
#ortho_audit P01AC.telTypeSupport
#check P01AC.typeSupport_subst
#print axioms P01AC.typeSupport_subst
#ortho_audit P01AC.typeSupport_subst
#check P01AC.typeSupport_wk
#print axioms P01AC.typeSupport_wk
#ortho_audit P01AC.typeSupport_wk
#check P01AC.psub_scoped_congr
#print axioms P01AC.psub_scoped_congr
#ortho_audit P01AC.psub_scoped_congr
#check P01AC.mixed_term_congr
#print axioms P01AC.mixed_term_congr
#ortho_audit P01AC.mixed_term_congr
#check P01AC.mixed_type_congr
#print axioms P01AC.mixed_type_congr
#ortho_audit P01AC.mixed_type_congr
#check P01AC.identityImages
#print axioms P01AC.identityImages
#ortho_audit P01AC.identityImages
#check P01AC.identityImages_length
#print axioms P01AC.identityImages_length
#ortho_audit P01AC.identityImages_length
#check P01AC.identityImages_get
#print axioms P01AC.identityImages_get
#ortho_audit P01AC.identityImages_get
#check P01AC.psub_identityImages
#print axioms P01AC.psub_identityImages
#ortho_audit P01AC.psub_identityImages
#check P01AC.mixed_identityImages
#print axioms P01AC.mixed_identityImages
#ortho_audit P01AC.mixed_identityImages
#check P01AC.parameterImages
#print axioms P01AC.parameterImages
#ortho_audit P01AC.parameterImages
#check P01AC.parameterImages_length
#print axioms P01AC.parameterImages_length
#ortho_audit P01AC.parameterImages_length
#check P01AC.parameterImages_get
#print axioms P01AC.parameterImages_get
#ortho_audit P01AC.parameterImages_get
#check P01AC.tsubst_parameterImages
#print axioms P01AC.tsubst_parameterImages
#ortho_audit P01AC.tsubst_parameterImages
#check P01AC.mixed_finite_identity
#print axioms P01AC.mixed_finite_identity
#ortho_audit P01AC.mixed_finite_identity
#check P01AC.lookup_form
#print axioms P01AC.lookup_form
#ortho_audit P01AC.lookup_form
#check P01AC.lookup_typeSupport
#print axioms P01AC.lookup_typeSupport
#ortho_audit P01AC.lookup_typeSupport
#check P01AC.MixedTerms.ofLookup
#print axioms P01AC.MixedTerms.ofLookup
#ortho_audit P01AC.MixedTerms.ofLookup
#check P01AC.MixedSub.id
#print axioms P01AC.MixedSub.id
#ortho_audit P01AC.MixedSub.id
#check P01AC.MixedSub.allElim
#print axioms P01AC.MixedSub.allElim
#ortho_audit P01AC.MixedSub.allElim
#check P01AC.mixed_finite_instance_top
#print axioms P01AC.mixed_finite_instance_top
#ortho_audit P01AC.mixed_finite_instance_top
#check P01AC.form_tinst
#print axioms P01AC.form_tinst
#ortho_audit P01AC.form_tinst
#check P01AC.has_tinst
#print axioms P01AC.has_tinst
#ortho_audit P01AC.has_tinst
#check P01AC.TypedSub
#print axioms P01AC.TypedSub
#ortho_audit P01AC.TypedSub
#check P01AC.TypedSub.toSubstitution
#print axioms P01AC.TypedSub.toSubstitution
#ortho_audit P01AC.TypedSub.toSubstitution
#check P01AC.TypedSub.form
#print axioms P01AC.TypedSub.form
#ortho_audit P01AC.TypedSub.form
#check P01AC.TypedSub.has
#print axioms P01AC.TypedSub.has
#ortho_audit P01AC.TypedSub.has
#check P01AC.TypedSub.scope
#print axioms P01AC.TypedSub.scope
#ortho_audit P01AC.TypedSub.scope
#check P01AC.TypedSub.comp
#print axioms P01AC.TypedSub.comp
#ortho_audit P01AC.TypedSub.comp
#check P01AC.TypedSub.id
#print axioms P01AC.TypedSub.id
#ortho_audit P01AC.TypedSub.id
#check P01AC.has_scoped
#print axioms P01AC.has_scoped
#ortho_audit P01AC.has_scoped
#check P01AC.lookup_exists
#print axioms P01AC.lookup_exists
#ortho_audit P01AC.lookup_exists
#check P01AC.has_form
#print axioms P01AC.has_form
#ortho_audit P01AC.has_form
#check P01AC.form_ctx
#print axioms P01AC.form_ctx
#ortho_audit P01AC.form_ctx
#check P01AC.form_scoped
#print axioms P01AC.form_scoped
#ortho_audit P01AC.form_scoped
#check P01AC.typeImages_mixed
#print axioms P01AC.typeImages_mixed
#ortho_audit P01AC.typeImages_mixed
#check P01AC.typeImages_trename
#print axioms P01AC.typeImages_trename
#ortho_audit P01AC.typeImages_trename
#check P01AC.typeImages_subst
#print axioms P01AC.typeImages_subst
#ortho_audit P01AC.typeImages_subst
#check P01AC.mixed_fin
#print axioms P01AC.mixed_fin
#ortho_audit P01AC.mixed_fin
#check P01AC.mixed_finite_instance
#print axioms P01AC.mixed_finite_instance
#ortho_audit P01AC.mixed_finite_instance
#check P01AC.subst_finite_instance
#print axioms P01AC.subst_finite_instance
#ortho_audit P01AC.subst_finite_instance
#check P01AC.trename_finite_instance
#print axioms P01AC.trename_finite_instance
#ortho_audit P01AC.trename_finite_instance
#check P01AC.trenameTel
#print axioms P01AC.trenameTel
#ortho_audit P01AC.trenameTel
#check P01AC.trenameTel_twk
#print axioms P01AC.trenameTel_twk
#ortho_audit P01AC.trenameTel_twk
#check P01AC.trenameTel_theta
#print axioms P01AC.trenameTel_theta
#ortho_audit P01AC.trenameTel_theta
#check P01AC.lookup_trename
#print axioms P01AC.lookup_trename
#ortho_audit P01AC.lookup_trename
#check P01AC.form_trename
#print axioms P01AC.form_trename
#ortho_audit P01AC.form_trename
#check P01AC.has_trename
#print axioms P01AC.has_trename
#ortho_audit P01AC.has_trename
#check P01AC.ctx_trename
#print axioms P01AC.ctx_trename
#ortho_audit P01AC.ctx_trename
#check P01AC.ctx_twk
#print axioms P01AC.ctx_twk
#ortho_audit P01AC.ctx_twk
#check P01AC.form_twk
#print axioms P01AC.form_twk
#ortho_audit P01AC.form_twk
#check P01AC.has_twk
#print axioms P01AC.has_twk
#ortho_audit P01AC.has_twk
#check P01AC.StructuralChecks.dependentReplacement
#print axioms P01AC.StructuralChecks.dependentReplacement
#ortho_audit P01AC.StructuralChecks.dependentReplacement
#check P01AC.StructuralChecks.dependentReplacement_formed
#print axioms P01AC.StructuralChecks.dependentReplacement_formed
#ortho_audit P01AC.StructuralChecks.dependentReplacement_formed
#check P01AC.StructuralChecks.dependentReplacement_not_closed
#print axioms P01AC.StructuralChecks.dependentReplacement_not_closed
#ortho_audit P01AC.StructuralChecks.dependentReplacement_not_closed
#check P01AC.StructuralChecks.dependent_mixed_map
#print axioms P01AC.StructuralChecks.dependent_mixed_map
#ortho_audit P01AC.StructuralChecks.dependent_mixed_map
#check P01AC.StructuralChecks.dependent_mixed_preserves
#print axioms P01AC.StructuralChecks.dependent_mixed_preserves
#ortho_audit P01AC.StructuralChecks.dependent_mixed_preserves
#check P01AC.StructuralChecks.finite_identity_tail
#print axioms P01AC.StructuralChecks.finite_identity_tail
#ortho_audit P01AC.StructuralChecks.finite_identity_tail
#check P01AC.StructuralChecks.finite_identity_not_total_identity
#print axioms P01AC.StructuralChecks.finite_identity_not_total_identity
#ortho_audit P01AC.StructuralChecks.finite_identity_not_total_identity
#check P01AC.StructuralChecks.dependent_all_elimination_map
#print axioms P01AC.StructuralChecks.dependent_all_elimination_map
#ortho_audit P01AC.StructuralChecks.dependent_all_elimination_map
#check P01AC.renSub
#print axioms P01AC.renSub
#ortho_audit P01AC.renSub
#check P01AC.renSub_lift
#print axioms P01AC.renSub_lift
#ortho_audit P01AC.renSub_lift
#check P01AC.Renaming
#print axioms P01AC.Renaming
#ortho_audit P01AC.Renaming
#check P01AC.Renaming.id
#print axioms P01AC.Renaming.id
#ortho_audit P01AC.Renaming.id
#check P01AC.Renaming.lift
#print axioms P01AC.Renaming.lift
#ortho_audit P01AC.Renaming.lift
#check P01AC.Renaming.weaken
#print axioms P01AC.Renaming.weaken
#ortho_audit P01AC.Renaming.weaken
#check P01AC.subst_theta_head
#print axioms P01AC.subst_theta_head
#ortho_audit P01AC.subst_theta_head
#check P01AC.Renaming.theta
#print axioms P01AC.Renaming.theta
#ortho_audit P01AC.Renaming.theta
#check P01AC.renSub_comp
#print axioms P01AC.renSub_comp
#ortho_audit P01AC.renSub_comp
#check P01AC.Renaming.comp
#print axioms P01AC.Renaming.comp
#ortho_audit P01AC.Renaming.comp
#check P01AC.subst_ren_shift
#print axioms P01AC.subst_ren_shift
#ortho_audit P01AC.subst_ren_shift
#check P01AC.psub_ren_shift
#print axioms P01AC.psub_ren_shift
#ortho_audit P01AC.psub_ren_shift
#check P01AC.form_pi_domain
#print axioms P01AC.form_pi_domain
#ortho_audit P01AC.form_pi_domain
#check P01AC.lookup_trename_inv
#print axioms P01AC.lookup_trename_inv
#ortho_audit P01AC.lookup_trename_inv
#check P01AC.Renaming.twk
#print axioms P01AC.Renaming.twk
#ortho_audit P01AC.Renaming.twk
#check P01AC.form_rename
#print axioms P01AC.form_rename
#ortho_audit P01AC.form_rename
#check P01AC.has_rename
#print axioms P01AC.has_rename
#ortho_audit P01AC.has_rename
#check P01AC.form_wk
#print axioms P01AC.form_wk
#ortho_audit P01AC.form_wk
#check P01AC.has_wk
#print axioms P01AC.has_wk
#ortho_audit P01AC.has_wk
#check P01AC.form_theta_head
#print axioms P01AC.form_theta_head
#ortho_audit P01AC.form_theta_head
#check P01AC.ctx_theta
#print axioms P01AC.ctx_theta
#ortho_audit P01AC.ctx_theta
#check P01AC.Ty
#print axioms P01AC.Ty
#ortho_audit P01AC.Ty
#check P01AC.subst
#print axioms P01AC.subst
#ortho_audit P01AC.subst
#check P01AC.wk
#print axioms P01AC.wk
#ortho_audit P01AC.wk
#check P01AC.inst
#print axioms P01AC.inst
#ortho_audit P01AC.inst
#check P01AC.motiveAt
#print axioms P01AC.motiveAt
#ortho_audit P01AC.motiveAt
#check P01AC.arr
#print axioms P01AC.arr
#ortho_audit P01AC.arr
#check P01AC.fin
#print axioms P01AC.fin
#ortho_audit P01AC.fin
#check P01AC.trename
#print axioms P01AC.trename
#ortho_audit P01AC.trename
#check P01AC.twk
#print axioms P01AC.twk
#ortho_audit P01AC.twk
#check P01AC.tup
#print axioms P01AC.tup
#ortho_audit P01AC.tup
#check P01AC.mixed
#print axioms P01AC.mixed
#ortho_audit P01AC.mixed
#check P01AC.tsubst
#print axioms P01AC.tsubst
#ortho_audit P01AC.tsubst
#check P01AC.tinst
#print axioms P01AC.tinst
#ortho_audit P01AC.tinst
#check P01AC.finSupport
#print axioms P01AC.finSupport
#ortho_audit P01AC.finSupport
#check P01AC.typeImages
#print axioms P01AC.typeImages
#ortho_audit P01AC.typeImages
#check P01AC.Tel
#print axioms P01AC.Tel
#ortho_audit P01AC.Tel
#check P01AC.Scoped
#print axioms P01AC.Scoped
#ortho_audit P01AC.Scoped
#check P01AC.TyScoped
#print axioms P01AC.TyScoped
#ortho_audit P01AC.TyScoped
#check P01AC.Lookup
#print axioms P01AC.Lookup
#ortho_audit P01AC.Lookup
#check P01AC.twkTel
#print axioms P01AC.twkTel
#ortho_audit P01AC.twkTel
#check P01AC.theta
#print axioms P01AC.theta
#ortho_audit P01AC.theta
#check P01AC.Ctx
#print axioms P01AC.Ctx
#ortho_audit P01AC.Ctx
#check P01AC.Form
#print axioms P01AC.Form
#ortho_audit P01AC.Form
#check P01AC.Has
#print axioms P01AC.Has
#ortho_audit P01AC.Has
#check P01AC.subst_id
#print axioms P01AC.subst_id
#ortho_audit P01AC.subst_id
#check P01AC.subst_comp
#print axioms P01AC.subst_comp
#ortho_audit P01AC.subst_comp
#check P01AC.subst_wk
#print axioms P01AC.subst_wk
#ortho_audit P01AC.subst_wk
#check P01AC.subst_wk_cancel
#print axioms P01AC.subst_wk_cancel
#ortho_audit P01AC.subst_wk_cancel
#check P01AC.inst_wk
#print axioms P01AC.inst_wk
#ortho_audit P01AC.inst_wk
#check P01AC.subst_inst
#print axioms P01AC.subst_inst
#ortho_audit P01AC.subst_inst
#check P01AC.subst_motiveAt
#print axioms P01AC.subst_motiveAt
#ortho_audit P01AC.subst_motiveAt
#check P01AC.motiveAt_inst
#print axioms P01AC.motiveAt_inst
#ortho_audit P01AC.motiveAt_inst
#check P01AC.motiveAt_wk_wk
#print axioms P01AC.motiveAt_wk_wk
#ortho_audit P01AC.motiveAt_wk_wk
#check P01AC.subst_arr
#print axioms P01AC.subst_arr
#ortho_audit P01AC.subst_arr
#check P01AC.subst_fin
#print axioms P01AC.subst_fin
#ortho_audit P01AC.subst_fin
#check P01AC.wk_fin
#print axioms P01AC.wk_fin
#ortho_audit P01AC.wk_fin
#check P01AC.inst_fin
#print axioms P01AC.inst_fin
#ortho_audit P01AC.inst_fin
#check P01AC.motiveAt_fin
#print axioms P01AC.motiveAt_fin
#ortho_audit P01AC.motiveAt_fin
#check P01AC.ScopedSub
#print axioms P01AC.ScopedSub
#ortho_audit P01AC.ScopedSub
#check P01AC.scoped_mono
#print axioms P01AC.scoped_mono
#ortho_audit P01AC.scoped_mono
#check P01AC.scoped_subst
#print axioms P01AC.scoped_subst
#ortho_audit P01AC.scoped_subst
#check P01AC.scoped_rename
#print axioms P01AC.scoped_rename
#ortho_audit P01AC.scoped_rename
#check P01AC.scoped_wk
#print axioms P01AC.scoped_wk
#ortho_audit P01AC.scoped_wk
#check P01AC.scopedSub_lift
#print axioms P01AC.scopedSub_lift
#ortho_audit P01AC.scopedSub_lift
#check P01AC.scopedSub_id
#print axioms P01AC.scopedSub_id
#ortho_audit P01AC.scopedSub_id
#check P01AC.scopedSub_comp
#print axioms P01AC.scopedSub_comp
#ortho_audit P01AC.scopedSub_comp
#check P01AC.scopedSub_cons
#print axioms P01AC.scopedSub_cons
#ortho_audit P01AC.scopedSub_cons
#check P01AC.scoped_pair
#print axioms P01AC.scoped_pair
#ortho_audit P01AC.scoped_pair
#check P01AC.scoped_fst
#print axioms P01AC.scoped_fst
#ortho_audit P01AC.scoped_fst
#check P01AC.scoped_snd
#print axioms P01AC.scoped_snd
#ortho_audit P01AC.scoped_snd
#check P01AC.scoped_j
#print axioms P01AC.scoped_j
#ortho_audit P01AC.scoped_j
#check P01AC.scoped_drop_absent
#print axioms P01AC.scoped_drop_absent
#ortho_audit P01AC.scoped_drop_absent
#check P01AC.scoped_abstract
#print axioms P01AC.scoped_abstract
#ortho_audit P01AC.scoped_abstract
#check P01AC.tyScoped_mono
#print axioms P01AC.tyScoped_mono
#ortho_audit P01AC.tyScoped_mono
#check P01AC.tyScoped_subst
#print axioms P01AC.tyScoped_subst
#ortho_audit P01AC.tyScoped_subst
#check P01AC.tyScoped_wk
#print axioms P01AC.tyScoped_wk
#ortho_audit P01AC.tyScoped_wk
#check P01AC.tyScoped_inst
#print axioms P01AC.tyScoped_inst
#ortho_audit P01AC.tyScoped_inst
#check P01AC.tyScoped_motiveAt
#print axioms P01AC.tyScoped_motiveAt
#ortho_audit P01AC.tyScoped_motiveAt
#check P01AC.tyScoped_fin
#print axioms P01AC.tyScoped_fin
#ortho_audit P01AC.tyScoped_fin
#check P01AC.lookup_lt
#print axioms P01AC.lookup_lt
#ortho_audit P01AC.lookup_lt
#check P01AC.polyConv_subst
#print axioms P01AC.polyConv_subst
#ortho_audit P01AC.polyConv_subst
#check P01AC.fundamental_var
#print axioms P01AC.fundamental_var
#ortho_audit P01AC.fundamental_var
#check P01AC.fundamental_pi_intro
#print axioms P01AC.fundamental_pi_intro
#ortho_audit P01AC.fundamental_pi_intro
#check P01AC.fundamental_pi_elim
#print axioms P01AC.fundamental_pi_elim
#ortho_audit P01AC.fundamental_pi_elim
#check P01AC.F_pair
#print axioms P01AC.F_pair
#ortho_audit P01AC.F_pair
#check P01AC.G_pair
#print axioms P01AC.G_pair
#ortho_audit P01AC.G_pair
#check P01AC.fundamental_sigma_intro
#print axioms P01AC.fundamental_sigma_intro
#ortho_audit P01AC.fundamental_sigma_intro
#check P01AC.fundamental_sigma_fst
#print axioms P01AC.fundamental_sigma_fst
#ortho_audit P01AC.fundamental_sigma_fst
#check P01AC.fundamental_sigma_snd
#print axioms P01AC.fundamental_sigma_snd
#ortho_audit P01AC.fundamental_sigma_snd
#check P01AC.fundamental_identity_intro
#print axioms P01AC.fundamental_identity_intro
#ortho_audit P01AC.fundamental_identity_intro
#check P01AC.fundamental_proof_erase
#print axioms P01AC.fundamental_proof_erase
#ortho_audit P01AC.fundamental_proof_erase
#check P01AC.fundamental_j
#print axioms P01AC.fundamental_j
#ortho_audit P01AC.fundamental_j

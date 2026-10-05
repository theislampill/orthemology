/- Exact kernel readbacks for the bounded typed-context nucleus. -/
import TypedBoundaryResults
import TypedLegacy

#print P01TC.Ty
#print P01TC.Ctx
#print P01TC.Form
#print P01TC.Has
#print P01TC.F
#print P01TC.G
#print P01TC.D
#print P01TC.E
#print P01TC.H
#print P01TC.TypeLaws
#print P01TC.ContextLaws
#print P01TC.Fundamental
#print P01TC.Hereditary
#print P01TC.TypedSub
#print P01TC.images
#print P01TC.Substitution
#print P01TC.representedContext
#print P01TC.representedType
#print P01TC.representedTerm
#print P01TC.representedSub
#print P01TC.contextualMotive
#print P01TC.representedContextualJ
#print P01DF.PolyConv

#check P01TC.Ty
#print axioms P01TC.Ty
#check P01TC.subst
#print axioms P01TC.subst
#check P01TC.wk
#print axioms P01TC.wk
#check P01TC.inst
#print axioms P01TC.inst
#check P01TC.motiveAt
#print axioms P01TC.motiveAt
#check P01TC.arr
#print axioms P01TC.arr
#check P01TC.fin
#print axioms P01TC.fin
#check P01TC.Tel
#print axioms P01TC.Tel
#check P01TC.Scoped
#print axioms P01TC.Scoped
#check P01TC.TyScoped
#print axioms P01TC.TyScoped
#check P01TC.Lookup
#print axioms P01TC.Lookup
#check P01TC.theta
#print axioms P01TC.theta
#check P01TC.F
#print axioms P01TC.F
#check P01TC.G
#print axioms P01TC.G
#check P01TC.zeroEnv
#print axioms P01TC.zeroEnv
#check P01TC.tail
#print axioms P01TC.tail
#check P01TC.D
#print axioms P01TC.D
#check P01TC.E
#print axioms P01TC.E
#check P01TC.H
#print axioms P01TC.H
#check P01TC.tail_cons
#print axioms P01TC.tail_cons
#check P01TC.cons_head_tail
#print axioms P01TC.cons_head_tail
#check P01TC.eval_pup_env
#print axioms P01TC.eval_pup_env
#check P01TC.eval_cons_poly
#print axioms P01TC.eval_cons_poly
#check P01TC.F_subst
#print axioms P01TC.F_subst
#check P01TC.G_subst
#print axioms P01TC.G_subst
#check P01TC.F_wk
#print axioms P01TC.F_wk
#check P01TC.G_wk
#print axioms P01TC.G_wk
#check P01TC.F_inst
#print axioms P01TC.F_inst
#check P01TC.G_inst
#print axioms P01TC.G_inst
#check P01TC.F_motiveAt
#print axioms P01TC.F_motiveAt
#check P01TC.G_motiveAt
#print axioms P01TC.G_motiveAt
#check P01TC.RelLaws
#print axioms P01TC.RelLaws
#check P01TC.RelLaws.per
#print axioms P01TC.RelLaws.per
#check P01TC.RelLaws.left
#print axioms P01TC.RelLaws.left
#check P01TC.RelLaws.right
#print axioms P01TC.RelLaws.right
#check P01TC.perLaws
#print axioms P01TC.perLaws
#check P01TC.ContextLaws
#print axioms P01TC.ContextLaws
#check P01TC.TypeLaws
#print axioms P01TC.TypeLaws
#check P01TC.Fundamental
#print axioms P01TC.Fundamental
#check P01TC.TypeLaws.raw
#print axioms P01TC.TypeLaws.raw
#check P01TC.Fundamental.unary
#print axioms P01TC.Fundamental.unary
#check P01TC.context_nil
#print axioms P01TC.context_nil
#check P01TC.context_ext
#print axioms P01TC.context_ext
#check P01TC.type_model
#print axioms P01TC.type_model
#check P01TC.type_param
#print axioms P01TC.type_param
#check P01TC.type_bottom
#print axioms P01TC.type_bottom
#check P01TC.type_allFinite
#print axioms P01TC.type_allFinite
#check P01TC.type_raw
#print axioms P01TC.type_raw
#check P01TC.type_identity
#print axioms P01TC.type_identity
#check P01TC.type_pi
#print axioms P01TC.type_pi
#check P01TC.type_sigma
#print axioms P01TC.type_sigma
#check P01TC.fundamental_var
#print axioms P01TC.fundamental_var
#check P01TC.fundamental_pi_intro
#print axioms P01TC.fundamental_pi_intro
#check P01TC.fundamental_pi_elim
#print axioms P01TC.fundamental_pi_elim
#check P01TC.F_pair
#print axioms P01TC.F_pair
#check P01TC.G_pair
#print axioms P01TC.G_pair
#check P01TC.fundamental_sigma_intro
#print axioms P01TC.fundamental_sigma_intro
#check P01TC.fundamental_sigma_fst
#print axioms P01TC.fundamental_sigma_fst
#check P01TC.fundamental_sigma_snd
#print axioms P01TC.fundamental_sigma_snd
#check P01TC.fundamental_identity_intro
#print axioms P01TC.fundamental_identity_intro
#check P01TC.fundamental_proof_erase
#print axioms P01TC.fundamental_proof_erase
#check P01TC.fundamental_j
#print axioms P01TC.fundamental_j
#check P01TC.objectOf
#print axioms P01TC.objectOf
#check P01TC.linkOf
#print axioms P01TC.linkOf
#check P01TC.F_arr
#print axioms P01TC.F_arr
#check P01TC.G_arr
#print axioms P01TC.G_arr
#check P01TC.fundamental_i
#print axioms P01TC.fundamental_i
#check P01TC.fundamental_k
#print axioms P01TC.fundamental_k
#check P01TC.fundamental_s
#print axioms P01TC.fundamental_s
#check P01TC.F_fin
#print axioms P01TC.F_fin
#check P01TC.G_fin
#print axioms P01TC.G_fin
#check P01TC.fundamental_finite
#print axioms P01TC.fundamental_finite
#check P01TC.subst_id
#print axioms P01TC.subst_id
#check P01TC.subst_comp
#print axioms P01TC.subst_comp
#check P01TC.subst_wk
#print axioms P01TC.subst_wk
#check P01TC.subst_wk_cancel
#print axioms P01TC.subst_wk_cancel
#check P01TC.inst_wk
#print axioms P01TC.inst_wk
#check P01TC.subst_inst
#print axioms P01TC.subst_inst
#check P01TC.subst_motiveAt
#print axioms P01TC.subst_motiveAt
#check P01TC.motiveAt_inst
#print axioms P01TC.motiveAt_inst
#check P01TC.motiveAt_wk_wk
#print axioms P01TC.motiveAt_wk_wk
#check P01TC.subst_arr
#print axioms P01TC.subst_arr
#check P01TC.subst_fin
#print axioms P01TC.subst_fin
#check P01TC.wk_fin
#print axioms P01TC.wk_fin
#check P01TC.inst_fin
#print axioms P01TC.inst_fin
#check P01TC.motiveAt_fin
#print axioms P01TC.motiveAt_fin
#check P01TC.ScopedSub
#print axioms P01TC.ScopedSub
#check P01TC.scoped_mono
#print axioms P01TC.scoped_mono
#check P01TC.scoped_subst
#print axioms P01TC.scoped_subst
#check P01TC.scoped_rename
#print axioms P01TC.scoped_rename
#check P01TC.scoped_wk
#print axioms P01TC.scoped_wk
#check P01TC.scopedSub_lift
#print axioms P01TC.scopedSub_lift
#check P01TC.scopedSub_id
#print axioms P01TC.scopedSub_id
#check P01TC.scopedSub_comp
#print axioms P01TC.scopedSub_comp
#check P01TC.scopedSub_cons
#print axioms P01TC.scopedSub_cons
#check P01TC.scoped_pair
#print axioms P01TC.scoped_pair
#check P01TC.scoped_fst
#print axioms P01TC.scoped_fst
#check P01TC.scoped_snd
#print axioms P01TC.scoped_snd
#check P01TC.scoped_j
#print axioms P01TC.scoped_j
#check P01TC.scoped_drop_absent
#print axioms P01TC.scoped_drop_absent
#check P01TC.scoped_abstract
#print axioms P01TC.scoped_abstract
#check P01TC.tyScoped_mono
#print axioms P01TC.tyScoped_mono
#check P01TC.tyScoped_subst
#print axioms P01TC.tyScoped_subst
#check P01TC.tyScoped_wk
#print axioms P01TC.tyScoped_wk
#check P01TC.tyScoped_inst
#print axioms P01TC.tyScoped_inst
#check P01TC.tyScoped_motiveAt
#print axioms P01TC.tyScoped_motiveAt
#check P01TC.tyScoped_fin
#print axioms P01TC.tyScoped_fin
#check P01TC.lookup_lt
#print axioms P01TC.lookup_lt
#check P01TC.polyConv_subst
#print axioms P01TC.polyConv_subst
#check P01TC.renSub
#print axioms P01TC.renSub
#check P01TC.renSub_lift
#print axioms P01TC.renSub_lift
#check P01TC.Renaming
#print axioms P01TC.Renaming
#check P01TC.Renaming.id
#print axioms P01TC.Renaming.id
#check P01TC.Renaming.lift
#print axioms P01TC.Renaming.lift
#check P01TC.Renaming.weaken
#print axioms P01TC.Renaming.weaken
#check P01TC.subst_theta_head
#print axioms P01TC.subst_theta_head
#check P01TC.Renaming.theta
#print axioms P01TC.Renaming.theta
#check P01TC.images
#print axioms P01TC.images
#check P01TC.TypedSub
#print axioms P01TC.TypedSub
#check P01TC.TypedSub.target
#print axioms P01TC.TypedSub.target
#check P01TC.TypedSub.source
#print axioms P01TC.TypedSub.source
#check P01TC.TypedSub.length
#print axioms P01TC.TypedSub.length
#check P01TC.TypedSub.lookup
#print axioms P01TC.TypedSub.lookup
#check P01TC.has_scoped
#print axioms P01TC.has_scoped
#check P01TC.lookup_exists
#print axioms P01TC.lookup_exists
#check P01TC.TypedSub.scope
#print axioms P01TC.TypedSub.scope
#check P01TC.renSub_comp
#print axioms P01TC.renSub_comp
#check P01TC.Renaming.comp
#print axioms P01TC.Renaming.comp
#check P01TC.subst_ren_shift
#print axioms P01TC.subst_ren_shift
#check P01TC.psub_ren_shift
#print axioms P01TC.psub_ren_shift
#check P01TC.form_pi_domain
#print axioms P01TC.form_pi_domain
#check P01TC.form_rename
#print axioms P01TC.form_rename
#check P01TC.has_rename
#print axioms P01TC.has_rename
#check P01TC.form_wk
#print axioms P01TC.form_wk
#check P01TC.has_wk
#print axioms P01TC.has_wk
#check P01TC.Substitution
#print axioms P01TC.Substitution
#check P01TC.Substitution.scope
#print axioms P01TC.Substitution.scope
#check P01TC.TypedSub.toSubstitution
#print axioms P01TC.TypedSub.toSubstitution
#check P01TC.Substitution.lift
#print axioms P01TC.Substitution.lift
#check P01TC.form_theta_head
#print axioms P01TC.form_theta_head
#check P01TC.ctx_theta
#print axioms P01TC.ctx_theta
#check P01TC.Substitution.theta
#print axioms P01TC.Substitution.theta
#check P01TC.form_subst
#print axioms P01TC.form_subst
#check P01TC.has_subst
#print axioms P01TC.has_subst
#check P01TC.TypedSub.form
#print axioms P01TC.TypedSub.form
#check P01TC.TypedSub.has
#print axioms P01TC.TypedSub.has
#check P01TC.has_form
#print axioms P01TC.has_form
#check P01TC.form_scoped
#print axioms P01TC.form_scoped
#check P01TC.images_map
#print axioms P01TC.images_map
#check P01TC.TypedSub.comp
#print axioms P01TC.TypedSub.comp
#check P01TC.Hereditary
#print axioms P01TC.Hereditary
#check P01TC.FormSound
#print axioms P01TC.FormSound
#check P01TC.TermSound
#print axioms P01TC.TermSound
#check P01TC.Hereditary.laws
#print axioms P01TC.Hereditary.laws
#check P01TC.form_sound
#print axioms P01TC.form_sound
#check P01TC.has_sound
#print axioms P01TC.has_sound
#check P01TC.context_sound
#print axioms P01TC.context_sound
#check P01TC.fundamental
#print axioms P01TC.fundamental
#check P01TC.unary_fundamental
#print axioms P01TC.unary_fundamental
#check P01TC.strong_diagonal
#print axioms P01TC.strong_diagonal
#check P01TC.two_sided_invariance
#print axioms P01TC.two_sided_invariance
#check P01TC.subEnv
#print axioms P01TC.subEnv
#check P01TC.subEnv_nil
#print axioms P01TC.subEnv_nil
#check P01TC.subEnv_cons
#print axioms P01TC.subEnv_cons
#check P01TC.TypedSub.related
#print axioms P01TC.TypedSub.related
#check P01TC.TypedSub.respects
#print axioms P01TC.TypedSub.respects
#check P01TC.TypedSub.valid
#print axioms P01TC.TypedSub.valid
#check P01TC.representedContext
#print axioms P01TC.representedContext
#check P01TC.representedType
#print axioms P01TC.representedType
#check P01TC.representedTerm
#print axioms P01TC.representedTerm
#check P01TC.representedTerm_code
#print axioms P01TC.representedTerm_code
#check P01TC.representedType_relation
#print axioms P01TC.representedType_relation
#check P01TC.representedSub
#print axioms P01TC.representedSub
#check P01TC.represented_substitution_code
#print axioms P01TC.represented_substitution_code
#check P01TC.intrinsic_type_ext
#print axioms P01TC.intrinsic_type_ext
#check P01TC.represented_substitution_type
#print axioms P01TC.represented_substitution_type
#check P01TC.contextual_related
#print axioms P01TC.contextual_related
#check P01TC.contextual_valid
#print axioms P01TC.contextual_valid
#check P01TC.contextualMotive
#print axioms P01TC.contextualMotive
#check P01TC.contextualProof
#print axioms P01TC.contextualProof
#check P01TC.contextualBase
#print axioms P01TC.contextualBase
#check P01TC.representedContextualJ
#print axioms P01TC.representedContextualJ
#check P01TC.representedContextualJ_code
#print axioms P01TC.representedContextualJ_code
#check P01TC.contextual_target_exact
#print axioms P01TC.contextual_target_exact
#check P01TC.alpha
#print axioms P01TC.alpha
#check P01TC.typedPair
#print axioms P01TC.typedPair
#check P01TC.typedPairType
#print axioms P01TC.typedPairType
#check P01TC.typed_pair_form
#print axioms P01TC.typed_pair_form
#check P01TC.typed_pair_has
#print axioms P01TC.typed_pair_has
#check P01TC.typed_pair_abstraction_form
#print axioms P01TC.typed_pair_abstraction_form
#check P01TC.typed_pair_abstraction_has
#print axioms P01TC.typed_pair_abstraction_has
#check P01TC.typed_pair_related
#print axioms P01TC.typed_pair_related
#check P01TC.typed_pair_abstraction_related
#print axioms P01TC.typed_pair_abstraction_related
#check P01TC.jContext
#print axioms P01TC.jContext
#check P01TC.jProofType
#print axioms P01TC.jProofType
#check P01TC.jMotive
#print axioms P01TC.jMotive
#check P01TC.jBaseType
#print axioms P01TC.jBaseType
#check P01TC.jTargetType
#print axioms P01TC.jTargetType
#check P01TC.jBase
#print axioms P01TC.jBase
#check P01TC.literalJ
#print axioms P01TC.literalJ
#check P01TC.j_context_formed
#print axioms P01TC.j_context_formed
#check P01TC.j_x_has
#print axioms P01TC.j_x_has
#check P01TC.j_y_has
#print axioms P01TC.j_y_has
#check P01TC.j_proof_form
#print axioms P01TC.j_proof_form
#check P01TC.j_e_has
#print axioms P01TC.j_e_has
#check P01TC.j_motive_form
#print axioms P01TC.j_motive_form
#check P01TC.j_motive_base_exact
#print axioms P01TC.j_motive_base_exact
#check P01TC.j_motive_target_exact
#print axioms P01TC.j_motive_target_exact
#check P01TC.j_base_form
#print axioms P01TC.j_base_form
#check P01TC.j_target_form
#print axioms P01TC.j_target_form
#check P01TC.j_base_has
#print axioms P01TC.j_base_has
#check P01TC.literal_j_has
#print axioms P01TC.literal_j_has
#check P01TC.literal_j_related
#print axioms P01TC.literal_j_related
#check P01TC.rawFibreType
#print axioms P01TC.rawFibreType
#check P01TC.raw_fibre_form
#print axioms P01TC.raw_fibre_form
#check P01TC.raw_fibre_pair_has
#print axioms P01TC.raw_fibre_pair_has
#check P01TC.raw_fibre_inhabited
#print axioms P01TC.raw_fibre_inhabited
#check P01TC.raw_fibres_nonempty_and_vary
#print axioms P01TC.raw_fibres_nonempty_and_vary
#check P01TC.identityParameters
#print axioms P01TC.identityParameters
#check P01TC.identity_parameters_I_SKK
#print axioms P01TC.identity_parameters_I_SKK
#check P01TC.concreteJEnv
#print axioms P01TC.concreteJEnv
#check P01TC.concrete_j_environment_related
#print axioms P01TC.concrete_j_environment_related
#check P01TC.concrete_j_nonraw_proof_control
#print axioms P01TC.concrete_j_nonraw_proof_control
#check P01TC.typed_pair_I_SKK_related
#print axioms P01TC.typed_pair_I_SKK_related
#check P01TC.typed_pair_I_SKK_control
#print axioms P01TC.typed_pair_I_SKK_control
#check P01TC.mandatory_raw_family_obstruction_unchanged
#print axioms P01TC.mandatory_raw_family_obstruction_unchanged
#check P01TC.Negative.totalRaw
#print axioms P01TC.Negative.totalRaw
#check P01TC.Negative.rawTotal
#print axioms P01TC.Negative.rawTotal
#check P01TC.Negative.rightSeparating
#print axioms P01TC.Negative.rightSeparating
#check P01TC.Negative.leftSeparating
#print axioms P01TC.Negative.leftSeparating
#check P01TC.Negative.pairContext
#print axioms P01TC.Negative.pairContext
#check P01TC.Negative.equalEnv
#print axioms P01TC.Negative.equalEnv
#check P01TC.Negative.splitEnv
#print axioms P01TC.Negative.splitEnv
#check P01TC.Negative.equalityTest
#print axioms P01TC.Negative.equalityTest
#check P01TC.Negative.pair_context_formed
#print axioms P01TC.Negative.pair_context_formed
#check P01TC.Negative.equality_test_formed
#print axioms P01TC.Negative.equality_test_formed
#check P01TC.Negative.right_cross_links_without_equality
#print axioms P01TC.Negative.right_cross_links_without_equality
#check P01TC.Negative.left_cross_links_without_equality
#print axioms P01TC.Negative.left_cross_links_without_equality
#check P01TC.Negative.no_universal_raw_variable
#print axioms P01TC.Negative.no_universal_raw_variable
#check P01TC.Negative.j_transport_requires_both_coordinates
#print axioms P01TC.Negative.j_transport_requires_both_coordinates
#check P01TC.Negative.j_endpoint_omission_fails
#print axioms P01TC.Negative.j_endpoint_omission_fails
#check P01TC.Negative.j_proof_coordinate_omission_fails
#print axioms P01TC.Negative.j_proof_coordinate_omission_fails
#check P01TC.Negative.conversion_scope_premise_necessary
#print axioms P01TC.Negative.conversion_scope_premise_necessary
#check P01TC.formedObject
#print axioms P01TC.formedObject
#check P01TC.formedLink
#print axioms P01TC.formedLink
#check P01TC.formedObject_rel
#print axioms P01TC.formedObject_rel
#check P01TC.formedLink_rel
#print axioms P01TC.formedLink_rel
#check P01TC.context_two_sided_invariance
#print axioms P01TC.context_two_sided_invariance
#check P01TC.context_strong_diagonal
#print axioms P01TC.context_strong_diagonal
#check P01TC.formedFibre
#print axioms P01TC.formedFibre
#check P01TC.formedFibre_coherent
#print axioms P01TC.formedFibre_coherent
#check P01TC.formed_pi_exact
#print axioms P01TC.formed_pi_exact
#check P01TC.formed_sigma_exact
#print axioms P01TC.formed_sigma_exact
#check P01TC.formed_identity_exact
#print axioms P01TC.formed_identity_exact
#check P01TC.raw_omega_typed
#print axioms P01TC.raw_omega_typed
#check P01TC.raw_omega_has_no_normal_reduct
#print axioms P01TC.raw_omega_has_no_normal_reduct

#print P01TC.Legacy.Derivation
#print P01TC.Legacy.Restricted
#print P01TC.Legacy.Translation
#print P01TC.Legacy.RawContext

#check P01TC.Legacy.RawContext
#print axioms P01TC.Legacy.RawContext
#check P01TC.Legacy.rawTel
#print axioms P01TC.Legacy.rawTel
#check P01TC.Legacy.rawTel_length
#print axioms P01TC.Legacy.rawTel_length
#check P01TC.Legacy.RawContext.ext
#print axioms P01TC.Legacy.RawContext.ext
#check P01TC.Legacy.rawTel_context
#print axioms P01TC.Legacy.rawTel_context
#check P01TC.Legacy.raw_term
#print axioms P01TC.Legacy.raw_term
#check P01TC.Legacy.RawContext.theta
#print axioms P01TC.Legacy.RawContext.theta
#check P01TC.Legacy.form_arr
#print axioms P01TC.Legacy.form_arr
#check P01TC.Legacy.form_fin
#print axioms P01TC.Legacy.form_fin
#check P01TC.Legacy.Translation
#print axioms P01TC.Legacy.Translation
#check P01TC.Legacy.Translation.form
#print axioms P01TC.Legacy.Translation.form
#check P01TC.Legacy.Translation.subst
#print axioms P01TC.Legacy.Translation.subst
#check P01TC.Legacy.Translation.inst
#print axioms P01TC.Legacy.Translation.inst
#check P01TC.Legacy.Translation.motiveAt
#print axioms P01TC.Legacy.Translation.motiveAt
#check P01TC.Legacy.Derivation
#print axioms P01TC.Legacy.Derivation
#check P01TC.Legacy.Derivation.erase
#print axioms P01TC.Legacy.Derivation.erase
#check P01TC.Legacy.Restricted
#print axioms P01TC.Legacy.Restricted
#check P01TC.Legacy.Restricted.embed
#print axioms P01TC.Legacy.Restricted.embed
#check P01TC.Legacy.Restricted.raw_embed
#print axioms P01TC.Legacy.Restricted.raw_embed
#check P01TC.Legacy.Restricted.scoped
#print axioms P01TC.Legacy.Restricted.scoped
#check P01TC.Legacy.Restricted.translation
#print axioms P01TC.Legacy.Restricted.translation
#check P01TC.Legacy.Restricted.formed
#print axioms P01TC.Legacy.Restricted.formed
#check P01TC.Legacy.Derivation.allFree
#print axioms P01TC.Legacy.Derivation.allFree
#check P01TC.Legacy.Restricted.allFree
#print axioms P01TC.Legacy.Restricted.allFree
#check P01TC.Legacy.no_allIntro
#print axioms P01TC.Legacy.no_allIntro
#check P01TC.Legacy.no_allElim
#print axioms P01TC.Legacy.no_allElim
#check P01TC.Legacy.Translation.F_agrees
#print axioms P01TC.Legacy.Translation.F_agrees
#check P01TC.Legacy.Translation.G_agrees
#print axioms P01TC.Legacy.Translation.G_agrees
#check P01TC.Legacy.decodeFinite
#print axioms P01TC.Legacy.decodeFinite
#check P01TC.Legacy.translate
#print axioms P01TC.Legacy.translate
#check P01TC.Legacy.decodeFinite_embed
#print axioms P01TC.Legacy.decodeFinite_embed
#check P01TC.Legacy.decodeFinite_sound
#print axioms P01TC.Legacy.decodeFinite_sound
#check P01TC.Legacy.translate_embedFinite
#print axioms P01TC.Legacy.translate_embedFinite
#check P01TC.Legacy.Translation.readback
#print axioms P01TC.Legacy.Translation.readback
#check P01TC.Legacy.Translation.unique
#print axioms P01TC.Legacy.Translation.unique
#check P01TC.Legacy.Translation.all_image
#print axioms P01TC.Legacy.Translation.all_image
#check P01TC.Legacy.Translation.object_agrees
#print axioms P01TC.Legacy.Translation.object_agrees
#check P01TC.Legacy.Restricted.object_agrees
#print axioms P01TC.Legacy.Restricted.object_agrees
#check P01TC.Legacy.no_dependentPolyType
#print axioms P01TC.Legacy.no_dependentPolyType
#check P01TC.Legacy.excludedFiniteConclusion
#print axioms P01TC.Legacy.excludedFiniteConclusion
#check P01TC.Legacy.no_excludedFiniteConclusion
#print axioms P01TC.Legacy.no_excludedFiniteConclusion
#check P01TC.Legacy.Restricted.old_judgment
#print axioms P01TC.Legacy.Restricted.old_judgment
#check P01TC.Legacy.Restricted.heterogeneous_agrees
#print axioms P01TC.Legacy.Restricted.heterogeneous_agrees
#check P01TC.Legacy.raw_variable_embedding
#print axioms P01TC.Legacy.raw_variable_embedding

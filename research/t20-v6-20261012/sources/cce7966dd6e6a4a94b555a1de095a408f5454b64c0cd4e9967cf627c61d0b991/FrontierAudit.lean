import P01RecursiveModel
import P01RecursiveAssertions
import P01CurryParametricity
import P01ModelWitnesses
import P01EffectSeeds
import P01FiniteCoupling
import P01EffectMass
import P01CouplingWitness
import AuditSupport
set_option pp.universes true
set_option format.width 120
#eval IO.println "AUDIT_BEGIN P01R.OEnv"
#check P01R.OEnv
#ortho_audit P01R.OEnv
#print axioms P01R.OEnv
#eval IO.println "AUDIT_END P01R.OEnv"
#eval IO.println "AUDIT_BEGIN P01R.REnv"
#check P01R.REnv
#ortho_audit P01R.REnv
#print axioms P01R.REnv
#eval IO.println "AUDIT_END P01R.REnv"
#eval IO.println "AUDIT_BEGIN P01R.renv_ext"
#check P01R.renv_ext
#ortho_audit P01R.renv_ext
#print axioms P01R.renv_ext
#eval IO.println "AUDIT_END P01R.renv_ext"
#eval IO.println "AUDIT_BEGIN P01R.diagEnv"
#check P01R.diagEnv
#ortho_audit P01R.diagEnv
#print axioms P01R.diagEnv
#eval IO.println "AUDIT_END P01R.diagEnv"
#eval IO.println "AUDIT_BEGIN P01R.REnv.at"
#check P01R.REnv.at
#ortho_audit P01R.REnv.at
#print axioms P01R.REnv.at
#eval IO.println "AUDIT_END P01R.REnv.at"
#eval IO.println "AUDIT_BEGIN P01R.extendEnv"
#check P01R.extendEnv
#ortho_audit P01R.extendEnv
#print axioms P01R.extendEnv
#eval IO.println "AUDIT_END P01R.extendEnv"
#eval IO.println "AUDIT_BEGIN P01R.extend_diag"
#check P01R.extend_diag
#ortho_audit P01R.extend_diag
#print axioms P01R.extend_diag
#eval IO.println "AUDIT_END P01R.extend_diag"
#eval IO.println "AUDIT_BEGIN P01R.link_ext"
#check P01R.link_ext
#ortho_audit P01R.link_ext
#print axioms P01R.link_ext
#eval IO.println "AUDIT_END P01R.link_ext"
#eval IO.println "AUDIT_BEGIN P01R.Model"
#check P01R.Model
#ortho_audit P01R.Model
#print axioms P01R.Model
#eval IO.println "AUDIT_END P01R.Model"
#eval IO.println "AUDIT_BEGIN P01R.Model.asLink"
#check P01R.Model.asLink
#ortho_audit P01R.Model.asLink
#print axioms P01R.Model.asLink
#eval IO.println "AUDIT_END P01R.Model.asLink"
#eval IO.println "AUDIT_BEGIN P01R.Model.asLink_diag"
#check P01R.Model.asLink_diag
#ortho_audit P01R.Model.asLink_diag
#print axioms P01R.Model.asLink_diag
#eval IO.println "AUDIT_END P01R.Model.asLink_diag"
#eval IO.println "AUDIT_BEGIN P01R.model_ext"
#check P01R.model_ext
#ortho_audit P01R.model_ext
#print axioms P01R.model_ext
#eval IO.println "AUDIT_END P01R.model_ext"
#eval IO.println "AUDIT_BEGIN P01R.varModel"
#check P01R.varModel
#ortho_audit P01R.varModel
#print axioms P01R.varModel
#eval IO.println "AUDIT_END P01R.varModel"
#eval IO.println "AUDIT_BEGIN P01R.bottomModel"
#check P01R.bottomModel
#ortho_audit P01R.bottomModel
#print axioms P01R.bottomModel
#eval IO.println "AUDIT_END P01R.bottomModel"
#eval IO.println "AUDIT_BEGIN P01R.arrowModel"
#check P01R.arrowModel
#ortho_audit P01R.arrowModel
#print axioms P01R.arrowModel
#eval IO.println "AUDIT_END P01R.arrowModel"
#eval IO.println "AUDIT_BEGIN P01R.bodyFamily"
#check P01R.bodyFamily
#ortho_audit P01R.bodyFamily
#print axioms P01R.bodyFamily
#eval IO.println "AUDIT_END P01R.bodyFamily"
#eval IO.println "AUDIT_BEGIN P01R.allModel"
#check P01R.allModel
#ortho_audit P01R.allModel
#print axioms P01R.allModel
#eval IO.println "AUDIT_END P01R.allModel"
#eval IO.println "AUDIT_BEGIN P01R.interpret"
#check P01R.interpret
#ortho_audit P01R.interpret
#print axioms P01R.interpret
#eval IO.println "AUDIT_END P01R.interpret"
#eval IO.println "AUDIT_BEGIN P01R.recursive_identity_extension"
#check P01R.recursive_identity_extension
#ortho_audit P01R.recursive_identity_extension
#print axioms P01R.recursive_identity_extension
#eval IO.println "AUDIT_END P01R.recursive_identity_extension"
#eval IO.println "AUDIT_BEGIN P01R.recursive_endpoint_restriction"
#check P01R.recursive_endpoint_restriction
#ortho_audit P01R.recursive_endpoint_restriction
#print axioms P01R.recursive_endpoint_restriction
#eval IO.println "AUDIT_END P01R.recursive_endpoint_restriction"
#eval IO.println "AUDIT_BEGIN P01R.recursive_respectfulness"
#check P01R.recursive_respectfulness
#ortho_audit P01R.recursive_respectfulness
#print axioms P01R.recursive_respectfulness
#eval IO.println "AUDIT_END P01R.recursive_respectfulness"
#eval IO.println "AUDIT_BEGIN P01R.recursive_raw_compatibility"
#check P01R.recursive_raw_compatibility
#ortho_audit P01R.recursive_raw_compatibility
#print axioms P01R.recursive_raw_compatibility
#eval IO.println "AUDIT_END P01R.recursive_raw_compatibility"
#eval IO.println "AUDIT_BEGIN P01R.renEnv"
#check P01R.renEnv
#ortho_audit P01R.renEnv
#print axioms P01R.renEnv
#eval IO.println "AUDIT_END P01R.renEnv"
#eval IO.println "AUDIT_BEGIN P01R.REnv.rename"
#check P01R.REnv.rename
#ortho_audit P01R.REnv.rename
#print axioms P01R.REnv.rename
#eval IO.println "AUDIT_END P01R.REnv.rename"
#eval IO.println "AUDIT_BEGIN P01R.Model.rename"
#check P01R.Model.rename
#ortho_audit P01R.Model.rename
#print axioms P01R.Model.rename
#eval IO.println "AUDIT_END P01R.Model.rename"
#eval IO.println "AUDIT_BEGIN P01R.renEnv_cons"
#check P01R.renEnv_cons
#ortho_audit P01R.renEnv_cons
#print axioms P01R.renEnv_cons
#eval IO.println "AUDIT_END P01R.renEnv_cons"
#eval IO.println "AUDIT_BEGIN P01R.rename_extend"
#check P01R.rename_extend
#ortho_audit P01R.rename_extend
#print axioms P01R.rename_extend
#eval IO.println "AUDIT_END P01R.rename_extend"
#eval IO.println "AUDIT_BEGIN P01R.rename_diag"
#check P01R.rename_diag
#ortho_audit P01R.rename_diag
#print axioms P01R.rename_diag
#eval IO.println "AUDIT_END P01R.rename_diag"
#eval IO.println "AUDIT_BEGIN P01R.rename_all"
#check P01R.rename_all
#ortho_audit P01R.rename_all
#print axioms P01R.rename_all
#eval IO.println "AUDIT_END P01R.rename_all"
#eval IO.println "AUDIT_BEGIN P01R.interpret_rename"
#check P01R.interpret_rename
#ortho_audit P01R.interpret_rename
#print axioms P01R.interpret_rename
#eval IO.println "AUDIT_END P01R.interpret_rename"
#eval IO.println "AUDIT_BEGIN P01R.subEnv"
#check P01R.subEnv
#ortho_audit P01R.subEnv
#print axioms P01R.subEnv
#eval IO.println "AUDIT_END P01R.subEnv"
#eval IO.println "AUDIT_BEGIN P01R.REnv.substitute"
#check P01R.REnv.substitute
#ortho_audit P01R.REnv.substitute
#print axioms P01R.REnv.substitute
#eval IO.println "AUDIT_END P01R.REnv.substitute"
#eval IO.println "AUDIT_BEGIN P01R.substitute_diag"
#check P01R.substitute_diag
#ortho_audit P01R.substitute_diag
#print axioms P01R.substitute_diag
#eval IO.println "AUDIT_END P01R.substitute_diag"
#eval IO.println "AUDIT_BEGIN P01R.Model.substitute"
#check P01R.Model.substitute
#ortho_audit P01R.Model.substitute
#print axioms P01R.Model.substitute
#eval IO.println "AUDIT_END P01R.Model.substitute"
#eval IO.println "AUDIT_BEGIN P01R.liftModels"
#check P01R.liftModels
#ortho_audit P01R.liftModels
#print axioms P01R.liftModels
#eval IO.println "AUDIT_END P01R.liftModels"
#eval IO.println "AUDIT_BEGIN P01R.subEnv_cons"
#check P01R.subEnv_cons
#ortho_audit P01R.subEnv_cons
#print axioms P01R.subEnv_cons
#eval IO.println "AUDIT_END P01R.subEnv_cons"
#eval IO.println "AUDIT_BEGIN P01R.rename_succ_extend"
#check P01R.rename_succ_extend
#ortho_audit P01R.rename_succ_extend
#print axioms P01R.rename_succ_extend
#eval IO.println "AUDIT_END P01R.rename_succ_extend"
#eval IO.println "AUDIT_BEGIN P01R.substitute_extend"
#check P01R.substitute_extend
#ortho_audit P01R.substitute_extend
#print axioms P01R.substitute_extend
#eval IO.println "AUDIT_END P01R.substitute_extend"
#eval IO.println "AUDIT_BEGIN P01R.substitute_all"
#check P01R.substitute_all
#ortho_audit P01R.substitute_all
#print axioms P01R.substitute_all
#eval IO.println "AUDIT_END P01R.substitute_all"
#eval IO.println "AUDIT_BEGIN P01R.interpret_lift"
#check P01R.interpret_lift
#ortho_audit P01R.interpret_lift
#print axioms P01R.interpret_lift
#eval IO.println "AUDIT_END P01R.interpret_lift"
#eval IO.println "AUDIT_BEGIN P01R.interpret_substitute"
#check P01R.interpret_substitute
#ortho_audit P01R.interpret_substitute
#print axioms P01R.interpret_substitute
#eval IO.println "AUDIT_END P01R.interpret_substitute"
#eval IO.println "AUDIT_BEGIN P01R.interpret_single"
#check P01R.interpret_single
#ortho_audit P01R.interpret_single
#print axioms P01R.interpret_single
#eval IO.println "AUDIT_END P01R.interpret_single"
#eval IO.println "AUDIT_BEGIN P01R.single_obj_environment"
#check P01R.single_obj_environment
#ortho_audit P01R.single_obj_environment
#print axioms P01R.single_obj_environment
#eval IO.println "AUDIT_END P01R.single_obj_environment"
#eval IO.println "AUDIT_BEGIN P01R.single_rel_environment"
#check P01R.single_rel_environment
#ortho_audit P01R.single_rel_environment
#print axioms P01R.single_rel_environment
#eval IO.println "AUDIT_END P01R.single_rel_environment"
#eval IO.println "AUDIT_BEGIN P01R.instantiate_obj"
#check P01R.instantiate_obj
#ortho_audit P01R.instantiate_obj
#print axioms P01R.instantiate_obj
#eval IO.println "AUDIT_END P01R.instantiate_obj"
#eval IO.println "AUDIT_BEGIN P01R.instantiate_rel"
#check P01R.instantiate_rel
#ortho_audit P01R.instantiate_rel
#print axioms P01R.instantiate_rel
#eval IO.println "AUDIT_END P01R.instantiate_rel"
#eval IO.println "AUDIT_BEGIN P01R.k_per"
#check P01R.k_per
#ortho_audit P01R.k_per
#print axioms P01R.k_per
#eval IO.println "AUDIT_END P01R.k_per"
#eval IO.println "AUDIT_BEGIN P01R.k_link"
#check P01R.k_link
#ortho_audit P01R.k_link
#print axioms P01R.k_link
#eval IO.println "AUDIT_END P01R.k_link"
#eval IO.println "AUDIT_BEGIN P01R.s_per"
#check P01R.s_per
#ortho_audit P01R.s_per
#print axioms P01R.s_per
#eval IO.println "AUDIT_END P01R.s_per"
#eval IO.println "AUDIT_BEGIN P01R.s_link"
#check P01R.s_link
#ortho_audit P01R.s_link
#print axioms P01R.s_link
#eval IO.println "AUDIT_END P01R.s_link"
#eval IO.println "AUDIT_BEGIN P01R.finite_fundamental"
#check P01R.finite_fundamental
#ortho_audit P01R.finite_fundamental
#print axioms P01R.finite_fundamental
#eval IO.println "AUDIT_END P01R.finite_fundamental"
#eval IO.println "AUDIT_BEGIN P01R.finite_new_model_member"
#check P01R.finite_new_model_member
#ortho_audit P01R.finite_new_model_member
#print axioms P01R.finite_new_model_member
#eval IO.println "AUDIT_END P01R.finite_new_model_member"
#eval IO.println "AUDIT_BEGIN P01R.recursive_all_self_instance"
#check P01R.recursive_all_self_instance
#ortho_audit P01R.recursive_all_self_instance
#print axioms P01R.recursive_all_self_instance
#eval IO.println "AUDIT_END P01R.recursive_all_self_instance"
#eval IO.println "AUDIT_BEGIN P01RAssertions.unconditional_recursive_IE"
#check P01RAssertions.unconditional_recursive_IE
#ortho_audit P01RAssertions.unconditional_recursive_IE
#print axioms P01RAssertions.unconditional_recursive_IE
#eval IO.println "AUDIT_END P01RAssertions.unconditional_recursive_IE"
#eval IO.println "AUDIT_BEGIN P01RAssertions.original_capture_avoiding_substitution"
#check P01RAssertions.original_capture_avoiding_substitution
#ortho_audit P01RAssertions.original_capture_avoiding_substitution
#print axioms P01RAssertions.original_capture_avoiding_substitution
#eval IO.println "AUDIT_END P01RAssertions.original_capture_avoiding_substitution"
#eval IO.println "AUDIT_BEGIN P01RAssertions.all_seven_original_finite_rules"
#check P01RAssertions.all_seven_original_finite_rules
#ortho_audit P01RAssertions.all_seven_original_finite_rules
#print axioms P01RAssertions.all_seven_original_finite_rules
#eval IO.println "AUDIT_END P01RAssertions.all_seven_original_finite_rules"
#eval IO.println "AUDIT_BEGIN P01RAssertions.no_external_uniformity_premise"
#check P01RAssertions.no_external_uniformity_premise
#ortho_audit P01RAssertions.no_external_uniformity_premise
#print axioms P01RAssertions.no_external_uniformity_premise
#eval IO.println "AUDIT_END P01RAssertions.no_external_uniformity_premise"
#eval IO.println "AUDIT_BEGIN P01RAssertions.both_endpoint_memberships"
#check P01RAssertions.both_endpoint_memberships
#ortho_audit P01RAssertions.both_endpoint_memberships
#print axioms P01RAssertions.both_endpoint_memberships
#eval IO.println "AUDIT_END P01RAssertions.both_endpoint_memberships"
#eval IO.println "AUDIT_BEGIN P01R.compile"
#check P01R.compile
#ortho_audit P01R.compile
#print axioms P01R.compile
#eval IO.println "AUDIT_END P01R.compile"
#eval IO.println "AUDIT_BEGIN P01R.ValRelated"
#check P01R.ValRelated
#ortho_audit P01R.ValRelated
#print axioms P01R.ValRelated
#eval IO.println "AUDIT_END P01R.ValRelated"
#eval IO.println "AUDIT_BEGIN P01R.valuations_left"
#check P01R.valuations_left
#ortho_audit P01R.valuations_left
#print axioms P01R.valuations_left
#eval IO.println "AUDIT_END P01R.valuations_left"
#eval IO.println "AUDIT_BEGIN P01R.valuations_right"
#check P01R.valuations_right
#ortho_audit P01R.valuations_right
#print axioms P01R.valuations_right
#eval IO.println "AUDIT_END P01R.valuations_right"
#eval IO.println "AUDIT_BEGIN P01R.valuations_cons"
#check P01R.valuations_cons
#ortho_audit P01R.valuations_cons
#print axioms P01R.valuations_cons
#eval IO.println "AUDIT_END P01R.valuations_cons"
#eval IO.println "AUDIT_BEGIN P01R.valuations_shift"
#check P01R.valuations_shift
#ortho_audit P01R.valuations_shift
#print axioms P01R.valuations_shift
#eval IO.println "AUDIT_END P01R.valuations_shift"
#eval IO.println "AUDIT_BEGIN P01R.abstraction_endpoint"
#check P01R.abstraction_endpoint
#ortho_audit P01R.abstraction_endpoint
#print axioms P01R.abstraction_endpoint
#eval IO.println "AUDIT_END P01R.abstraction_endpoint"
#eval IO.println "AUDIT_BEGIN P01R.curry_fundamental"
#check P01R.curry_fundamental
#ortho_audit P01R.curry_fundamental
#print axioms P01R.curry_fundamental
#eval IO.println "AUDIT_END P01R.curry_fundamental"
#eval IO.println "AUDIT_BEGIN P01R.emptyLink"
#check P01R.emptyLink
#ortho_audit P01R.emptyLink
#print axioms P01R.emptyLink
#eval IO.println "AUDIT_END P01R.emptyLink"
#eval IO.println "AUDIT_BEGIN P01R.finite_polymorphic_I"
#check P01R.finite_polymorphic_I
#ortho_audit P01R.finite_polymorphic_I
#print axioms P01R.finite_polymorphic_I
#eval IO.println "AUDIT_END P01R.finite_polymorphic_I"
#eval IO.println "AUDIT_BEGIN P01R.recursive_polymorphic_I_nonempty"
#check P01R.recursive_polymorphic_I_nonempty
#ortho_audit P01R.recursive_polymorphic_I_nonempty
#print axioms P01R.recursive_polymorphic_I_nonempty
#eval IO.println "AUDIT_END P01R.recursive_polymorphic_I_nonempty"
#eval IO.println "AUDIT_BEGIN P01R.recursive_polymorphic_I_uniform"
#check P01R.recursive_polymorphic_I_uniform
#ortho_audit P01R.recursive_polymorphic_I_uniform
#print axioms P01R.recursive_polymorphic_I_uniform
#eval IO.println "AUDIT_END P01R.recursive_polymorphic_I_uniform"
#eval IO.println "AUDIT_BEGIN P01R.recursive_polymorphic_I_self_instance"
#check P01R.recursive_polymorphic_I_self_instance
#ortho_audit P01R.recursive_polymorphic_I_self_instance
#print axioms P01R.recursive_polymorphic_I_self_instance
#eval IO.println "AUDIT_END P01R.recursive_polymorphic_I_self_instance"
#eval IO.println "AUDIT_BEGIN P01R.all_variable_empty"
#check P01R.all_variable_empty
#ortho_audit P01R.all_variable_empty
#print axioms P01R.all_variable_empty
#eval IO.println "AUDIT_END P01R.all_variable_empty"
#eval IO.println "AUDIT_BEGIN P01R.fixed_assumption_cannot_generalise"
#check P01R.fixed_assumption_cannot_generalise
#ortho_audit P01R.fixed_assumption_cannot_generalise
#print axioms P01R.fixed_assumption_cannot_generalise
#eval IO.println "AUDIT_END P01R.fixed_assumption_cannot_generalise"
#eval IO.println "AUDIT_BEGIN P01R.unrestricted_allI_is_not_admissible"
#check P01R.unrestricted_allI_is_not_admissible
#ortho_audit P01R.unrestricted_allI_is_not_admissible
#print axioms P01R.unrestricted_allI_is_not_admissible
#eval IO.println "AUDIT_END P01R.unrestricted_allI_is_not_admissible"
#eval IO.println "AUDIT_BEGIN P01R.typing_excludes_markers"
#check P01R.typing_excludes_markers
#ortho_audit P01R.typing_excludes_markers
#print axioms P01R.typing_excludes_markers
#eval IO.println "AUDIT_END P01R.typing_excludes_markers"
#eval IO.println "AUDIT_BEGIN P01R.original_finite_markers_untypable"
#check P01R.original_finite_markers_untypable
#ortho_audit P01R.original_finite_markers_untypable
#print axioms P01R.original_finite_markers_untypable
#eval IO.println "AUDIT_END P01R.original_finite_markers_untypable"
#eval IO.println "AUDIT_BEGIN P01R.skk"
#check P01R.skk
#ortho_audit P01R.skk
#print axioms P01R.skk
#eval IO.println "AUDIT_END P01R.skk"
#eval IO.println "AUDIT_BEGIN P01R.skk_application"
#check P01R.skk_application
#ortho_audit P01R.skk_application
#print axioms P01R.skk_application
#eval IO.println "AUDIT_END P01R.skk_application"
#eval IO.println "AUDIT_BEGIN P01R.skk_per"
#check P01R.skk_per
#ortho_audit P01R.skk_per
#print axioms P01R.skk_per
#eval IO.println "AUDIT_END P01R.skk_per"
#eval IO.println "AUDIT_BEGIN P01R.identity_skk_link"
#check P01R.identity_skk_link
#ortho_audit P01R.identity_skk_link
#print axioms P01R.identity_skk_link
#eval IO.println "AUDIT_END P01R.identity_skk_link"
#eval IO.println "AUDIT_BEGIN P01R.finite_skk_identity"
#check P01R.finite_skk_identity
#ortho_audit P01R.finite_skk_identity
#print axioms P01R.finite_skk_identity
#eval IO.println "AUDIT_END P01R.finite_skk_identity"
#eval IO.println "AUDIT_BEGIN P01R.finite_polymorphic_skk"
#check P01R.finite_polymorphic_skk
#ortho_audit P01R.finite_polymorphic_skk
#print axioms P01R.finite_polymorphic_skk
#eval IO.println "AUDIT_END P01R.finite_polymorphic_skk"
#eval IO.println "AUDIT_BEGIN P01R.recursive_polymorphic_I_skk"
#check P01R.recursive_polymorphic_I_skk
#ortho_audit P01R.recursive_polymorphic_I_skk
#print axioms P01R.recursive_polymorphic_I_skk
#eval IO.println "AUDIT_END P01R.recursive_polymorphic_I_skk"
#eval IO.println "AUDIT_BEGIN P01R.recursive_parametric_equality_not_raw_conversion"
#check P01R.recursive_parametric_equality_not_raw_conversion
#ortho_audit P01R.recursive_parametric_equality_not_raw_conversion
#print axioms P01R.recursive_parametric_equality_not_raw_conversion
#eval IO.println "AUDIT_END P01R.recursive_parametric_equality_not_raw_conversion"
#eval IO.println "AUDIT_BEGIN P01R.EExpr"
#check P01R.EExpr
#ortho_audit P01R.EExpr
#print axioms P01R.EExpr
#eval IO.println "AUDIT_END P01R.EExpr"
#eval IO.println "AUDIT_BEGIN P01R.Seed"
#check P01R.Seed
#ortho_audit P01R.Seed
#print axioms P01R.Seed
#eval IO.println "AUDIT_END P01R.Seed"
#eval IO.println "AUDIT_BEGIN P01R.seedFintype"
#check P01R.seedFintype
#ortho_audit P01R.seedFintype
#print axioms P01R.seedFintype
#eval IO.println "AUDIT_END P01R.seedFintype"
#eval IO.println "AUDIT_BEGIN P01R.seedInhabited"
#check P01R.seedInhabited
#ortho_audit P01R.seedInhabited
#print axioms P01R.seedInhabited
#eval IO.println "AUDIT_END P01R.seedInhabited"
#eval IO.println "AUDIT_BEGIN P01R.run"
#check P01R.run
#ortho_audit P01R.run
#print axioms P01R.run
#eval IO.println "AUDIT_END P01R.run"
#eval IO.println "AUDIT_BEGIN P01R.erase"
#check P01R.erase
#ortho_audit P01R.erase
#print axioms P01R.erase
#eval IO.println "AUDIT_END P01R.erase"
#eval IO.println "AUDIT_BEGIN P01R.embed"
#check P01R.embed
#ortho_audit P01R.embed
#print axioms P01R.embed
#eval IO.println "AUDIT_END P01R.embed"
#eval IO.println "AUDIT_BEGIN P01R.erase_embed"
#check P01R.erase_embed
#ortho_audit P01R.erase_embed
#print axioms P01R.erase_embed
#eval IO.println "AUDIT_END P01R.erase_embed"
#eval IO.println "AUDIT_BEGIN P01R.seed_outcome"
#check P01R.seed_outcome
#ortho_audit P01R.seed_outcome
#print axioms P01R.seed_outcome
#eval IO.println "AUDIT_END P01R.seed_outcome"
#eval IO.println "AUDIT_BEGIN P01R.outcome_has_seed"
#check P01R.outcome_has_seed
#ortho_audit P01R.outcome_has_seed
#print axioms P01R.outcome_has_seed
#eval IO.println "AUDIT_END P01R.outcome_has_seed"
#eval IO.println "AUDIT_BEGIN P01R.seed_support_exact"
#check P01R.seed_support_exact
#ortho_audit P01R.seed_support_exact
#print axioms P01R.seed_support_exact
#eval IO.println "AUDIT_END P01R.seed_support_exact"
#eval IO.println "AUDIT_BEGIN P01R.EHas"
#check P01R.EHas
#ortho_audit P01R.EHas
#print axioms P01R.EHas
#eval IO.println "AUDIT_END P01R.EHas"
#eval IO.println "AUDIT_BEGIN P01R.original_effect_embeds"
#check P01R.original_effect_embeds
#ortho_audit P01R.original_effect_embeds
#print axioms P01R.original_effect_embeds
#eval IO.println "AUDIT_END P01R.original_effect_embeds"
#eval IO.println "AUDIT_BEGIN P01R.shared_seed_fundamental"
#check P01R.shared_seed_fundamental
#ortho_audit P01R.shared_seed_fundamental
#print axioms P01R.shared_seed_fundamental
#eval IO.println "AUDIT_END P01R.shared_seed_fundamental"
#eval IO.println "AUDIT_BEGIN P01R.run_embed_independent"
#check P01R.run_embed_independent
#ortho_audit P01R.run_embed_independent
#print axioms P01R.run_embed_independent
#eval IO.println "AUDIT_END P01R.run_embed_independent"
#eval IO.println "AUDIT_BEGIN P01R.original_outcome_finite"
#check P01R.original_outcome_finite
#ortho_audit P01R.original_outcome_finite
#print axioms P01R.original_outcome_finite
#eval IO.println "AUDIT_END P01R.original_outcome_finite"
#eval IO.println "AUDIT_BEGIN P01R.original_seed_relational"
#check P01R.original_seed_relational
#ortho_audit P01R.original_seed_relational
#print axioms P01R.original_seed_relational
#eval IO.println "AUDIT_END P01R.original_seed_relational"
#eval IO.println "AUDIT_BEGIN P01Probability.support"
#check P01Probability.support
#ortho_audit P01Probability.support
#print axioms P01Probability.support
#eval IO.println "AUDIT_END P01Probability.support"
#eval IO.println "AUDIT_BEGIN P01Probability.pushMass"
#check P01Probability.pushMass
#ortho_audit P01Probability.pushMass
#print axioms P01Probability.pushMass
#eval IO.println "AUDIT_END P01Probability.pushMass"
#eval IO.println "AUDIT_BEGIN P01Probability.jointMass"
#check P01Probability.jointMass
#ortho_audit P01Probability.jointMass
#print axioms P01Probability.jointMass
#eval IO.println "AUDIT_END P01Probability.jointMass"
#eval IO.println "AUDIT_BEGIN P01Probability.support_mem"
#check P01Probability.support_mem
#ortho_audit P01Probability.support_mem
#print axioms P01Probability.support_mem
#eval IO.println "AUDIT_END P01Probability.support_mem"
#eval IO.println "AUDIT_BEGIN P01Probability.push_nonnegative"
#check P01Probability.push_nonnegative
#ortho_audit P01Probability.push_nonnegative
#print axioms P01Probability.push_nonnegative
#eval IO.println "AUDIT_END P01Probability.push_nonnegative"
#eval IO.println "AUDIT_BEGIN P01Probability.joint_nonnegative"
#check P01Probability.joint_nonnegative
#ortho_audit P01Probability.joint_nonnegative
#print axioms P01Probability.joint_nonnegative
#eval IO.println "AUDIT_END P01Probability.joint_nonnegative"
#eval IO.println "AUDIT_BEGIN P01Probability.push_total"
#check P01Probability.push_total
#ortho_audit P01Probability.push_total
#print axioms P01Probability.push_total
#eval IO.println "AUDIT_END P01Probability.push_total"
#eval IO.println "AUDIT_BEGIN P01Probability.joint_left_marginal"
#check P01Probability.joint_left_marginal
#ortho_audit P01Probability.joint_left_marginal
#print axioms P01Probability.joint_left_marginal
#eval IO.println "AUDIT_END P01Probability.joint_left_marginal"
#eval IO.println "AUDIT_BEGIN P01Probability.joint_right_marginal"
#check P01Probability.joint_right_marginal
#ortho_audit P01Probability.joint_right_marginal
#print axioms P01Probability.joint_right_marginal
#eval IO.println "AUDIT_END P01Probability.joint_right_marginal"
#eval IO.println "AUDIT_BEGIN P01Probability.joint_positive_has_seed"
#check P01Probability.joint_positive_has_seed
#ortho_audit P01Probability.joint_positive_has_seed
#print axioms P01Probability.joint_positive_has_seed
#eval IO.println "AUDIT_END P01Probability.joint_positive_has_seed"
#eval IO.println "AUDIT_BEGIN P01Probability.joint_zero_off_support"
#check P01Probability.joint_zero_off_support
#ortho_audit P01Probability.joint_zero_off_support
#print axioms P01Probability.joint_zero_off_support
#eval IO.println "AUDIT_END P01Probability.joint_zero_off_support"
#eval IO.println "AUDIT_BEGIN P01Probability.push_positive_iff"
#check P01Probability.push_positive_iff
#ortho_audit P01Probability.push_positive_iff
#print axioms P01Probability.push_positive_iff
#eval IO.println "AUDIT_END P01Probability.push_positive_iff"
#eval IO.println "AUDIT_BEGIN P01Probability.observations_same_law"
#check P01Probability.observations_same_law
#ortho_audit P01Probability.observations_same_law
#print axioms P01Probability.observations_same_law
#eval IO.println "AUDIT_END P01Probability.observations_same_law"
#eval IO.println "AUDIT_BEGIN P01R.seedWeight"
#check P01R.seedWeight
#ortho_audit P01R.seedWeight
#print axioms P01R.seedWeight
#eval IO.println "AUDIT_END P01R.seedWeight"
#eval IO.println "AUDIT_BEGIN P01R.seed_weight_positive"
#check P01R.seed_weight_positive
#ortho_audit P01R.seed_weight_positive
#print axioms P01R.seed_weight_positive
#eval IO.println "AUDIT_END P01R.seed_weight_positive"
#eval IO.println "AUDIT_BEGIN P01R.seed_weight_total"
#check P01R.seed_weight_total
#ortho_audit P01R.seed_weight_total
#print axioms P01R.seed_weight_total
#eval IO.println "AUDIT_END P01R.seed_weight_total"
#eval IO.println "AUDIT_BEGIN P01R.outputMass"
#check P01R.outputMass
#ortho_audit P01R.outputMass
#print axioms P01R.outputMass
#eval IO.println "AUDIT_END P01R.outputMass"
#eval IO.println "AUDIT_BEGIN P01R.outputSupport"
#check P01R.outputSupport
#ortho_audit P01R.outputSupport
#print axioms P01R.outputSupport
#eval IO.println "AUDIT_END P01R.outputSupport"
#eval IO.println "AUDIT_BEGIN P01R.outputCoupling"
#check P01R.outputCoupling
#ortho_audit P01R.outputCoupling
#print axioms P01R.outputCoupling
#eval IO.println "AUDIT_END P01R.outputCoupling"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_nonnegative"
#check P01R.output_mass_nonnegative
#ortho_audit P01R.output_mass_nonnegative
#print axioms P01R.output_mass_nonnegative
#eval IO.println "AUDIT_END P01R.output_mass_nonnegative"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_total"
#check P01R.output_mass_total
#ortho_audit P01R.output_mass_total
#print axioms P01R.output_mass_total
#eval IO.println "AUDIT_END P01R.output_mass_total"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_support_exact"
#check P01R.output_mass_support_exact
#ortho_audit P01R.output_mass_support_exact
#print axioms P01R.output_mass_support_exact
#eval IO.println "AUDIT_END P01R.output_mass_support_exact"
#eval IO.println "AUDIT_BEGIN P01R.common_coupling"
#check P01R.common_coupling
#ortho_audit P01R.common_coupling
#print axioms P01R.common_coupling
#eval IO.println "AUDIT_END P01R.common_coupling"
#eval IO.println "AUDIT_BEGIN P01R.related_observations_equal"
#check P01R.related_observations_equal
#ortho_audit P01R.related_observations_equal
#print axioms P01R.related_observations_equal
#eval IO.println "AUDIT_END P01R.related_observations_equal"
#eval IO.println "AUDIT_BEGIN P01R.original_common_coupling"
#check P01R.original_common_coupling
#ortho_audit P01R.original_common_coupling
#print axioms P01R.original_common_coupling
#eval IO.println "AUDIT_END P01R.original_common_coupling"
#eval IO.println "AUDIT_BEGIN P01R.original_positive_support"
#check P01R.original_positive_support
#ortho_audit P01R.original_positive_support
#print axioms P01R.original_positive_support
#eval IO.println "AUDIT_END P01R.original_positive_support"
#eval IO.println "AUDIT_BEGIN P01R.coupling_total"
#check P01R.coupling_total
#ortho_audit P01R.coupling_total
#print axioms P01R.coupling_total
#eval IO.println "AUDIT_END P01R.coupling_total"
#eval IO.println "AUDIT_BEGIN P01R.seed_weight_app"
#check P01R.seed_weight_app
#ortho_audit P01R.seed_weight_app
#print axioms P01R.seed_weight_app
#eval IO.println "AUDIT_END P01R.seed_weight_app"
#eval IO.println "AUDIT_BEGIN P01R.seed_weight_mix"
#check P01R.seed_weight_mix
#ortho_audit P01R.seed_weight_mix
#print axioms P01R.seed_weight_mix
#eval IO.println "AUDIT_END P01R.seed_weight_mix"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_pure"
#check P01R.output_mass_pure
#ortho_audit P01R.output_mass_pure
#print axioms P01R.output_mass_pure
#eval IO.println "AUDIT_END P01R.output_mass_pure"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_application"
#check P01R.output_mass_application
#ortho_audit P01R.output_mass_application
#print axioms P01R.output_mass_application
#eval IO.println "AUDIT_END P01R.output_mass_application"
#eval IO.println "AUDIT_BEGIN P01R.coin_left_count"
#check P01R.coin_left_count
#ortho_audit P01R.coin_left_count
#print axioms P01R.coin_left_count
#eval IO.println "AUDIT_END P01R.coin_left_count"
#eval IO.println "AUDIT_BEGIN P01R.coin_right_count"
#check P01R.coin_right_count
#ortho_audit P01R.coin_right_count
#print axioms P01R.coin_right_count
#eval IO.println "AUDIT_END P01R.coin_right_count"
#eval IO.println "AUDIT_BEGIN P01R.coin_sum"
#check P01R.coin_sum
#ortho_audit P01R.coin_sum
#print axioms P01R.coin_sum
#eval IO.println "AUDIT_END P01R.coin_sum"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_mixture_seed"
#check P01R.output_mass_mixture_seed
#ortho_audit P01R.output_mass_mixture_seed
#print axioms P01R.output_mass_mixture_seed
#eval IO.println "AUDIT_END P01R.output_mass_mixture_seed"
#eval IO.println "AUDIT_BEGIN P01R.output_mass_mixture"
#check P01R.output_mass_mixture
#ortho_audit P01R.output_mass_mixture
#print axioms P01R.output_mass_mixture
#eval IO.println "AUDIT_END P01R.output_mass_mixture"
#eval IO.println "AUDIT_BEGIN P01R.fairWeight"
#check P01R.fairWeight
#ortho_audit P01R.fairWeight
#print axioms P01R.fairWeight
#eval IO.println "AUDIT_END P01R.fairWeight"
#eval IO.println "AUDIT_BEGIN P01R.witnessContext"
#check P01R.witnessContext
#ortho_audit P01R.witnessContext
#print axioms P01R.witnessContext
#eval IO.println "AUDIT_END P01R.witnessContext"
#eval IO.println "AUDIT_BEGIN P01R.witnessEffect"
#check P01R.witnessEffect
#ortho_audit P01R.witnessEffect
#print axioms P01R.witnessEffect
#eval IO.println "AUDIT_END P01R.witnessEffect"
#eval IO.println "AUDIT_BEGIN P01R.leftValues"
#check P01R.leftValues
#ortho_audit P01R.leftValues
#print axioms P01R.leftValues
#eval IO.println "AUDIT_END P01R.leftValues"
#eval IO.println "AUDIT_BEGIN P01R.rightValues"
#check P01R.rightValues
#ortho_audit P01R.rightValues
#print axioms P01R.rightValues
#eval IO.println "AUDIT_END P01R.rightValues"
#eval IO.println "AUDIT_BEGIN P01R.witness_typed"
#check P01R.witness_typed
#ortho_audit P01R.witness_typed
#print axioms P01R.witness_typed
#eval IO.println "AUDIT_END P01R.witness_typed"
#eval IO.println "AUDIT_BEGIN P01R.witness_inputs_related"
#check P01R.witness_inputs_related
#ortho_audit P01R.witness_inputs_related
#print axioms P01R.witness_inputs_related
#eval IO.println "AUDIT_END P01R.witness_inputs_related"
#eval IO.println "AUDIT_BEGIN P01R.left_I_mass"
#check P01R.left_I_mass
#ortho_audit P01R.left_I_mass
#print axioms P01R.left_I_mass
#eval IO.println "AUDIT_END P01R.left_I_mass"
#eval IO.println "AUDIT_BEGIN P01R.right_I_mass"
#check P01R.right_I_mass
#ortho_audit P01R.right_I_mass
#print axioms P01R.right_I_mass
#eval IO.println "AUDIT_END P01R.right_I_mass"
#eval IO.println "AUDIT_BEGIN P01R.right_skk_mass"
#check P01R.right_skk_mass
#ortho_audit P01R.right_skk_mass
#print axioms P01R.right_skk_mass
#eval IO.println "AUDIT_END P01R.right_skk_mass"
#eval IO.println "AUDIT_BEGIN P01R.non_diagonal_mass"
#check P01R.non_diagonal_mass
#ortho_audit P01R.non_diagonal_mass
#print axioms P01R.non_diagonal_mass
#eval IO.println "AUDIT_END P01R.non_diagonal_mass"
#eval IO.println "AUDIT_BEGIN P01R.different_raw_output_laws"
#check P01R.different_raw_output_laws
#ortho_audit P01R.different_raw_output_laws
#print axioms P01R.different_raw_output_laws
#eval IO.println "AUDIT_END P01R.different_raw_output_laws"
#eval IO.println "AUDIT_BEGIN P01R.witness_one_coupling_for_all_relations"
#check P01R.witness_one_coupling_for_all_relations
#ortho_audit P01R.witness_one_coupling_for_all_relations
#print axioms P01R.witness_one_coupling_for_all_relations
#eval IO.println "AUDIT_END P01R.witness_one_coupling_for_all_relations"
#eval IO.println "AUDIT_BEGIN P01R.witness_all_respectful_observations_agree"
#check P01R.witness_all_respectful_observations_agree
#ortho_audit P01R.witness_all_respectful_observations_agree
#print axioms P01R.witness_all_respectful_observations_agree
#eval IO.println "AUDIT_END P01R.witness_all_respectful_observations_agree"

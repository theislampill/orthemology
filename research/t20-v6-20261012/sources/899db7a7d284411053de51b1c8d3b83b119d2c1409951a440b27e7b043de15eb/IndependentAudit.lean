import P01RecursiveModel
import P01RecursiveAssertions
import P01CurryParametricity
import P01ModelWitnesses
import P01EffectSeeds
import P01FiniteCoupling
import P01EffectMass
import P01CouplingWitness
set_option pp.universes true
set_option pp.explicit true
set_option format.width 180
#check @P01R.OEnv
#print axioms P01R.OEnv
#check @P01R.REnv
#print axioms P01R.REnv
#check @P01R.renv_ext
#print axioms P01R.renv_ext
#check @P01R.diagEnv
#print axioms P01R.diagEnv
#check @P01R.REnv.at
#print axioms P01R.REnv.at
#check @P01R.extendEnv
#print axioms P01R.extendEnv
#check @P01R.extend_diag
#print axioms P01R.extend_diag
#check @P01R.link_ext
#print axioms P01R.link_ext
#check @P01R.Model
#print axioms P01R.Model
#check @P01R.Model.asLink
#print axioms P01R.Model.asLink
#check @P01R.Model.asLink_diag
#print axioms P01R.Model.asLink_diag
#check @P01R.model_ext
#print axioms P01R.model_ext
#check @P01R.varModel
#print axioms P01R.varModel
#check @P01R.bottomModel
#print axioms P01R.bottomModel
#check @P01R.arrowModel
#print axioms P01R.arrowModel
#check @P01R.bodyFamily
#print axioms P01R.bodyFamily
#check @P01R.allModel
#print axioms P01R.allModel
#check @P01R.interpret
#print axioms P01R.interpret
#check @P01R.recursive_identity_extension
#print axioms P01R.recursive_identity_extension
#check @P01R.recursive_endpoint_restriction
#print axioms P01R.recursive_endpoint_restriction
#check @P01R.recursive_respectfulness
#print axioms P01R.recursive_respectfulness
#check @P01R.recursive_raw_compatibility
#print axioms P01R.recursive_raw_compatibility
#check @P01R.renEnv
#print axioms P01R.renEnv
#check @P01R.REnv.rename
#print axioms P01R.REnv.rename
#check @P01R.Model.rename
#print axioms P01R.Model.rename
#check @P01R.renEnv_cons
#print axioms P01R.renEnv_cons
#check @P01R.rename_extend
#print axioms P01R.rename_extend
#check @P01R.rename_diag
#print axioms P01R.rename_diag
#check @P01R.rename_all
#print axioms P01R.rename_all
#check @P01R.interpret_rename
#print axioms P01R.interpret_rename
#check @P01R.subEnv
#print axioms P01R.subEnv
#check @P01R.REnv.substitute
#print axioms P01R.REnv.substitute
#check @P01R.substitute_diag
#print axioms P01R.substitute_diag
#check @P01R.Model.substitute
#print axioms P01R.Model.substitute
#check @P01R.liftModels
#print axioms P01R.liftModels
#check @P01R.subEnv_cons
#print axioms P01R.subEnv_cons
#check @P01R.rename_succ_extend
#print axioms P01R.rename_succ_extend
#check @P01R.substitute_extend
#print axioms P01R.substitute_extend
#check @P01R.substitute_all
#print axioms P01R.substitute_all
#check @P01R.interpret_lift
#print axioms P01R.interpret_lift
#check @P01R.interpret_substitute
#print axioms P01R.interpret_substitute
#check @P01R.interpret_single
#print axioms P01R.interpret_single
#check @P01R.single_obj_environment
#print axioms P01R.single_obj_environment
#check @P01R.single_rel_environment
#print axioms P01R.single_rel_environment
#check @P01R.instantiate_obj
#print axioms P01R.instantiate_obj
#check @P01R.instantiate_rel
#print axioms P01R.instantiate_rel
#check @P01R.k_per
#print axioms P01R.k_per
#check @P01R.k_link
#print axioms P01R.k_link
#check @P01R.s_per
#print axioms P01R.s_per
#check @P01R.s_link
#print axioms P01R.s_link
#check @P01R.finite_fundamental
#print axioms P01R.finite_fundamental
#check @P01R.finite_new_model_member
#print axioms P01R.finite_new_model_member
#check @P01R.recursive_all_self_instance
#print axioms P01R.recursive_all_self_instance
#check @P01RAssertions.unconditional_recursive_IE
#print axioms P01RAssertions.unconditional_recursive_IE
#check @P01RAssertions.original_capture_avoiding_substitution
#print axioms P01RAssertions.original_capture_avoiding_substitution
#check @P01RAssertions.all_seven_original_finite_rules
#print axioms P01RAssertions.all_seven_original_finite_rules
#check @P01RAssertions.no_external_uniformity_premise
#print axioms P01RAssertions.no_external_uniformity_premise
#check @P01RAssertions.both_endpoint_memberships
#print axioms P01RAssertions.both_endpoint_memberships
#check @P01R.compile
#print axioms P01R.compile
#check @P01R.ValRelated
#print axioms P01R.ValRelated
#check @P01R.valuations_left
#print axioms P01R.valuations_left
#check @P01R.valuations_right
#print axioms P01R.valuations_right
#check @P01R.valuations_cons
#print axioms P01R.valuations_cons
#check @P01R.valuations_shift
#print axioms P01R.valuations_shift
#check @P01R.abstraction_endpoint
#print axioms P01R.abstraction_endpoint
#check @P01R.curry_fundamental
#print axioms P01R.curry_fundamental
#check @P01R.emptyLink
#print axioms P01R.emptyLink
#check @P01R.finite_polymorphic_I
#print axioms P01R.finite_polymorphic_I
#check @P01R.recursive_polymorphic_I_nonempty
#print axioms P01R.recursive_polymorphic_I_nonempty
#check @P01R.recursive_polymorphic_I_uniform
#print axioms P01R.recursive_polymorphic_I_uniform
#check @P01R.recursive_polymorphic_I_self_instance
#print axioms P01R.recursive_polymorphic_I_self_instance
#check @P01R.all_variable_empty
#print axioms P01R.all_variable_empty
#check @P01R.fixed_assumption_cannot_generalise
#print axioms P01R.fixed_assumption_cannot_generalise
#check @P01R.unrestricted_allI_is_not_admissible
#print axioms P01R.unrestricted_allI_is_not_admissible
#check @P01R.typing_excludes_markers
#print axioms P01R.typing_excludes_markers
#check @P01R.original_finite_markers_untypable
#print axioms P01R.original_finite_markers_untypable
#check @P01R.skk
#print axioms P01R.skk
#check @P01R.skk_application
#print axioms P01R.skk_application
#check @P01R.skk_per
#print axioms P01R.skk_per
#check @P01R.identity_skk_link
#print axioms P01R.identity_skk_link
#check @P01R.finite_skk_identity
#print axioms P01R.finite_skk_identity
#check @P01R.finite_polymorphic_skk
#print axioms P01R.finite_polymorphic_skk
#check @P01R.recursive_polymorphic_I_skk
#print axioms P01R.recursive_polymorphic_I_skk
#check @P01R.recursive_parametric_equality_not_raw_conversion
#print axioms P01R.recursive_parametric_equality_not_raw_conversion
#check @P01R.EExpr
#print axioms P01R.EExpr
#check @P01R.Seed
#print axioms P01R.Seed
#check @P01R.seedFintype
#print axioms P01R.seedFintype
#check @P01R.seedInhabited
#print axioms P01R.seedInhabited
#check @P01R.run
#print axioms P01R.run
#check @P01R.erase
#print axioms P01R.erase
#check @P01R.embed
#print axioms P01R.embed
#check @P01R.erase_embed
#print axioms P01R.erase_embed
#check @P01R.seed_outcome
#print axioms P01R.seed_outcome
#check @P01R.outcome_has_seed
#print axioms P01R.outcome_has_seed
#check @P01R.seed_support_exact
#print axioms P01R.seed_support_exact
#check @P01R.EHas
#print axioms P01R.EHas
#check @P01R.original_effect_embeds
#print axioms P01R.original_effect_embeds
#check @P01R.shared_seed_fundamental
#print axioms P01R.shared_seed_fundamental
#check @P01R.run_embed_independent
#print axioms P01R.run_embed_independent
#check @P01R.original_outcome_finite
#print axioms P01R.original_outcome_finite
#check @P01R.original_seed_relational
#print axioms P01R.original_seed_relational
#check @P01Probability.support
#print axioms P01Probability.support
#check @P01Probability.pushMass
#print axioms P01Probability.pushMass
#check @P01Probability.jointMass
#print axioms P01Probability.jointMass
#check @P01Probability.support_mem
#print axioms P01Probability.support_mem
#check @P01Probability.push_nonnegative
#print axioms P01Probability.push_nonnegative
#check @P01Probability.joint_nonnegative
#print axioms P01Probability.joint_nonnegative
#check @P01Probability.push_total
#print axioms P01Probability.push_total
#check @P01Probability.joint_left_marginal
#print axioms P01Probability.joint_left_marginal
#check @P01Probability.joint_right_marginal
#print axioms P01Probability.joint_right_marginal
#check @P01Probability.joint_positive_has_seed
#print axioms P01Probability.joint_positive_has_seed
#check @P01Probability.joint_zero_off_support
#print axioms P01Probability.joint_zero_off_support
#check @P01Probability.push_positive_iff
#print axioms P01Probability.push_positive_iff
#check @P01Probability.observations_same_law
#print axioms P01Probability.observations_same_law
#check @P01R.seedWeight
#print axioms P01R.seedWeight
#check @P01R.seed_weight_positive
#print axioms P01R.seed_weight_positive
#check @P01R.seed_weight_total
#print axioms P01R.seed_weight_total
#check @P01R.outputMass
#print axioms P01R.outputMass
#check @P01R.outputSupport
#print axioms P01R.outputSupport
#check @P01R.outputCoupling
#print axioms P01R.outputCoupling
#check @P01R.output_mass_nonnegative
#print axioms P01R.output_mass_nonnegative
#check @P01R.output_mass_total
#print axioms P01R.output_mass_total
#check @P01R.output_mass_support_exact
#print axioms P01R.output_mass_support_exact
#check @P01R.common_coupling
#print axioms P01R.common_coupling
#check @P01R.related_observations_equal
#print axioms P01R.related_observations_equal
#check @P01R.original_common_coupling
#print axioms P01R.original_common_coupling
#check @P01R.original_positive_support
#print axioms P01R.original_positive_support
#check @P01R.coupling_total
#print axioms P01R.coupling_total
#check @P01R.seed_weight_app
#print axioms P01R.seed_weight_app
#check @P01R.seed_weight_mix
#print axioms P01R.seed_weight_mix
#check @P01R.output_mass_pure
#print axioms P01R.output_mass_pure
#check @P01R.output_mass_application
#print axioms P01R.output_mass_application
#check @P01R.coin_left_count
#print axioms P01R.coin_left_count
#check @P01R.coin_right_count
#print axioms P01R.coin_right_count
#check @P01R.coin_sum
#print axioms P01R.coin_sum
#check @P01R.output_mass_mixture_seed
#print axioms P01R.output_mass_mixture_seed
#check @P01R.output_mass_mixture
#print axioms P01R.output_mass_mixture
#check @P01R.fairWeight
#print axioms P01R.fairWeight
#check @P01R.witnessContext
#print axioms P01R.witnessContext
#check @P01R.witnessEffect
#print axioms P01R.witnessEffect
#check @P01R.leftValues
#print axioms P01R.leftValues
#check @P01R.rightValues
#print axioms P01R.rightValues
#check @P01R.witness_typed
#print axioms P01R.witness_typed
#check @P01R.witness_inputs_related
#print axioms P01R.witness_inputs_related
#check @P01R.left_I_mass
#print axioms P01R.left_I_mass
#check @P01R.right_I_mass
#print axioms P01R.right_I_mass
#check @P01R.right_skk_mass
#print axioms P01R.right_skk_mass
#check @P01R.non_diagonal_mass
#print axioms P01R.non_diagonal_mass
#check @P01R.different_raw_output_laws
#print axioms P01R.different_raw_output_laws
#check @P01R.witness_one_coupling_for_all_relations
#print axioms P01R.witness_one_coupling_for_all_relations
#check @P01R.witness_all_respectful_observations_agree
#print axioms P01R.witness_all_respectful_observations_agree

import LawCompletionCompact
import LawCompletionCounterexample
import LawCompletionBranches
set_option autoImplicit false
set_option pp.universes true

-- Exact public interfaces and kernel dependency readbacks.
#check LawCompletion.Survives
#check LawCompletion.Backward
#check LawCompletion.SingletonSurvival
#check LawCompletion.UniqueBackward
#check LawCompletion.UniformAttraction
#check LawCompletion.PointwiseAttraction
#print LawCompletion.Survives
#print LawCompletion.Backward
#print LawCompletion.SingletonSurvival
#print LawCompletion.UniqueBackward
#print LawCompletion.UniformAttraction
#print LawCompletion.PointwiseAttraction

#check LawCompletion.backward_iterate
#print axioms LawCompletion.backward_iterate
#check LawCompletion.backward_survives
#print axioms LawCompletion.backward_survives
#check LawCompletion.fixed_survives
#print axioms LawCompletion.fixed_survives
#check LawCompletion.survives_forward
#print axioms LawCompletion.survives_forward
#check LawCompletion.singleton_fixed
#print axioms LawCompletion.singleton_fixed
#check LawCompletion.singleton_unique_fixed
#print axioms LawCompletion.singleton_unique_fixed
#check LawCompletion.singleton_unique_backward
#print axioms LawCompletion.singleton_unique_backward
#check LawCompletion.unique_backward_constant
#print axioms LawCompletion.unique_backward_constant
#check LawCompletion.uniform_iff_tendstoUniformly
#print axioms LawCompletion.uniform_iff_tendstoUniformly
#check LawCompletion.uniform_pointwise
#print axioms LawCompletion.uniform_pointwise
#check LawCompletion.uniform_fixed_singleton
#print axioms LawCompletion.uniform_fixed_singleton
#check LawCompletion.range_succ_subset
#print axioms LawCompletion.range_succ_subset
#check LawCompletion.range_antitone
#print axioms LawCompletion.range_antitone
#check LawCompletion.compact_surviving_predecessor
#print axioms LawCompletion.compact_surviving_predecessor
#check LawCompletion.compact_survivor_realized
#print axioms LawCompletion.compact_survivor_realized
#check LawCompletion.compact_survival_iff_realized
#print axioms LawCompletion.compact_survival_iff_realized
#check LawCompletion.compact_unique_backward_singleton
#print axioms LawCompletion.compact_unique_backward_singleton
#check LawCompletion.compact_singleton_uniform
#print axioms LawCompletion.compact_singleton_uniform
#check LawCompletion.compact_singleton_iff_unique_backward
#print axioms LawCompletion.compact_singleton_iff_unique_backward
#check LawCompletion.compact_singleton_iff_uniform_fixed
#print axioms LawCompletion.compact_singleton_iff_uniform_fixed
#check LawCompletion.compact_completion_equivalences
#print axioms LawCompletion.compact_completion_equivalences

#print LawCompletion.ControlA.State
#print LawCompletion.ControlA.law
#check LawCompletion.ControlA.dist_formula
#print axioms LawCompletion.ControlA.dist_formula
#check LawCompletion.ControlA.bounded
#print axioms LawCompletion.ControlA.bounded
#check LawCompletion.ControlA.law_continuous
#print axioms LawCompletion.ControlA.law_continuous
#check LawCompletion.ControlA.iterate_none
#print axioms LawCompletion.ControlA.iterate_none
#check LawCompletion.ControlA.iterate_some
#print axioms LawCompletion.ControlA.iterate_some
#check LawCompletion.ControlA.range_formula
#print axioms LawCompletion.ControlA.range_formula
#check LawCompletion.ControlA.singleton_survival
#print axioms LawCompletion.ControlA.singleton_survival
#check LawCompletion.ControlA.unique_backward
#print axioms LawCompletion.ControlA.unique_backward
#check LawCompletion.ControlA.backward_exact
#print axioms LawCompletion.ControlA.backward_exact
#check LawCompletion.ControlA.orbit_distance
#print axioms LawCompletion.ControlA.orbit_distance
#check LawCompletion.ControlA.orbit_not_tendsto
#print axioms LawCompletion.ControlA.orbit_not_tendsto
#check LawCompletion.ControlA.not_pointwise_attraction
#print axioms LawCompletion.ControlA.not_pointwise_attraction
#check LawCompletion.ControlA.image_start_failure
#print axioms LawCompletion.ControlA.image_start_failure
#check LawCompletion.ControlA.no_attracting_fixed_point
#print axioms LawCompletion.ControlA.no_attracting_fixed_point
#check LawCompletion.ControlA.counterexample
#print axioms LawCompletion.ControlA.counterexample

#print LawCompletion.ControlB.State
#print LawCompletion.ControlB.law
#check LawCompletion.ControlB.dist_formula
#print axioms LawCompletion.ControlB.dist_formula
#check LawCompletion.ControlB.bounded
#print axioms LawCompletion.ControlB.bounded
#check LawCompletion.ControlB.law_continuous
#print axioms LawCompletion.ControlB.law_continuous
#check LawCompletion.ControlB.branch_predecessor
#print axioms LawCompletion.ControlB.branch_predecessor
#check LawCompletion.ControlB.branch_capacity
#print axioms LawCompletion.ControlB.branch_capacity
#check LawCompletion.ControlB.branch_not_survives
#print axioms LawCompletion.ControlB.branch_not_survives
#check LawCompletion.ControlB.branch_reaches_r
#print axioms LawCompletion.ControlB.branch_reaches_r
#check LawCompletion.ControlB.r_survives
#print axioms LawCompletion.ControlB.r_survives
#check LawCompletion.ControlB.survival_exact
#print axioms LawCompletion.ControlB.survival_exact
#check LawCompletion.ControlB.backward_exact
#print axioms LawCompletion.ControlB.backward_exact
#check LawCompletion.ControlB.unique_backward
#print axioms LawCompletion.ControlB.unique_backward
#check LawCompletion.ControlB.not_singleton_survival
#print axioms LawCompletion.ControlB.not_singleton_survival
#check LawCompletion.ControlB.eventually_fixed
#print axioms LawCompletion.ControlB.eventually_fixed
#check LawCompletion.ControlB.pointwise_attraction
#print axioms LawCompletion.ControlB.pointwise_attraction
#check LawCompletion.ControlB.counterexample
#print axioms LawCompletion.ControlB.counterexample
